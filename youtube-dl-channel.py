#!/usr/bin/python3
# youtube-dl-channel
#
# Utility to download Youtube a channel's playlists.
# Inspired by https://github.com/jordoncm/youtube-dl-playlist
#
# Python 3.x support only !
#
# @author Justin Duplessis
# @license GPL version 2 <http://www.gnu.org/licenses/gpl2.html>

import sys
import http.client
import urllib.parse
import json
from subprocess import call


class YoutubeApi:

    """Call youtube api and return json object of playlists from a user"""
    def getUserPlaylists(channel_id, start, limit):
        connection = http.client.HTTPConnection('gdata.youtube.com')
        connection.request('GET', '/feeds/api/users/' + str(channel_id) +
        '/playlists?' + urllib.parse.urlencode({
                'alt': 'json',
                'max-results': limit,
                'start-index': start,
                'v': 2
            }))
        response = connection.getresponse()

        if response.status != 200:
            print('Error: Not a valid/public user.')
            print(start)
            print(limit)
            sys.exit(1)
        data = response.read()
        return json.loads(data.decode('utf8'))


class ChannelDownloader:

    playlist_ids = []
    playlist_count = 1

    def __fetchPlaylists(self, channel_id, start=1, limit=25):
        data = YoutubeApi.getUserPlaylists(channel_id, start, limit)
        if(data['feed'] and data['feed']['entry']):
            playlists = data['feed']['entry']
            for playlist in playlists:
                self.playlist_ids.append(playlist['yt$playlistId']['$t'])
                self.playlist_count += 1

    def __getAllPlaylists(self, channel_id):
        data = YoutubeApi.getUserPlaylists(channel_id, 1, 0)
        playlist_total_count = data['feed']['openSearch$totalResults']['$t']
        while self.playlist_count < playlist_total_count:
            self.__fetchPlaylists(channel_id, self.playlist_count)
        return self.playlist_ids

    def download(self, channel_id, destination):
        print("Fetching user playlists...")
        playlist_ids = self.__getAllPlaylists(user)
        total_playlist_count = len(playlist_ids)
        print("Got %d playlists" % total_playlist_count)
        for playlist_id in playlist_ids:
            call(["youtube-dl-playlist", playlist_id, destination])

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage: youtube-dl-channel USER [DESTINATION]')
        sys.exit(1)
    else:
        user = sys.argv[1]
    if len(sys.argv) > 2:
        destination = sys.argv[2]
    else:
        destination = "."

    channel_info = ChannelDownloader()
    channel_info.download(user, destination)