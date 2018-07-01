from django.db import models


class Artist(models.Model):

    name = models.CharField(max_length=64, default='STS9', null=False)

    def __str__(self):
        return '{}'.format(self.name)

class Venue(models.Model):

    name = models.CharField(max_length=64, null=True)
    city = models.CharField(max_length=64, null=False)
    state = models.CharField(max_length=4, null=True)
    country = models.CharField(max_length=4, null=False)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.name, self.city, self.state, self.country)

class Song(models.Model):

    name = models.CharField(max_length=128, null=False)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)

    def __str__(self):
        return '{} - {}'.format(self.name, self.artist)

class Tour(models.Model):

    name = models.CharField(max_length=64)

class Show(models.Model):

    #Belongs to Venue
    venue = models.ForeignKey(Venue, null=True, on_delete=models.PROTECT)

    #Belongs to Tour
    tour = models.ForeignKey(Tour, null=True, on_delete=models.PROTECT)

    #Used for Import
    show_key = models.CharField(max_length=7, null=False)


    date = models.DateField()

    def __str__(self):
        return '{} - {}'.format(self.date, self.venue)

class Set(models.Model):

    # SET choices to reduce entry errors

    SET1 = 'S1'
    SET2 = 'S2'
    SET3 = 'S3'
    ENCORE = 'E1'
    ENCORE2 = 'E2'
    AXE = 'AX'
    PA = 'PA'

    SET_CHOICES = (
        (SET1, 'Set 1'),
        (SET2, 'Set 2'),
        (SET3, 'Set 3'),
        (ENCORE, 'Encore'),
        (ENCORE2, 'Encore 2'),
        (AXE, 'Axe The Cables'),
        (PA, 'PA Set')
    )

    # unique properties
    name = models.CharField(
        max_length=2,
        choices=SET_CHOICES,
        default=SET1,
        null=False,
    )

    #Belongs to Show
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    #Set Position in Show
    set_pos = models.IntegerField()

    def __str__(self):
        return '{} - {}'.format(self.show, self.name)

class ShowSong(models.Model):

    #Belongs to Show through a Set
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    set = models.ForeignKey(Set, on_delete=models.CASCADE)

    #Is a Song
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)

    #Unique Values for particular show
    track = models.IntegerField()
    segue = models.CharField(max_length=4, null=True)
    notes = models.CharField(max_length=128, null=True)
    guest = models.CharField(max_length=64, null=True)

    def __str__(self):
        return '{} - {}'.format(self.show, self.song)


