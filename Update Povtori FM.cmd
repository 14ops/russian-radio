@echo off
rem Povtori FM updater. Downloads only the files that changed or are missing, checks each one, then puts it in place.
rem Keep this file next to "Povtori FM.html". Needs Windows 10 or 11 and an internet connection.
setlocal
set "POVTORI_DIR=%~dp0"
set "POVTORI_SELF=%~f0"
title Update Povtori FM
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s = [IO.File]::ReadAllText($env:POVTORI_SELF); Invoke-Expression $s.Substring($s.LastIndexOf('#' + 'POWERSHELL'))" & echo. & pause & exit /b
#POWERSHELL
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch { }
$root = [IO.Path]::GetFullPath($env:POVTORI_DIR)
$base = 'https://raw.githubusercontent.com/14ops/russian-radio/main/'
if ($env:POVTORI_BASE) { $base = $env:POVTORI_BASE }
if (-not $base.EndsWith('/')) { $base += '/' }
$curlName = 'curl.exe'
if ($env:POVTORI_CURL) { $curlName = $env:POVTORI_CURL }
$curl = Get-Command $curlName -ErrorAction SilentlyContinue
$tmp = Join-Path ([IO.Path]::GetTempPath()) ('povtori-update-' + [guid]::NewGuid().ToString('N'))
[void][IO.Directory]::CreateDirectory($tmp)

function Get-File([string]$url, [string]$dest) {
  if ($curl) {
    & $curl.Source -fsS --retry 3 --retry-delay 2 -L -o $dest $url
    if ($LASTEXITCODE -ne 0) { throw ('could not download ' + $url + ' (curl error ' + $LASTEXITCODE + ')') }
  } else {
    Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $dest
  }
}
function Get-Sha([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Get-Url([string]$rel) { $base + ((($rel -split '/') | ForEach-Object { [Uri]::EscapeDataString($_) }) -join '/') }
function Get-Local([string]$rel) { [IO.Path]::GetFullPath([IO.Path]::Combine($root, $rel)) }

try {
  Write-Host ''
  Write-Host '  Povtori FM updater' -ForegroundColor Yellow
  Write-Host ('  Folder: ' + $root)
  $probe = Join-Path $root ('.povtori-write-test-' + [guid]::NewGuid().ToString('N'))
  try { [IO.File]::WriteAllText($probe, 'x'); [IO.File]::Delete($probe) }
  catch { throw 'this folder is read-only. Unlock the USB stick, or copy the folder somewhere you can write.' }

  Write-Host '  Getting the list of files...'
  $listFile = Join-Path $tmp 'files.json'
  Get-File ($base + 'files.json') $listFile
  $remote = [IO.File]::ReadAllText($listFile, [Text.Encoding]::UTF8) | ConvertFrom-Json
  $known = @{}
  $localList = Get-Local 'files.json'
  if ([IO.File]::Exists($localList)) {
    try { foreach ($f in ([IO.File]::ReadAllText($localList, [Text.Encoding]::UTF8) | ConvertFrom-Json).files) { $known[$f.path] = $f.sha256 } } catch { }
  }

  $files = @($remote.files)
  $need = New-Object System.Collections.ArrayList
  $n = 0
  foreach ($f in $files) {
    $n++
    if ($n % 25 -eq 0) { Write-Host ('  Checking files: ' + $n + ' of ' + $files.Count) }
    if ($f.path -match '(^|[\\/])\.\.([\\/]|$)' -or $f.path -match '^[\\/]' -or $f.path -match ':') { Write-Host ('  Skipping a strange path: ' + $f.path); continue }
    $p = Get-Local $f.path
    $good = $false
    if ([IO.File]::Exists($p) -and (New-Object IO.FileInfo $p).Length -eq [int64]$f.size) {
      if ($known[$f.path] -eq $f.sha256) { $good = $true }
      elseif ((Get-Sha $p) -eq $f.sha256) { $good = $true }
    }
    if (-not $good) { [void]$need.Add($f) }
  }

  if ($need.Count -eq 0) {
    Write-Host ''
    Write-Host ('  Already up to date: Povtori FM v' + $remote.version + '.') -ForegroundColor Green
  } else {
    $bytes = 0
    foreach ($f in $need) { $bytes += [int64]$f.size }
    Write-Host ('  ' + $need.Count + ' files to download, ' + [math]::Round($bytes / 1MB, 1) + ' MB.')
    $i = 0
    foreach ($f in $need) {
      $i++
      Write-Host ('  [' + $i + '/' + $need.Count + '] ' + $f.path + ' (' + [math]::Round($f.size / 1MB, 2) + ' MB)')
      $dl = Join-Path $tmp ([guid]::NewGuid().ToString('N'))
      Get-File (Get-Url $f.path) $dl
      if ((Get-Sha $dl) -ne $f.sha256) { throw ('the download of ' + $f.path + ' came out damaged. Run the update again.') }
      $dest = Get-Local $f.path
      [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dest))
      [IO.File]::Copy($dl, $dest, $true)
      [IO.File]::Delete($dl)
    }
    Write-Host ''
    Write-Host ('  Done. Povtori FM is now v' + $remote.version + '.') -ForegroundColor Green
  }
  [IO.File]::Copy($listFile, $localList, $true)
  Write-Host '  Open it with "Start Povtori FM.cmd".'
} catch {
  Write-Host ''
  Write-Host ('  Update failed: ' + $_.Exception.Message) -ForegroundColor Red
  Write-Host '  Check the internet connection, then run it again. Files that already came down stay.'
  $global:LASTEXITCODE = 1
} finally {
  Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
}
