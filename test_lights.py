#!/usr/bin/env python3
import time
import treelights
from treelights.ledstrip import LEDStrip, Colors
from colour import Color
import animations
import itertools

def zoom_colors(strip):
  colors = [
    Colors.red,
    Colors.yellow,
    Colors.green,
    Colors.blue,
  ]
  for j in range (0, 10):
    c = colors[j % len(colors)]
    for i in range(0, strip.ledCount):
      strip.set(i, c)
      strip.update()
      time.sleep(0.005)
      strip.setOff(i)

if __name__ == '__main__':
  LED_COUNT = 100
  strip = LEDStrip(LED_COUNT)
  strip.off()
  for delay in itertools.islice(animations.zoom_multi(strip), 100):
    time.sleep(delay or 0.03)
  strip.off()
  for delay in itertools.islice(animations.rainbow(strip), 100):
    time.sleep(delay or 0.03)
  strip.off()
  for delay in itertools.islice(animations.zoom_colors(strip), 400):
    time.sleep(delay or 0.03)
  strip.off()