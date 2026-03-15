"""ILI9341 demo (bouncing boxes)."""
from machine import Pin, SPI, UART
import time
from time import sleep
from ili9341 import Display, color565
from xglcd_font import XglcdFont
# from PIL import Image


def main():
    print("this is running")
    spi = SPI(0,
        baudrate=10000000,
        polarity=1,
        phase=1,
        bits=8,
        firstbit=SPI.MSB,
        sck=Pin(18),
        mosi=Pin(19),
        miso=Pin(16))

    display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14), rotation=90)

    # -------------------------------
    # INITIAL VALUES
    # -------------------------------
    temp = 90
    batt = 67
    temp_dir = 1
    mode = 1

    display.width = 320
    display.height = 240
    white = color565(255, 255, 255)
    gray = color565(150, 150, 150)
    blue = color565(3, 140, 252)
    dark_blue = color565(0, 53, 97)
    green = color565(60, 140, 40)
    yellow = color565(255, 230, 0)
    red = color565(255, 0, 0)

    font = XglcdFont('EspressoDolce18x24.c', 18, 24)

    # -------------------------------
    # BUTTONS
    # -------------------------------
    buttons = [1,
             Pin(2, Pin.IN, Pin.PULL_UP),  # K1
             Pin(3, Pin.IN, Pin.PULL_UP),  # K2
             Pin(4, Pin.IN, Pin.PULL_UP),  # K2
             Pin(5, Pin.IN, Pin.PULL_UP)   # K2
             ]

    # -------------------------------
    # STATIC UI
    # -------------------------------
    display.clear(color565(0, 0, 0))
    display.draw_image('teddy54x70.raw', 260, 8, 54, 70)

    # -------------------------------
    # MODE DRAW FUNCTION
    # -------------------------------
    class Button:
        def __init__(self, x, y, label, index, txtOffset=0):
            self.x = x
            self.y = y
            self.txtOffset = txtOffset
            self.label = label
            self.idx = index

            self.clx = x + 30
            self.cly = y + 30
            self.crx = x + 30 + 77
            self.cry = y + 30
            self.cr = 30

            self.rx = x + 30
            self.ry = y
            self.rw = 77
            self.rh = 61

            self.ox = x
            self.oy = y
            self.ow = 137
            self.oh = 60
    def draw_modes(active):
        ModeButtons = [
            Button(15, 90, "Mode 1", 1, 32),
            Button(168, 90, "Mode 2", 2, 32),
            Button(15, 165, "Mode 3", 3, 32),
            Button(168, 165, "Mode 4", 4, 32)
        ]

        for b in ModeButtons:
            if b.idx == active:
                display.fill_circle(b.clx, b.cly, b.cr, green)
                display.draw_circle(b.clx, b.cly, b.cr, yellow)
                display.fill_circle(b.crx, b.cry, b.cr, green)
                display.draw_circle(b.crx, b.cry, b.cr, yellow)
                display.fill_rectangle(b.rx, b.ry, b.rw, b.rh, green)
                # display.draw_rectangle(x, y, w, h, yellow)  # border
                y2 = b.ry + b.rh - 1
                display.draw_hline(b.rx, b.ry, b.rw, yellow)
                display.draw_hline(b.rx, y2, b.rw, yellow)
                bg = green
            else:
                display.fill_circle(b.clx, b.cly, b.cr, blue)
                display.fill_circle(b.crx, b.cry, b.cr, blue)
                display.fill_rectangle(b.rx, b.ry, b.rw, b.rh, blue)
                bg = blue

            display.draw_text(b.ox + b.txtOffset, b.oy + 21, b.label, font, white, bg)

        #
        # KILLSWITCH
        #
        kB = Button(92, 15, "Kill Switch", 0, 16)
        display.fill_circle(kB.clx, kB.cly, kB.cr, red)
        display.fill_circle(kB.crx, kB.cry, kB.cr, red)
        display.fill_rectangle(kB.rx, kB.ry, kB.rw, kB.rh, red)

        display.draw_text(kB.ox + kB.txtOffset, kB.oy + 21, "Kill Switch", font, white, red)

    # Draw initial mode
    draw_modes(mode)
    previous_mode = mode

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    while True:
        display.draw_text(15, 30, f"{round(batt, 1)}% ", font, white)

        # BUTTON HANDLING
        for i in range(len(buttons)):
            if i == 0:
                continue
            if buttons[i].value() == 0:
                mode = i
                sleep(0.15)

        # Only redraw mode UI when it CHANGES
        if mode != previous_mode:
            draw_modes(mode)
            previous_mode = mode

        # BATT VISUAL MOVEMENT
        # Just for showing movement

        batt = max(0, batt - 0.0005)
        sleep(0.05)

main()
