#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyDJ7jIvgvXxY4Ox9kLONyhEl3O6s9-mM_4'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(query, max_results):
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append(
                '%s (%s)' % (
                    search_result['snippet']['title'],
                    search_result['id']['videoId'])
            )
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append(
                '%s (%s)' % (
                    search_result['snippet']['title'],
                    search_result['id']['channelId']
                )
            )
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append(
                '%s (%s)' % (
                    search_result['snippet']['title'],
                    search_result['id']['playlistId']
                )
            )

    print('Videos:\n', '\n'.join(videos), '\n')
    print('Channels:\n', '\n'.join(channels), '\n')
    print('Playlists:\n', '\n'.join(playlists), '\n')

    vids = search_response.get('items', [])
    # return the search results from this fuction
    return vids


def json_dump(json_data, filename):
    # dump the json_json data to a file with filename
    json_fname = '{}.json'.format(filename)
    with open(json_fname, 'w') as fname:
        json.dump(json_data, fname, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='surgery')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()

    # get the query and max_results inputs
    query = args.q
    max_results = args.max_results

    try:
        # assign search results to variable
        search_results = youtube_search(query, max_results)
    except HttpError as e:
        print(
            'An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content)
        )
    json_dump(search_results, 'video_data')

