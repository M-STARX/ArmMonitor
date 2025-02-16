from machine import UART, Pin
import time

dbg_led = Pin(25, Pin.OUT)
dbg_led.value(0)

def blink(delay):
  dbg_led.value(1)
  time.sleep(delay)
  dbg_led.value(0)
  time.sleep(delay)

def blink_n(delay, n):
  for _ in range(0, n):
    blink(delay)

blink(0.5)
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
blink_n(0.1, 3)
