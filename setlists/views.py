from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):

    context = {

    }

    return render(request, 'home/index.html', context)

def stats(request):

    context = {

    }

    return render(request, 'stats/index.html', context)

#all shows by year
def shows(request, year=None):

    #gets a list of all years that shows were played for years nav bar
    years_list = Show.manager.years_list()

    #grabs most recent year object and pulls year
    latest_year = years_list[0].year

    #if no year is given in url sets year to most recent
    if year == None:
        year = latest_year


    shows = Show.manager.by_year(year).order_by('date')

    #set footnote variable

    #counts num of shows in the year
    show_count = shows.count()

    context = {
        'shows': shows,
        'year': year,
        'show_count': show_count,
        'years_list': years_list,
    }
    return render(request, 'setlists/index.html', context)

#page for one show view
def show(request, show_id):

    #get show by slug url
    show = Show.manager.show(show_id)

    context = {
        'show': show,
    }
    return render(request, 'setlists/show.html', context)

#view to list all songs and how many times played
def songs(request):

    #gets an annotated set of song | playcount
    songs = Song.data.all_songs_play_count()

    song_count = songs.count()

    context = {
        'songs': songs,
        'song_count': song_count,
    }
    return render(request, 'songs/index.html', context)

#lists all shows where a song was played
def song(request, song_id):

    song_name, avg_gap, show_list = Show.manager.song_appearances(song_id)

    context = {
        'song_name': song_name,
        'show_list': show_list,
        'show_count': len(show_list),
        'avg_gap': avg_gap,
        }

    return render(request, 'songs/song.html', context)