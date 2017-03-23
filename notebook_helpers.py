from __future__ import division
import pandas as pd

import common

def get_frame(having_lyrics=False):
    om = common.get_omnisong()
    om['ratio'] = om['raw'] / om['comp']
    om['date'] = pd.to_datetime(om['date'])
    om['year'] = om['date'].apply(lambda d: d.year)
    om['yearf'] = om['date'].apply(lambda d: d.year + d.month*(12/365) + d.day/365)
    if having_lyrics:
        om = om[(om['raw'] > 2) & om['scraped']].copy()
    return om

def get_lyrics_frame():
    return get_frame(True)
