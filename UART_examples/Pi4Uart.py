import serial
import time

# fill in x with the correct port number
# the pi3hat uses UART5, which is pins 33 and 34
# this appears as ttyAMA5 device
ser = serial.Serial('/dev/ttyAMA5', baudrate=9600, timeout=1)

print("UART Test ready")

# infinite loop
while True:
    # if there is anything received
    if ser.in_waiting > 0:
        # there appears to be some poor wiring issues that have an effect here
        # the issue arises from the decoding part
        # you can opt to print without the utf-8, but you may
        # receive garbage form time to time
        message = ser.readline().decode('utf-8').strip()
        if message:
            print("Received:", message)
            
    # due to poor timing constraints
    # running two-way will not always work
    # comment the chunk below to receive data from the pico --------
    ser.write("This is from the Pi")
    print("Wrote data")
    time.sleep(0.1)
