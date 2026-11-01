"""
Single MeshPocket over BLE: announce + send/receive LXMF dummies.
Run the same script on two PCs (each with its own bonded MeshPocket).

Usage:
  python ble_lxmf_node.py --addr FE:27:4D:E8:49:6E
  python ble_lxmf_node.py --addr F8:62:53:9C:2B:17 --name "RNode 6702"

Requires: pip install rns lxmf bleak
"""
from __future__ import annotations

import argparse
import os
import time

import LXMF
import RNS

FREQ = 869525000
BW = 125000
SF = 8
CR = 6
TX = 14


def write_config(config_dir: str, ble_addr: str, ble_name: str | None) -> None:
    os.makedirs(os.path.join(config_dir, "storage"), exist_ok=True)
    # Prefer address; name is optional comment for humans
    port = f"ble://{ble_addr}"
    cfg = f"""[reticulum]
  enable_transport = Yes
  share_instance = No
  instance_name = meshp_ble_lxmf

[logging]
  loglevel = 6

[interfaces]
  # No AutoInterface — force LoRa path only (no LAN shortcut)
  [[MeshPocketBLE]]
    type = RNodeInterface
    enabled = Yes
    port = {port}
    frequency = {FREQ}
    bandwidth = {BW}
    txpower = {TX}
    spreadingfactor = {SF}
    codingrate = {CR}
"""
    path = os.path.join(config_dir, "config")
    with open(path, "w", encoding="utf-8") as f:
        f.write(cfg)
    print(f"Config written: {path}")
    print(f"  port={port}" + (f"  # {ble_name}" if ble_name else ""))


def main() -> None:
    ap = argparse.ArgumentParser(description="MeshPocket BLE LXMF node")
    ap.add_argument("--addr", required=True, help="BLE MAC, e.g. FE:27:4D:E8:49:6E")
    ap.add_argument("--name", default=None, help="Optional display name, e.g. RNode E827")
    ap.add_argument(
        "--dir",
        default=os.path.join(os.environ.get("TEMP", "."), "meshp_ble_lxmf"),
        help="Reticulum config/storage directory",
    )
    ap.add_argument("--interval", type=float, default=15.0, help="Announce / send interval seconds")
    args = ap.parse_args()

    write_config(args.dir, args.addr.strip(), args.name)

    RNS.loglevel = RNS.LOG_NOTICE
    RNS.Reticulum(args.dir)

    idpath = os.path.join(args.dir, "storage", "identity")
    try:
        identity = RNS.Identity.from_file(idpath)
    except Exception:
        identity = None
    if identity is None:
        identity = RNS.Identity()
        identity.to_file(idpath)
        print("Created new identity")

    lxmf_dir = os.path.join(args.dir, "lxmf")
    os.makedirs(lxmf_dir, exist_ok=True)
    router = LXMF.LXMRouter(identity=identity, storagepath=lxmf_dir)
    local = router.register_delivery_identity(
        identity, display_name=args.name or f"PC-{args.addr[-5:]}"
    )

    def on_delivery(message):
        content = message.content
        if isinstance(content, (bytes, bytearray)):
            content = content.decode("utf-8", errors="replace")
        print(
            f"MSG_IN from={RNS.prettyhexrep(message.source_hash)} text={content!r}",
            flush=True,
        )

    router.register_delivery_callback(on_delivery)

    peers: dict[bytes, float] = {}

    class AH:
        aspect_filter = "lxmf.delivery"

        @staticmethod
        def received_announce(destination_hash, announced_identity, app_data):
            if destination_hash == local.hash:
                return
            peers[destination_hash] = time.time()
            print(f"PEER {RNS.prettyhexrep(destination_hash)}", flush=True)

    RNS.Transport.register_announce_handler(AH())

    print(f"Local lxmf={RNS.prettyhexrep(local.hash)}", flush=True)
    for iface in RNS.Transport.interfaces:
        print(f"  {iface} online={iface.online}", flush=True)

    if not any(getattr(i, "online", False) for i in RNS.Transport.interfaces):
        print("FAIL: RNode BLE not online. Bond the MeshPocket in Windows first, then retry.")
        return

    local.announce()
    print("Announced. Waiting for peer…", flush=True)

    n = 0
    last = 0.0
    while True:
        now = time.time()
        if now - last >= args.interval:
            local.announce()
            # Send a dummy to every known peer that has a path
            for ph in list(peers.keys()):
                if not RNS.Transport.has_path(ph):
                    RNS.Transport.request_path(ph)
                    print(f"Requesting path to {RNS.prettyhexrep(ph)}", flush=True)
                    continue
                peer_id = RNS.Identity.recall(ph)
                if peer_id is None:
                    continue
                dest = RNS.Destination(
                    peer_id,
                    RNS.Destination.OUT,
                    RNS.Destination.SINGLE,
                    "lxmf",
                    "delivery",
                )
                text = f"hello-from-{args.addr[-5:]}-{n}-{int(now)}"
                msg = LXMF.LXMessage(dest, local, text, desired_method=LXMF.LXMessage.DIRECT)
                router.handle_outbound(msg)
                print(f"MSG_OUT {text!r} -> {RNS.prettyhexrep(ph)}", flush=True)
                n += 1
            last = now
        time.sleep(0.4)


if __name__ == "__main__":
    main()
