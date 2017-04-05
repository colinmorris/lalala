from __future__ import division
import pandas as pd
import os
import re

import common

# this title should be a saint
def canonize_title(title):
    trans = title
    trans = re.sub('\s+', ' ', title)
    clitics = ['ll', 's', 't']
    for clitic in clitics:
        trans = trans.replace(' '+clitic, "'"+clitic)
    return trans

db = common.get_songdb()
rows = []
merged = 0
for artist_discog in db.itervalues():
    title_to_row = {}
    for title, song in artist_discog.iteritems():
        try:
            raw, comp = common.get_sizes(song)
            scraped = True
            inf_raw, inf_comp = common.get_inf_ratio(song)
            ratio = inf_raw / inf_comp
            assert raw == inf_raw, "{} != {}".format(raw, inf_raw)
        except common.NotScrapedException:
            raw = comp = None
            scraped = False
            ir = None
        canon_title = canonize_title(title)
        if canon_title not in title_to_row:
            row = dict(artist=song.artist, title=canon_title, date=song.earliest,
                peak=song.peakPos, scraped=scraped, 
                raw=raw, comp=comp, icomp=inf_comp, ratio=ratio,
            )
            title_to_row[canon_title] = row
        # Got a dupe. Merge them.
        else:
            merged += 1
            extant = title_to_row[canon_title]
            extant['peak'] = min(extant['peak'], song.peakPos)
            extant['scraped'] = extant['scraped'] or scraped
            extant['date'] = min(extant['date'], song.earliest)

    rows.extend(title_to_row.values())

print "Merged {} duplicate rows".format(merged)

df = pd.DataFrame(rows)
df['date'] = pd.to_datetime(df['date'])
# Blargh. Can't do this with nullable col. http://stackoverflow.com/a/21290084/262271
#df['raw'] = df['raw'].astype(int)
#df['comp'] = df['comp'].astype(int)
print "Saving god frame with shape {}".format(df.shape)
df.to_pickle(common.OMNI_PICKLE_NAME)
