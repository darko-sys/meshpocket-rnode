# MeshPocket flashen (Windows)

Firmware: [`dist/meshpocket_rnode_868.uf2`](dist/meshpocket_rnode_868.uf2) (EU 868 / Modell `0xCE`).

Community port of [RNode Firmware CE](https://github.com/liberatedsystems/RNode_Firmware_CE) for Heltec MeshPocket — not an official Heltec or Mark Qvist product.

## 1. Kabel

Nur das **magnetische USB-Datenkabel**. Der Lade-USB-C-Port reicht nicht für DFU/Serial.

## 2. Flashen

1. Magnetkabel anschließen.
2. **RST zweimal kurz** → Laufwerk `HT-n5262`.
3. `meshpocket_rnode_868.uf2` auf das Laufwerk kopieren.
4. Gerät startet neu. Nach ein paar Sekunden sollte das **E-Ink** die RNode-UI zeigen (langsam; Full-Refresh alle paar Minuten).

Kein Meshtastic-Factory-Erase nötig: die UF2 überschreibt die App-Partition; SoftDevice/Bootloader bleiben.

### Troubleshooting

Wenn nach dem Flash nichts passiert (kein E-Ink, kein USB-Serial): SoftDevice/Bootloader prüfen (`INFO_UF2.TXT` im DFU-Laufwerk, typisch SoftDevice **6.1.x**). Ein SoftDevice-Mismatch ist selten; Factory-Erase-UF2s liefern wir bewusst nicht mit.

## 3. Prüfen (USB)

Diese UF2 bringt Factory-EEPROM (Produkt `0xD2`, Modell `0xCE`). Für den ersten Test meist kein `rnodeconf --autoinstall` nötig:

```powershell
# COM-Port im Geräte-Manager (magnetisches Kabel)
rnodeconf COMx -i
```

Optional: Menü **Heltec MeshPocket** / Band **868**, Firmware-Hash setzen. Lokal kann `rnodeconf` MeshPocket-IDs brauchen — siehe [`tools/patch_rnodeconf_meshpocket.py`](tools/patch_rnodeconf_meshpocket.py).

## 4. Reticulum (PC über USB) — empfohlen

Ein Host gleichzeitig (USB **oder** BLE, nicht beides). Sideband/Windows: **USB**, nicht `ble://` (kann abstürzen).

In `%USERPROFILE%\.reticulum\config`:

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

EU 868: **max. 14 dBm** in dieser Anleitung. Dann `rnstatus` / Sideband am PC.

## 5. Bluetooth / Sideband (Handy) — experimentell

BLE **advertised** (Name z. B. `RNode A1B2`). Pairing ist auf vielen Android-15+/Graphene-Geräten unzuverlässig; **USB oder USB-OTG bevorzugen**.

Nach Boot öffnet die Firmware ~**90 s** Pairing (PIN auf dem E-Ink). USER-Taste:

| Aktion | Effekt |
|--------|--------|
| Kurz tippen | Bluetooth an/aus |
| Länger halten | Pairing-Modus (PIN) |

In Sideband (nicht in den Android-System-Bluetooth-Einstellungen zuerst koppeln):

1. Hardware → RNode: gleiche Frequenzparameter wie oben; **Connect using Bluetooth** + **Device requires BLE**.
2. **Pair New Device** während Pairing-Fenster; PIN vom Display; Nearby Devices **und** Standort erlauben.
3. Connectivity → **Connect via RNode** → App neu starten.

Guide (allgemein): https://unsigned.io/guides/2023_01_19_RNode_Bluetooth_Setup_In_Sideband_On_Android.html

## Build-Hinweis (SPI)

Falls der Build die falsche AVR-`SPI`-/`Wire`-Lib zieht: Ordner in `Documents\Arduino\libraries` umbenennen (`SPI_AVR_CONFLICT_DISABLED`, `Wire_AVR_CONFLICT_DISABLED`).
