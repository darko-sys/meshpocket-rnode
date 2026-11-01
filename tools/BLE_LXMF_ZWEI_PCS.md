# Zwei PCs: je ein MeshPocket per BLE

Ziel: Nachrichtenaustausch **nur über LoRa** (kein WLAN / kein AutoInterface).

## Ergebnis (2026-11-01)

**Bestanden.** Zwei Windows-PCs, je ein MeshPocket nur über BLE (`ble://…`), EU-Radio-Baseline.

| Host | Gerät | Rolle |
|------|--------|--------|
| PC A | RNode E827 (`FE:27:4D:E8:49:6E`) | `ble_lxmf_node.py` → `online=True` |
| PC B | RNode 6702 (`F8:62:53:9C:2B:17`) | gleiches Script |

Beobachtet: gegenseitige `PEER`-Announces, `MSG_OUT` mit Delivery-Proof, `MSG_IN` (z. B. `hello-from-2B:17-…` / `hello-from-49:6E-…`), RNS-Link RTT ~2 s. Kein USB, kein Sideband, AutoInterface aus.

Hinweis: Pro Windows-Host ist typischerweise nur **eine** aktive MeshPocket-BLE-Session sinnvoll — deshalb bewusst zwei PCs, nicht zwei BLE-Links auf demselben Rechner.

## Voraussetzungen

- Firmware aus [`dist/`](../dist/) (siehe [FLASH.md](../FLASH.md))
- **Python 3.13 x64** (Windows). 3.15 und Co. passen nicht zu den Offline-Wheels.
- Pakete: `rns`, `lxmf`, `bleak` — online per `pip`, oder offline über [`ble_lxmf_setup/`](ble_lxmf_setup/)

## Auf jedem PC

1. MeshPocket in **Windows-Bluetooth** koppeln (PIN vom E-Ink). Gerät nur an **einem** PC gekoppelt halten.
2. Sideband schließen, **kein USB** am MeshPocket.
3. Script starten (Adressen anpassen):

**PC A (E827):**

```powershell
python ble_lxmf_node.py --addr FE:27:4D:E8:49:6E --name "RNode E827"
```

**PC B (6702)** — empfohlen mit Offline-Kit:

```powershell
cd ble_lxmf_setup
.\setup.ps1          # nutzt py -3.13 + wheels\
.\.venv\Scripts\Activate.ps1
python ble_lxmf_node.py --addr F8:62:53:9C:2B:17 --name "RNode 6702"
```

Erfolg: `online=True`, dann `PEER …`, `MSG_OUT` / `MSG_IN`.

## Technik

- Config unter `%TEMP%\meshp_ble_*\` — **ohne** AutoInterface (sonst LAN-Shortcut).
- Radio: 869.525 MHz / 125 kHz / SF8 / CR6 / 14 dBm.
- Script: [`ble_lxmf_node.py`](ble_lxmf_node.py) (Kopie auch in `ble_lxmf_setup/` für USB-Stick-Workflow).
