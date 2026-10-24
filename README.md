# MeshPocket + RNode (Reticulum)

Community board support that turns a **Heltec MeshPocket** into an **RNode** (LoRa modem for [Reticulum](https://reticulum.network/)). The network stack runs on your PC or phone; this firmware drives the radio, e-ink status UI, and optional BLE link.

This is **not** an official Heltec, Mark Qvist, or Liberated Systems product. It is a derivative of [RNode Firmware CE](https://github.com/liberatedsystems/RNode_Firmware_CE) (GPL-3). Upstream Mark Qvist’s RNode repo does not accept new hardware PRs; CE does.

Related community threads: [Reticulum #887](https://github.com/markqvist/Reticulum/discussions/887), [CE #87](https://github.com/liberatedsystems/RNode_Firmware_CE/pull/87).

## Status

| Feature | State |
|---------|--------|
| USB KISS / Reticulum | Works |
| LoRa EU 865.2 MHz @ 14 dBm, SF8, BW125, CR5 | Works |
| E-ink status UI | Works |
| BLE advertising / pairing | Experimental — Android Sideband often flaky; prefer USB |
| Windows Sideband `ble://` | Avoid — can crash the app |

## Quick start

1. Read **[FLASH.md](FLASH.md)** — magnetic USB cable, double-tap RST, copy `dist/meshpocket_rnode_868.uf2`.
2. Point Reticulum at the COM port (see FLASH.md). Keys are `spreadingfactor` / `codingrate` (not `spreading_factor`).

## Repo layout

| Path | Role |
|------|------|
| `RNode_Firmware_CE/` | Firmware sources (branch `meshpocket-support`) |
| `dist/meshpocket_rnode_868.uf2` | Ready-to-flash EU 868 image |
| `tools/patch_rnodeconf_meshpocket.py` | Hint/re-apply MeshPocket IDs in local `rnodeconf` after `pip install -U rns` |
| `UPSTREAM_PR.md` | Notes for contributing board support back to CE |

Product / board IDs: `0xD2` / `0xCE` / `0x46` (EU 868 model).

## Build (Windows)

```powershell
cd RNode_Firmware_CE
arduino-cli core update-index --config-file arduino-cli.yaml
# Install nRF cores + libs (see Makefile target prep-nrf), then:
arduino-cli compile --fqbn Heltec_nRF52:Heltec_nRF52:HT-n5262 -e `
  --build-property "compiler.cpp.extra_flags=`"-DBOARD_MODEL=0x46`" `"-DBOARD_VARIANT=0xCE`""
```

Or: `make firmware-heltec_meshpocket`. Output under `build/Heltec_nRF52.Heltec_nRF52.HT-n5262/`.

## Credits

- Mark Qvist — RNode / Reticulum
- Liberated Embedded Systems — [RNode Firmware CE](https://github.com/liberatedsystems/RNode_Firmware_CE)
- Heltec — MeshPocket hardware
- Contributors exploring MeshPocket RNode support in the threads linked above

## License

GPL-3.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).
