# Minimal SSD1306 128x64 I2C driver for MicroPython
# Based on the public SSD1306 command/data protocol.
import framebuf

class SSD1306_I2C:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.pages = self.height // 8
        self.buffer = bytearray(self.width * self.pages)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self._write_cmd(0xAE)
        for cmd in (
            0x20, 0x00, 0x40, 0xA1, 0xA8, self.height - 1,
            0xC8, 0xD3, 0x00, 0xDA, 0x12 if self.height == 64 else 0x02,
            0xD5, 0x80, 0xD9, 0xF1, 0xDB, 0x30, 0x81, 0xFF,
            0xA4, 0xA6, 0x8D, 0x14, 0xAF
        ):
            self._write_cmd(cmd)

    def _write_cmd(self, cmd):
        self.i2c.writeto(self.addr, b"\x00" + bytes([cmd]))

    def fill(self, color):
        self.framebuf.fill(color)

    def pixel(self, x, y, color=None):
        return self.framebuf.pixel(x, y, color)

    def text(self, string, x, y, color=1):
        self.framebuf.text(str(string), x, y, color)

    def show(self):
        for page in range(self.pages):
            self._write_cmd(0xB0 | page)
            self._write_cmd(0x00)
            self._write_cmd(0x10)
            start = page * self.width
            self.i2c.writeto(self.addr, b"\x40" + self.buffer[start:start + self.width])
