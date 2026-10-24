# MeshPocket flashen (Windows)

Gebaute Firmware: [`dist/meshpocket_rnode_868.uf2`](dist/meshpocket_rnode_868.uf2) (EU 868 / Modell `0xCE`).

## 1. Kabel

Nur das **magnetische USB-Datenkabel** vom MeshPocket. Der Lade-USB-C-Port reicht nicht für DFU/Serial.

## 2. Von Meshtastic: einmal löschen

1. [Meshtastic Web Flasher](https://flasher.meshtastic.org/) → Gerät → **Erase**.
2. Oder Erase-UF2 auf das DFU-Laufwerk kopieren.
3. Danach erneut in DFU gehen.

## 3. RNode flashen

1. **RST** zweimal kurz drücken → Laufwerk `HT-n5262`.
2. `dist/meshpocket_rnode_868.uf2` auf das Laufwerk kopieren.
3. Gerät startet neu (E-Ink bleibt vorerst leer/alt — Display ist in dieser Firmware noch aus).

## 4. Provisionieren

```powershell
# COM-Port in Geräte-Manager prüfen (magnetisches Kabel)
rnodeconf COMx -i
rnodeconf --autoinstall
```

Im Menü: **[17] Heltec MeshPocket** → Band **868**.

Danach Firmware-Hash setzen (wenn `rnodeconf` danach fragt / laut CE-Doku), z. B. nach Upload-Pfad im Makefile.

## 5. Reticulum

`%USERPROFILE%\.reticulum\config` — Interface anlegen (Port anpassen):

```ini
[[MeshPocket RNode]]
  type = RNodeInterface
  enabled = True
  port = COMx
  frequency = 865200000
  bandwidth = 125000
  txpower = 14
  spreading_factor = 8
  coding_rate = 5
```

```powershell
rnstatus
```

## Hinweis SPI-Konflikt

Falls der Build wieder die falsche AVR-`SPI`-Lib zieht: Ordner  
`Documents\Arduino\libraries\SPI` umbenennen (hier schon als `SPI_AVR_CONFLICT_DISABLED`).
