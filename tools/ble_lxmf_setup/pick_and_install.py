"""Offline install of rns/lxmf/bleak using only compatible wheels."""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

from pip._internal.models.wheel import Wheel
from pip._internal.utils.compatibility_tags import get_supported


def main() -> int:
    wheel_dir = pathlib.Path(__file__).resolve().parent / "wheels"
    print("Python", sys.version.replace("\n", " "))
    print("Executable", sys.executable)

    supported = get_supported()
    print("Tags:", ", ".join(str(t) for t in supported[:6]), "...")

    cffi_ok = []
    cffi_bad = []
    for whl in sorted(wheel_dir.glob("cffi-*.whl")):
        w = Wheel(whl.name)
        if w.supported(supported):
            cffi_ok.append(whl.name)
        else:
            cffi_bad.append(whl.name)
    print("cffi compatible:", cffi_ok or "(none!)")
    if cffi_bad:
        print("cffi skipped:", cffi_bad)

    if not cffi_ok:
        print(
            "ERROR: No cffi wheel for this Python/platform.\n"
            "Need Windows x64 Python 3.11, 3.12 or 3.13.\n"
            "Check: python --version   and   python -c \"import struct; print(struct.calcsize('P')*8)\"",
            file=sys.stderr,
        )
        return 1

    env = os.environ.copy()
    env["PIP_NO_INDEX"] = "1"
    env.pop("PIP_INDEX_URL", None)
    env.pop("PIP_FIND_LINKS", None)

    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--no-index",
        "--find-links",
        str(wheel_dir),
        "rns",
        "lxmf",
        "bleak",
    ]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
