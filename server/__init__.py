#!/usr/bin/env python3

from flask import Flask, appcontext_tearing_down, render_template, redirect, url_for
import threading
import time
import atexit
import os
from treelights.ledstrip import LEDStrip, Colors
from collections import defaultdict

LED_COUNT = 100

class SharedState(object):
  def __init__(self):
    self.__mode = 'off'
    self.__exit = False

  def exit(self):
    self.__exit = True

  def shouldExit(self):
    return self.__exit

  def setMode(self, mode):
    self.__mode = mode

  def getMode(self):
    return self.__mode

class LightThread(threading.Thread):
  def __init__(self, shared_state):
    threading.Thread.__init__(self)
    self.__shared_state = shared_state
    self.__strip = LEDStrip(LED_COUNT)
    self.__strip.off()

    self.__handlers = defaultdict(
      lambda: self.off,
      {
        'zoom_multi': self.zoom_multi,
        'off': self.off,
      }
    )

  def off(self):
    self.__strip.off()
    time.sleep(1)

  def zoom_multi(self):
    skip = 10
    colors = [
      Colors.red,
      Colors.green,
      Colors.white,
    ]
    for t in range(0, self.__strip.ledCount):
      j = 0
      colorIndex = 0
      while j < self.__strip.ledCount:
        color = colors[colorIndex % len(colors)]
        ledIndex = (j + t) % self.__strip.ledCount
        self.__strip.set(ledIndex, color)
        colorIndex = colorIndex + 1
        j = j + skip
      self.__strip.update()
      time.sleep(0.03)
      self.__strip.fillOff()

  def run(self):
    print("Starting LightThread.")
    self.process_data()
    print("Stopping LightThread.")

  def process_data(self):
    while not self.__shared_state.shouldExit():
      handler = self.__handlers[self.__shared_state.getMode()]
      handler()

def stop_light_thread():
  print("App shutting down, sending exit signal to LightThread...")
  shared_state.exit()
  light_thread.join()
  print("LightThread shut down...")

shared_state = SharedState()
light_thread = LightThread(shared_state)
light_thread.start()
atexit.register(stop_light_thread)

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # a simple page that says hello
  @app.route('/')
  def root():
    return render_template('root.html')

  @app.route('/zoom_multi')
  def zoom_multi():
    shared_state.setMode('zoom_multi')
    return redirect(url_for('root'))

  @app.route('/off')
  def off():
    shared_state.setMode('off')
    return redirect(url_for('root'))

  return app