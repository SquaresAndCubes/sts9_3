import csv
import datetime
from setlists import models


def import_artists():
    data_filepath = 'songs.csv'
    results = {"created": 0, "skipped": 0}
    with open(data_filepath, "r", encoding='utf8') as f:
        reader = csv.reader(f)
        # skip header
        next(reader, None)
        for row in reader:

            artist = row[7]

            if artist == 'NULL':
                artist = 'STS9'

            new_artist, created = models.Artist.objects.get_or_create(
                name=artist)

            if created:
                results['created'] += 1
            else:
                results['skipped'] += 1

        print("Finished - Created {} Artists, Duplicates: {}".format(
            results["created"], results["skipped"]))


def import_venues():
    data_filepath = "shows.csv"
    results = {"created": 0, "skipped": 0}
    with open(data_filepath, "r", encoding='utf8') as f:
        reader = csv.reader(f)
        # skip header
        next(reader, None)
        for row in reader:

            for i in range(len(row)):
                if row[i] == 'NULL':
                    row[i] = None
            # get_or_create returns 2 things, the first thing is the object we wanted, and the second thing
            # is a true / false value that lets us know if the object was newly created or if was already there
            new_obj, created = models.Venue.objects.get_or_create(name=row[2], city=row[3], state=row[4],
                                                                  country=row[5])

            # this is just being done for our print statement at the end, to let us know how many things were imported
            if created:
                results["created"] += 1
            else:
                results["skipped"] += 1

    print("Finished - Created {} Venues, Duplicates: {}".format(results["created"], results["skipped"]))


def import_songs():
    data_filepath = 'songs.csv'
    results = {"created": 0, "skipped": 0}
    with open(data_filepath, "r", encoding='utf8') as f:
        reader = csv.reader(f)
        # skip header
        next(reader, None)
        for row in reader:

            in_artist = row[7]

            if in_artist == 'NULL':
                in_artist = 'STS9'

            artist = models.Artist.objects.get(name=in_artist)

            new_song, created = models.Song.objects.get_or_create(name=row[2],
                                                                  artist=artist)

            if created:
                results['created'] += 1
            else:
                results['skipped'] += 1

        print("Finished - Created {} Songs, Duplicates: {}".format(
            results["created"], results["skipped"]))


def import_shows():
    # path to our csv file
    data_filepath = "shows.csv"
    results = {"created": 0, "skipped": 0}
    with open(data_filepath, "r", encoding='utf8') as f:
        reader = csv.reader(f)
        # skip header
        next(reader, None)
        for row in reader:

            for i in range(len(row)):
                if row[i] == 'NULL':
                    row[i] = None
            # by asking for a venue by the name, city, state and country, we ensure that we are getting the correct venue
            venue = models.Venue.objects.get(name=row[2], city=row[3],
                                             state=row[4], country=row[5])

            show_date = datetime.datetime.strptime(row[1], '%Y-%m-%d')

            # the new show needs to be saved after we create it
            new_show = models.Show(show_key=row[0], date=show_date, venue=venue)

            # thats done here
            new_show.save()

            # done for our print statement at the end
            results["created"] += 1
    print("Finished - Created {} Shows".format(results["created"]))


def import_showsong():
    data_filepath = 'songs.csv'
    results = {"created": 0, "skipped": 0}
    with open(data_filepath, "r", encoding='utf8') as f:
        reader = csv.reader(f)
        # skip header
        next(reader, None)
        for row in reader:

            song = models.Song.objects.get(name=row[2])

            in_name = row[3]

            new_name = None

            if in_name == 'Set 1':
                new_name = models.ShowSong.SET1
            elif in_name == 'Set 2':
                new_name = models.ShowSong.SET2
            elif in_name == 'Set 3':
                new_name = models.ShowSong.SET3
            elif in_name == 'Encore':
                new_name = models.ShowSong.ENCORE
            elif in_name == 'Encore 2':
                new_name = models.ShowSong.ENCORE2
            elif in_name == 'Axe the Cables':
                new_name = models.ShowSong.AXE
            elif in_name == 'PA Set':
                new_name = models.ShowSong.PA

            for i in range(len(row)):
                if row[i] == 'NULL':
                    row[i] = None

            show = models.Show.objects.get(show_key=row[1])

            new_showsong = models.ShowSong(show=show, song=song, set=new_name,
                                           track=row[4], segue=row[5],
                                           notes=row[6], guest=row[8])

            new_showsong.save()

            results["created"] += 1
    print("Finished - Created {} Performances".format(results["created"]))


def import_all():
    import_artists()
    import_venues()
    import_songs()
    import_shows()
    import_showsong()
