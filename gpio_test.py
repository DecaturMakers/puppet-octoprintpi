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

import board
from neopixel import NeoPixel, GRBW
from microcontroller import Pin

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

    def run(self):
        print("run.")


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
