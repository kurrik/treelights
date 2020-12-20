#!/usr/bin/env python3
import time
import treelights
from treelights.ledstrip import LEDStrip, Colors
from colour import Color
import animations
import itertools
import inspect

def run_animation(strip, animation, cycles=100, delay=0.03):
  strip.off()
  for d in itertools.islice(animation(strip), cycles):
    time.sleep(d or delay)

if __name__ == '__main__':
  LED_COUNT = 100
  strip = LEDStrip(LED_COUNT)
  try:
    run_animation(strip, animations.sparkle, cycles=1000)
    run_animation(strip, animations.rainbow)
    run_animation(strip, animations.zoom_colors, cycles=400)
    run_animation(strip, animations.zoom_multi)
  finally:
    strip.off()
