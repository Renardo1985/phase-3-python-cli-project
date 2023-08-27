from models import User, Songs, Playlist
from sessions import session
import re

import requests
import json # https://www.w3schools.com/python/python_json.asp


def find_by_title(title):
    response = requests.get(f"https://itunes.apple.com/search?term={title}&media=music&entity=song&attribute=songTerm&country=US&limit=30")
    if response.status_code == 200:
        data = json.loads(response.text)
           
        results = data["results"]                
        songs = []     
        for track in results:
            song = Songs(title= track["trackName"], artist= track["artistName"],genre= track["primaryGenreName"])
            if song in songs:
                pass
            else:
                songs.append(song)
        
        if songs:
            return songs
    else:
        return response.status_code


def find_by_artist(artist):
    response = requests.get(f"https://itunes.apple.com/search?term={artist}&media=music&entity=song&attribute=artistTerm&country=US&limit=50")  
    if response.status_code == 200:
        data = json.loads(response.text)
           
        results = data["results"]                
        songs = []     
        for track in results:
            if re.match(track["artistName"], artist, re.IGNORECASE):
                song = Songs(title= track["trackName"], artist= track["artistName"],genre= track["primaryGenreName"])
                if song in songs:
                    pass
                else:
                    songs.append(song)
        
        if songs:
            return songs
    else:
        return response.status_code
    
    

        