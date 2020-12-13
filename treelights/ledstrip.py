import spidev
from colour import Color

class Colors:
  """Constants for easier color specification.
  """
  white = Color(rgb=(1.0, 1.0, 1.0))
  off = Color(rgb=(0, 0, 0))

  red = Color(rgb=(1.0, 0, 0))
  orange = Color(rgb=(1.0, 0.5, 0))
  yellow = Color(rgb=(1.0, 1.0, 0))
  green = Color(rgb=(0, 1.0, 0))
  blue = Color(rgb=(0, 0, 1.0))
  indigo = Color(rgb=(.3, 0, 0.5))
  violet = Color(rgb=(.55, 0, 1.0))

class LPD8806(object):
  """Driver for LPD8806 based LED strips.
  """
  def __init__(self):
    self.spi = spidev.SpiDev()
    self.spi.open(0,0) # Device, equivalent to /dev/spidev0.0
    self.spi.max_speed_hz = 12000000

  def update(self, buffer):
    """Flushes a byte array to the LED strand.

    Args:
        buffer (bytearray): A byte array with three bytes per pixel in the
            strand, with colors set in the expected channel order.
    """
    self.spi.xfer2(buffer)
    self.spi.xfer2([0x00,0x00,0x00])
    self.spi.xfer2([0x00]) # Latch

class ChannelOrder:
  RGB = [0,1,2]
  GRB = [1,0,2]
  BRG = [1,2,0]

class LEDStrip:
  def __init__(self, led_count, channel_order=ChannelOrder.GRB):
    """Controller for a LED strip (only supports LPD8806 strips).

    Args:
        led_count (int): Number of LEDs in the strand.
        channel_order (ChannelOrder, optional): Color order expected by the
            strand. Defaults to ChannelOrder.GRB.
    """
    self.driver = LPD8806()
    self.channelOrder = channel_order
    self.ledCount = led_count
    self.lastIndex = self.ledCount - 1
    self.gamma = bytearray(256)
    self.buffer = bytearray(self.ledCount * 3)
    self.brightness = 1.0

    # Gamma lookup table.
    for i in range(256):
      self.gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

  def update(self):
    """Sends the buffered colors to the strand.
    """
    self.driver.update(self.buffer)

  def setBrightness(self, bright):
    """Set the global brightness for the strand.

    Args:
        bright (float): Value between 0.0 (off) and 1.0 (full brightness)

    Raises:
        ValueError: If out of expected range.
    """
    if(bright > 1.0 or bright < 0.0):
      raise ValueError('Brightness must be between 0.0 and 1.0')
    self.brightness = bright

  #Fill the strand (or a subset) with a single color using a Color object
  def fill(self, color, start=0, end=-1):
    """Sets a range of LEDs to the specified color.

    Args:
        color (colour.Color): Color to set the range to.  RGB (0,0,0) is off.
        start (int, optional): Index of the LED to start with. Defaults to 0.
        end (int, optional): Index of the end of the range, inclusive. -1 is
            the end of the strand. Defaults to -1.
    """
    if start < 0:
      start = 0
    if end < 0 or end > self.lastIndex:
      end = self.lastIndex
    for led in range(start, end + 1):
      self.set(led, color)

  def fillOff(self, start=0, end=-1):
    """ Convenience method for turning off all LEDs in a range.

    Args:
        start (int, optional): Index of the LED to start with. Defaults to 0.
        end (int, optional): Index of the end of the range, inclusive. -1 is
            the end of the strand. Defaults to -1.
    """
    self.fill(Colors.off, start, end)

  def __get_gamma_byte(self, value):
    """Scales an input value using global brightness and gamma correction.

    Args:
        value (float): A 0.0-1.0 value to convert (expected: an R,G,B channel).

    Returns:
        byte: A value from 0-255 corresponding to the gamma corrected and
            brightness adjusted input.
    """
    return self.gamma[int(value * 255 * self.brightness)]

  def set(self, pixel, color):
    """Sets the specified pixel to the specified color in the buffer. Needs a
    call to `update` to flush to strand.

    Args:
        pixel (int): 0-based index of the pixel to set.
        color (colour.Color): Color to set the pixel to. RGB (0,0,0) is off.
    """
    if (pixel < 0 or pixel > self.lastIndex):
      return
    index = pixel * 3
    self.buffer[index + self.channelOrder[0]] = self.__get_gamma_byte(color.red)
    self.buffer[index + self.channelOrder[1]] = self.__get_gamma_byte(color.green)
    self.buffer[index + self.channelOrder[2]] = self.__get_gamma_byte(color.blue)

  #turns off the desired pixel
  def setOff(self, pixel):
    """Convenience method for turning off the specified pixel.

    Args:
        pixel (int): Index of the pixel to turn off.
    """
    self.set(pixel, Colors.off)

  def off(self):
    """Turns off all of the lights in the strand and flushes the buffer to
    the strand.
    """
    self.fillOff()
    self.update()