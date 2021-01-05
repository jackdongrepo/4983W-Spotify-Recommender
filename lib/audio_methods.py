import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def findTrack(description):
    return sp.search(description)['tracks']['items'][0]['uri']

def getNameOfTrack(trackuri):
    return sp.track(trackuri)['name']

def getArtistOfTrack(trackuri):
    temp = sp.track(trackuri)['artists']
    artists = ', '.join([i['name'] for i in temp])
    return artists

def getAudioFeatures(trackuri):
    return sp.audio_features(trackuri)[0]

def getAudioAnalysis(trackuri):
    temp = sp.audio_analysis(trackuri)
    del temp['meta']
    del temp['track']['codestring']
    del temp['track']['echoprintstring']
    del temp['track']['synchstring']
    del temp['track']['rhythmstring']
    return temp

def getAlbumGenres(albumuri):
    return sp.album(albumuri)

def getTrack(trackuri):
    return sp.track(trackuri)

def getArtistGenre(trackuri):
    artisturi = getTrack(trackuri)['artists'][0]['uri']
    return sp.artist(artisturi)['genres']

def getTrackBasicInfo(trackuri):
    return sp.track(trackuri)
