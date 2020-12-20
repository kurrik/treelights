from treelights.ledstrip import Colors
import time

def zoom_multi(strip):
  skip = 10
  colors = [
    Colors.red,
    Colors.green,
    Colors.white,
  ]
  t = 0
  while True:
    j = 0
    colorIndex = 0
    strip.fillOff()
    while j < strip.ledCount:
      color = colors[colorIndex % len(colors)]
      ledIndex = (j + t) % strip.ledCount
      strip.set(ledIndex, color)
      colorIndex = colorIndex + 1
      j = j + skip
    strip.update()
    t = t + 1
    yield

def off(strip):
  strip.off()
  while True:
    yield
