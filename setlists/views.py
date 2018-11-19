from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from django.db.models import OuterRef, Exists, Subquery
from django.views.generic import YearArchiveView
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractYear



def home(request):
    context = {

    }

    return render(request, 'home/index.html', context)


def about(request):
    context = {

    }

    return render(request, 'about/index.html', context)


def stats_view(request, mystats=False):
    # set song var from URL
    song_name = request.GET.get('song')

    # build list of kwargs from url to get queryset
    stat_filters = {

        'date__year__in': request.GET.getlist('year'),
        'date__month__in': request.GET.getlist('month'),
        'date__day__in': request.GET.getlist('day'),
        'date__week_day__iexact__in': request.GET.getlist('weekday'),
        'venue_id__in': request.GET.getlist('venue'),
        'venue__city__iexact__in': request.GET.getlist('city'),
        'venue__state__iexact__in': request.GET.getlist('state'),
        'venue__country__iexact__in': request.GET.getlist('country'),

    }

    # only pass kwargs with values
    stat_filters = {k: v for k, v in stat_filters.items() if v}

    # only search for songs if there is a song input from url
    if song_name:

        # outeref for subquery to pass to next script to see if
        # song exists in show
        showsongs = ShowSong.objects.filter(show=OuterRef('pk'),
                                            song__name__iexact=song_name)

        # build queryset based on parameters
        shows = Show.objects.annotate(song_exists=Exists(showsongs)).filter(
            **stat_filters, song_exists=True)

    else:
        # if no song input from url just build queryset on everything else
        shows = Show.objects.filter(**stat_filters)

    # returns how many distinct songs were played within the queryset
    song_count = shows.aggregate(
        song_count=Count('showsong__song_id', distinct=True))

    #originals covers played count non unique
    originals_played_count = ShowSong.objects.filter(song__artist__name='STS9',
                                        show__in=shows).count()

    covers_played_count = ShowSong.objects.filter(show__in=shows).exclude(
        song__artist__name='STS9').count()

    # number of shows per weekday within queryset
    weekdays_distribution = \
        shows.annotate(
            weekday=ExtractWeekDay('date__week_day')) \
            .values('weekday').annotate(count=Count('id')).values('weekday',
                                                                  'count')

    # number of shows per month within queryset
    months_distribution = \
        shows.annotate(month=ExtractMonth('date__month')) \
            .values('month').annotate(count=Count('id')).values('month', 'count')

    # number of shows per year within queryset
    years_distribution = \
        shows.annotate(year=ExtractYear('date__year')).values(
            'year').annotate(count=Count('id')).values('year', 'count')

    geo_distribution = \
        shows.values('venue__state').annotate(count=Count('id')).values(
            'venue__state', 'count')


    context = {

        'get_request_stats': request.GET.items(),
        'shows': shows.order_by('-date'),
        'song_count': song_count,
        'originals_played_count': originals_played_count,
        'others_played_count': covers_played_count,
        'weekdays_distribution': weekdays_distribution,
        'months_distribution': months_distribution,
        'years_distribution': years_distribution,
        'geo_distribution': geo_distribution,
    }

    return render(request, 'stats/index.html', context)


# display shows by year inheriting YearArchiveView
class ShowsByYearView(YearArchiveView):
    template_name = 'setlists/index.html'

    queryset = Show.objects.all()

    # date field from Show model
    date_field = 'date'
    make_object_list = True
    allow_future = True
    context_object_name = 'shows'


    def get_ordering(self):

        ordering = self.request.GET.get('ordering', '-date')

        return ordering


    # override the get_year function to default to the latest year
    # if none provided
    def get_year(self):

        year = self.year
        if year is None:
            try:
                year = self.kwargs['year']
            except KeyError:
                try:
                    year = self.request.GET['year']
                except KeyError:
                    year = \
                        self.queryset.dates(self.date_field, 'year',
                                            order='DESC')[0].year
        return year

    def get_context_data(self, **kwargs):
        context = super(ShowsByYearView, self).get_context_data(**kwargs)
        # passes distinct years to template via context
        context['years_available'] = self.queryset.dates(self.date_field,
                                                         'year')
        #Pass the ordering to the template so that the button state can be set
        context['ordering'] = self.get_ordering()

        return context


# page for one show view
def show(request, show_id):
    # get show by slug url
    show = Show.manager.show(show_id)

    context = {
        'show': show,
    }
    return render(request, 'setlists/show.html', context)


@login_required(login_url='login')
@atomic
def my_shows(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST,
                                            instance=request.user.userprofile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('home')
    else:
        user_profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'user/myshows.html',
                  {'user_profile_form': user_profile_form})


# view to list all songs and how many times played
def songs(request):
    # gets an annotated set of song | playcount
    songs = Song.data.all_songs_play_count()

    song_count = songs.count()

    originals_count = Song.objects.filter(artist__name='STS9').count()

    covers_count = Song.objects.filter().exclude(artist__name='STS9').count()

    context = {
        'songs': songs,
        'song_count': song_count,
        'originals_count': originals_count,
        'covers_count': covers_count,
    }
    return render(request, 'songs/index.html', context)


# lists all shows where a song was played
def song(request, song_id):

    song_name, avg_gap, show_list = Show.manager.song_appearances(song_id)

    context = {
        'song_name': song_name,
        'show_list': show_list,
        'show_count': len(show_list),
        'avg_gap': avg_gap,
    }

    return render(request, 'songs/song.html', context)


# view for users to signup to the site
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
