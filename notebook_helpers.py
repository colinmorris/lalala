from __future__ import division
import pandas as pd
import math

import common

BIAS_ADJUSTED_RATIO = 1
#BIAS = 34.775287769
# 10 for the header, 8 for the footer, 1 for the block prefix (really 3 bits, but I'm rounding up)
BIAS = 10 + 8 + 1
BASE = 2

def get_frame(having_lyrics=False):
    om = common.get_omnisong()
    # Set this in both cases just for flexibility if I wanna turn adjustment on and off
    om['raw_ratio'] = om['raw'] / om['comp']
    if BIAS_ADJUSTED_RATIO:
        om['unbiased_ratio'] = om['raw'] / (om['comp']-BIAS)
    else:
        om['unbiased_ratio'] = om['raw'] / om['comp']
    om['year'] = om['date'].apply(lambda d: d.year)
    om['yearf'] = om['date'].apply(lambda d: d.year + d.month/12 + d.day/365)
    # Ratio = the one calculated using infgen (set in god_frame.py)
    om['rscore'] = om['ratio'].apply(lambda x: math.log(x, BASE))
    if having_lyrics:
        om = om[(om['raw'] > 2) & om['scraped']].copy()
    return om

def get_lyrics_frame():
    return get_frame(True)
