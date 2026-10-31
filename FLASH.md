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

Optional: [`tools/watch_uf2_flash.ps1`](tools/watch_uf2_flash.ps1) wartet auf `HT-n5262` und kopiert die UF2 automatisch.

## 3. USER-Taste (Hold wie RNode)

Dauer bis Loslassen:

| Aktion | Effekt |
|--------|--------|
| kurz tippen | Bluetooth an/aus |
| halten ≈ 0,7 s+ | **Airplane sleep**: LoRa+BLE aus → E-Ink „AIRPLANE“ → nRF `SYSTEMOFF`; Wake = USER (voller Boot, wieder BLE+LoRa an mit EU-Defaults) |
| halten ≈ 5 s+ | Pairing / neue PIN auf dem E-Ink |

Boot-Baseline (RAM-EEPROM): BLE an, LoRa an, **869.525 MHz / 125 kHz / SF8 / CR6 / 14 dBm**. Host überschreibt Parameter beim Connect.

## 4. Host am PC (empfohlen zum Validieren)

### USB

```ini
[[MeshPocket RNode]]
  type = RNodeInterface
  enabled = True
  port = COMx
  frequency = 869525000
  bandwidth = 125000
  txpower = 14
  spreadingfactor = 8
  codingrate = 6
```

EU: **max. 14 dBm**. Prüfen: `rnodeconf COMx -i`

### BLE (ohne Sideband Desktop)

Windows Sideband mit `port = ble://…` oft **Absturz** — BLE am PC mit `rns` / `bleak` testen. Nach dem Bond (PIN vom E-Ink) ist NUS/KISS nutzbar.

Zwei MeshPockets: einer USB, einer BLE → getrennte Reticulum-Instanzen beweisen den **LoRa-Luftpfad** (Announce + LXMF).

Handy-BLE und PC-USB nicht parallel auf dem **selben** MeshPocket.

## 5. Sideband auf dem Handy (Best-effort)

Zwischenstand: auf getesteten **Xiaomi**-Geräten oft nur „gepaired“, E-Ink zeigt kein stabiles **connected**. Die MeshPocket-Firmware ist per PC-BLE nachgewiesen; der Bruch liegt vermutlich bei Phone/OS/Sideband.

Bitte mit **stock Sideband** auf anderen Phones nachstellen (siehe [README](README.md) Call for testers).

Kurzchecklist, falls du es trotzdem versuchst:

1. System-Bluetooth: alte „RNode …“-Bonds **vergessen**.
2. Sideband: Nearby Devices + Standort; **Device requires BLE**.
3. Frequenz im UI als **869.525** (MHz), nicht die volle Hz-Zahl.
4. Pairing: MeshPocket ~5 s Hold → PIN → in Sideband pairen; nach Bond kurz disconnect (normal), dann reconnect.
5. Connectivity → **Connect via RNode** → Sideband komplett neu starten.
6. Erfolgskriterium: E-Ink **connected**, nicht nur Android „paired“.

## 6. Build-Hinweis (SPI)

Falls der Build die falsche AVR-`SPI`-/`Wire`-Lib zieht: Ordner in `Documents\Arduino\libraries` umbenennen (`SPI_AVR_CONFLICT_DISABLED`, `Wire_AVR_CONFLICT_DISABLED`).

Optional MeshPocket-IDs in lokalem `rnodeconf`: [`tools/patch_rnodeconf_meshpocket.py`](tools/patch_rnodeconf_meshpocket.py).
