#!/usr/bin/python3
# youtube-dl-channel
#
# Utility to download Youtube a channel's playlists. Updated for api v3.
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
import os
import re #used to check youtube-user-id's pattern

from subprocess import call


class YoutubeApi:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_channel_id(self, user):

        if re.match(r'^[A-Z]+-[\w]+$', user): #FIXME improve this pattern checking
            return user #user is the channel_id itself, if pattern matches

        params = urllib.parse.urlencode({
                'part': 'id',
                'forUsername': user,
                'key': self.api_key
            })
        connection = http.client.HTTPSConnection('www.googleapis.com')
        connection.request('GET', '/youtube/v3/channels?' + params)
        response = connection.getresponse()
        data = json.loads(response.read().decode('utf8'))

        if response.status != 200:
            print(data.error.message)
            exit(1)

        if data['pageInfo']['totalResults'] != 1:
            print('Error: Not a valid/public user.')
            exit(1)

        return data['items'][0]['id']

    def get_all_user_playlists(self, channel_id):
        has_next_token = True
        token = None
        playlists = []

        while has_next_token:
            items, next_token = self._get_user_playlists(channel_id, token)
            playlists.extend(items)
            if next_token:
                token = next_token
                has_next_token = True
            else:
                has_next_token = False
        return playlists

    def _get_user_playlists(self, channel_id, page_token):
        raw_params = {
            'part': 'snippet',
            'channelId': channel_id,
            'key': self.api_key,
            'maxResults': 50
        }

        if page_token:
            raw_params['pageToken'] = page_token
        params = urllib.parse.urlencode(raw_params)

        connection = http.client.HTTPSConnection('www.googleapis.com')
        connection.request('GET', '/youtube/v3/playlists?' + params)

        response = connection.getresponse()
        data = json.loads(response.read().decode('utf8'))

        if response.status != 200:
            print(data['error']['message'])
            exit(1)

        next_token = None
        if 'nextPageToken' in data:
            next_token = data['nextPageToken']

        playlists = []
        for playlist in data['items']:
            playlists.append({
                'id': playlist['id'],
                'name': playlist['snippet']['title']
            })
        return playlists, next_token


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

    api_key = 'AIzaSyDRAsVVqrWSRAK-WPrFM-A5IfyqK3XgmFs'
    api = YoutubeApi(api_key)

    print('Resolving user "{}" as a channel id...'.format(user))
    channel_id = api.get_channel_id(user)
    print('Got channel id {}'.format(channel_id))

    playlists = api.get_all_user_playlists(channel_id)
    print('Got {} playlists'.format(len(playlists)))

    for playlist in playlists:
        playlist_dest = os.path.join(destination, playlist['name'])
        call(['youtube-dl', '-o', os.path.join(playlist_dest,
            '%(playlist_index)s - %(title)s-%(id)s.%(ext)s'), playlist['id']])
