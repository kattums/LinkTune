# LinkTune
LinkTune is a Python command line tool that allows users to convert music links between music streaming services and perform simple song searches across these platforms. Created to facilitate easy music sharing between people using different music services, LinkTune currently supports link conversion between Spotify, Apple Music, Tidal, and Deezer.

## Installation
working on it

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
    
    info: Diazepam by Ren, url: http://www.tidal.com/track/176483583

### `search`
The `search` command allows you to search for a track across multiple music services. 

Syntax:

    linktune search --artist <artist> --title <title> --service <service>

or use shorthand options, e.g.:

    linktune search -a ren -t diazepam -s apple

    Diazepam by Ren: https://music.apple.com/us/album/diazepam/1652019136?i=1652019316&uo=4

## Supported services
LinkTune currently supports these music services:
- Spotify
- Apple Music
- Tidal
- Deezer