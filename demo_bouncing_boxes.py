"""ILI9341 demo (bouncing boxes)."""
from machine import Pin, SPI
from random import random, seed
from ili9341 import Display, color565
from utime import sleep_us, ticks_cpu, ticks_us, ticks_diff
from time import sleep  
from xglcd_font import XglcdFont

        
from ili9341 import Display, color565
from machine import Pin, SPI

##test to set background color to white (works)
def test_color():
    spi = SPI(0,
                  baudrate=10000000,
                   polarity=1,
                   phase=1,
                   bits=8,
                   firstbit=SPI.MSB,
                  sck=Pin(18),
                  mosi=Pin(19),
                   miso=Pin(16))
    display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))

    # Fill the entire screen with blue (RGB565 format)
    display.clear(color565(255, 255, 255))

    print("Display background set to blue")
test_color()

#test for text 

def test_Text():
    spi = SPI(0,
                  baudrate=10000000,
                   polarity=1,
                   phase=1,
                   bits=8,
                   firstbit=SPI.MSB,
                  sck=Pin(18),
                  mosi=Pin(19),
                   miso=Pin(16))
    display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
    
    # Fill the entire screen with blue
    display.draw_rectangle(0, 0, display.width, display.height, color565(255, 255, 255))

    
    # arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
    # display.draw_text(50, 50, "Arcade Pix 9x11", color565(0, 0, 0))
    display.draw_text(50, 50, "STARX The GOAT",  XglcdFont('ArcadePix9x11.c', 9, 11), color565(255, 255, 255))
    print("Display background set to white with black font")
test_Text()



    
#code for shapes 
# def test():
#     """Test code."""
#     spi = SPI(0,
#                   baudrate=10000000,s
#                    polarity=1,
#                    phase=1,
#                    bits=8,
#                    firstbit=SPI.MSB,
#                   sck=Pin(18),
#                   mosi=Pin(19),
#                    miso=Pin(16))
#     display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
#     display.clear()

#     display.draw_hline(10, 319, 229, color565(255, 0, 255))
#     sleep(1)

#     display.draw_vline(10, 0, 319, color565(0, 255, 255))
#     sleep(1)

#     display.fill_hrect(23, 50, 30, 75, color565(255, 255, 255))
#     sleep(1)

#     display.draw_hline(0, 0, 222, color565(255, 0, 0))
#     sleep(1)

#     display.draw_line(127, 0, 64, 127, color565(255, 255, 0))
#     sleep(2)

#     display.clear()

#     coords = [[0, 63], [78, 80], [122, 92], [50, 50], [78, 15], [0, 63]]
#     display.draw_lines(coords, color565(0, 255, 255))
#     sleep(1)

#     display.clear()
#     display.fill_polygon(7, 120, 120, 100, color565(0, 255, 0))
#     sleep(1)

#     display.fill_rectangle(0, 0, 15, 227, color565(255, 0, 0))
#     sleep(1)

#     display.clear()

#     display.fill_rectangle(0, 0, 163, 163, color565(128, 128, 255))
#     sleep(1)

#     display.draw_rectangle(0, 64, 163, 163, color565(255, 0, 255))
#     sleep(1)

#     display.fill_rectangle(64, 0, 163, 163, color565(128, 0, 255))
#     sleep(1)

#     display.draw_polygon(3, 120, 286, 30, color565(0, 64, 255), rotate=15)
#     sleep(3)

#     display.clear()

#     display.fill_circle(132, 132, 70, color565(0, 255, 0))
#     sleep(1)

#     display.draw_circle(132, 96, 70, color565(0, 0, 255))
#     sleep(1)

#     display.fill_ellipse(96, 96, 30, 16, color565(255, 0, 0))
#     sleep(1)

#     display.draw_ellipse(96, 256, 16, 30, color565(255, 255, 0))

#     sleep(5)
#     display.cleanup()


# # test()

# # # def test():
# # #     """Bouncing box."""
# # #     try:
# # #         # Baud rate of 40000000 seems about the max
# #             spi = SPI(0,
# #                   baudrate=10000000,
# #                   polarity=1,
# #                   phase=1,
# #                   bits=8,
# #                   firstbit=SPI.MSB,
# #                   sck=Pin(18),
# #                   mosi=Pin(19),
# #                   miso=Pin(16))
# #         display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14))
# #         display.clear()

# #         colors = [color565(255, 0, 0),
# #                   color565(0, 255, 0),
# #                   color565(0, 0, 255),
# #                   color565(255, 255, 0),
# #                   color565(0, 255, 255),
# #                   color565(255, 0, 255)]
# #         sizes = [12, 11, 10, 9, 8, 7]
# #         boxes = [Box(239, 319, sizes[i], display,
# #                  colors[i]) for i in range(6)]

# #         while True:
# #             print("displaying...")
# #             timer = ticks_us()
# #             for b in boxes:
# #                 b.update_pos()
# #                 b.draw()
# #             # Attempt to set framerate to 30 FPS
# #             timer_dif = 33333 - ticks_diff(ticks_us(), timer)
# #             if timer_dif > 0:
# #                 sleep_us(timer_dif)

# #     except KeyboardInterrupt:
# #         display.cleanup()


# # test()

#beggining of a code 
# class Box(object):
#     """Bouncing box."""

#     def __init__(self, screen_width, screen_height, size, display, color):
#         """Initialize box.

#         Args:
#             screen_width (int): Width of screen.
#             screen_height (int): Width of height.
#             size (int): Square side length.
#             display (ILI9341): display object.
#             color (int): RGB565 color value.
#         """
#         self.size = size
#         self.w = screen_width
#         self.h = screen_height
#         self.display = display
#         self.color = color
#         # Generate non-zero random speeds between -5.0 and 5.0
#         seed(ticks_cpu())
#         r = random() * 10.0
#         self.x_speed = 5.0 - r if r < 5.0 else r - 10.0
#         r = random() * 10.0
#         self.y_speed = 5.0 - r if r < 5.0 else r - 10.0

#         self.x = self.w / 2.0
#         self.y = self.h / 2.0
#         self.prev_x = self.x
#         self.prev_y = self.y

#     def update_pos(self):
#         """Update box position and speed."""
#         x = self.x
#         y = self.y
#         size = self.size
#         w = self.w
#         h = self.h
#         x_speed = abs(self.x_speed)
#         y_speed = abs(self.y_speed)
#         self.prev_x = x
#         self.prev_y = y

#         if x + size >= w - x_speed:
#             self.x_speed = -x_speed
#         elif x - size <= x_speed + 1:
#             self.x_speed = x_speed

#         if y + size >= h - y_speed:
#             self.y_speed = -y_speed
#         elif y - size <= y_speed + 1:
#             self.y_speed = y_speed

#         self.x = x + self.x_speed
#         self.y = y + self.y_speed

#     def draw(self):
#         """Draw box."""
#         x = int(self.x)
#         y = int(self.y)
#         size = self.size
#         prev_x = int(self.prev_x)
#         prev_y = int(self.prev_y)
#         self.display.fill_hrect(prev_x - size,
#                                 prev_y - size,
#                                 size, size, 0)
                        
#         self.display.fill_hrect(x - size,
#                                 y - size,
#                                 size, size, self.color)
