import pickle
import os
import parse_infgen

CHARTDATA_FILENAME = 'hot-100-chartdata.pickle'
DB_FILENAME = 'hot-100.pickle'
LYRICS_DIR = 'lyrics'
OMNI_PICKLE_NAME = 'omnisongs.pickle'

class NotScrapedException(Exception):
    pass

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

def get_omnisong():
    with open(OMNI_PICKLE_NAME) as f:
        om = pickle.load(f)
    return om

def get_chartdata():
    with open(CHARTDATA_FILENAME) as f:
        cd = pickle.load(f)
    return cd

def get_sizes(song_or_key):
    if isinstance(song_or_key, basestring):
        k = song_or_key
    else:
        k = song_key(song_or_key)
    path = os.path.join(LYRICS_DIR, k+'.txt')
    try:
        raw = os.path.getsize(path)
    except OSError:
        raise NotScrapedException
    comp = os.path.getsize(path+'.gz')
    return (raw, comp)

def get_inf_sizes(song_or_key):
    """Return raw/compressed sizes used when calculating the infgen-based 
    compression ratio. Raw size will be the same as above (i.e. just the
    number you'd get from `wc -c` on the text file).
    The compressed size will be an approximation of the size of the LZ-77
    compressed data *before* Huffman coding. Assumes 1 byte per literal, 3
    bytes per match."""
    if isinstance(song_or_key, basestring):
        k = song_or_key
    else:
        k = song_key(song_or_key)
    path = os.path.join(LYRICS_DIR, k+'.txt.gz.infgen')
    with open(path) as f:
        return parse_infgen.parse_ratio(f)
