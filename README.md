# For logging into the pi
Username: starx
Password: STARX

# After logging in
Set the settings of the serial port:
`sudo stty -F /dev/ttyS0 -echo -onlcr 115200`
Input password when prompted; the password won't show you typing it.

Disables echo, newline to CR, and sets baudrate to 115200 Hz.

To read from the serial:
`cat /dev/ttyS0`

To read from the serial to a file:
`cat /dev/ttyS0 > path/to/file`

# On the pico
Run the contents of the file `test.py`.
Critically,

```py
from machine import UART, Pin

uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
# write to uart
uart1.write('some content')
# flush, just in case
uart1.flush()

# read from uart some number of bytes (the argument)
uart1.read(5)
```
