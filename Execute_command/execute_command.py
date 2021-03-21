#!/usr/bin/env python

import subprocess # Used to execute terminal commands
import smtplib # Allows sending email

def send_email(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "msg * You have been hacked"
subprocess.Popen(command, shell=True)