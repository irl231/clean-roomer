<#
.SYNOPSIS
  Checks a repository against cleanroom/deny-list.txt. Works in Windows PowerShell 5.1 and pwsh 7+.
  A Python twin with the same behaviour is cleanroom_scan.py (use it where PowerShell is absent).

.DESCRIPTION
  Deny-list format (one entry per line, '#' starts a comment):
    term:   <text>   case-insensitive text that must not appear in text files
    notice: <text>   like term, reported as a vendor notice (copyright lines, trademarks)
    meta:   <text>   case-insensitive bytes that must not appear in the first 256 KiB of ANY file
                     (catches producer / creator-tool metadata inside binary fixtures)
    ext:    .abc     file extension that must not be tracked
    path:   <glob>   path glob that must not be tracked (for example plan/**)
    allow:  <glob>   TEXT files exempt from term / notice / meta (the profile, ADRs, the deny-list
                     itself). Binary files are never exempt: a vendor-made binary under an allowed
                     folder is still a finding. ext and path are never exempt.

  What is scanned:
    - Files: in a git work tree, everything tracked plus untracked files that are not ignored
      (so a forgotten observation note is caught before it is committed). Outside git, every file
      except .git, node_modules, target, dist, build, .venv, __pycache__.
    - Text files are detected as UTF-8 (default) or UTF-16 LE/BE (BOM or byte pattern) and scanned
      line by line whatever their size. Files with other NUL bytes are binary: meta only.
    - Nothing is skipped silently. A file that cannot be read or that git lists but the file
      system cannot find is reported as 'error'.

  Exit status: 0 clean, 1 findings, 2 configuration error.

.EXAMPLE
  ./cleanroom_scan.ps1 -Root .
  ./cleanroom_scan.ps1 -SelfTest
#>
[CmdletBinding()]
param(
    [string]$Root = '.',
    [string]$DenyList = '',
    [switch]$SelfTest
)

$ErrorActionPreference = 'Stop'
$SkipDirs = @('.git', 'node_modules', 'target', 'dist', 'build', '.venv', '__pycache__')
$MetaBytes = 256KB
$Latin1 = [Text.Encoding]::GetEncoding(28591)
$Utf8NoBom = New-Object Text.UTF8Encoding($false)

function ConvertTo-GlobRegex([string]$Glob) {
    $sb = New-Object Text.StringBuilder
    $i = 0
    while ($i -lt $Glob.Length) {
        $c = $Glob[$i]
        if ($c -eq '*') {
            if ($Glob.Substring($i).StartsWith('**/')) { [void]$sb.Append('(?:.*/)?'); $i += 3; continue }
            if ($Glob.Substring($i).StartsWith('**')) { [void]$sb.Append('.*'); $i += 2; continue }
            [void]$sb.Append('[^/]*')
        }
        elseif ($c -eq '?') { [void]$sb.Append('[^/]') }
        else { [void]$sb.Append([regex]::Escape([string]$c)) }
        $i++
    }
    return [regex]('^' + $sb.ToString() + '$')
}

function Read-DenyList([string]$Path) {
    $cfg = @{ Terms = @(); Meta = @(); Exts = @(); Paths = @(); PathSrc = @(); Allow = @() }
    $n = 0
    foreach ($raw in [IO.File]::ReadLines($Path)) {
        $n++
        $line = $raw.Trim()
        if ($line -eq '' -or $line.StartsWith('#')) { continue }
        $idx = $line.IndexOf(':')
        if ($idx -lt 1) { throw "${Path}:${n}: expected 'kind: value'" }
        $kind = $line.Substring(0, $idx).Trim()
        $value = $line.Substring($idx + 1).Trim()
        if ($value -eq '') { throw "${Path}:${n}: empty value" }
        switch ($kind) {
            'term'   { $cfg.Terms += , @('term', $value) }
            'notice' { $cfg.Terms += , @('notice', $value) }
            'meta'   { $cfg.Meta += $value }
            'ext'    { $e = $value.ToLowerInvariant(); if (-not $e.StartsWith('.')) { $e = '.' + $e }; $cfg.Exts += $e }
            'path'   { $cfg.Paths += (ConvertTo-GlobRegex $value); $cfg.PathSrc += $value }
            'allow'  { $cfg.Allow += (ConvertTo-GlobRegex $value) }
            default  { throw "${Path}:${n}: unknown kind '$kind'" }
        }
    }
    return $cfg
}

