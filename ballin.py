"""ILI9341 demo (bouncing boxes)."""
from machine import Pin, SPI
from time import sleep
from ili9341 import Display, color565
from xglcd_font import XglcdFont


def test_Text():
    # -------------------------------
    # DISPLAY SETUP
    # -------------------------------
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
    mode_one = False

    display.width = 320
    display.height = 240
    white = color565(255, 255, 255)
    gray = color565(150, 150, 150)
    blue = color565(3, 140, 252)
    dark_blue = color565(0, 53, 97)

    # -------------------------------
    # BUTTONS
    # -------------------------------
    button_mode1 = Pin(2, Pin.IN, Pin.PULL_UP)  # K1
    button_mode2 = Pin(3, Pin.IN, Pin.PULL_UP)  # K2

    # -------------------------------
    # STATIC UI
    # -------------------------------
    display.clear(color565(0, 0, 0))
    font = XglcdFont('EspressoDolce18x24.c', 18, 24)

    display.fill_rectangle(15, 15, 290, 60, gray)
    display.fill_rectangle(15, 90, 290, 60, gray)

    display.draw_text(65, 35, "Temperature:", font, white, gray)
    display.draw_text(65, 110, "Percentage:", font, white, gray)

    # -------------------------------
    # MODE DRAW FUNCTION
    # -------------------------------
    def draw_modes(active_mode_1):
        if active_mode_1:
            display.fill_rectangle(15, 165, 137, 60, dark_blue)
            display.fill_rectangle(168, 165, 137, 60, blue)
            display.draw_text(45, 185, "Mode 1", font, white, dark_blue)
            display.draw_text(195, 185, "Mode 2", font, white, blue)
        else:
            display.fill_rectangle(15, 165, 137, 60, blue)
            display.fill_rectangle(168, 165, 137, 60, dark_blue)
            display.draw_text(45, 185, "Mode 1", font, white, blue)
            display.draw_text(195, 185, "Mode 2", font, white, dark_blue)

    # Draw initial mode
    draw_modes(mode_one)
    previous_mode = mode_one

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    while True:
        # Draw temp and battery
        display.fill_rectangle(229, 34, 122, 20, gray)
        display.fill_rectangle(229, 109, 122, 20, gray)

        display.draw_text(230, 35, f"{temp} F", font, white, gray)
        display.draw_text(230, 110, f"{round(batt)}%", font, white, gray)

        # BUTTON HANDLING
        if button_mode1.value() == 0:
            mode_one = True

        if button_mode2.value() == 0:
            mode_one = False

        # Only redraw mode UI when it CHANGES
        if mode_one != previous_mode:
            draw_modes(mode_one)
            previous_mode = mode_one

        # TEMP+BATT VISUAL MOVEMENT
        temp += temp_dir
        if temp >= 100:
            temp = 100
            temp_dir = -1
        if temp <= 50:
            temp = 50
            temp_dir = 1

        batt = max(0, batt - 0.05)

        sleep(0.05)

test_Text()