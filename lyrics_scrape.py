import pickle
import time
import os

import Lyrics

PICKLE_NAME = 'hot-100.pickle'
LYRICS_DIR = 'lyrics'
SLEEPYTIME = 1
EXT = '.txt'

def song_key(song):
    k = song.artist[:15] + '-' + song.title[:20]
    k = k.replace('/', '')
    return k.replace(' ', '_')

def unicode_unfuck(s):
    return ''.join(map(lambda c: chr(ord(c)), s))

def load_extant(d):
    keys = set()
    for fname in os.listdir(d):
        if fname.endswith(EXT):
            keys.add(fname[:-len(EXT)])
    return keys

with open(PICKLE_NAME) as f:
    db = pickle.load(f)

i = 0
lim = float('inf')
# nvm. probably better just to use os.path.exists each time. we need to sleep
# between requests anyways, so who cares if it's slower
#extant = load_extant(LYRICS_DIR)
malencoded = 0
with open('song_404s.txt', 'w') as skips_file:
    for artist in db:
        for song in db[artist].itervalues():
            k = song_key(song)
            #if k in extant:
            #    continue
            path = os.path.join(LYRICS_DIR, k + EXT)
            if os.path.exists(path):
                continue
            try:
                time.sleep(SLEEPYTIME)
                lyrics, url = Lyrics.get_lyrics2(song)
            except Lyrics.LyricsNotFoundException:
                print "Failed to find lyrics for {} ({})".format(song, url)
                try:
                    skips_file.write('\t'.join([song.artist, song.title, k]) + '\n')
                except UnicodeEncodeError:
                    malencoded += 1
                    continue

                #skipped.add( (song.artist, song.title) )
                continue
            if len(lyrics) == 0:
                print "WARNING: Got length 0 lyrics for {} ({})".format(song, url)
                skips_file.write('\t' + '\t'.join([song.artist, song.title, k]) + '\n')
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
            if i % 100 == 0:
                print '.',
        if i >= lim:
            break

print "Skipped {} malencoded songs".format(malencoded)
