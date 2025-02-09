#![no_std]
#![no_main]

use embedded_hal::i2c::{I2c, SevenBitAddress};
use fugit::{HertzU32, RateExtU32};
use panic_halt as _;

use embedded_hal::{delay::DelayNs, digital::OutputPin};
use rp235x_hal::gpio::{
  self, FunctionI2C, FunctionSio, PinId, PullType, PullUp, SioOutput,
};

use rp235x_hal::timer::TimerDevice;
use rp235x_hal::uart::{DataBits, StopBits, UartConfig};
use rp235x_hal::{self as hal, Clock, Sio, Timer};

#[link_section = ".start_block"]
#[used]
pub static IMAGE_DEF: hal::block::ImageDef = hal::block::ImageDef::secure_exe();

const XTAL_FREQ_HZ: u32 = 12_000_000u32;

fn blink_led<I: PinId, P: PullType, D: TimerDevice>(
  led: &mut gpio::Pin<I, FunctionSio<SioOutput>, P>,
  timer: &mut Timer<D>,
  delay: u32,
) {
  led.set_high().unwrap();
  timer.delay_ms(delay);
  led.set_low().unwrap();
  timer.delay_ms(delay);
}

#[hal::entry]
fn main() -> ! {
  let mut pac = hal::pac::Peripherals::take().unwrap();

  let mut watchdog = hal::Watchdog::new(pac.WATCHDOG);
  let clocks = hal::clocks::init_clocks_and_plls(
    XTAL_FREQ_HZ,
    pac.XOSC,
    pac.CLOCKS,
    pac.PLL_SYS,
    pac.PLL_USB,
    &mut pac.RESETS,
    &mut watchdog,
  )
  .unwrap();

  let sio = hal::Sio::new(pac.SIO);
  let pins = hal::gpio::Pins::new(
    pac.IO_BANK0,
    pac.PADS_BANK0,
    sio.gpio_bank0,
    &mut pac.RESETS,
  );

  let mut timer = Timer::new_timer0(pac.TIMER0, &mut pac.RESETS, &clocks);
  let mut led = pins.gpio25.into_push_pull_output();

  let uart0_pins = (pins.gpio2.into_function(), pins.gpio3.into_function());
  let mut uart0 =
    hal::uart::UartPeripheral::new(pac.UART0, uart0_pins, &mut pac.RESETS)
      .enable(
        UartConfig::new(115200.Hz(), DataBits::Eight, None, StopBits::One),
        clocks.peripheral_clock.freq(),
      )
      .unwrap();

  #[cfg(feature = "master")]
  {
    uart0.write_full_blocking(b"1234");
    loop {
      blink_led(&mut led, &mut timer, 100);
    }
  }

  #[cfg(feature = "slave")]
  {
    let mut buf = [0; 4];

    while !uart0.uart_is_readable() {
      blink_led(&mut led, &mut timer, 1000);
    }

    if uart0.read_full_blocking(&mut buf).is_err() {
      loop {
        blink_led(&mut led, &mut timer, 500);
      }
    }
    loop {
      blink_led(&mut led, &mut timer, 100);
    }
  }

  loop {
    hal::arch::wfi();
  }
}

#[link_section = ".bi_entries"]
#[used]
pub static PICOTOOL_ENTRIES: [hal::binary_info::EntryAddr; 2] = [
  hal::binary_info::rp_cargo_version!(),
  hal::binary_info::rp_program_description!(c"Pico-RS"),
];
