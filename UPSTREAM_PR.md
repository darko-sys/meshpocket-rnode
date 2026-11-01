# Upstream PR notes (liberatedsystems / RNode_Firmware_CE)

Public forks already exist (`darko-sys/meshpocket-rnode`,
`darko-sys/RNode_Firmware_CE-meshpocket`). Open the CE PR against
https://github.com/liberatedsystems/RNode_Firmware_CE (not markqvist/RNode_Firmware —
new hardware is directed to CE).

## Suggested title

Add Heltec MeshPocket board support (EU 868, e-ink, BLE)

## Suggested body

```markdown
## Summary

- Board definition for Heltec MeshPocket (`PRODUCT_HELTEC_MESHP` / `BOARD_HELTEC_MESHP`, models `0xCD` / `0xCE`)
- Pin map and SX1262 path aligned with Meshtastic heltec_mesh_pocket / T114-class hardware
- SSD1680 e-ink status UI (GxEPD2_213_B74), landscape layout, battery ADC
- BLE + LoRa on by default after boot (EU 869.525 / 125k / SF8 / CR6 / 14 dBm baseline)
- RNode-compatible USER hold: tap BLE, hold airplane SYSTEMOFF, long hold pairing
- Factory / validate behaviour tuned so MeshPocket comes up over USB without a signed flash gate blocking use

## Test plan

- [ ] Flash UF2 via magnetic cable, double-RST → `HT-n5262`
- [ ] `rnodeconf COMx -i` shows product `d2:ce:46` (or equivalent)
- [ ] Reticulum `RNodeInterface` Up at 869525000 / 125000 / 14 / SF8 / CR6 (USB)
- [ ] BLE: Windows bond + NUS/KISS (`bleak`/`rns`); e-ink shows connected under a working host
- [x] Two MeshPockets (USB host + BLE host on one PC): LoRa announce and LXMF message exchange
- [x] Two PCs, each one MeshPocket over BLE only: LoRa LXMF both directions (2026-11-01)
- [ ] E-ink shows RNode UI + battery; airplane sleep splash; wake via USER
- [ ] (Community) Stock Sideband on non-Xiaomi phones — report connect vs pair-only

## Notes

- MeshPocket RNode path is host-driven (official RNode model); on-device settings menu is out of scope.
- Android Sideband BLE remains flaky on some OEMs; treat USB / PC `rns` BLE as the validation path.
- Dual-PC procedure: `tools/BLE_LXMF_ZWEI_PCS.md` in the meta-repo.
- Local `rnodeconf` may need MeshPocket product IDs until `rns` ships them.
- Related: reticulum discussion #887, CE PR #87 (earlier experimental work).
```

## Diff scope (keep the PR focused)

Prefer committing only firmware board support under CE:

- `Boards.h`, `Display.h`, `Bluetooth.h`, `Utilities.h`, `Power.h`, `Input.h`, `RNode_Firmware_CE.ino`, radio/TX power if needed
- Short doc blurb in CE README for MeshPocket flash

Leave wrapper-only files (`FLASH.md`, `dist/*.uf2`, `tools/patch_*.py`) out of the CE PR; ship those via this meta-repo / Releases.
