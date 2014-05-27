#!/bin/sh

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root (or with sudo)." >&2
    exit 1
fi

# Check and install youtube-dl
echo "Checking for youtube-dl"
if [ -f "/usr/local/bin/youtube-dl" ]; then
    echo "youtube-dl is already installed !"
else
    echo "Installing youtube-dl"
    $(wget https://yt-dl.org/downloads/2014.05.19/youtube-dl -O /usr/local/bin/youtube-dl)
    $(chmod a+x /usr/local/bin/youtube-dl)
fi

# Check and install youtube-dl-playlist
echo "Checking for youtube-dl-playlist"
if [ -f "/usr/local/bin/youtube-dl-playlist" ]; then
    echo "youtube-dl-playlist is already installed !"
else
    echo "Installing youtube-dl-playlist"
    $(wget https://raw.githubusercontent.com/jdupl/youtube-dl-playlist/master/youtube-dl-playlist.py -O /usr/local/bin/youtube-dl-playlist)
    $(chmod a+x /usr/local/bin/youtube-dl-playlist)
fi

# Check and install youtube-dl-channel
echo "Looking for previous installations"
if [ -f "/usr/local/bin/youtube-dl-channel" ]; then
    echo "youtube-dl-channel is already installed !"
else
    echo "Installing youtube-dl-channel"
    $(wget https://raw.githubusercontent.com/jdupl/youtube-dl-channel/master/youtube-dl-channel.py -O /usr/local/bin/youtube-dl-channel)
    $(chmod a+x /usr/local/bin/youtube-dl-channel)
fi

exit 0
