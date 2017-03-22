import pickle
import os

CHARTDATA_FILENAME = 'hot-100-chartdata.pickle'
DB_FILENAME = 'hot-100.pickle'
LYRICS_DIR = 'lyrics'

def have_lyrics(song):
    k = song_key(song)
    path = os.path.join(LYRICS_DIR, k+'.txt')
    return os.path.exists(path)

def song_key(song):
    k = song.artist[:15] + '-' + song.title[:20]
    k = k.replace('/', '')
    return k.replace(' ', '_')

def get_songdb():
    with open(DB_FILENAME) as f:
        db = pickle.load(f)
    return db

def get_chartdata():
    with open(CHARTDATA_FILENAME) as f:
        cd = pickle.load(f)
    return cd

def get_sizes(k):
    path = os.path.join(LYRICS_DIR, k+'.txt')
    raw = os.path.getsize(path)
    comp = os.path.getsize(path+'.gz')
    return (raw, comp)
