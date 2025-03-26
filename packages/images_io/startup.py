#!/usr/bin/env python3
import socket

def check_internet(host="8.8.8.8", port=53, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection((host, port))
        print("Internet access is working!")
        with open("InternetAccessIsWorking", "w") as file:
            file.write("Internet access is working!")
            print("Internet access is working!")
    except Exception as e:
        with open("NoAccess", "w") as file:
            file.write("No access")
            print("No access")
        
check_internet()