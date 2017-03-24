# TODO: if you rerun this later, make sure you check against filenames in "bad_lyrics" dir,
# to avoid scraping them twice 
import pickle
import time
import os
import re

import common
import Lyrics

PICKLE_NAME = 'hot-100.pickle'
LYRICS_DIR = 'lyrics'
SLEEPYTIME = 1
EXT = '.txt'

def unicode_unfuck(s):
    return ''.join(map(lambda c: chr(ord(c)), s))

def load_extant(d):
    keys = set()
    for fname in os.listdir(d):
        if fname.endswith(EXT):
            keys.add(fname[:-len(EXT)])
    return keys

class FakeSong(object):
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title

    def __str__(self):
        return '{} - {}'.format(self.artist, self.title)

artists_renamed = {
        'Beyonce': 'Beyonce Knowles',
        'Janet': 'Janet Jackson',
        'India.Arie': 'India Arie',
        'James Brown And The Famous Flames': 'James Brown',
        "Go-Go's": "The Gogos",
}
andy_artists = [
    'Peter And Gordon', 'Blood, Sweat & Tears', 'Captain & Tennille',
    'Crosby, Stills & Nash',
]

for andy in andy_artists:
    canon = andy.replace(' & ', ' ')
    canon = canon.replace(' And ', ' ')
    artists_renamed[andy] = canon

def transformed_songs(song):
    trans = []
    cp = lambda: FakeSong(song.artist, song.title)
    artist = song.artist
    title = song.title
    if '#' in artist or '#' in title:
        yield song
    if artist.startswith('The '):
        s = cp()
        s.artist = artist[len('The '):]
        yield s
    if artist.startswith('Gladys Knight '):
        s = cp()
        s.artist = 'Gladys Knight'
        yield s
    if artist == 'Earth, Wind & Fire':
        s = cp()
        s.artist = 'Earth Wind Fire'
        yield s
    if artist == 'Big & Rich':
        s = cp()
        s.artist = 'Big Rich'
        yield s
    if artist == 'Peaches & Herb':
        s = cp()
        s.artist = 'Peaches Herb'
        yield s
    if artist == 'Maroon5':
        s = cp()
        s.artist = 'Maroon 5'
        yield s
    if 'B****' in title:
        s = cp()
        s.title = title.replace('B****', 'Bitch')
        yield s
    if artist in artists_renamed:
        s = cp()
        s.artist = artists_renamed[artist]
        yield s
        
    # cause it has no parens. yuk yuk.
    orphaned = re.sub('\(.*\)', '', title)
    if orphaned != title:
        s = cp()
        s.title = orphaned
        yield s
    if artist.endswith(' s'):
        s = cp()
        s.artist = artist[:-2]+'s'
        yield s

with open(PICKLE_NAME) as f:
    db = pickle.load(f)

# nvm. probably better just to use os.path.exists each time. we need to sleep
# between requests anyways, so who cares if it's slower
#extant = load_extant(LYRICS_DIR)
malencoded = 0
with open('song_404s.txt') as to_retry:
    bad_keys = set([line.split('\t')[-1].strip() for line in to_retry])

with open('still_404s.txt', 'w') as skips_file:
    for artist in db:
        for orig_song in db[artist].itervalues():
            k = common.song_key(orig_song)
            if k not in bad_keys:
                continue
            path = os.path.join(LYRICS_DIR, k + EXT)
            found = False
            for song in transformed_songs(orig_song):
                #print "Transformed {} to {}".format(orig_song, song)
                try:
                    lyrics, url = Lyrics.get_lyrics2(song)
                    time.sleep(SLEEPYTIME)
                except Lyrics.LyricsNotFoundException:
                    time.sleep(SLEEPYTIME)
                    continue
                if len(lyrics) < 5:
                    continue
                else:
                    found = True
                    break
            if not found:
                try:
                    skips_file.write('\t'.join([orig_song.artist, orig_song.title, k]) + '\n')
                except UnicodeEncodeError:
                    malencoded += 1
            else:
                print "Success! {}".format(orig_song)
                with open(path, 'w') as f:
                    try:
                        f.write(lyrics)
                    except UnicodeEncodeError:
                        # Blah blah fishcakes. Somehow got into a situation where, like, if there are multi-byte
                        # unicode code points in the lyrics, we get each byte encoded in utf-8, rather than the 
                        # whole thing. TODO: should probably file a bug on... someone
                        lyrics = unicode_unfuck(lyrics)
                        f.write(lyrics)

print "Skipped {} malencoded songs".format(malencoded)
