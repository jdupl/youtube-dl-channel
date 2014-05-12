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

    video_count = 1
    video_ids = []

    def __fetchVideos(self, playlist_id, start=1, limit=25):
        data = YoutubeApi.getPlaylistsVideos(playlist_id, start, limit)
        if('feed' in data and 'entry' in data['feed']):
            videos = data['feed']['entry']
            for video in videos:
                self.video_ids.append(video['media$group']['yt$videoid']['$t'])
                self.video_count += 1
            return len(videos)
        else:
            return -1

    def getAllVideos(self, playlist_id):
        self.video_ids = []
        self.video_count = 1
        
        data = YoutubeApi.getPlaylistsVideos(playlist_id, 1, 0)

        video_total_count = data['feed']['openSearch$totalResults']['$t']
        title = data['feed']['title']['$t']
        print("Getting videos for playlist %s" % title)
        playlist = {'id': playlist_id, 'title': title, 'video_ids': []}
        videos_got = 0
        while self.video_count <= video_total_count and videos_got > -1:
            videos_got = self.__fetchVideos(playlist_id, self.video_count)
        playlist['video_ids'] = self.video_ids
        print("Got %d videos, expected %d" %
        (len(self.video_ids), video_total_count))
        return playlist


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

    def getAllPlaylists(self, channel_id):
        data = YoutubeApi.getUserPlaylists(channel_id, 1, 0)
        playlist_total_count = data['feed']['openSearch$totalResults']['$t']
        while self.playlist_count < playlist_total_count:
            self.__fetchPlaylists(channel_id, self.playlist_count)
        return self.playlist_ids

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: youtube-dl-channel USER')
        sys.exit(1)
    else:
        user = sys.argv[1]

    channel_info = ChannelDownloader()
    playlist_info = PlaylistDownloader()
    playlists = []
    total_video_count = 0
    total_playlist_count = 0

    print("Fetching user playlists...")
    playlist_ids = channel_info.getAllPlaylists(user)
    total_playlist_count = len(playlist_ids)
    print("Got %d playlists" % total_playlist_count)

    print("Fetching playlists videos...")
    for playlist_id in playlist_ids:
        p = playlist_info.getAllVideos(playlist_id)
        playlists.append(p)
        total_video_count += len(p['video_ids'])
    print("Got %d videos to download in %d playlists" %
     (total_video_count, total_playlist_count))
