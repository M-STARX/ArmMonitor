#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/i2c.h"
#include "pico/i2c_slave.h"

#ifndef LED_DELAY_MS
#define LED_DELAY_MS 250
#endif

void pico_led_init() {
  gpio_init(PICO_DEFAULT_LED_PIN);
  gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
}

void pico_set_led(bool led_on) {
  gpio_put(PICO_DEFAULT_LED_PIN, led_on);
}

void blink_led(uint32_t delay) {
  pico_set_led(true);
  sleep_ms(delay);
  pico_set_led(false);
  sleep_ms(delay);
}

void blink_led_n(uint32_t delay, uint8_t n) {
  for (uint8_t i = 0; i < n; i++) {
    blink_led(delay);
  }
}

void blink_control() {
  while (1) {
    while (!multicore_fifo_rvalid()); // spinlock until requested
    multicore_fifo_pop_blocking();
    blink_led(LED_DELAY_MS);
  }
}


void incoming_handler(i2c_inst_t * i2c, i2c_slave_event_t event) {
  multicore_fifo_push_blocking(1);
  switch (event) {
    case I2C_SLAVE_REQUEST:
      i2c_write_byte_raw(i2c, 8);
    default:
      multicore_fifo_push_blocking(1);
  }
}

#define TARGET_PIN 20

static void setup_slave() {
  gpio_init(4); // slave SDA
  gpio_set_function(4, GPIO_FUNC_I2C);
  gpio_pull_up(4);

  gpio_init(5); // slave SDA
  gpio_set_function(5, GPIO_FUNC_I2C);
  gpio_pull_up(5);

  i2c_init(i2c0, 100*1000);
}

int main () {
  pico_led_init();
  blink_led_n(LED_DELAY_MS, 3);

  multicore_launch_core1(blink_control);

  i2c_inst_t* i2c_inst = i2c_get_instance(0);
  i2c_init(i2c_inst, 100 * 1000);

  i2c_slave_init(i2c_inst, 0x20, incoming_handler);

  while (1); // spinlock
}
