#!/usr/bin/python3
# youtube-dl-channel
#
# Utility to download Youtube a channel's' playlists.
# Inspired by https://github.com/jordoncm/youtube-dl-playlist
#
# Python 3.X support only
#
# @author Justin Duplessis
# @license GPL version 2 <http://www.gnu.org/licenses/gpl2.html>

import sys
import http.client
import urllib.parse
import json


class ChannelDownloader:

    def fetchPlaylists(self, channel_id):
        connection = http.client.HTTPConnection('gdata.youtube.com')
        connection.request('GET', '/feeds/api/users/' + str(channel_id) +
        '/playlists?' + urllib.parse.urlencode({
                'alt': 'json',
                'v': 2
            }))
        response = connection.getresponse()
        if response.status != 200:
            print('Error: Not a valid/public user.')
            sys.exit(1)
        data = response.read()
        data = json.loads(data.decode('utf8'))
        playlists = data['feed']['entry']
        for playlist in playlists:
            print(playlist['title']['$t'])
        return data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: youtube-dl-channel USER')
        sys.exit(1)
    else:
        user = sys.argv[1]
    downloader = ChannelDownloader()
    downloader.fetchPlaylists(user)