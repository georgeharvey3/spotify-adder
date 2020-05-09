# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:48:40 2020

@author: George
"""

import os
import spotipy
import spotipy.util as util
from collections import namedtuple

if os.getcwd() != os.path.dirname(os.path.abspath(__file__)):
    import config
else:
    import Pack.config as config

    
token = util.prompt_for_user_token(username=config.USERNAME, scope=config.SCOPE,
                                   client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET,
                                   redirect_uri=config.REDIRECT_URI)

# create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)


class AlbumError(Exception):
    """Error raised when album cannot be found"""
    pass

class ArtistError(Exception):
    """Error raised when artist cannot be found"""
    pass


def parse_album_name(album_name):

    """Parse album name so it will be recognised in Spotify"""
    
    album_name_as_list = [letter for letter in album_name.lower()
             if letter.isalpha() or letter == ' ']
    
    joined_album_name = ''.join(album_name_as_list)
    
    return joined_album_name


def search_for_artist(artist_name):

    """Search Spotify for artist """

    search_result = spotifyObject.search(artist_name, 1, 0, 'artist') 
    
    try:
        artist_id = search_result['artists']['items'][0]['id']
    except IndexError:
        raise ArtistError(f'{artist_name} not found')
    
    return artist_id


def find_genres(artist_name):

    """Find a list of genres associated with the artist"""

    search_result = spotifyObject.search(artist_name, 1, 0, 'artist')
    genres = (search_result['artists']['items'][0]['genres'])[:2]
    return genres


def extend_tuple(artist_tuple):

    """Add genres as an extra field to named tuple"""

    search_result = spotifyObject.search(artist_tuple.artist, 1, 0, 'artist')
    try:
        genres = (search_result['artists']['items'][0]['genres'])[:2]
    except IndexError:
        genres = ''
    
    if genres:
        genres = '/'.join(genres)
    else:
        genres = 'N/A'
    FullAlbumTup = namedtuple('FullAlbumTup', 'artist album genres')
    return FullAlbumTup(*artist_tuple, genres)


def apply_extend(tup_iter):

    """Implements extend_tuple function"""

    return (extend_tuple(tup) for tup in tup_iter)


def search_for_album(artist_id, search_album_name):

    """Searches for an album name within an artist's discography"""
    
    album_results = spotifyObject.artist_albums(artist_id)
    album_results = album_results['items']
    
    parsed_search_album_name = parse_album_name(search_album_name)

    for album in album_results:
        unparsed_name = album['name']
        album_name = parse_album_name(unparsed_name)
        if parsed_search_album_name == album_name:
            return album['id']
        
    else:
        raise AlbumError(f'{search_album_name} not found')


def search_for_tracks(album_id):

    """Obtains a list of tracks for a given album_id"""
    
    track_results = spotifyObject.album_tracks(album_id)
    track_results = track_results['items']
    ids = [track['id'] for track in track_results]

    return ids


def execute_search(artist_name, album_name):

    """Executes a full search of artist_name and album_name and returns corresponding track_ids"""
    
    artist_id = search_for_artist(artist_name)
    album_id = search_for_album (artist_id, album_name)
    
    track_ids = search_for_tracks(album_id)
    
    return track_ids


def add_to_playlist(track_ids):

    """Adds supplied tracks to specified playlist"""
        
    spotifyObject.user_playlist_add_tracks(config.USERNAME, config.PLAYLIST_ID,
                                           track_ids, position=None)


def current_tracks(playlist_id):

    """Obtains a list of tracks currently in specified playlist"""

    tracks = spotifyObject.playlist_tracks(playlist_id)
    tracks = tracks['items']
    
    has_ids = [t['track']['name'] for t in tracks]
    

    return has_ids
