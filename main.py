"""ILI9341 demo (bouncing boxes)."""
from machine import Pin, SPI, UART
import time
import select
from time import sleep
from ili9341 import Display, color565
from xglcd_font import XglcdFont

# import audiopwmio
# import audiocore

# from PIL import Image

import network
import socket
import time


# --- Configuration ---
SSID = 'ralph'              # pi 4 hotspot name
PASSWORD = 'something'      # pi 4 hotspot password
SERVER_IP = '10.42.0.1'     # default IP
SERVER_PORT = 19840

# SSID = "Grant's Galaxy S21 Ultra 5G"              # pi 4 hotspot name
# PASSWORD = 'ylga096/'      # pi 4 hotspot password
# SERVER_IP = '10.42.0.1'     # default IP
# SERVER_PORT = 19840

def connect_to_hotspot(display, font):
    wlan = network.WLAN(network.STA_IF)
    # wlan.active(False)
    # time.sleep(0.5) 
    wlan.active(True)
    
    wlan.connect(SSID, PASSWORD)

    print(f"Connecting to Pi 4 Hotspot: '{SSID}'...")
    max_wait = 10000
    while max_wait > 0:
        status_code = wlan.status() # Get the exact status code
        print(f"{status_code}")
        display.draw_text(0, 120, f"Status: {status_code}", font, color565(0, 53, 97))
        
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for Wi-Fi connection...')
        display.draw_text(0, 0, "Waiting for WiFi", font, color565(0, 53, 97))
        time.sleep(1)

    if wlan.status() != 3:
        display.draw_text(0, 20, "Hotspot connection failed!", font, color565(0, 53, 97))
        display.draw_text(0, 40, "Check SSID/Password.", font, color565(0, 53, 97))
        raise RuntimeError('Hotspot connection failed! Check SSID/Password.')
    else:
        display.draw_text(0, 20, "Connected to Pi 4 Hotspot!", font, color565(0, 53, 97))
        print('Connected to Pi 4 Hotspot!')
        status = wlan.ifconfig()
        display.draw_text(0, 40, f"Pico IP assigned by Pi 4: {status[0]}", font, color565(0, 53, 97))
        print(f'Pico IP assigned by Pi 4: {status[0]}')
    
    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.getaddrinfo(SERVER_IP, SERVER_PORT)[0][-1]))
    # s.setblocking(False) 
    print("Successfully connected to the Pi 4 Server!")
    return s

