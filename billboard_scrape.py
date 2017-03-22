import billboard
import time
import pickle
import datetime

chartname = 'hot-100'
DATE_FMT = '%Y-%m-%d'
SLEEPYTIME = 1

class SongDB(object):
    def __init__(self, path):
        self.path = path
        try:
            f = open(path)
            self.db = pickle.load(f)
        except IOError:
            self.db = {}

    def add_song(self, song, date):
        if song.artist not in self.db:
            self.db[song.artist] = {}

        artist_songs = self.db[song.artist]
        if song.title in artist_songs:
            extant = artist_songs[song.title]
            # Not strictly necessary if we're guaranteed to always
            # iterate in reverse chrono order, but doesn't hurt to
            # be safe.
            extant.weeks = max(extant.weeks, song.weeks)
            extant.peakPos = min(extant.peakPos, song.peakPos)
            extant.earliest = min(extant.earliest, date)
        else:
            song.earliest = date
            artist_songs[song.title] = song

    def save(self):
        with open(self.path, 'w') as f:
            pickle.dump(self.db, f)

    def size(self):
        n = 0
        for artist_songs in self.db.itervalues():
            n += len(artist_songs)
        return n



path = chartname + '.pickle'
chartpicklename = chartname + '-chartdata.pickle'
try:
    with open(chartpicklename) as f:
        charts = pickle.load(f)
        date = charts[-1].previousDate
except IOError:
    charts = []
    date = None

db = SongDB(path)
i = 0
lim = float('inf')
# TODO: load pickled charts
try:
    while 1:
        chart = billboard.ChartData(chartname, date)
        dt = datetime.datetime.strptime(chart.date, DATE_FMT).date()

        for song in chart:
            db.add_song(song, dt)
        charts.append(chart)
        time.sleep(SLEEPYTIME)

        i += 1
        if not chart.previousDate or i >= lim:
            break
        if (i % 26) == 0:
            print date
        date = chart.previousDate
except: # gotta catchemall
    if i == 0:
        raise
    print "Uh oh. Got unexpected exception. Saving whatever we've accumulated before bailing"
    db.save()
    with open(chartpicklename, 'w') as f:
        pickle.dump(charts, f)
    raise


db.save()
print "Saved db with {} songs to {}".format(db.size(), path)
with open(chartpicklename, 'w') as f:
    pickle.dump(charts, f)

