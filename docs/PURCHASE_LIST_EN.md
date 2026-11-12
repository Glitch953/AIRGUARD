# AIRGUARD — One-unit procurement list

This purchasing list is based on the project's existing `BOM_RevC_Minimal.csv`, plus one complete OLED display module. The original BOM includes only the OLED board header, not the display module itself. The user has confirmed that they currently own none of the parts; mark every Have it field as unchecked.

## Pricing notes
- Prices are indicative references/estimates, not guaranteed quotes. Stock, MOQ, packaging, shipping and taxes can change the checkout total.
- Capacitor, resistor and header prices are budget estimates; use the links to select the exact value and 0603 package.
- Do not combine USD and JOD into one total. The OLED module is listed at JOD 6 from a Jordanian seller.
- Distributor MOQ may exceed the number populated on the PCB. Buy the smallest available order quantity, but keep the PCB populated quantity unchanged.

## OLED module
Suggested module: 0.96-inch SSD1306, 128x64, I2C, 4-pin. The store lists pin order GND, VCC, SCL, SDA. PCB J2 order is 1=GND, 2=3V3, 3=SDA, 4=SCL. The suggested display listing uses GND, VCC, SCL, SDA. Do not connect by physical position without checking signal labels. Use four jumper leads and cross SDA/SCL as required; verify polarity before power-up.

## OLED wiring leads
- Add four jumper leads matching the connector genders on the PCB and display (often female-to-female if both sides have male headers).
- Connect by signal name: GND-to-GND, VCC-to-3V3, SDA-to-SDA, SCL-to-SCL. Do not assume the physical pin order matches.

## PCB fabrication
- Request a quote for 5 boards, 2 layers, approximately 68.75 x 50.00 mm, FR-4, 1.6 mm thickness, at https://jlcpcb.com/
- No fixed PCB price is included because a valid quote requires verified fabrication Gerbers/Drill and shipping destination.
- **Do not manufacture from `reference_gerbers_unmodified`.** These are old, unchanged reference files. No verified ERC/DRC or fresh manufacturing export has been completed.
- In KiCad, update PCB from schematic, refill zones, review ERC/DRC, export fresh Gerber and Drill files, and inspect them before ordering.

## Do not buy/populate in this revision
- R7: DNP (not populated).
- U3 / buzzer: DNP; buzzer disabled. Do not fit the buzzer or drive it directly from an MCU GPIO.

## Preliminary total
The USD-priced line items in the CSV total approximately USD 7.55, plus JOD 6.00 for the OLED. This is a preliminary parts-only estimate; it excludes MOQ overages, shipping, taxes and PCB fabrication. Confirm all live prices at checkout.

## Project status
This archive is a design/software/procurement package for a prototype. It does not mean the PCB has been validated or is fabrication-ready, and it does not claim the device has been assembled or tested on hardware.
