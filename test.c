#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/uart.h"
#include "hardware/irq.h"

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

#define UART_ID uart0

void on_uart_rx() {
  while (uart_is_readable(UART_ID)) {
    uint8_t ch = uart_getc(UART_ID);
    if (uart_is_writable(UART_ID)) {
      ch++;
      uart_putc(UART_ID, ch);
    }
  }
}

int main () {
  pico_led_init();
  blink_led_n(LED_DELAY_MS, 3);

  uart_init(UART_ID, 9600);

  gpio_set_function(0, UART_FUNCSEL_NUM(UART_ID, 0));
  gpio_set_function(1, UART_FUNCSEL_NUM(UART_ID, 1));

  uart_set_hw_flow(UART_ID, false, false);
  uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);  

  uart_set_fifo_enabled(UART_ID, false);

  blink_led_n(150, 3);

  irq_set_exclusive_handler(UART0_IRQ, on_uart_rx);
  irq_set_enabled(UART0_IRQ, true);

  uart_set_irq_enables(UART_ID, true, false);

  uart_puts(UART_ID, "hey\n");

  blink_led(1000);
  while (1) {
    tight_loop_contents();
  }
}
