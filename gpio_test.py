#!/usr/bin/env python
"""
Test of OctoPrintPi GPIO devices.

Dependencies
------------

pip install rpi_ws281x adafruit-circuitpython-neopixel

"""

import sys
import argparse
import logging
from typing import List, Tuple, Callable
import time

import board
from neopixel import NeoPixel, GRBW
from microcontroller import Pin
from digitalio import DigitalInOut, Direction, Pull
from pwmio import PWMOut

logging.basicConfig(
    level=logging.WARNING,
    format="[%(asctime)s %(levelname)s] %(message)s"
)
logger: logging.Logger = logging.getLogger()

NEOPIXEL_PIN: Pin = board.D18
NEOPIXEL_COUNT: int = 24
NEOPIXEL_ORDER: str = GRBW
GREEN_LED_PIN: Pin = board.D12  # set high for on
GREEN_BUTTON_PIN: Pin = board.D5  # button to ground
RED_LED_PIN: Pin = board.D13  # set high for on
RED_BUTTON_PIN: Pin = board.D6  # button to ground


class GpioTester:

    def __init__(self):
        logger.debug(
            'Instantiating Neopixels on pin %s; num_pixels=%d, order=%s',
            NEOPIXEL_PIN, NEOPIXEL_COUNT, NEOPIXEL_ORDER
        )
        self.pixels: NeoPixel = NeoPixel(
            NEOPIXEL_PIN, NEOPIXEL_COUNT, pixel_order=NEOPIXEL_ORDER
        )
        logger.debug(
            'Instantiating green button on pin %s as input, with pull up',
            GREEN_BUTTON_PIN
        )
        self.green_button: DigitalInOut = DigitalInOut(GREEN_BUTTON_PIN)
        self.green_button.direction = Direction.INPUT
        self.green_button.pull = Pull.UP
        logger.debug(
            'Instantiating red button on pin %s as input, with pull up',
            RED_BUTTON_PIN
        )
        self.red_button: DigitalInOut = DigitalInOut(RED_BUTTON_PIN)
        self.red_button.direction = Direction.INPUT
        self.red_button.pull = Pull.UP
        logger.debug(
            'Instantiating green LED as PWMOut on pin %s', GREEN_LED_PIN
        )
        self.green_led: PWMOut = PWMOut(
            GREEN_LED_PIN, frequency=100, duty_cycle=0
        )
        logger.debug(
            'Instantiating red LED as PWMOut on pin %s', RED_LED_PIN
        )
        self.red_led: PWMOut = PWMOut(
            RED_LED_PIN, frequency=5000, duty_cycle=0
        )

    def _neopixel_on_full(self):
        logger.debug('neopixel on full')
        self.pixels.fill((0, 0, 0, 255))

    def _neopixel_on_half(self):
        logger.debug('neopixel on half')
        self.pixels.fill((0, 0, 0, 127))

    def _neopixel_on_low(self):
        logger.debug('neopixel on low')
        self.pixels.fill((0, 0, 0, 80))

    def _neopixel_off(self):
        logger.debug('neopixel off')
        self.pixels.fill((0, 0, 0, 0))

    def _read_green(self):
        logger.debug('waiting for GREEN button press')
        while self.green_button.value is True:
            time.sleep(0.05)
        print('Green button was pressed')

    def _read_red(self):
        logger.debug('waiting for RED button press')
        while self.red_button.value is True:
            time.sleep(0.05)
        print('Red button was pressed')

    def _green_led_on(self):
        # note that gpiozero natively supports pulsing LEDs
        logger.debug('GREEN led ON')
        # duty cycle is 0 to 65535
        self.green_led.duty_cycle = 65535

    def _green_led_off(self):
        logger.debug('GREEN led OFF')
        self.green_led.duty_cycle = 0

    def _breathe_until_button(self, led: PWMOut, button: DigitalInOut):
        num_steps = 20
        dwell = 0.5
        while button.value is True:
            for dc in range(0, 65535, int(65535 / num_steps)):
                led.duty_cycle = dc
                time.sleep(0.05)
            time.sleep(dwell)
            for dc in range(65535, 0, -1 * int(65535 / num_steps)):
                led.duty_cycle = dc
                time.sleep(0.05)
            time.sleep(dwell)

    def _green_breathe_until_button(self):
        self._breathe_until_button(self.green_led, self.green_button)

    def _red_breathe_until_button(self):
        self._breathe_until_button(self.red_led, self.red_button)

    def _red_led_on(self):
        logger.debug('RED led ON')
        # duty cycle is 0 to 65535
        self.red_led.duty_cycle = 65535

    def _red_led_off(self):
        logger.debug('RED led OFF')
        self.red_led.duty_cycle = 0

    def run(self):
        options: List[Tuple[str, Callable]] = [
            ('Neopixel ON full', self._neopixel_on_full),
            ('Neopixel ON half', self._neopixel_on_half),
            ('Neopixel ON low', self._neopixel_on_low),
            ('Neopixel OFF', self._neopixel_off),
            ('Read GREEN Button', self._read_green),
            ('Read RED Button', self._read_red),
            ('GREEN led ON', self._green_led_on),
            ('GREEN led OFF', self._green_led_off),
            ('RED led ON', self._red_led_on),
            ('RED led OFF', self._red_led_off),
            ('GREEN breathe until button', self._green_breathe_until_button),
            ('RED breathe until button', self._red_breathe_until_button),
        ]
        item: Tuple[str, Callable]
        choice: Callable
        while True:
            print('#' * 80)
            for idx, item in enumerate(options):
                print(f'{idx}) {item[0]}')
            print('exit) exit program')
            try:
                res = input('Enter your choice: ')
                if res.strip() == 'exit':
                    break
                choice = options[int(res)][1]
            except Exception as ex:
                sys.stderr.write(f'ERROR: {ex}\n')
                continue
            choice()


def parse_args(argv):
    p = argparse.ArgumentParser(description='OctoPrintPi GPIO Tester')
    p.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                   default=False, help='verbose output')
    args = p.parse_args(argv)
    return args


def set_log_info(l: logging.Logger):
    """set logger level to INFO"""
    set_log_level_format(
        l,
        logging.INFO,
        '%(asctime)s %(levelname)s:%(name)s:%(message)s'
    )


def set_log_debug(l: logging.Logger):
    """set logger level to DEBUG, and debug-level output format"""
    set_log_level_format(
        l,
        logging.DEBUG,
        "%(asctime)s [%(levelname)s %(filename)s:%(lineno)s - "
        "%(name)s.%(funcName)s() ] %(message)s"
    )


def set_log_level_format(lgr: logging.Logger, level: int, fmt: str):
    """Set logger level and format."""
    formatter = logging.Formatter(fmt=fmt)
    lgr.handlers[0].setFormatter(formatter)
    lgr.setLevel(level)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    # set logging level
    if args.verbose:
        set_log_debug(logger)
    else:
        set_log_info(logger)

    GpioTester().run()
