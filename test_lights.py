#!/usr/bin/env python3
import time
import treelights
from treelights.ledstrip import LEDStrip, Colors
from colour import Color

LED_COUNT = 100

strip = LEDStrip(LED_COUNT)
strip.off()

rainbow = [
  Colors.red,
  Colors.orange,
  Colors.yellow,
  Colors.green,
  Colors.blue,
  Colors.indigo,
  Colors.violet,
]

for j in range(1, 50):
  for i in range(0, LED_COUNT):
    strip.set(i, rainbow[(i + j) % len(rainbow)])
  strip.update()
  time.sleep(0.05)

strip.off()

for i in range(0, LED_COUNT):
  strip.set(i, Color(rgb=(0, 1.0, 0)))
  strip.update()
  time.sleep(0.01)
  strip.setOff(i)

strip.off()