from machine import UART, Pin
import time

# using UART0, which is tx pins 0 and 1
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# testing counter
count = 0
while True:
    message = f"This was sent from the pico {count}\n"
    uart.write(message)
    print("Sent:", message.strip())  
    count += 1
    time.sleep(1)
        
    # check if we have UART input
    if uart.any():
        mes = uart.readline().decode('utf-8').strip()
        print("Received:", mes)
        
        # send reply
        uart.write("Pico Response")
        print("Responded")