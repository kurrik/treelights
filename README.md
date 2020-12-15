# treelights
Playing with programmable tree lights.

## Setup
```
pip3 install -r requirements.txt
```

Written for Python 3.7.

Expects an [Adafruit LPD8806 LED
strip](https://learn.adafruit.com/digital-led-strip) wired according to this
diagram:

![Wiring diagram](docs/raspberry_pi_diagram.png)

## Running
Test the strand with some patterns.
```
python test_lights.py
```

Run server (needs to be set up as a production web app):
```
sudo FLASK_APP=server flask run --host=0.0.0.0 --port=80
```

## References
- https://github.com/adammhaile/RPi-LPD8806/
- http://learn.adafruit.com/light-painting-with-raspberry-pi

## Ribbon cable wiring

![Ribbon cable pins](docs/ribbon-cable.jpg)

I put the cable key facing out from the Raspberry Pi board.  This makes the
following cable assignments:

- Position 18 : SCLK / CI
- Position 22 : MOSI / DI
- Position 35 : GND
- Position 39 : +5V
