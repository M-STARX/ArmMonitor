# Reasoning
## What is UART?
UART stands for **U**niversal **A**synchronous **R**eceiver/**T**ransmitter;
it's a serial protocol for communication between two devices.
Since it only has to support two, it's a lot simpler than alternatives like SPI or I2C.
For now, we only need to support communication between the exo's pi and the arm monitor pico,
and so we don't need the added complexity of SPI and I2C.
Quite simply, UART uses two pins on each device:
- The `tx` pin, which **t**ransmits data,
- and the `rx` pin, which **r**eceives data.
One device's `tx` should be connected to the other device's `rx`, and vice versa.
In addition, the two devices' grounds should be connected.
UART can transmit numbers over the interface via a bit of magic that we don't need to worry about.
If you want to know how it works under the hood, check out
[this resource](https://www.analog.com/en/resources/analog-dialogue/articles/uart-a-hardware-communication-protocol.html).
Essentially, you can write arbitrary data to the interface and read some number of bytes from the interface on both ends,
but you have to provide the method of encoding/decoding the data you send.

## Programming for UART on the Pico
MicroPython provides a convenient wrapper for these functions in the form of the `UART` class
(documentation [here](https://docs.micropython.org/en/latest/library/machine.UART.html)).
The `read*` and `write` methods aren't particularly unique to `UART`.
Familiarise yourself with the concept of a stream, and you should be good.
The mysterious method is `init`. For our purposes, most of the default parameters will work just fine.
The ones we have to pay attention to are `baudrate`, `tx`, and `rx`.
`tx` and `rx` are easy; they should be set to [`Pin`](https://docs.micropython.org/en/latest/library/machine.Pin.html)s which
represent the `tx` and `rx` pins used on the pico. They can't just be any pins, they have to be pins which support the feature;
you can check [this datasheet](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf) for what each pin's capabilities are.
Only the pins marked `UART1` can be used (`UART0` is used by MicroPython to run a repl over USB).
You can choose one of the two pairs:
- `tx=Pin(4)` and `rx=Pin(5)`
- `tx=Pin(8)` and `rx=Pin(9)`
Due to hardware limitations, you can't mix and match (i.e. `tx=Pin(8)` and `rx=Pin(5)` does **NOT** work).

`baudrate` is a bit unclear; it's a number that represents what "frequency" the UART is transmitting with;
the standard baudrates are as follows:
- 4800
- 9600
- 19200
- 38400
- 57600
- 115200
- 230400
- 460800
- 921600
In general, you should pick either `9600` or `115200`: `9600` is the default for MicroPython, and `115200` is the default on the raspberry pi.
Both sides have to agree on the baudrate for it to work properly
(sort of like how walkie talkies have to match frequencies to be able to communicate with each other),
so you'll need to set at least one explicitly (although I ***strongly*** recommend explicitly setting both — don't leave anything up to chance!).

So, to initialise a `UART` device in MicroPython:
```py
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
```
The `1` tells it which UART hardware to use; since `UART0` is taken already, we have to use `UART1`.

## Testing on the Pi
To make sure the pico is actually sending data appropriately, we can read what it sends on a raspberry pi,
simulating the environment it'll be in on the exo.
A raspberry pi also has support for two UARTs. The most accessible one is on pins 14 (`tx`) and 15 (`rx`).
Remember, connect `tx` to `rx` and `rx` to `tx`.
To enable the raspberry pi to listen for serial, you can use `raspi-config`:
In the `Interface` settings, turn on `Serial`, but decline to turn on the login shell over serial.
The serial will be created as a character device at `/dev/ttyS0`
(for more information on what that means, check out
[this article](https://docs.oracle.com/en/operating-systems/oracle-linux/6/admin/ol_about_devices.html)).
This means it can be read from with the [`cat`](https://www.ibm.com/docs/kk/aix/7.1?topic=c-cat-command) command, as in `cat /dev/ttyS0`.
Do note that `cat` will NOT print to the screen until a `\n` is sent.
Before you can do try this though, you'll have to disable echo mode and set the baudrate.
By default, the pi will echo any data it receives on `tx` back onto `rx`.
You can disable this and set the baudrate all in one go with this command:
```bash
sudo stty -F /dev/ttyS0 -echo -onlcr 115200`
```
`stty`'s arguments are a bit confusing if you're used to other linux commands;
the `-` does not indicate that they are flags but rather that they should be disabled.
- `-echo` disables the echoing
- `115200` is the baudrate (make sure it matches the pico — you might have used `9600`)
- `-onlcr` disables translation of `\n` to `\r\n` (fun little added bonus so things don't get weird)

Now you should be able to read from it using `cat`, and write to it using `echo`:
```bash
cat /dev/ttyS0 # read, terminate with C-c
echo -n "some message" > /dev/ttyS0 # `-n` indicates to not add a `\n` to the message, `>` redirects the output into the device
```
If you want a little more knowledge on piping and redirection on the command line, check out
[this blog post](https://ryanstutorials.net/linuxtutorial/piping.php).

Once we work more with the pi, we'll have more information on how to access and read/write from UART using python code.

# Instructions for use
If you just can't remember the correct series of commands to run, here's some brief instructions.

## For logging into the pi
Username: starx
Password: STARX

## After logging in
Set the settings of the serial port:
`sudo stty -F /dev/ttyS0 -echo -onlcr 115200`
Input password when prompted; the password won't show you typing it.

Disables echo, disables `\n` to `\r\n`, and sets baudrate to 115200 Hz.

To read from the serial:
`cat /dev/ttyS0`

To read from the serial to a file:
`cat /dev/ttyS0 > path/to/file`

## On the pico
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
