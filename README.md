# AIRGUARD

A portable, privacy-focused Wi-Fi environment analyzer based on the ESP32-S3. AIRGUARD passively scans nearby Wi-Fi network beacons and displays network metadata (SSID, channel, RSSI and security type) on an SSD1306 OLED.

## Project status

This repository is a **design-stage prototype package**, not a validated manufacturing release. The KiCad source files are included for review and continued development. The PCB copper layout has not been rerouted in this package, and no KiCad ERC/DRC validation or hardware test is claimed.

The Gerber and drill files in `hardware/reference_gerbers_unmodified/` are copied from the original export and are provided for historical reference only. **They do not represent a newly revised PCB and must not be sent for fabrication as the final design.** Generate fresh fabrication outputs from the reviewed final KiCad board after electrical and mechanical checks.

## Repository layout

- `hardware/kicad/` — editable KiCad PCB, schematic and project source.
- `hardware/bom/` — minimal prototype BOM and placement list; verify manufacturer part numbers, quantities and sourcing before ordering.
- `hardware/reference_gerbers_unmodified/` — unchanged original Gerber/drill export for reference only.
- `firmware/micropython/` — initial MicroPython firmware and SSD1306 driver.
- `docs/` — revision status and assembly/firmware cautions.

## Firmware

The firmware uses MicroPython on ESP32-S3. It performs passive Wi-Fi scanning only; it does not connect to networks, capture passwords, transmit deauthentication frames, or jam networks. The pin map is a design assumption and must be checked against the assembled hardware before use.

## Important hardware cautions

- R7 and U3 are marked DNP in the prototype assembly notes. Do not populate them as-is.
- The buzzer output needs a suitable transistor/MOSFET driver before a buzzer is connected; do not drive the magnetic buzzer directly from an ESP32 GPIO.
- Confirm the OLED I2C pin mapping and all power/USB connections against the final schematic and datasheets.
- GPIO3 is a boot-strapping pin; avoid holding its button during reset/boot.

## Validation status

- KiCad ERC: not run.
- KiCad PCB DRC: not run.
- Gerber regeneration from this source: not performed.
- Physical assembly and firmware test: not performed; components are not yet available.

## License

Add a license before accepting external contributions or reuse.
