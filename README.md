# LinkTune
LinkTune is a Python command line tool that allows users to convert music links between music streaming services and perform simple song searches across these platforms. Created to facilitate easy music sharing between people using different music services. 
### Supported services
LinkTune currently supports these music services:
- Spotify
- Apple Music
- YouTube Music
- Tidal
- Deezer

## Usage

LinkTune provides two commands: `convert` and `search`.

### `convert`

The `convert` command allows you to convert a music link from one streaming service to another. 

Syntax:

    linktune convert <source_url> <destination_service>

where `<source_url>` is the link to be converted and `<destination_service>` is the streaming service you'd like to generate the link for.

For example, to convert a Spotify link to a Tidal link:

    linktune convert https://open.spotify.com/track/3pUlXJnQx66IitZVn8Lcki tidal

Will return: 
    
    Diazepam by Ren
    Tidal: http://www.tidal.com/track/256813274

### `search`
The `search` command allows you to search for a track across multiple music services. Omitting `--service` will return the track on all services.

Syntax:

    linktune search --artist <artist> --title <title> --service <service>

or use shorthand options, e.g.:

    linktune search -a ren -t diazepam -s apple

    Diazepam by Ren
    Apple Music: https://music.apple.com/us/album/diazepam/1652019136?i=1652019316&uo=4


You may optionally include an `--album` or `-al` flag, e.g.:

    linktune search -a eminem -t mockingbird -al 'curtain call'

    Mockingbird by Eminem
    Spotify: https://open.spotify.com/track/0TGd9kXFDRQG9FF0netmah
    Tidal: http://www.tidal.com/track/622475
    Deezer: https://www.deezer.com/track/1109739
    Apple Music: https://music.apple.com/us/album/mockingbird/1445726870?i=1445727499&uo=4
    YouTube Music: https://music.youtube.com/watch?v=FjVjHkezTIM

## Installation

    pip install linktune
    
### Get a Spotify API key
This app uses the Spotify API, which requires the use of a Spotify client ID and client secret to authenticate API requests. You can generate these for free by creating a Spotify account and navigating to the [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications).

You can then set your local environment variables for `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` as follows:

    export SPOTIPY_CLIENT_ID=<your_client_id>
    export SPOTIPY_CLIENT_SECRET=<your_client_secret>

You can now run the commands described above.

