import common
import os
import pandas as pd
import normalizer
import time

GENRE_FILE = 'msd_tagtraum_cd2.cls'
SAVE = True

omni = common.get_omnisong()
omni['genre'] = None

def build_trackid_to_genre():
    f = open(GENRE_FILE)
    ttg = {}
    for line in f:
        if line.startswith('#'):
            continue
        fields = line.split('\t')
        trackid = fields[0]
        # Has a majority genre and an optional "minority genre". always take the majority.
        genre = fields[1].strip()
        ttg[trackid] = genre
    f.close()
    return ttg

def song_key(title, artist, bb=False):
    if bb:
        # billboard specific transforms
        for clitic in ['s', 't', 'll']:
            title = title.replace(' {} '.format(clitic), '{} '.format(clitic))
    return tuple(map(normalizer.normalize_no_rotation, [title, artist]))


t0 = time.time()
# Build a mapping from existing title/artist pairs to index
normalized_lookup = {}
for i, (title, artist) in enumerate(omni[ ['title', 'artist'] ].values):
    k = song_key(title, artist, bb=True)
    normalized_lookup[k] = i
print "Built normalized lookup in {:.1f} seconds".format(time.time()-t0)
t0 = time.time()

ttg = build_trackid_to_genre()
print "Built genre lookup in {:.1f} seconds".format(time.time()-t0)

found = 0
with open('unique_tracks.txt') as f:
    for line in f:
        trackid, _, artist, title = line.split('<SEP>')
        try:
            genre = ttg[trackid]
        except KeyError:
            continue
        k = song_key(title.strip(), artist)
        try:
            i = normalized_lookup[k]
        except KeyError:
            continue
        omni.loc[i, 'genre'] = genre
        found +=1

print "Found {} genre labels out of {} songs".format(found, len(omni))

if SAVE:
    omni.to_pickle(common.OMNI_PICKLE_NAME)

