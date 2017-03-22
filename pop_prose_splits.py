import common
import pickle
import os

N_SONGS = 100
MIN_CHART_POS = 10
PROSE_SOURCES = ['poynton', 'comments', 'hansard']

def get_recent_keys(n=N_SONGS, min_pos=MIN_CHART_POS):
    charts = common.get_chartdata()
    found = set()
    for chart in charts:
        for song in chart[:min_pos]:
            k = common.song_key(song)
            if k in found:
                continue
            if common.have_lyrics(song):
                found.add(k)
                if len(found) >= N_SONGS:
                    break

        if len(found) >= N_SONGS:
            break
    return found

if __name__ == '__main__':
    song_keys = get_recent_keys()
    print "Loaded song keys to match against"
    prosedir = 'prose'
    prosefiles = {src: open(os.path.join(prosedir, src+'.txt')) 
            for src in PROSE_SOURCES} 
    try:
        os.mkdir(os.path.join(prosedir, 'fragments'))
    except OSError:
        pass
    for prose_src in prosefiles:
        try:
            os.mkdir(os.path.join(prosedir, 'fragments', prose_src))
        except OSError:
            pass

    for i, song_key in enumerate(song_keys):
        fname = str(i)
        size = os.path.getsize(os.path.join(common.LYRICS_DIR, song_key+'.txt'))
        for prose_src, prosefile in prosefiles.iteritems():
            acc = ''
            while len(acc) < size and abs(len(acc) - size) > 5:
                acc += prosefile.readline()
            with open(os.path.join(prosedir, 'fragments', prose_src, fname), 'w') as f:
                f.write(acc)


