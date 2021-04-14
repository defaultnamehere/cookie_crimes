#ADPATED FROM https://github.com/defaultnamehere/cookie_crimes/blob/master/cookie_crimes.py

import os
import shlex
import shutil
import signal
import sys
import time
import json
import subprocess
import requests
import websocket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', metavar='file', type=str,
    help="Full path to .json files containing cookies")
parser.add_argument("-c", "--clear", action="store_true",
    help="clear all current cookies in the browser")

def escape(s):
    return s.replace(" ", "\ ")

def cookie_reader(cookies):
    f = open(cookies, "r")
    USER_COOKIES = f.read()
    COOKIES = json.loads(USER_COOKIES)
    SET_COOKIES = json.dumps({"id": 1, "method": "Network.setCookies", "params":{"cookies":COOKIES}})
    return SET_COOKIES

os_flags = [] 

# Determining the OS to make sure chrome is opened correctly
if sys.platform.startswith("linux"):
    CHROME_CMD = "google-chrome"
    KILL_CMD = "pkill chrome"
    LINUX_CHROME_CMDS = ["/usr/bin/google-chrome-stable", "/usr/bin/google-chrome-beta", "/usr/bin/google-chrome"]
    for cmd in LINUX_CHROME_CMDS:
        if os.path.isfile(cmd):
            CHROME_CMD = cmd
            break

elif sys.platform.startswith("darwin"):
    KILL_CMD = "killall Google\ Chrome"
    CHROME_CMD = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    os_flags.append("--crash-dumps-dir=/tmp")

elif sys.platform.startswith("win"):
    KILL_CMD = "taskkill /F /IM chrome.exe"
    CHROME_CMD = "C:\PROGRA~2\Google\Chrome\Application\chrome.exe"

else:
    raise RuntimeError("\"%s\"?" % sys.platform)

chrome_args = [
        "https://google.com",
        "--remote-debugging-port=9222",
        "--disable-gpu",
        "--no-sandbox" 
        ]

CHROME_DEBUGGING_CMD = [escape(CHROME_CMD)] + chrome_args + os_flags
CHROME_DEBUGGING_CMD = " ".join(CHROME_DEBUGGING_CMD)

def kill_chrome():
    process = subprocess.Popen(KILL_CMD, shell=True)

def clear_cookies(ws_url, clear):
    if clear == True:
        CLEAR_COOKIES = json.dumps({"id": 1, "method": "Network.clearBrowserCookies"})
        ws = websocket.create_connection(ws_url)
        ws.send(CLEAR_COOKIES)
        ws.close()
        print("All previous cookies cleared.")
    else:
        print("Cookies not cleared")

def start_chrome():
    process = subprocess.Popen(CHROME_DEBUGGING_CMD, shell=True)
    time.sleep(3)
    return process

def find_websocket():
    response = requests.get("http://localhost:9222/json")
    websocket_url = response.json()[0].get("webSocketDebuggerUrl")
    return websocket_url

def insert_cookies(ws_url, SET_COOKIES):
    ws = websocket.create_connection(ws_url)
    #print(SET_COOKIES)
    ws.send(SET_COOKIES)
    ws.close()
    print("Loaded cookies")

if __name__ == "__main__":
    args = parser.parse_args()
    cookies = args.file
    clear = args.clear
    SET_COOKIES = cookie_reader(cookies)
    kill_chrome()
    time.sleep(2)
    process = start_chrome()
    ws_url = find_websocket()
    time.sleep(1) #let it start up before you try to load cookies
    clear_cookies(ws_url, clear)
    insert_cookies(ws_url, SET_COOKIES)

