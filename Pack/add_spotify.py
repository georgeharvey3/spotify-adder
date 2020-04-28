# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:48:40 2020

@author: George
"""

import os
import sys
import spotipy
import json
import webbrowser
import spotipy.util as util
from collections import namedtuple
from json.decoder import JSONDecodeError

#print(json.dumps(user, sort_keys=True, indent=4))

USERNAME = 'effilyg' #your spotify username
CLIENT_ID = '8f4eb11b9f704a1c8dca356698b067f3'#set at your developer account
CLIENT_SECRET = 'ad896f7b86084d2abab43243d39fcbe5' #set at your developer account
REDIRECT_URI = 'http://google.com/'
PLAYLIST_ID = 'spotify:playlist:1RwPHhqgAkx25Hig5KqWx6'
SCOPE = 'playlist-modify-public'
    
token = util.prompt_for_user_token(username=USERNAME, scope=SCOPE, client_id=CLIENT_ID, 
                                       client_secret=CLIENT_SECRET, 
                                       redirect_uri=REDIRECT_URI)

#create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

class AlbumError(Exception):
    pass

class ArtistError(Exception):
    pass


def parse_album_name(album_name):
    
    album_name_as_list = [letter for letter in album_name.lower()
             if letter.isalpha() or letter == ' ']
    
    joined_album_name = ''.join(album_name_as_list)
    
    return joined_album_name

def search_for_artist(artist_name):

    search_result = spotifyObject.search(artist_name, 1, 0, 'artist') 
    
    try:
        artist_id = search_result['artists']['items'][0]['id']
    except IndexError:
        raise ArtistError(f'{artist_name} not found')
    
    return artist_id

def find_genres(artist_name):
    search_result = spotifyObject.search(artist_name, 1, 0, 'artist')
    genres = (search_result['artists']['items'][0]['genres'])[:2]
    return genres

def extend_tuple(artist_tuple):
    search_result = spotifyObject.search(artist_tuple.artist, 1, 0, 'artist')
    genres = (search_result['artists']['items'][0]['genres'])[:2]
    
    if genres:
        genres = '/'.join(genres)
    else:
        genres = 'N/A'
    FullAlbumTup = namedtuple('FullAlbumTup', 'artist album genres')
    return FullAlbumTup(*artist_tuple, genres)

def apply_extend(tup_iter):
    return (extend_tuple(tup) for tup in tup_iter)

def search_for_album(artist_id, search_album_name):
    
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
    
    track_results = spotifyObject.album_tracks(album_id)
    track_results = track_results['items']
    ids = [track['id'] for track in track_results]

    return ids

def execute_search(artist_name, album_name):
    
    artist_id = search_for_artist(artist_name)
    album_id = search_for_album (artist_id, album_name)
    
    track_ids = search_for_tracks(album_id)
    
    return track_ids

def add_to_playlist(track_ids):
        
    spotifyObject.user_playlist_add_tracks(USERNAME, PLAYLIST_ID, 
                                           track_ids, position=None)

def current_tracks(playlist_id):
    tracks = spotifyObject.playlist_tracks(playlist_id)
    tracks = tracks['items']
    
    has_ids = [t['track']['name'] for t in tracks]
    

    return has_ids
