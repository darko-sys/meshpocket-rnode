# MeshPocket flashen (Windows)

Firmware: [`dist/meshpocket_rnode_868.uf2`](dist/meshpocket_rnode_868.uf2) (EU 868 / Modell `0xCE`).

Community port of [RNode Firmware CE](https://github.com/liberatedsystems/RNode_Firmware_CE) for Heltec MeshPocket — not an official Heltec or Mark Qvist product.

## 1. Kabel

Nur das **magnetische USB-Datenkabel**. Der Lade-USB-C-Port reicht nicht für DFU/Serial.

## 2. Flashen

1. Magnetkabel anschließen.
2. **RST zweimal kurz** → Laufwerk `HT-n5262`.
3. `meshpocket_rnode_868.uf2` auf das Laufwerk kopieren.
4. Gerät startet neu. Nach ein paar Sekunden sollte das **E-Ink** die RNode-UI zeigen.

Kein Meshtastic-Factory-Erase nötig.

### Troubleshooting

Wenn nach dem Flash nichts kommt: SoftDevice in `INFO_UF2.TXT` prüfen (typisch **6.1.x**).

## 3. BLE zuerst (Priorität)

Ziel: Sideband auf dem Handy per BLE, ohne USB-Host.

### Vor dem Pairing

- **USB-Serial am PC schließen** (Sideband/Windows/`rnsd` aus) — RNode = ein Host gleichzeitig.
- Auf dem Handy: alte „RNode …“-Einträge unter Bluetooth **vergessen**.
- Sideband: Nearby Devices + **Standort** erlauben.
- **Nicht** zuerst in den Android-System-Bluetooth-Einstellungen koppeln — Pairing läuft **in Sideband**.

### Pairing

1. MeshPocket neu starten (oder USER länger halten). Nach Boot ~**90 s** Pairing; **PIN auf dem E-Ink**.
2. Sideband → Hardware → RNode:
   - Frequenz **865200000**, BW **125000**, TX **14**, SF **8**, CR **5**
   - **Connect using Bluetooth** + **Device requires BLE** an
   - **Pair New Device** → Gerät wählen → PIN eingeben
3. Nach erfolgreichem Bond trennt das RNode kurz (normal) und wirbt erneut — Sideband verbindet als **bereits gepaartes** Gerät.
4. Connectivity → **Connect via RNode** an → Sideband **komplett** neu starten (Menü → Shutdown).

USER-Taste:

| Aktion | Effekt |
|--------|--------|
| Kurz | Bluetooth an/aus |
| ~2 s halten | Pairing (neue PIN, alte Bonds auf dem Gerät gelöscht) |

### Windows Sideband + BLE

**`port = ble://…` in `~\.reticulum\config` lässt Sideband Desktop oft hart abstürzen** — das ist ein Host-/Stack-Problem, nicht „Android only“.

Für den PC:

- Sideband am PC weiter über **USB** (`port = COM…`) nutzen, **oder**
- BLE am PC nur mit `rns`/`bleak` testen, nicht mit Sideband Desktop.

Handy-BLE und PC-USB nicht parallel auf demselben MeshPocket.

## 4. USB / Reticulum (Fallback & PC)

```ini
[[MeshPocket RNode]]
  type = RNodeInterface
  enabled = True
  port = COMx
  frequency = 865200000
  bandwidth = 125000
  txpower = 14
  spreadingfactor = 8
  codingrate = 5
```

EU: **max. 14 dBm**. Prüfen: `rnodeconf COMx -i`

Optional MeshPocket-IDs in lokalem `rnodeconf`: [`tools/patch_rnodeconf_meshpocket.py`](tools/patch_rnodeconf_meshpocket.py).

## 5. Build-Hinweis (SPI)

Falls der Build die falsche AVR-`SPI`-/`Wire`-Lib zieht: Ordner in `Documents\Arduino\libraries` umbenennen (`SPI_AVR_CONFLICT_DISABLED`, `Wire_AVR_CONFLICT_DISABLED`).
