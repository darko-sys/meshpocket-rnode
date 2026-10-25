# Capture MeshPocket RNode USB debug lines (115200).
# Usage: .\tools\meshp_serial_debug.ps1
#     or: .\tools\meshp_serial_debug.ps1 -Port COM17

param(
  [string]$Port = ""
)

if (-not $Port) {
  $ports = Get-CimInstance Win32_SerialPort | Where-Object {
    $_.Name -match 'Adafruit|nRF|USB Serial|COM' -and $_.Name -notmatch 'Bluetooth'
  }
  if ($ports) {
    $Port = ($ports | Select-Object -First 1).DeviceID
    Write-Host "Using $Port ($(($ports | Select-Object -First 1).Name))"
  } else {
    Write-Host "No serial port found. Plug magnetic USB cable and pass -Port COMx"
    exit 1
  }
}

$baud = 115200
Write-Host "Opening $Port @ $baud — reset the MeshPocket now. Ctrl+C to stop."
Write-Host "Look for: PAIRING ON / PIN= / pairing_complete / REJECT / MITM OK"
Write-Host "----"

$sp = New-Object System.IO.Ports.SerialPort $Port, $baud, None, 8, One
$sp.ReadTimeout = 500
$sp.DtrEnable = $true
$sp.RtsEnable = $true
try {
  $sp.Open()
  while ($true) {
    try {
      $line = $sp.ReadLine()
      $ts = Get-Date -Format "HH:mm:ss.fff"
      Write-Host "[$ts] $line"
    } catch [System.TimeoutException] {
      # idle
    }
  }
} finally {
  if ($sp.IsOpen) { $sp.Close() }
}
