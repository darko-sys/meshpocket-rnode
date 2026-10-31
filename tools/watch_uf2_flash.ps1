# Wait for MeshPocket DFU volume (HT-n5262) and copy UF2.
# Usage: .\tools\watch_uf2_flash.ps1
# Then: magnet cable + double-tap RST on each device (one at a time).

$ErrorActionPreference = 'Stop'
$uf2 = Join-Path $PSScriptRoot '..\dist\meshpocket_rnode_868.uf2' | Resolve-Path
if (-not (Test-Path $uf2)) { throw "UF2 missing: $uf2" }

Write-Host "UF2: $uf2"
Write-Host "Waiting for drive label HT-n5262 (Ctrl+C to stop)..."
Write-Host "Plug magnetic USB, then double-tap RST."

$flashed = @{}
while ($true) {
  $vol = Get-Volume -ErrorAction SilentlyContinue |
    Where-Object { $_.FileSystemLabel -eq 'HT-n5262' -and $_.DriveLetter }
  foreach ($v in $vol) {
    $letter = "$($v.DriveLetter):"
    if ($flashed.ContainsKey($letter)) { continue }
    $dest = Join-Path $letter 'meshpocket_rnode_868.uf2'
    Write-Host "$(Get-Date -Format 'HH:mm:ss') Flashing -> $dest"
    Copy-Item -LiteralPath $uf2 -Destination $dest -Force
    $flashed[$letter] = $true
    Write-Host "$(Get-Date -Format 'HH:mm:ss') Done. Device should reboot; unplug when e-ink shows RNode UI."
    Write-Host "Ready for next device (or Ctrl+C)."
  }
  Start-Sleep -Milliseconds 800
}
