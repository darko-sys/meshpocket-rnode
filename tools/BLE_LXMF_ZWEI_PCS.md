# Zwei PCs: je ein MeshPocket per BLE

Ziel: Nachrichtenaustausch **nur über LoRa** (nicht WLAN).

## Auf **jedem** PC einmal

1. Python 3.10+ installieren.
2. In PowerShell:

```powershell
pip install -U rns lxmf bleak
```

3. MeshPocket in **Windows-Bluetooth** koppeln (PIN vom E-Ink, ~5 s Hold).
4. Notiere die BLE-Adresse (z. B. `FE:27:4D:E8:49:6E`) und den Namen (`RNode E827` / `RNode 6702`).
5. **Kein USB** am MeshPocket. Sideband schließen.

## Script

Datei: `tools/ble_lxmf_node.py` (aus dem `meshpocket-rnode`-Repo auf den anderen PC kopieren, USB-Stick reicht).

**PC A** (Beispiel E827):

```powershell
cd <ordner-mit-script>
python ble_lxmf_node.py --addr FE:27:4D:E8:49:6E --name "RNode E827"
```

**PC B** (Beispiel 6702):

```powershell
python ble_lxmf_node.py --addr F8:62:53:9C:2B:17 --name "RNode 6702"
```

Erfolg sieht so aus:

- `online=True`
- `PEER <…>` (Gegenstelle gesehen)
- `MSG_IN …` / `MSG_OUT …`

## Hinweise

- Das Script schreibt eine eigene Config nach `%TEMP%\meshp_ble_lxmf\` — **ohne** AutoInterface (kein LAN-Shortcut).
- Radio: 869.525 MHz / 125 kHz / SF8 / CR6 / 14 dBm (wie Firmware-Baseline).
- Sideband 2.2.0 brauchst du für diesen Test **nicht**. Wenn Sideband offen ist, kann es BLE blockieren.
- Adressen ggf. anpassen, falls Windows andere MACs zeigt.
