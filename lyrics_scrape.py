import pickle
import time
import os

import Lyrics

PICKLE_NAME = 'hot-100.pickle'
LYRICS_DIR = 'lyrics'
SLEEPYTIME = 1

def song_key(song):
    k = song.artist[:10] + '-' + song.title[:40]
    k = k.replace('/', '')
    return k.replace(' ', '_')

def unicode_unfuck(s):
    return ''.join(map(lambda c: chr(ord(c)), s))

with open(PICKLE_NAME) as f:
    db = pickle.load(f)

skipped = set()
i = 0
lim = float('inf')
for artist in db:
    for song in db[artist].itervalues():
        k = song_key(song)
        path = os.path.join(LYRICS_DIR, k + '.txt')
        if os.path.exists(path):
            continue
        query = song.artist + ' ' + song.title
        try:
            lyrics = Lyrics.get_lyrics(query)
            time.sleep(SLEEPYTIME)
        except Lyrics.LyricsNotFoundException:
            print "Failed to find lyrics for {} using query: {}".format(song, query)
            skipped.add(k)
            continue
        if len(lyrics) == 0:
            print "WARNING: Got length 0 lyrics for {}".format(song)
            i += 1
            continue
        with open(path, 'w') as f:
            try:
                f.write(lyrics)
            except UnicodeEncodeError:
                # Blah blah fishcakes. Somehow got into a situation where, like, if there are multi-byte
                # unicode code points in the lyrics, we get each byte encoded in utf-8, rather than the 
                # whole thing. TODO: should probably file a bug on... someone
                lyrics = unicode_unfuck(lyrics)
                f.write(lyrics)
        i += 1
        if i >= lim:
            break
        if i % 10 == 0:
            print '.',
    if i >= lim:
        break

print "Failed to find {} songs: {}".format(len(skipped), skipped)
