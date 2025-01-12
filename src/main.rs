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

const MASTER_ADDRESS: SevenBitAddress = 0x32;
const SLAVE_ADDRESS: SevenBitAddress = 0x33;

fn run_master(mut pac: hal::pac::Peripherals) {
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

  let mut timer = hal::Timer::new_timer0(pac.TIMER0, &mut pac.RESETS, &clocks);

  let sio = Sio::new(pac.SIO);
  let pins = hal::gpio::Pins::new(
    pac.IO_BANK0,
    pac.PADS_BANK0,
    sio.gpio_bank0,
    &mut pac.RESETS,
  );

  let sda_pin: gpio::Pin<_, FunctionI2C, PullUp> = pins.gpio18.reconfigure();
  let scl_pin: gpio::Pin<_, FunctionI2C, PullUp> = pins.gpio19.reconfigure();
  let mut led_pin = pins.gpio25.into_push_pull_output();
  let mut i2c = hal::I2C::new_controller(
    pac.I2C1,
    sda_pin,
    scl_pin,
    400.kHz(),
    &mut pac.RESETS,
    clocks.system_clock.freq(),
  );

  blink_led(&mut led_pin, &mut timer, 400);
  timer.delay_ms(5000);
  blink_led(&mut led_pin, &mut timer, 400);

  let mut buf: [u8; 4] = [0; 4];

  if i2c.write_read(SLAVE_ADDRESS, b"1234", &mut buf).is_err() {
    loop {
      blink_led(&mut led_pin, &mut timer, 500);
    }
  }

  loop {
    blink_led(&mut led_pin, &mut timer, 100);
  }
}

//#[cfg(feature = "slave")]
fn run_slave(mut pac: hal::pac::Peripherals) {
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

  let mut timer = hal::Timer::new_timer0(pac.TIMER0, &mut pac.RESETS, &clocks);

  let sio = Sio::new(pac.SIO);
  let pins = hal::gpio::Pins::new(
    pac.IO_BANK0,
    pac.PADS_BANK0,
    sio.gpio_bank0,
    &mut pac.RESETS,
  );

  let sda_pin: gpio::Pin<_, FunctionI2C, PullUp> = pins.gpio18.reconfigure();
  let scl_pin: gpio::Pin<_, FunctionI2C, PullUp> = pins.gpio19.reconfigure();
  let mut led_pin = pins.gpio25.into_push_pull_output();

  let mut i2c = hal::I2C::new_peripheral_event_iterator(
    pac.I2C1,
    sda_pin,
    scl_pin,
    &mut pac.RESETS,
    SLAVE_ADDRESS,
  );

  blink_led(&mut led_pin, &mut timer, 400);

  let mut buf: [u8; 4] = [0; 4];

  while i2c.rx_fifo_empty() {
    blink_led(&mut led_pin, &mut timer, 500);
  }

  let bytes_read = i2c.read(&mut buf);
  for _ in 0..=bytes_read + 1 {
    blink_led(&mut led_pin, &mut timer, 200);
  }

  loop {
    blink_led(&mut led_pin, &mut timer, 100);
  }
}

#[hal::entry]
fn main() -> ! {
  let pac = hal::pac::Peripherals::take().unwrap();

  #[cfg(feature = "master")]
  run_master(pac);
  #[cfg(feature = "slave")]
  run_slave(pac);

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
