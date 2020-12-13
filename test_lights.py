#!/usr/bin/env python3
import time
import treelights
from treelights.ledstrip import LEDStrip, Colors
from colour import Color

def rainbow(strip):
  colors = [
    Colors.red,
    Colors.orange,
    Colors.yellow,
    Colors.green,
    Colors.blue,
    Colors.indigo,
    Colors.violet,
  ]
  for j in range(1, 50):
    for i in range(0, strip.ledCount):
      strip.set(i, colors[(i + j) % len(colors)])
    strip.update()
    time.sleep(0.05)

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

def zoom_multi(strip):
  skip = 10
  colors = [
    Colors.red,
    Colors.green,
    Colors.white,
  ]
  for t in range(0, 100):
    j = 0
    colorIndex = 0
    while j < strip.ledCount:
      color = colors[colorIndex % len(colors)]
      ledIndex = (j + t) % strip.ledCount
      strip.set(ledIndex, color)
      colorIndex = colorIndex + 1
      j = j + skip
    strip.update()
    time.sleep(0.03)
    strip.fillOff()

if __name__ == '__main__':
  LED_COUNT = 100
  strip = LEDStrip(LED_COUNT)
  strip.off()
  zoom_multi(strip)
  rainbow(strip)
  strip.off()
  zoom_colors(strip)
  strip.off()