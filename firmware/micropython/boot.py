# AIRGUARD boot.py
# Keep USB serial available for REPL / Thonny where supported.
import time
try:
    import machine
    machine.freq(160000000)
except Exception:
    pass
