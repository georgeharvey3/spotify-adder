# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:48:21 2020

@author: George
"""


from bs4 import BeautifulSoup
import requests
from collections import namedtuple


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

#month = input('Enter the month you would like to see (YYYY-MM): ')
month = '2020-04'
page = 'https://downbeat.com/reviews/editorspicks/'


def find_albums(page, month):
    
    page = page + month
    
    res = requests.get(page, headers = headers, verify=False)
    if res.status_code != 200:
        print('Web site does not exist') 
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'html.parser')
    
    all_heads = soup.find_all('h2')
    all_subs = soup.find_all('subhead')
    
    if len(all_heads) == 0:
        raise ValueError('Month may have been invalid')
    
    heads_text = (BeautifulSoup.get_text(head) for head in all_heads)
    subs_text = (BeautifulSoup.get_text(sub).replace('\n', '').strip() 
                 for sub in all_subs)
    
    pairs = zip(heads_text, subs_text)
    
    return process_albums(pairs)


def process_albums(pairs):

    
    AlbumTup = namedtuple('AlbumTup', 'artist album')
    album_tups = (AlbumTup(*pair) for pair in pairs)
    
    return album_tups
    
    