def main():
    print("this is running")
    # time.sleep(1);
    
    # INITALIZATION -----------------------------------------------------------
    # initialize UART
    # using UART0, which is tx pins 0 and 1
    uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

    # initialize SPI
    spi = SPI(0,
        baudrate=400000000,
        polarity=1,
        phase=1,
        bits=8,
        firstbit=SPI.MSB,
        sck=Pin(18),
        mosi=Pin(19),
        miso=Pin(16))

    # initializing display
    display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(14), width = 320, height = 240, rotation=270)
    time.sleep(1)
    font = XglcdFont('EspressoDolce18x24.c', 18, 24)

    # connect to the ralph Pi4
    s = connect_to_hotspot(display, font)
    
    # start a poller for the connection
    poller = select.poll()
    poller.register(s, select.POLLIN)

    # -------------------------------
    # INITIAL VALUES
    # -------------------------------
    temp = 90
    batt = 67
    temp_dir = 1
    mode = 1

    white = color565(255, 255, 255)
    gray = color565(150, 150, 150)
    blue = color565(3, 140, 252)
    dark_blue = color565(0, 53, 97)
    green = color565(60, 140, 40)
    yellow = color565(255, 230, 0)
    red = color565(255, 0, 0)
    black = color565(0, 0, 0)

    # -------------------------------
    # BUTTONS
    # -------------------------------
    buttons = [1,
             Pin(20, Pin.IN, Pin.PULL_UP),  # K1
             Pin(21, Pin.IN, Pin.PULL_UP),  # K2
             Pin(7, Pin.IN, Pin.PULL_UP),  # K2
             Pin(6, Pin.IN, Pin.PULL_UP),   # K2
             Pin(22, Pin.IN, Pin.PULL_UP)   # K2
             ]
    
    
    # -------------------------------
    # HEIGHT INITIALIZATION SCREEN
    # -------------------------------
    display.clear(color565(0, 0, 0))
    display.draw_image('teddy54x70.raw', 260, 8, 54, 70)
    
    print("Height Initialization")
    
    class Button:
        def __init__(self, x, y, label, index, txtOffset=0):
            self.x = x
            self.y = y
            self.txtOffset = txtOffset
            self.label = label
            self.idx = index

            # SHRUNK DIMENSIONS:
            self.cr = 20                   # Radius shrunk from 30 to 20
            self.clx = x + self.cr         
            self.cly = y + self.cr         
            
            self.rw = 60                   # Middle rect width shrunk from 77 to 60
            self.crx = self.clx + self.rw  
            self.cry = self.cly            
            
            self.rx = self.clx             
            self.ry = y                    
            self.rh = self.cr * 2          # Height is now 40 instead of 60
            
            self.ox = x
            self.oy = y
            self.ow = self.cr * 2 + self.rw
            self.oh = self.rh
            
    y_offset = 10            
    HeightButtons = [
        Button(15, 90 + y_offset, "-", 1, 44),
        Button(168, 90 + y_offset, "+", 2, 44),
        # Button(15, 165 + y_offset, "Mode 3", 3, 32),
        Button(168, 165 + y_offset, "Enter", 4, 24)
    ]
    feet = 5
    inch = 9
    for b in HeightButtons:
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
        display.draw_text(b.ox + b.txtOffset, b.oy + 11, b.label, font, white, bg)
    display.draw_text(10, 15, f"{feet}ft, {inch}inch", font, white)
    # while (not buttons[4]): 
    buttonVal = 0
    while buttonVal != 4:
        for i in range(len(buttons)):
            if i == 0:
                continue
            if buttons[i].value() == 0:
                buttonVal = i
                print(f"{i}")
                sleep(0.15)
        if (buttonVal == 2):
            print("0")
            inch = inch + 1
            if inch == 12:
                inch = 0
                feet = feet + 1
            display.fill_rectangle(10, 15, 150, 50, black)
            display.draw_text(10, 15, f"{feet}ft, {inch}inch", font, white)
            # sleep(0.15)
            buttonVal = -1
        elif (buttonVal == 1):
            print("1")
            inch = inch - 1
            if inch == -1:
                inch = 11
                feet = feet - 1
            if feet == -1:
                feet = 0
                inch = 0
            display.fill_rectangle(10, 15, 150, 50, black)
            display.draw_text(10, 15, f"{feet}ft, {inch}inch", font, white)
            # sleep(0.15)
            buttonVal = -1
            
    heightMSG = f"Height:{12 * feet + inch}\n"
    print(f"Sending: {heightMSG.strip()}")
    s.send(heightMSG.encode('utf-8'))
        
    # -------------------------------
    # STATIC UI
    # -------------------------------
    display.clear(color565(0, 0, 0))
    display.draw_image('teddy54x70.raw', 260, 8, 54, 70)

    # -------------------------------
    # MODE DRAW FUNCTION
    # -------------------------------
    def draw_modes(active, previous_mode, init):
        # Tighter packing for the smaller 100px wide buttons
        ModeButtons = [
            Button(5, 130, "Mode 1", 1, 10),
            Button(115, 130, "Mode 2", 2, 10),
            Button(5, 180, "Mode 3", 3, 10),
            Button(115, 180, "Mode 4", 4, 10)
        ]

        for b in ModeButtons:
            if b.idx == active:
                display.fill_circle(b.clx, b.cly, b.cr, green)
                display.draw_circle(b.clx, b.cly, b.cr, yellow)
                display.fill_circle(b.crx, b.cry, b.cr, green)
                display.draw_circle(b.crx, b.cry, b.cr, yellow)
                display.fill_rectangle(b.rx, b.ry, b.rw, b.rh, green)
                
                y2 = b.ry + b.rh - 1
                display.draw_hline(b.rx, b.ry, b.rw, yellow)
                display.draw_hline(b.rx, y2, b.rw, yellow)
                bg = green
                # Changed Y offset to +8 for vertical centering
                display.draw_text(b.ox + b.txtOffset, b.oy + 8, b.label, font, white, bg) 
            elif b.idx == previous_mode or init:
                display.fill_circle(b.clx, b.cly, b.cr, blue)
                display.fill_circle(b.crx, b.cry, b.cr, blue)
                display.fill_rectangle(b.rx, b.ry, b.rw, b.rh, blue)
                bg = blue
                # Changed Y offset to +8 for vertical centering
                display.draw_text(b.ox + b.txtOffset, b.oy + 8, b.label, font, white, bg)

        # KILLSWITCH
        if init:
            # Shrunk and moved slightly right to make room for top-left stats
            kB = Button(110, 80, "Kill", 0, 20) 
            display.fill_circle(kB.clx, kB.cly, kB.cr, red)
            display.fill_circle(kB.crx, kB.cry, kB.cr, red)
            display.fill_rectangle(kB.rx, kB.ry, kB.rw, kB.rh, red)
            display.draw_text(kB.ox + kB.txtOffset, kB.oy + 8, "Kill", font, white, red)
            
    # Draw initial mode
    previous_mode = -1
    draw_modes(mode, previous_mode, 1)
    
    def parse_incoming_data(s, poller, batt, m1, m2, m3, m4):
        # check if there is data waiting to be read. 
        # timeout=0 means it returns instantly, never blocking.
        events = poller.poll(0)
    
        # if there were events in the poller, it means we received data from the exo
        if events:
            try:
                # receive the data
                data = s.recv(1024)
                if data:
                    messages = data.decode('utf-8').strip().split('\n')
                    # decode the data
                    for msg in messages:
                        parts = msg.strip().split()
                        if len(parts) >= 2:
                            key = parts[0].upper()
                            try:
                                value = float(parts[1])
                                
                                if key == "BATT":
                                    batt = value
                                elif key == "M1":
                                    m1 = value
                                elif key == "M2":
                                    m2 = value
                                elif key == "M3":
                                    m3 = value
                                elif key == "M4":
                                    m4 = value
                            except ValueError:
                                print(f"Could not parse number from: {msg}")
            except Exception as e:
                print(f"Socket Error during read: {e}")
                
        return batt, m1, m2, m3, m4
    
    motor1_temp = 0
    motor2_temp = 0
    motor3_temp = 0
    motor4_temp = 0
    last_ping_time = time.time()

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    while True:
        # parse the data coming from the exo
        batt, motor1_temp, motor2_temp, motor3_temp, motor4_temp = parse_incoming_data(
            s, poller, batt, motor1_temp, motor2_temp, motor3_temp, motor4_temp
        )
        
        # current_time = time.time()
        # if current_time - last_ping_time > 2.0:
        #     try:
        #         # Send the tiny heartbeat packet
        #         s.send(b"PING\n")
        #     except OSError:
        #         pass # If the socket is dead, ignore it so the script doesn't crash
        #     last_ping_time = current_time
        
        # Battery is displayed in the top left
        # motor temperatures are displayed in the bottom right
        display.draw_text(10, 10, f"Bat: {round(batt, 1)}% ", font, white, black)
        display.draw_text(220, 90, f"M1: {round(motor1_temp, 1)}C ", font, white, black)
        display.draw_text(220, 120, f"M2: {round(motor2_temp, 1)}C ", font, white, black)
        display.draw_text(220, 150, f"M3: {round(motor3_temp, 1)}C ", font, white, black)
        display.draw_text(220, 180, f"M4: {round(motor4_temp, 1)}C ", font, white, black)
        
        # BUTTON HANDLING
        for i in range(len(buttons)):
            if i == 0:
                continue
            if buttons[i].value() == 0:
                mode = i
                sleep(0.15)

        # Only redraw mode UI when it CHANGES
        # Transmit mode to the exo on mode change
        if mode != previous_mode:
            draw_modes(mode, previous_mode, 0)
            previous_mode = mode
            
            modeMSG = f"Mode {mode}\n"
            print(f"Sending message {modeMSG.strip()}")
            s.send(modeMSG.encode('utf-8'))
            
            print(f"Switched to Mode {mode}")

        sleep(0.05)

main()
