from machine import Pin, PWM, Timer
import math
import time

PWM_PIN = 3
SD_PIN = 2
SAMPLE_RATE = 8000        # Lowered to 8kHz so MicroPython can keep up
TABLE_SIZE = 256
AUDIO_FREQ = 440
VOLUME = 1.0

# Setup Amplifier Shutdown Pin
SD = Pin(SD_PIN, Pin.OUT)
SD.high()

# Setup PWM (Carrier frequency needs to be high enough above audio frequency)
pwm = PWM(Pin(PWM_PIN))
pwm.freq(62500)

# Generate LUT (0 to 65535)
MAX_DUTY = 65535
sine_table = [
    int(((math.sin(2 * math.pi * i / TABLE_SIZE) + 1) / 2) * MAX_DUTY * VOLUME)
    for i in range(TABLE_SIZE)
]

# State variables for the interrupt (Using integers for speed)
# We multiply the phase by 256 to create "fixed point" math, avoiding slow floats
phase = 0
phase_inc = int((TABLE_SIZE * AUDIO_FREQ * 256) / SAMPLE_RATE)

def audio_tick(timer):
    global phase
    # Get the integer part of the phase, modulo the table size
    index = (phase >> 8) % TABLE_SIZE
    pwm.duty_u16(sine_table[index])
    phase += phase_inc

print("Playing Sine Wave... Press Ctrl+C to stop.")

# Create a hardware timer to execute exactly at the sample rate
timer = Timer(-1)
timer.init(freq=SAMPLE_RATE, mode=Timer.PERIODIC, callback=audio_tick)

try:
    # The main loop now does nothing! The timer interrupt handles the audio in the background.
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    timer.deinit()
    pwm.deinit()
    SD.low()
    print("\nPlayback stopped.")