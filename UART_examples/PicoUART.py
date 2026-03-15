from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

count = 0
while True:
    message = f"This was sent from the pico {count}\n"
    uart.write(message)
    print("Sent:", message.strip())  
    count += 1
    time.sleep(1)
    #while uart.in_waiting < 0:
        
    if uart.any():
        mes = uart.readline().decode('utf-8').strip()
        print("Received:", mes)
        
        # send reply
        uart.write("Pico Response")
        print("Responded")