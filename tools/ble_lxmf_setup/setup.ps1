# Offline setup with Python 3.13 x64.
#   cd <dieser-ordner>
#   .\setup.ps1
# Optional:
#   .\setup.ps1 -PythonExe "C:\Path\to\Python313\python.exe"
param(
  [string]$PythonExe = ""
)
$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$Wheel = Join-Path $Root "wheels"
Set-Location $Root

$env:PIP_NO_INDEX = "1"
Remove-Item Env:PIP_FIND_LINKS -ErrorAction SilentlyContinue
Remove-Item Env:PIP_INDEX_URL -ErrorAction SilentlyContinue

function Resolve-Python313 {
  param([string]$Explicit)
  if ($Explicit -and (Test-Path $Explicit)) { return (Resolve-Path $Explicit).Path }

  # Windows Python launcher
  try {
    $p = & py -3.13 -c "import sys; print(sys.executable)" 2>$null
    if ($LASTEXITCODE -eq 0 -and $p) { return $p.Trim() }
  } catch {}

  foreach ($cand in @(
      "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
      "$env:ProgramFiles\Python313\python.exe",
      "C:\Python313\python.exe"
    )) {
    if (Test-Path $cand) { return $cand }
  }
  return $null
}

$PyBase = Resolve-Python313 -Explicit $PythonExe
if (-not $PyBase) {
  Write-Host "FEHLER: Python 3.13 x64 nicht gefunden."
  Write-Host "Installiere von https://www.python.org/downloads/ (Haken: 'Add to PATH' + 'py launcher')."
  Write-Host "Oder: .\setup.ps1 -PythonExe `"C:\Users\...\Python313\python.exe`""
  exit 1
}

Write-Host "=== Using ==="
Write-Host $PyBase
& $PyBase --version
& $PyBase -c "import struct, platform, sys; assert sys.version_info[:2]==(3,13), sys.version; print('bits', struct.calcsize('P')*8, 'machine', platform.machine())"

if (-not (Test-Path "$Wheel\rns-1.5.7-py3-none-any.whl")) {
  Write-Host "FEHLER: wheels\ unvollstaendig — Ordner komplett neu kopieren."
  exit 1
}

Write-Host "Creating venv with 3.13 ..."
if (Test-Path "$Root\.venv") { Remove-Item -Recurse -Force "$Root\.venv" }
& $PyBase -m venv .venv
$Py = "$Root\.venv\Scripts\python.exe"

if (-not (Test-Path "$Root\.venv\Scripts\pip.exe")) {
  & $Py -m ensurepip --default-pip
}

Write-Host "Installing from wheels\ (offline) ..."
if (Test-Path "$Root\pick_and_install.py") {
  & $Py "$Root\pick_and_install.py"
} else {
  & $Py -m pip install --no-index --find-links "$Wheel" rns lxmf bleak
}
if ($LASTEXITCODE -ne 0) { throw "install failed" }

& $Py -c "import RNS, LXMF, bleak; print('imports OK')"

Write-Host ""
Write-Host "Activate + run:"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  python ble_lxmf_node.py --addr F8:62:53:9C:2B:17 --name `"RNode 6702`""
