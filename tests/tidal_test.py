import pytest 
from unittest.mock import MagicMock
from linktune.api.tidal import Tidal

# Mock Tidal API response
TIDAL_API_RESPONSE = {}

@pytest.fixture
def tidal():
    return Tidal()

def test_get_track_id(tidal):
    assert tidal._get_track_id('http://www.tidal.com/track/33849349') == '33849349'
    assert tidal._get_track_id('http://www.tidal.com/track/105885587') == '105885587'


def test_get_track_info(tidal):
    tidal.tidal.get_track = MagicMock(return_value = {
        'title': 'Test Title',
        'artist': {'name': 'Test Artist'},
        'album': {'title': 'Test Album'}
    })
    assert tidal.get_track_info('https://tidal.com/browse/track/12345') == {
        'title': 'Test Title',
        'artist': 'Test Artist',
        'album': 'Test Album'
    }

def test_get_track_info_invalid_url(tidal):
    tidal.tidal.get_track_info = MagicMock(return_value = None)
    assert tidal.get_track_info('invalid_url') is None

def test_get_service_url(tidal):
    tidal.tidal.search = MagicMock(return_value = {
        'items': [
            {
                'title': 'Test Title',
                'artists': [{'name': 'Test Artist'}],
                'url': 'https://tidal.com/browse/track/12345'
            }
        ]
    })
    assert tidal.get_service_url({'title': 'Test Title', 'artist': 'Test Artist'}) == {
        'service': 'Tidal',
        'title': 'Test Title',
        'artist': ['Test Artist'],
        'url': 'https://tidal.com/browse/track/12345'
    }

def test_get_service_url_album(tidal):
    tidal.tidal.search = MagicMock(return_value = {
        'items': [
            {
                'title': 'Test Title',
                'artists': [{'name': 'Test Artist'}],
                'url': 'https://tidal.com/browse/track/12345'
            }
        ]
    })
    assert tidal.get_service_url({'title': 'Test Title', 'artist': 'Test Artist', 'album': 'Test Album'}) == {
        'service': 'Tidal',
        'title': 'Test Title',
        'artist': ['Test Artist'],
        'url': 'https://tidal.com/browse/track/12345'
    }