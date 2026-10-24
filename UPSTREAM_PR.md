# Upstream PR notes (liberatedsystems / RNode_Firmware_CE)

When this work is ready to go public, open a PR against
https://github.com/liberatedsystems/RNode_Firmware_CE (not markqvist/RNode_Firmware —
new hardware is directed to CE).

## Suggested title

Add Heltec MeshPocket board support (EU 868, e-ink, BLE)

## Suggested body

```markdown
## Summary

- Board definition for Heltec MeshPocket (`PRODUCT_HELTEC_MESHP` / `BOARD_HELTEC_MESHP`, models `0xCD` / `0xCE`)
- Pin map and SX1262 path aligned with T114-class hardware
- SSD1680 e-ink status UI (GxEPD2_213_B74), landscape layout
- BLE enabled by default with longer pairing window for slow e-ink
- Factory EEPROM / validate behaviour tuned so MeshPocket brings up over USB without a signed flash gate blocking use

## Test plan

- [ ] Flash UF2 via magnetic cable, double-RST → `HT-n5262`
- [ ] `rnodeconf COMx -i` shows product `d2:ce:46` (or equivalent)
- [ ] Reticulum `RNodeInterface` Up at 865200000 / 125000 / 14 / SF8 / CR5
- [ ] E-ink shows RNode UI after boot
- [ ] (Optional) BLE advertises `RNode xxxx`; note Android Sideband pairing remains flaky on some OS versions

## Notes

- Prefer documenting USB as the reliable host path; BLE is best-effort.
- Local `rnodeconf` may need MeshPocket product IDs until `rns` ships them.
- Related: reticulum discussion #887, CE PR #87 (earlier experimental work).
```

## Diff scope (keep the PR focused)

Prefer committing only firmware board support under CE:

- `Boards.h`, `Display.h`, `Bluetooth.h`, `Utilities.h`, `RNode_Firmware_CE.ino`, radio/TX power if needed
- Short doc blurb in CE README for MeshPocket flash

Leave wrapper-only files (`FLASH.md`, `dist/*.uf2`, `tools/patch_*.py`) out of the CE PR; ship those via this meta-repo / Releases.
