# MeshPocket + Reticulum (RNode)

Turn a Heltec MeshPocket into an **RNode** (LoRa modem for Reticulum). The Reticulum stack runs on your PC/phone; this firmware only drives the radio.

## Repo layout

- `RNode_Firmware_CE/` — fork branch `meshpocket-support` with MeshPocket board support (IDs `d2:ce:46`, EU 868 model `0xCE`).

## Build (Windows)

```powershell
cd RNode_Firmware_CE
arduino-cli core update-index --config-file arduino-cli.yaml
# Install nRF cores + libs (see Makefile target prep-nrf), then:
arduino-cli compile --fqbn Heltec_nRF52:Heltec_nRF52:HT-n5262 -e `
  --build-property "compiler.cpp.extra_flags=`"-DBOARD_MODEL=0x46`" `"-DBOARD_VARIANT=0xCE`""
```

Or: `make firmware-heltec_meshpocket` (needs Unix-ish `make`).

Output UF2/hex under `build/Heltec_nRF52.Heltec_nRF52.HT-n5262/`.

## Flash

1. Use the **magnetic USB data cable** (not charge-only USB-C).
2. Coming from Meshtastic: erase once (Meshtastic erase UF2), then DFU again.
3. Double-press **RST** → drive `HT-n5262` → copy the `.uf2`.
4. Provision EEPROM: `rnodeconf --autoinstall` and choose **Heltec MeshPocket** / 868 MHz, **or** after flash set firmware hash as documented by CE.

Local `rnodeconf` was patched for MeshPocket product IDs (`0xD2` / `0xCE` / board `0x46`). Re-apply after `pip install -U rns` if needed (see `tools/patch_rnodeconf_meshpocket.py`).

## Reticulum config

In `%USERPROFILE%\.reticulum\config`:

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

Then: `rnstatus`

## Later

- Propagation node on Raspberry Pi (Pi-hole host) — not part of this firmware.
- E-Ink UI — deferred until radio + USB are solid.