# Returns @{ Files = string[]; Missing = string[] }. Missing: listed by git, absent on disk.
function Get-RepoFiles([string]$RootDir) {
    $rootFull = (Resolve-Path $RootDir).Path
    $git = Get-Command git -ErrorAction SilentlyContinue
    if ($git) {
        $prev = $ErrorActionPreference; $ErrorActionPreference = 'SilentlyContinue'
        $prevEnc = $null
        try { $prevEnc = [Console]::OutputEncoding; [Console]::OutputEncoding = $Utf8NoBom } catch { $prevEnc = $null }
        $inRepo = (& git -C $rootFull rev-parse --is-inside-work-tree 2>&1) -join ''
        $out = $null
        if ($inRepo.Trim() -eq 'true') {
            $out = & git -c core.quotepath=off -C $rootFull ls-files -z --cached --others --exclude-standard 2>$null
        }
        if ($prevEnc) { try { [Console]::OutputEncoding = $prevEnc } catch { } }
        $ErrorActionPreference = $prev
        if ($inRepo.Trim() -eq 'true' -and $out) {
            $list = ($out -join '') -split "`0" | Where-Object { $_ -ne '' }
            $files = New-Object Collections.Generic.List[string]
            $missing = New-Object Collections.Generic.List[string]
            foreach ($rel in $list) {
                $p = Join-Path $rootFull $rel
                if (Test-Path -LiteralPath $p -PathType Leaf) { $files.Add($rel) }
                elseif (-not (Test-Path -LiteralPath $p -PathType Container)) { $missing.Add($rel) }  # containers are submodules
            }
            return @{ Files = $files.ToArray(); Missing = $missing.ToArray() }
        }
    }
    $files = New-Object Collections.Generic.List[string]
    $stack = New-Object Collections.Generic.Stack[string]
    $stack.Push($rootFull)
    while ($stack.Count -gt 0) {
        $dir = $stack.Pop()
        foreach ($d in [IO.Directory]::GetDirectories($dir)) {
            if ($SkipDirs -notcontains [IO.Path]::GetFileName($d)) { $stack.Push($d) }
        }
        foreach ($f in [IO.Directory]::GetFiles($dir)) {
            $files.Add($f.Substring($rootFull.Length).TrimStart('\', '/').Replace('\', '/'))
        }
    }
    return @{ Files = $files.ToArray(); Missing = @() }
}

# Classifies the head bytes: returns 'utf8', 'utf16le', 'utf16be' or 'binary'.
function Get-TextKind([byte[]]$buf, [int]$read) {
    if ($read -ge 2 -and $buf[0] -eq 0xFF -and $buf[1] -eq 0xFE) { return 'utf16le' }
    if ($read -ge 2 -and $buf[0] -eq 0xFE -and $buf[1] -eq 0xFF) { return 'utf16be' }
    $probe = [Math]::Min($read, 8192)
    $nulEven = 0; $nulOdd = 0; $nul = 0
    for ($b = 0; $b -lt $probe; $b++) {
        if ($buf[$b] -eq 0) { $nul++; if (($b % 2) -eq 0) { $nulEven++ } else { $nulOdd++ } }
    }
    if ($nul -eq 0) { return 'utf8' }
    # UTF-16 without BOM: NULs sit almost only on one parity (ASCII-range text).
    $half = [Math]::Floor($probe / 2)
    if ($half -ge 8) {
        if ($nulOdd -ge ($half * 0.6) -and $nulEven -le ($half * 0.05)) { return 'utf16le' }
        if ($nulEven -ge ($half * 0.6) -and $nulOdd -le ($half * 0.05)) { return 'utf16be' }
    }
    return 'binary'
}

function Invoke-Scan([string]$RootDir, $cfg) {
    $rootFull = (Resolve-Path $RootDir).Path
    $findings = New-Object Collections.Generic.List[string]
    $listing = Get-RepoFiles $rootFull
    foreach ($m in $listing.Missing) {
        $findings.Add(('error  {0}: listed by git but not found on disk (encoding or case problem); fix before trusting this scan' -f $m.Replace('\', '/')))
    }
    # Pre-compute meta needles: Latin-1 view of UTF-8 bytes (for raw heads) and the plain string (for UTF-16 text).
    $metaRaw = @($cfg.Meta | ForEach-Object { $Latin1.GetString([Text.Encoding]::UTF8.GetBytes($_)) })
    $cmp = [StringComparison]::OrdinalIgnoreCase
    foreach ($rel0 in ($listing.Files | Sort-Object)) {
        $rel = $rel0.Replace('\', '/')
        $low = $rel.ToLowerInvariant()
        for ($k = 0; $k -lt $cfg.Paths.Count; $k++) {
            if ($cfg.Paths[$k].IsMatch($rel)) { $findings.Add(('path   {0}: matches forbidden path ''{1}''' -f $rel, $cfg.PathSrc[$k])) }
        }
        foreach ($ext in $cfg.Exts) {
            if ($low.EndsWith($ext)) { $findings.Add(('ext    {0}: forbidden extension ''{1}''' -f $rel, $ext)) }
        }
        $allowed = $false
        foreach ($a in $cfg.Allow) { if ($a.IsMatch($rel)) { $allowed = $true; break } }
        $full = Join-Path $rootFull $rel
        try {
            $size = (Get-Item -LiteralPath $full -Force).Length
            $fs = [IO.File]::Open($full, 'Open', 'Read', 'ReadWrite')
            try {
                $buf = New-Object byte[] ([Math]::Min([long]$MetaBytes, $size))
                $read = if ($buf.Length -gt 0) { $fs.Read($buf, 0, $buf.Length) } else { 0 }
            } finally { $fs.Dispose() }
        } catch {
            $findings.Add(('error  {0}: cannot read ({1})' -f $rel, $_.Exception.Message)); continue
        }
        $kind = Get-TextKind $buf $read
        $isText = $kind -ne 'binary'
        if ($allowed -and $isText) { continue }   # allow exempts text files only

        # meta: raw head bytes, or the decoded head for UTF-16 text
        if ($cfg.Meta.Count -gt 0) {
            if ($kind -eq 'utf16le' -or $kind -eq 'utf16be') {
                $enc = if ($kind -eq 'utf16le') { [Text.Encoding]::Unicode } else { [Text.Encoding]::BigEndianUnicode }
                $head = $enc.GetString($buf, 0, $read)
                for ($i = 0; $i -lt $cfg.Meta.Count; $i++) {
                    if ($head.IndexOf($cfg.Meta[$i], $cmp) -ge 0) { $findings.Add(('meta   {0}: contains ''{1}'' in file metadata area' -f $rel, $cfg.Meta[$i])) }
                }
            } else {
                $head = $Latin1.GetString($buf, 0, $read)
                for ($i = 0; $i -lt $cfg.Meta.Count; $i++) {
                    if ($head.IndexOf($metaRaw[$i], $cmp) -ge 0) { $findings.Add(('meta   {0}: contains ''{1}'' in file metadata area' -f $rel, $cfg.Meta[$i])) }
                }
            }
        }
        if (-not $isText -or $cfg.Terms.Count -eq 0) { continue }

        # term / notice: streamed line scan of the whole file, any size
        $enc = switch ($kind) { 'utf16le' { [Text.Encoding]::Unicode } 'utf16be' { [Text.Encoding]::BigEndianUnicode } default { $Utf8NoBom } }
        $n = 0
        try {
            $sr = New-Object IO.StreamReader($full, $enc, $true)
            try {
                while ($null -ne ($line = $sr.ReadLine())) {
                    $n++
                    foreach ($t in $cfg.Terms) {
                        if ($line.IndexOf($t[1], $cmp) -ge 0) { $findings.Add(('{0,-6} {1}:{2}: ''{3}''' -f $t[0], $rel, $n, $t[1])) }
                    }
                }
            } finally { $sr.Dispose() }
        } catch {
            $findings.Add(('error  {0}: cannot read as text ({1})' -f $rel, $_.Exception.Message))
        }
    }
    return , $findings.ToArray()
}

function Invoke-SelfTest {
    # Prove the check can fail: plant one violation of every kind and require each is found,
    # first in a plain folder, then (if git is available) in a real repository.
    $script:failures = New-Object Collections.Generic.List[string]
    function W([string]$base, [string]$rel, [byte[]]$data) {
        $p = Join-Path $base $rel
        New-Item -ItemType Directory -Force -Path (Split-Path $p) | Out-Null
        [IO.File]::WriteAllBytes($p, $data)
    }
    function T([string]$s) { [Text.Encoding]::UTF8.GetBytes($s) }
    function Assert-Scan([string]$label, [string]$found, [string[]]$expected, [string[]]$unexpected) {
        $missing = @($expected | Where-Object { -not $found.Contains($_) })
        $wrong = @($unexpected | Where-Object { $found.Contains($_) })
        if ($missing.Count -gt 0 -or $wrong.Count -gt 0) {
            $script:failures.Add("[$label] missing: " + ($missing -join '; ') + ' | unexpected: ' + ($wrong -join '; ') + "`n" + $found)
        }
    }

    # --- Part A: plain folder, one of every kind ---
    $tmp = Join-Path ([IO.Path]::GetTempPath()) ('cleanroom_selftest_' + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $tmp | Out-Null
    try {
        W $tmp 'deny.txt' (T "term: forbidden-name`nnotice: (c) acme`nmeta: made-by-acme`next: .acmepreset`npath: plan/**`nallow: deny.txt`nallow: docs/**`n")
        W $tmp 'src/a.txt' (T "hello`nuses Forbidden-Name here`n")
        W $tmp 'src/b.txt' (T "Copyright (C) Acme Corp`n")
        W $tmp 'fixtures/x.bin' ([byte[]](0, 0, 0) + (T 'Made-By-Acme') + [byte[]](0, 0))
        W $tmp 'assets/p.acmepreset' (T 'x')
        W $tmp 'plan/notes.md' (T 'observation notes')
        W $tmp 'docs/profile.md' (T "forbidden-name is the target; (c) acme; producer string made-by-acme`n")
        W $tmp 'docs/vendor-export.bin' ([byte[]](0, 1, 0) + (T 'made-by-acme'))          # binary under allow: still found
        W $tmp 'src/res.rc' ([Text.Encoding]::Unicode.GetPreamble() + [Text.Encoding]::Unicode.GetBytes("STRINGTABLE`nCopyright (C) Acme`n"))
        W $tmp 'src/nobom.txt' ([Text.Encoding]::Unicode.GetBytes("plain text line`nforbidden-name without bom`n"))
        W $tmp 'src/be.txt' ([Text.Encoding]::BigEndianUnicode.GetPreamble() + [Text.Encoding]::BigEndianUnicode.GetBytes("made-by-acme in utf-16be text`n"))
        $sb = New-Object Text.StringBuilder
        for ($i = 0; $i -lt 120000; $i++) { [void]$sb.AppendLine('padding line of text to grow the file well beyond five megabytes') }
        [void]$sb.AppendLine('forbidden-name at the end of a large file')
        W $tmp 'src/huge.txt' (T $sb.ToString())
        W $tmp 'src/clean.txt' (T "nothing to see`n")
        $cfg = Read-DenyList (Join-Path $tmp 'deny.txt')
        $found = (Invoke-Scan $tmp $cfg) -join "`n"
        Assert-Scan 'folder' $found @(
            'term   src/a.txt:2', 'notice src/b.txt:1', 'meta   fixtures/x.bin', 'ext    assets/p.acmepreset',
            'path   plan/notes.md', 'meta   docs/vendor-export.bin', 'notice src/res.rc:2', 'term   src/nobom.txt:2',
            'meta   src/be.txt', 'term   src/huge.txt:120001'
        ) @('docs/profile.md', 'src/clean.txt', 'deny.txt')
    } finally { Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue }

    # --- Part B: real git repository (listing path, non-ASCII names, untracked and ignored files) ---
    $git = Get-Command git -ErrorAction SilentlyContinue
    if ($git) {
        $tmp = Join-Path ([IO.Path]::GetTempPath()) ('cleanroom_selftest_git_' + [Guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $tmp | Out-Null
        try {
            $prev = $ErrorActionPreference; $ErrorActionPreference = 'SilentlyContinue'
            & git -C $tmp init -q . 2>&1 | Out-Null
            & git -C $tmp config user.email 'selftest@example.invalid' 2>&1 | Out-Null
            & git -C $tmp config user.name 'selftest' 2>&1 | Out-Null
            & git -C $tmp config core.autocrlf false 2>&1 | Out-Null
            $ErrorActionPreference = $prev
            W $tmp 'cleanroom/deny-list.txt' (T "term: forbidden-name`nmeta: made-by-acme`npath: plan/**`nallow: cleanroom/**`n")
            W $tmp '.gitignore' (T "ignored/`n")
            W $tmp 'src/größe.txt' (T "forbidden-name in a file with a non-ascii name`n")
            W $tmp 'src/with space.txt' (T "forbidden-name`n")
            W $tmp 'cleanroom/export.bin' ([byte[]](0, 0) + (T 'Made-By-Acme'))
            W $tmp 'cleanroom/PROJECT-PROFILE.md' (T "producer string: made-by-acme; forbidden-name`n")
            W $tmp 'src/ok.txt' (T "fine`n")
            $prev = $ErrorActionPreference; $ErrorActionPreference = 'SilentlyContinue'
            & git -C $tmp add -A 2>&1 | Out-Null
            & git -C $tmp commit -q -m init 2>&1 | Out-Null
            $ErrorActionPreference = $prev
            W $tmp 'plan/notes.md' (T 'untracked observation note')              # untracked, not ignored: must be found
            W $tmp 'ignored/scratch.txt' (T "forbidden-name in an ignored file`n") # ignored: never committed, not scanned
            $cfg = Read-DenyList (Join-Path $tmp 'cleanroom/deny-list.txt')
            $found = (Invoke-Scan $tmp $cfg) -join "`n"
            Assert-Scan 'git' $found @(
                'term   src/größe.txt:1', 'term   src/with space.txt:1', 'meta   cleanroom/export.bin', 'path   plan/notes.md'
            ) @('cleanroom/PROJECT-PROFILE.md', 'cleanroom/deny-list.txt', 'src/ok.txt', 'ignored/scratch.txt', 'error')
        } finally { Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue }
    } else {
        Write-Host 'selftest note: git not found, repository listing not tested'
    }

    if ($script:failures.Count -gt 0) {
        Write-Host 'selftest FAILED'
        foreach ($f in $script:failures) { Write-Host $f }
        return 1
    }
    Write-Host 'selftest ok: every planted violation was detected (folder and git modes), allowed text files were skipped'
    return 0
}

if ($SelfTest) { exit (Invoke-SelfTest) }

# Emit UTF-8 so findings with non-ASCII paths print the same as from cleanroom_scan.py.
$prevOut = $null
try { $prevOut = [Console]::OutputEncoding; [Console]::OutputEncoding = $Utf8NoBom } catch { $prevOut = $null }
try {
    if (-not $DenyList) { $DenyList = Join-Path $Root 'cleanroom/deny-list.txt' }
    try { $cfg = Read-DenyList $DenyList } catch {
        [Console]::Error.WriteLine("configuration error: $($_.Exception.Message)"); exit 2
    }
    $findings = Invoke-Scan $Root $cfg
    foreach ($f in $findings) { [Console]::Out.WriteLine($f) }
    if ($findings.Count -gt 0) {
        [Console]::Error.WriteLine("`n$($findings.Count) finding(s). Fix the cause; do not edit the deny-list to pass.")
        exit 1
    }
    [Console]::Out.WriteLine('clean-room scan: no findings')
    exit 0
} finally {
    if ($prevOut) { try { [Console]::OutputEncoding = $prevOut } catch { } }
}
