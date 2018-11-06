from django.views.generic.dates import YearArchiveView
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic

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
        'date__week_day': weekday,
        'venue_id': venue,
        'venue__city': city,
        'venue__state': state,
        'venue__country': country,

    }

    #remove none types
    stat_filters = {k: v for k, v in stat_filters.items() if v}

    #build queryset based on parameters
    show_list = Show.objects.filter(**stat_filters).order_by('-date')

    context = {

        'show_list': show_list,

    }

    return render(request, 'stats/index.html', context)


#display shows by year
class ShowsByYearView(YearArchiveView):

    template_name = 'setlists/index.html'

    queryset = Show.objects.all()
    #date field from Show model
    date_field = 'date'
    make_object_list = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super(ShowsByYearView, self).get_context_data(**kwargs)
        #passes distinct years to template via context
        context['years_available'] = self.queryset.dates(self.date_field, 'year')
        return context

    context_object_name = 'shows'

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