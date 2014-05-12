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

    """Call youtube api and return json object of videos from a playlist"""
    def getPlaylistsVideos(playlist_id, start, limit):
        connection = http.client.HTTPConnection('gdata.youtube.com')
        connection.request('GET', '/feeds/api/playlists/' +
         str(playlist_id) + '/?' + urllib.parse.urlencode({
                'alt': 'json',
                'max-results': limit,
                'start-index': start,
                'v': 2
            }))

        response = connection.getresponse()
        if response.status != 200:
            print('Error: Not a valid/public playlist.')
            sys.exit(1)

        data = response.read()
        return json.loads(data.decode('utf8'))


class PlaylistDownloader:

    def __fetchVideos(self, playlist_id, start=1, limit=25):
        return

    def __fetchAllVideos(self, playlist_id, start, limit):
        return


class ChannelDownloader:

    playlist_ids = []
    playlist_count = 1

    def __fetchPlaylists(self, channel_id, start=1, limit=25):
        data = YoutubeApi.getUserPlaylists(channel_id, start, limit)
        if(data['feed'] and data['feed']['entry']):
            playlists = data['feed']['entry']
            for playlist in playlists:
                playlist_id = playlist['yt$playlistId']['$t']
                playlist_name = playlist['title']['$t']
                print(str(self.playlist_count) + " " + playlist_name)
                self.playlist_count = self.playlist_count + 1
                self.playlist_ids.append(playlist_id)

    def getAllPlaylists(self, channel_id):
        data = YoutubeApi.getUserPlaylists(channel_id, 1, 0)
        playlist_total_count = data['feed']['openSearch$totalResults']['$t']
        print("Getting info for " + str(playlist_total_count) + " playlists")
        while self.playlist_count < playlist_total_count:
            self.fetchPlaylists(channel_id, self.playlist_count)
        print("ok")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: youtube-dl-channel USER')
        sys.exit(1)
    else:
        user = sys.argv[1]
    downloader = ChannelDownloader()
    downloader.getAllPlaylists(user)