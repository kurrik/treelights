from treelights.ledstrip import Colors
import time

def off(strip):
  strip.off()
  while True:
    yield

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
  j = 0
  while True:
    for i in range(0, strip.ledCount):
      strip.set(i, colors[(i + j) % len(colors)])
    strip.update()
    j = j + 1
    yield 0.03

def zoom_colors(strip):
  colors = [
    Colors.red,
    Colors.yellow,
    Colors.green,
    Colors.blue,
  ]
  j = 0
  while True:
    c = colors[j % len(colors)]
    for i in range(0, strip.ledCount):
      strip.set(i, c)
      strip.update()
      yield 0.005
      strip.setOff(i)
    j = j + 1

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
    yield 0.03
