#!/usr/bin/env python

import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    write_binary_file(file_name, get_response.content)

def write_binary_file(file_name, content):
    with open(file_name, "wb") as file:
        file.write(content)


if __name__ == "__main__":
    download("https://i.ytimg.com/vi/kjzkSHH8LqE/maxresdefault.jpg")