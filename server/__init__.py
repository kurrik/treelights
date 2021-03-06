#!/usr/bin/env python3

from flask import Flask, appcontext_tearing_down, render_template, redirect, url_for, send_from_directory, make_response
import threading
import time
import atexit
import os
import os.path
from treelights.ledstrip import LEDStrip, Colors
from collections import defaultdict
import signal
import logging
import animations

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
      lambda: animations.off,
      animations.animations_list)

  def run(self):
    logging.info("Starting LightThread.")
    self.process_data()
    logging.info("Stopping LightThread.")

  def process_data(self):
    current_mode = "None"
    current_handler = animations.off(self.__strip)
    while not self.__shared_state.shouldExit():
      new_mode = self.__shared_state.getMode()
      if new_mode != current_mode:
        current_handler = self.__handlers[new_mode].handler(self.__strip)
        current_mode = new_mode
        self.__strip.off()
      try:
        delay = next(current_handler)
      except StopIteration:
        current_handler = animations.off(self.__strip)
      time.sleep(delay or 0.03)

def on_exit_signal(signum, frame):
  if not shared_state.shouldExit():
    logging.info("Got signal {}, stopping light thread...".format(signum))
    stop_light_thread()
  else:
    logging.info("Got signal {} but program was already exiting.".format(signum))

def stop_light_thread():
  logging.info("App shutting down, sending exit signal to LightThread...")
  shared_state.exit()
  light_thread.join()
  logging.info("LightThread shut down...")

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
shared_state = SharedState()
light_thread = LightThread(shared_state)
light_thread.start()
atexit.register(on_exit_signal, signum=signal.SIGUSR1, frame=None)
if __name__ == '__main__':
  logging.info('Running in main thread. Registering signal handlers.')
  signal.signal(signal.SIGINT, on_exit_signal)
  signal.signal(signal.SIGTERM, on_exit_signal)
else:
  logging.info('Not running in main thread! Not registering signal handlers.')

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
    response = make_response(render_template('root.html',
      mode=shared_state.getMode(),
      animations=animations.animations_list))
    response.headers['Service-Worker-Allowed'] = '/'
    return response

  @app.route('/favicon.ico')
  def favicon():
    return app.send_static_file('icon-32.png')

  @app.route('/apple-touch-icon.png')
  def apple_touch_icon():
    return app.send_static_file('icon-180.png')

  @app.route('/manifest.webmanifest')
  def manifest():
    return send_from_directory(
      app.static_folder,
      'manifest.webmanifest',
      mimetype='application/manifest+json;charset=UTF-8',
      as_attachment=False)

  @app.route('/serviceworker.js')
  def serviceworker():
    response = make_response(send_from_directory(
      os.path.join(app.static_folder, 'js'),
      'serviceworker.js',
      mimetype='application/javascript;charset=UTF-8',
      as_attachment=False))
    response.headers['Service-Worker-Allowed'] = '/'
    return response

  @app.route('/animate/<animation>')
  def animate(animation):
    shared_state.setMode(animation)
    return redirect(url_for('root'))

  return app