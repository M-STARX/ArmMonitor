import serial
import time

# fill in x with the correct port number
# the pi3hat uses UART5, which is pins 33 and 34
ser = serial.Serial('/dev/ttyAMAx', baudrate=9600, timeout=1)

print("UART Test ready")

while True:
    # if there is anything received
    if ser.in_waiting > 0:
        message = ser.readline().decode('utf-8').strip()
        if message:
            print("Received:", message)
            
    ser.write("This is from the Pi")
    time.sleep(0.1)
