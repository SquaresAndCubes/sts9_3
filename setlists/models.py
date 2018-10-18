from django.db import models
from django.db.models import Count, Min, Max, Window
from django.db.models.functions.window import Rank
from django.db.models.functions import TruncDate


class Artist(models.Model):

    name = models.CharField(max_length=64, default='STS9', null=False)

    def __str__(self):
        return '{}'.format(self.name)

class Venue(models.Model):

    name = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=False)
    state = models.CharField(max_length=4, null=True, blank=True)
    country = models.CharField(max_length=4, null=False)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.name, self.city, self.state, self.country)

class Tour(models.Model):

    name = models.CharField(max_length=64)

class ShowFilters(models.Manager):

    def by_year(self, year):
        # return only shows of the specified year
        return self.filter(date__year=year)

    def years_list(self):
        # get list of unique years
        return self.dates('date', 'year', order='DESC')

    def show(self, show_id):
        # return one show
        return self.get(id=show_id)

    def song_appearances(self, song_id):

        #create list for filtered queryset
        show_list = []
        show_ranks = []
        prev_rank = 0
        #sort shows by date, loop through, annotate rank
        for show in self.annotate(rank=Window(order_by=TruncDate('date'), expression=Rank())):

            #filter queryset from above looking for song_id occurances in all sets of show
            if show.showsong_set.filter(song_id=song_id).exists():

                #build show dictionary includes calculation for show gap
                show_with_gap = {
                    'show_id': show.id,
                    'date': show.date,
                    'venue': show.venue.name,
                    'city': show.venue.city,
                    'state': show.venue.state,
                    'country': show.venue.country,
                    'show_gap': show.rank - prev_rank,
                }

                show_ranks.append(show.rank)

                #save previous rank for future iteration calculations of show gap
                prev_rank = show.rank

                #append filtered shows to list
                show_list.append(show_with_gap)

        #calc avg performance gap round to 2 decimal places
        avg_gap = float("{0:.2f}".format((max(show_ranks) - min(show_ranks)) / (len(show_ranks) - 0.9999999999)))

        #return the song name and the show_list
        return Song.objects.get(id=song_id).name, avg_gap, show_list


class Show(models.Model):

    #Belongs to Venue
    venue = models.ForeignKey(Venue, null=True, on_delete=models.PROTECT)

    #Belongs to Tour
    tour = models.ForeignKey(Tour, null=True, on_delete=models.PROTECT, blank=True)

    #Used for Import
    show_key = models.CharField(max_length=7, null=False, blank=True)

    date = models.DateField()

    #show filter class sticky custom mm
    manager = ShowFilters()

    #default model manager
    objects = models.Manager()

    def __str__(self):
        return '{} - {}'.format(self.date, self.venue)

class SongsLists(models.Manager):

    def all_songs_play_count(self):
        #returns all songs ordered by play count
        return self.annotate(play_count=Count('showsong__show__id', distinct = True),
                             #gets the date song was first played
                             first_played=Min('showsong__show__date'),
                             #gets most recent date played
                             last_played=Max('showsong__show__date'),
                             ).order_by('play_count').reverse()

    def song(self, song_id):
        #returns song name and all shows played ordered by date
        return self.get(id=song_id).name, self.get(id=song_id).showsong_set.distinct('show__date').order_by('show__date').reverse()

class Song(models.Model):

    name = models.CharField(max_length=128, null=False)

    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)

    #model manager sticky
    data = SongsLists()

    #default model manager
    objects = models.Manager()

    def __str__(self):
        return '{} - {}'.format(self.artist, self.name)


class ShowSong(models.Model):

    SET1 = 'S1'
    SET2 = 'S2'
    SET3 = 'S3'
    ENCORE = 'E1'
    ENCORE2 = 'E2'
    AXE = 'AX'
    PA = 'PA'
    WS1 = 'W1'
    WS2 = 'W2'

    SET_CHOICES = (
        (SET1, 'Set 1'),
        (SET2, 'Set 2'),
        (SET3, 'Set 3'),
        (ENCORE, 'Encore'),
        (ENCORE2, 'Encore 2'),
        (AXE, 'Axe The Cables'),
        (PA, 'PA Set'),
        (WS1, 'Wave Spell 1'),
        (WS2, 'Wave Spell 2')
    )

    # unique properties
    set = models.CharField(
        max_length=2,
        choices=SET_CHOICES,
        default=SET1,
        null=False,
    )


    #Belongs to Show through a Set
    show = models.ForeignKey(Show, on_delete=models.CASCADE)


    #Is a Song
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)

    #Unique Values for particular show
    track = models.IntegerField(null=False)
    segue = models.CharField(max_length=1, null=True, blank=True)
    notes = models.CharField(max_length=128, null=True, blank=True)
    guest = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        ordering = ['track']

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.show, self.set, self.track, self.song)


