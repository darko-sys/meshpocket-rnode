Zweiter PC — Offline-Kit (Windows x64, Python 3.13)

Siehe auch: ../BLE_LXMF_ZWEI_PCS.md (Testergebnis 2026-11-01: bestanden).

1) Python 3.13 x64 installieren (nicht 3.15). py-Launcher aktivieren.
   Pruefen:  py -3.13 --version

2) Diesen Ordner komplett kopieren (inkl. wheels\).

3) .\setup.ps1
   -> venv mit 3.13, install aus wheels\ (kein PyPI noetig)

4) MeshPocket nur an DIESEM PC koppeln (PIN vom Display). Sideband zu, kein USB.

5) Start:
   .\.venv\Scripts\Activate.ps1
   python ble_lxmf_node.py --addr F8:62:53:9C:2B:17 --name "RNode 6702"

Erfolg: online=True, PEER, MSG_IN / MSG_OUT
