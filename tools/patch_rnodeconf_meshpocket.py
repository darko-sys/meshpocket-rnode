"""Re-apply MeshPocket IDs to installed rnodeconf after pip upgrade of rns.

Run: python tools/patch_rnodeconf_meshpocket.py
"""
from __future__ import annotations

import pathlib
import sys

MARKER = "PRODUCT_HELTEC_MESHP"
SNIPPET_ROM = """
    PRODUCT_HELTEC_MESHP = 0xD2
    BOARD_HELTEC_MESHP   = 0x46
    MODEL_CD             = 0xCD # Heltec MeshPocket, 470-510 MHz
    MODEL_CE             = 0xCE # Heltec MeshPocket, 863-928 MHz
"""

def main() -> int:
    try:
        import RNS.Utilities.rnodeconf as rc
    except ImportError:
        print("rns not installed; pip install rns", file=sys.stderr)
        return 1
    path = pathlib.Path(rc.__file__)
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"Already patched: {path}")
        return 0
    needle = "    PRODUCT_HELTEC_T114 = 0xC2"
    if needle not in text:
        print("Unexpected rnodeconf.py layout; patch manually", file=sys.stderr)
        return 1
    print(f"Please re-apply MeshPocket support to:\n  {path}\nSee project README / git history for the full patch.")
    print("ROM constants to add after T114 block:")
    print(SNIPPET_ROM)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
