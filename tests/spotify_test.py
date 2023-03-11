# Tests for the Spotify module

import pytest 
import json
from unittest.mock import MagicMock
from linktune.api.spotify import Spotify

# Mock Spotify API response
SPOTIFY_API_RESPONSE = {
    'tracks': {
        'total': 1,
        'items': [
            {
                'name': 'Test Track',
                'external_urls': {
                    'spotify': 'https://open.spotify.com/track/12345'
                },
                'artists': [
                    {'name': 'Test Artist'}
                ]
            }
        ]
    }
}


@pytest.fixture
def spotify():
    # use test credentials
    client_id = 'test_client_id'
    client_secret = 'test_client_secret'
    return Spotify(client_id, client_secret)

# Test get_track_id returns correct track id string from url and returns None from non-spotify urls
def test_get_track_id(spotify):
    assert spotify._get_track_id('https://open.spotify.com/track/4O4A5zbsLjBtN6Xsi2jLRt?si=7eb26b245d504370') == '4O4A5zbsLjBtN6Xsi2jLRt'
    assert spotify._get_track_id('spotify:track:4O4A5zbsLjBtN6Xsi2jLRt') == '4O4A5zbsLjBtN6Xsi2jLRt'
    assert spotify._get_track_id('https://google.com') is None

def test_get_track_info(spotify):
    # mock track id and spotify api response
    track_id = '12345'
    spotify.sp.track = MagicMock(return_value={
                'name': 'Test Track',
        'artists': [
            {'name': 'Test Artist'}
        ],
        'album': {
            'name': 'Test Album'
        }
    })

    assert spotify.get_track_info(f'https://open.spotify.com/track/{track_id}') == {
        'artist': 'Test Artist',
        'title': 'Test Track',
        'album': 'Test Album'
    }

def test_get_track_info_invalid_track_url(spotify):
    assert spotify.get_track_info('invalid url') == 'Could not identify Spotify track ID'

# test searching spotify to retrieve url
def test_get_service_url(spotify):
    # mock track info
    track_info = {
        'artist': 'Test Artist',
        'title': 'Test Track',
        'album': 'Test Album'
    }
    # mock Spotify API response
    spotify.sp.search = MagicMock(return_value = SPOTIFY_API_RESPONSE)
    assert spotify.get_service_url(track_info) == {
        'service': 'Spotify',
        'title': 'Test Track',
        'artist': ['Test Artist'],
        'url': 'https://open.spotify.com/track/12345'
    }

# test searching with a query that yields no results
def test_get_service_url_no_results(spotify):
    # mock track info
    track_info = {
        'artist': 'Test Artist',
        'title': 'Test Track',
        'album': 'Test Album'
    }
    # mock Spotify API response with no results
    spotify.sp.search = MagicMock(return_value={'tracks': {'total': 0}})
    assert spotify.get_service_url(track_info) == None