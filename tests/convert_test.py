import pytest
from linktune.api.convert import Convert

# Define test data
TEST_LINKS = {
    'spotify': 'https://open.spotify.com/track/5WHTFyqSii0lmT9R21abT8?si=be883a33fde04d9e',
    'tidal': 'https://tidal.com/browse/track/95267869',
    'deezer': 'https://www.deezer.com/track/1987073717',
    'youtube': 'https://music.youtube.com/watch?v=SYto6vfUwXo',
    'apple': 'https://music.apple.com/us/album/hello/1544494115?i=1544494392'
}

def test_convert_link():
    converter = Convert()

    # Test converting each song from one service to each other service
    for source_service, source_link in TEST_LINKS.items():
        for target_service in ['spotify', 'tidal', 'deezer', 'youtube', 'apple']:
            if target_service == source_service:
                continue  # skip converting to the same service
            result = converter.convert_link(source_link, target_service)
            print(result)
            assert isinstance(result, dict)
            assert 'title' in result
            assert 'artist' in result
            assert 'service_url' in result
            assert isinstance(result['service_url'], list)
            assert all(isinstance(service, dict) and len(service) == 1 and isinstance(list(service.values())[0], str) for service in result['service_url'])
# this is a link that is not found on Spotify or Apple; good for testing. also not on Tidal but its wonky atm 
# https://www.deezer.com/en/track/4631046