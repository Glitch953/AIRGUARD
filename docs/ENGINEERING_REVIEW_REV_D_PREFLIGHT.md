# AIRGUARD — Engineering Review & Source Cleanup (Rev D-preflight)

Date: 2026-11-12

## What was actually changed in this package

1. Normalized schematic instance Value fields to match the actual BOM/PCB manufacturer part identifiers for D1, D2, J1, J3, SW1–SW6, U2 and U3.
2. Kept R7 and U3 marked DNP in the schematic. They are excluded from the populated Rev C BOM/CPL.
3. Corrected firmware and README wording: MicroPython `WLAN.scan()` is not proof of passive-only RF scanning. The firmware does not associate with APs, collect credentials, deauthenticate or jam, but the scan mode must be verified for the exact ESP32 MicroPython port before claiming passive-only behavior.
4. Documented the OLED connector signal order and added four jumper leads to the purchase BOM. J2 PCB order is GND, 3V3, SDA, SCL; the suggested OLED listing order is GND, VCC, SCL, SDA. Wire by signal labels, not physical order.

## Confirmed issues that remain open

### R7 pull-down conflict
PCB pads for R7 are GPIO1-to-GND. This conflicts with the firmware's `Pin.PULL_UP` use if R7 is populated. R7 remains DNP and must not be fitted on this prototype. A future PCB revision may redesign it as a 3V3 pull-up only after schematic and board are updated together.

### Buzzer drive
The original board connects U3 directly between BUZZER_DRV and GND. This is not approved for the specified magnetic buzzer load. U3 remains DNP and buzzer functionality is disabled. A proper driver stage and routed PCB revision are required before adding a buzzer.

### OLED wiring
J2 signal order and the selected display module's listed physical pin order differ. Use jumper leads and connect by signal name. Verify the exact module silk labels and supply voltage before powering.

### ESP32 scan mode
The current MicroPython `WLAN.scan()` call does not set a passive-only scan flag. Do not advertise the current firmware as passive-only. To meet a strict passive-only requirement, use a supported ESP-IDF/native implementation that explicitly configures passive scanning, then verify over-the-air behavior.

### PCB fabrication release
The package still contains unchanged reference Gerber/Drill files. The board has not been rerouted in this revision. No genuine KiCad ERC, PCB DRC, zone refill, netlist equivalence check, fresh Gerber export, or physical hardware test has been performed in this environment.

**Do not upload `hardware/reference_gerbers_unmodified/` to a fabricator as final manufacturing data.**

## Required KiCad work before ordering PCB

1. Open `hardware/kicad/New_Board.kicad_pro` in KiCad.
2. Run Update PCB from Schematic and inspect all 28 footprints and nets.
3. Review ESP32-S3 module pad numbering and antenna keepout against the official module datasheet and footprint.
4. Verify USB-C CC1/CC2, D+/D− routing, ESD device pinout, and differential pair geometry against the exact connector/protection datasheets and fabricator stack-up.
5. Review AP2112K input/output capacitors, thermal dissipation and peak ESP32 current budget.
6. Keep R7 and U3 DNP in this prototype, or redesign both circuits and routes in a new revision.
7. Refill copper zones; run ERC and DRC; fix all errors and review warnings.
8. Generate fresh Gerber, drill, BOM and CPL from the exact checked PCB. Inspect exported layers and dimensions before ordering.

## Scope statement

This is a source/documentation cleanup and engineering preflight, **not a validated electrical redesign** and **not a manufacturing release**. The PCB copper geometry and routing are intentionally unchanged because modifying routes without KiCad's native engine and a complete ERC/DRC verification would be unsafe.
