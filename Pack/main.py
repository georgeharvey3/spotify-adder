# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:46:57 2020

@author: George
"""

import add_spotify
import get_albums
import datetime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

page = 'https://downbeat.com/reviews/editorspicks/'

def get_dt():
    dt = datetime.datetime.utcnow()
    dt_month_string = datetime.datetime.strftime(dt, '%Y-%m')
    
    return dt_month_string

def run_program(page, month=None):
    if month is None:
        month = get_dt()
            
    results = get_albums.find_albums(page, month)
    
    artist_genres = {result.artist:add_spotify.find_genres(result.artist)
                     for result in results}
    print(artist_genres)

    for album in results:
        try:
            track_ids = add_spotify.execute_search(album.artist, album.album)
            add_spotity.add_to_playlist(track_ids)
        except (add_spotify.ArtistError, spotify.AlbumError) as ex:
            print(ex)
            
#run_program(page)

def run_program2(page, month=None):
    if month is None:
        month = get_dt()
            
    results = get_albums.find_albums(page, month)
    
    print(list(results))
    

            
run_program2(page)       


