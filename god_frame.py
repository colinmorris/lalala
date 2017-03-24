import pandas as pd
import os

import common

db = common.get_songdb()
#columns=['artist', 'title', 'date', 'peak', 'scraped', 'raw', 'comp', ]
rows = []
for artist_discog in db.itervalues():
    for song in artist_discog.itervalues():
        try:
            raw, comp = common.get_sizes(song)
            scraped = True
        except common.NotScrapedException:
            raw = comp = None
            scraped = False

        row = dict(artist=song.artist, title=song.title, date=song.earliest,
                peak=song.peakPos, scraped=scraped, raw=raw, comp=comp)
        rows.append(row)

df = pd.DataFrame(rows)
df['date'] = pd.to_datetime(df['date'])
# Blargh. Can't do this with nullable col. http://stackoverflow.com/a/21290084/262271
#df['raw'] = df['raw'].astype(int)
#df['comp'] = df['comp'].astype(int)
print "Saving god frame with shape {}".format(df.shape)
df.to_pickle(common.OMNI_PICKLE_NAME)
