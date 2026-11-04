# AIRGUARD - MicroPython firmware
# Target: ESP32-S3-WROOM-1-N8
# Passive Wi-Fi environment scanner. Does NOT connect to APs or transmit deauth/jam frames.

import time
import gc
import network
from machine import Pin, SoftI2C
import ssd1306

# ---- Pin map from AIRGUARD PCB nets ----
# OLED J2: pin 3 SDA -> module pad 6 (GPIO6); pin 4 SCL -> module pad 7 (GPIO7)
I2C_SDA = 6
I2C_SCL = 7

# SW1..SW5 connect GPIO1..GPIO5 to GND when pressed (active LOW)
BTN_UP = 1
BTN_DOWN = 2
BTN_SELECT = 3
BTN_BACK = 4
BTN_SCAN = 5

OLED_WIDTH = 128
OLED_HEIGHT = 64
SCAN_LIMIT = 80
DEBOUNCE_MS = 35

AUTH_NAMES = {
    0: "OPEN",
    1: "WEP",
    2: "WPA",
    3: "WPA2",
    4: "WPA/WPA2",
    5: "WPA2-ENT",
    6: "WPA3",
}

def safe_text(value):
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except Exception:
            return value.decode("latin-1", "replace")
    return str(value)

class Button:
    def __init__(self, gpio):
        self.pin = Pin(gpio, Pin.IN, Pin.PULL_UP)
        self.last_raw = self.pin.value()
        self.stable = self.last_raw
        self.changed_at = time.ticks_ms()
        self.pressed_event = False

    def update(self, now):
        raw = self.pin.value()
        self.pressed_event = False
        if raw != self.last_raw:
            self.last_raw = raw
            self.changed_at = now
        elif raw != self.stable and time.ticks_diff(now, self.changed_at) >= DEBOUNCE_MS:
            self.stable = raw
            if self.stable == 0:
                self.pressed_event = True
        return self.pressed_event

class AirGuard:
    def __init__(self):
        self.display = None
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.buttons = {
            "up": Button(BTN_UP),
            "down": Button(BTN_DOWN),
            "select": Button(BTN_SELECT),
            "back": Button(BTN_BACK),
            "scan": Button(BTN_SCAN),
        }
        self.access_points = []
        self.selected = 0
        self.detail = False
        self.message = "Ready"
        self.last_draw = 0

        # SoftI2C keeps this project independent from board-specific I2C pin defaults.
        self.i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
        devices = self.i2c.scan()
        if 0x3C in devices:
            self.display = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, self.i2c, addr=0x3C)
        elif 0x3D in devices:
            self.display = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, self.i2c, addr=0x3D)

    def draw(self):
        if self.display is None:
            return
        d = self.display
        d.fill(0)

        if self.detail and self.access_points:
            ap = self.access_points[self.selected]
            d.text("AIRGUARD  AP INFO", 0, 0)
            d.text("SSID:", 0, 12)
            d.text(ap["ssid"][:19], 0, 22)
            d.text("CH:{} RSSI:{}dB".format(ap["channel"], ap["rssi"]), 0, 34)
            d.text(ap["auth"][:20], 0, 46)
            d.text("BACK: return", 0, 56)
        else:
            d.text("AIRGUARD Wi-Fi", 0, 0)
            if not self.access_points:
                d.text(self.message[:20], 0, 18)
                d.text("SCAN: GPIO5", 0, 34)
                d.text("SEL: details", 0, 46)
            else:
                d.text("{} networks".format(len(self.access_points)), 0, 10)
                start = max(0, min(self.selected - 1, len(self.access_points) - 3))
                for row in range(3):
                    idx = start + row
                    if idx >= len(self.access_points):
                        break
                    ap = self.access_points[idx]
                    marker = ">" if idx == self.selected else " "
                    ssid = ap["ssid"] if ap["ssid"] else "<hidden>"
                    d.text("{}{}".format(marker, ssid[:15]), 0, 22 + row * 10)
                d.text("UP/DN  SEL  SCAN", 0, 56)
        d.show()

    def scan(self):
        self.message = "Scanning..."
        self.draw()
        try:
            # Passive scan only. No association, credential collection or packet injection.
            found = self.wlan.scan()
            aps = []
            for item in found[:SCAN_LIMIT]:
                ssid = safe_text(item[0]).strip()
                channel = int(item[2])
                rssi = int(item[3])
                auth_id = int(item[4])
                hidden = int(item[5]) if len(item) > 5 else 0
                if hidden and not ssid:
                    ssid = ""
                aps.append({
                    "ssid": ssid,
                    "channel": channel,
                    "rssi": rssi,
                    "auth": AUTH_NAMES.get(auth_id, "SECURED({})".format(auth_id)),
                })
            aps.sort(key=lambda x: x["rssi"], reverse=True)
            self.access_points = aps
            self.selected = 0
            self.detail = False
            self.message = "{} found".format(len(aps))
        except Exception as exc:
            self.access_points = []
            self.message = "Scan error"
            print("Wi-Fi scan failed:", repr(exc))
        gc.collect()
        self.draw()

    def handle_buttons(self):
        now = time.ticks_ms()
        events = []
        for name, button in self.buttons.items():
            if button.update(now):
                events.append(name)

        if "scan" in events:
            self.scan()
        elif "back" in events:
            self.detail = False
            self.draw()
        elif "up" in events and self.access_points:
            self.detail = False
            self.selected = max(0, self.selected - 1)
            self.draw()
        elif "down" in events and self.access_points:
            self.detail = False
            self.selected = min(len(self.access_points) - 1, self.selected + 1)
            self.draw()
        elif "select" in events and self.access_points:
            self.detail = not self.detail
            self.draw()

    def run(self):
        print("AIRGUARD MicroPython started")
        print("I2C scan:", self.i2c.scan())
        if self.display is None:
            print("OLED not found at 0x3C/0x3D. Check SDA=GPIO6, SCL=GPIO7 and power.")
        self.draw()
        while True:
            self.handle_buttons()
            time.sleep_ms(15)

app = AirGuard()
app.run()
