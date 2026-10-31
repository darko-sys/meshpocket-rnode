# MeshPocket + RNode (Reticulum)

Community board support that turns a **Heltec MeshPocket** into an **RNode** (LoRa modem for [Reticulum](https://reticulum.network/)). The network stack runs on a host (PC, phone, Pi); this firmware drives the radio, e-ink status UI, BLE link, and deep sleep.

This is **not** an official Heltec, Mark Qvist, or Liberated Systems product. It is a derivative of [RNode Firmware CE](https://github.com/liberatedsystems/RNode_Firmware_CE) (GPL-3). Upstream Mark Qvist’s RNode repo does not accept new hardware PRs; CE does.

Related community threads: [Reticulum #887](https://github.com/markqvist/Reticulum/discussions/887), [CE #87](https://github.com/liberatedsystems/RNode_Firmware_CE/pull/87).

## Focus

Primary work is **Heltec MeshPocket firmware** (USB + BLE RNode, e-ink, sleep, battery). Companion apps (Sideband, custom clients) are secondary: they consume a working RNode; they are not the product.

## Status (interim)

| Feature | State |
|---------|--------|
| USB KISS / Reticulum | **Proven** |
| BLE NUS / KISS (Windows `bleak` / `rns`) | **Proven** (bond + encrypted NUS) |
| LoRa air path (two MeshPockets: USB host ↔ BLE host on one PC) | **Proven** — bidirectional LXMF dummy messages |
| Radio baseline after boot | EU **869.525 MHz**, BW 125 kHz, SF8, CR6, TX 14 dBm |
| E-ink status + battery bars (ADC) | Works |
| USER hold UX (RNode-compatible) + airplane `SYSTEMOFF` | Works |
| Stock Sideband on Android (esp. Xiaomi) | **Unreliable so far** — often pairs but does not stay **connected**; may be phone/OS/app, not the MeshPocket |

### Call for testers (Sideband)

If you have **stock Sideband** on a **non-Xiaomi** Android (Pixel/Graphene, Samsung, …) or iOS:

1. Flash the UF2 from [`dist/`](dist/) (see [FLASH.md](FLASH.md)).
2. Radio: **869.525** MHz / 125 kHz / SF8 / CR6 / 14 dBm, **Device requires BLE**.
3. Report whether the MeshPocket e-ink shows BLE **connected** (not only system “paired”), and whether announces/messages reach a second RNode (USB PC or another phone).

That feedback separates “MeshPocket BLE broken” from “this phone/Sideband stack is flaky”.

## Quick start

1. Read **[FLASH.md](FLASH.md)** — magnetic USB cable, double-tap RST, copy `dist/meshpocket_rnode_868.uf2`.
2. Point Reticulum at the COM port or `ble://…` (PC: prefer USB for Sideband Desktop; BLE via `rns`/`bleak` is fine). Config keys are `spreadingfactor` / `codingrate`.

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

## Repositories (private for now)

| Repo | Contents |
|------|----------|
| https://github.com/darko-sys/meshpocket-rnode | Docs, UF2 releases, this meta-repo |
| https://github.com/darko-sys/RNode_Firmware_CE-meshpocket | Firmware (`meshpocket-support`), based on CE |

When public: open a PR to [liberatedsystems/RNode_Firmware_CE](https://github.com/liberatedsystems/RNode_Firmware_CE) using [UPSTREAM_PR.md](UPSTREAM_PR.md).

## License

GPL-3.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).
