from machine import UART, Pin
import time

# Initialize UART0 on the Pico (TX=GP0)
uart0 = UART(0, baudrate=115200, tx=Pin(0))

message = "Hello from Raspberry Pi Pico: "

count = 0
while True:
    count += 1
    uart0.write(message + str(count) + "\n")  # Properly formatted message
    time.sleep(0.5)  # Send message every half second
