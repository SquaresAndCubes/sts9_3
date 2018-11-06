from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from django.db.models import OuterRef, Exists


def home(request):

    context = {

    }

    return render(request, 'home/index.html', context)

def about(request):

    context = {

    }

    return render(request, 'about/index.html', context)

def stats(request):

    #get parameters from url for query

    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    weekday = request.GET.get('weekday')
    venue = request.GET.get('venue')
    song = request.GET.get('song')
    city = request.GET.get('city')
    state = request.GET.get('state')
    country = request.GET.get('country')



    #build dict to pass into Show.objects.filter()
    stat_filters = {

        'date__year': year,
        'date__month': month,
        'date__day': day,
        'date__week_day__iexact': weekday,
        'venue_id': venue,
        'venue__city__iexact': city,
        'venue__state__iexact': state,
        'venue__country__iexact': country,

    }

    #remove none types
    stat_filters = {k: v for k, v in stat_filters.items() if v}


    #only search for songs if there is a song input from url
    if song:

        #outeref for subquery to pass to next script to see if song exists in show
        showsongs = ShowSong.objects.filter(show=OuterRef('pk'),song__name__iexact=song)

        #build queryset based on parameters
        show_list = Show.objects.annotate(song_exists=Exists(showsongs)).filter(**stat_filters, song_exists=True).order_by('-date')

    else:
        #if there is no song input from url just build queryset on everything else
        show_list = Show.objects.filter(**stat_filters).order_by('-date')

    context = {

        'show_list': show_list,

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

    order = request.GET.get('order', 'asc')

    shows = Show.manager.by_year(year)

    if(order == 'desc'):
        shows = shows.order_by('-date')

    elif(order == 'asc'):
        shows = shows.order_by('date')


    #set footnote variable

    #counts num of shows in the year
    show_count = shows.count()

    context = {
        'shows': shows,
        'year': year,
        'show_count': show_count,
        'years_list': years_list,
        'order': order,
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

@login_required(login_url='login')
@atomic
def my_shows(request):

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('home')
    else:
        user_profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'user/myshows.html', {'user_profile_form': user_profile_form})


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

#view for users to signup to the site
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})