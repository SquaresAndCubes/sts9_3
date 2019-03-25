from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from django.db.models import OuterRef, Exists
from django.views.generic import YearArchiveView
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractYear
from django.utils.timezone import datetime


def social_login_page(request):
    context = {
        'next': request.GET.get('next')

    }

    return render(request, 'social/login.html', context)


def home(request):
    context = {
        'show': Show.objects.order_by('-date')[0],
        'today_in_history': Show.objects.order_by('-date').filter(date__day=datetime.today().day-1,
                                                                  date__month=datetime.today().month)
    }

    return render(request, 'home/index.html', context)


def about(request):
    context = {

    }

    return render(request, 'about/index.html', context)


def stats_view(request):
    # set song var from URL
    song_name = request.GET.get('song')

    # build list of kwargs from url to get queryset
    stat_filters = {

        'date__year__in': request.GET.getlist('year'),
        'date__month__in': request.GET.getlist('month'),
        'date__day__in': request.GET.getlist('day'),
        'date__week_day__in': request.GET.getlist('weekday'),
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

    # originals covers played count non unique
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
    shows_per_year = \
        shows.annotate(year=ExtractYear('date__year')).values(
            'year').annotate(count=Count('id')).values('year', 'count')

    shows_yr = Show.manager.shows_per_year()

    shows_yr = dict([tuple(d.values()) for d in shows_yr])

    shows_per_year = dict([tuple(d.values()) for d in shows_per_year])

    years_distribution = []

    # builds list of tuples for year heat map
    for year in shows_yr.keys():
        years_distribution.append(
            (year, shows_per_year.get(year, 0))
        )

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
        'years_distribution': sorted(years_distribution),
        'geo_distribution': geo_distribution,
        'stats_name': 'Statistics'
    }

    return render(request, 'stats/index.html', context)


@login_required(login_url='social login')
def my_stats(request):
    shows = UserProfile.objects.get(user=request.user).shows.all()

    # returns how many distinct songs were played within the queryset
    song_count = shows.aggregate(
        song_count=Count('showsong__song_id', distinct=True))

    # originals covers played count non unique
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
    shows_per_year = \
        shows.annotate(year=ExtractYear('date__year')).values(
            'year').annotate(count=Count('id')).values('year', 'count')

    shows_yr = Show.manager.shows_per_year()

    shows_yr = dict([tuple(d.values()) for d in shows_yr])

    shows_per_year = dict([tuple(d.values()) for d in shows_per_year])

    years_distribution = []

    # builds list of tuples for year heat map
    for year in shows_yr.keys():
        years_distribution.append(
            (year, shows_per_year.get(year, 0))
        )

    geo_distribution = \
        shows.values('venue__state').annotate(count=Count('id')).values(
            'venue__state', 'count')

    context = {

        'shows': shows.order_by('-date'),
        'song_count': song_count,
        'originals_played_count': originals_played_count,
        'others_played_count': covers_played_count,
        'weekdays_distribution': weekdays_distribution,
        'months_distribution': months_distribution,
        'years_distribution': sorted(years_distribution),
        'geo_distribution': geo_distribution,
        'stats_name': request.user.username + "'s Statistics"
    }

    return render(request, 'stats/index.html', context)

@login_required(login_url='social login')
def my_stats_top_ten(request):

    #gets all show objects for user
    shows = UserProfile.objects.get(user=request.user).shows.all()

    #returns top 10 play count for user
    top_ten_songs = shows.values('showsong__song__name').annotate(count=Count('pk', distinct=True)).order_by('-count')[:10]
    top_ten_venues = shows.values('venue__name').annotate(count=Count('pk', distinct=True)).order_by('-count')[:10]

    #build out code to count song occurances
    context = {

        'top_ten_songs': top_ten_songs,
        'top_ten_venues': top_ten_venues,
        'stats_name': request.user.username + "'s Top Ten Lists"
    }

    return render(request, 'stats/user_top_ten.html', context)

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
        # Pass the ordering to the template so that the button state can be set
        context['ordering'] = self.get_ordering()

        return context


# page for one show view
def show(request, show_id):

    # get show by slug url
    show = Show.manager.show(show_id)

    years_available = Show.manager.years_list()

    context = {
        'show': show,
        'years_available': years_available
    }
    return render(request, 'setlists/show.html', context)


@login_required(login_url='social login')
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

    # years heat calc

    # grab total shows per year for heat calc
    shows_yr = Show.manager.shows_per_year()

    # get times song way played per year for heat
    plays_yr = Show.objects.filter(
        showsong__song_id=song_id).annotate(
        year=ExtractYear('date__year')).values('year') \
        .annotate(count=Count('id', distinct=Show)).values('year', 'count')

    # convert to tuples for calc script
    shows_yr = dict([tuple(d.values()) for d in shows_yr])
    plays_yr = dict([tuple(d.values()) for d in plays_yr])

    song_year_heat = []

    # builds list of tuples for year heat map
    for year in shows_yr.keys():
        song_year_heat.append(
            (year, round((plays_yr.get(year, 0) / shows_yr[year]) * 100))
        )

    # months heat calc
    shows_month = Show.manager.shows_per_month()

    plays_month = Show.objects.filter(
        showsong__song_id=song_id).annotate(
        month=ExtractMonth('date__month')).values('month') \
        .annotate(count=Count('id', distinct=Show)).values('month', 'count')

    shows_month = dict([tuple(d.values()) for d in shows_month])
    plays_month = dict([tuple(d.values()) for d in plays_month])

    song_month_heat = []

    # builds list of tuples for year heat map
    for month in shows_month.keys():
        song_month_heat.append(
            (month, round((plays_month.get(month, 0) / shows_month[month]) * 100))
        )

    # days heat calc
    shows_weekday = Show.manager.shows_per_weekday()

    plays_weekday = Show.objects.filter(
        showsong__song_id=song_id).annotate(
        weekday=ExtractWeekDay('date__week_day')).values('weekday') \
        .annotate(count=Count('id', distinct=Show)).values('weekday', 'count')

    shows_weekday = dict([tuple(d.values()) for d in shows_weekday])
    plays_weekday = dict([tuple(d.values()) for d in plays_weekday])

    song_weekday_heat = []

    # builds list of tuples for year heat map
    for weekday in shows_weekday.keys():
        song_weekday_heat.append(
            (weekday, round((plays_weekday.get(weekday, 0) / shows_weekday[weekday]) * 100))
        )

    # geo heat calc

    shows_state = Show.manager.shows_per_state()

    print(shows_state)

    plays_state = Show.objects.filter(
        showsong__song_id=song_id).select_related('venue').values('venue__state') \
        .annotate(count=Count('id', distinct=Show)).values('venue__state', 'count')

    shows_state = dict([tuple(d.values()) for d in shows_state])
    plays_state = dict([tuple(d.values()) for d in plays_state])

    song_state_heat = []

    # builds list of tuples for year heat map
    for state in shows_state.keys():
        try:
            song_state_heat.append(
                (state, round((plays_state.get(state, 0) / shows_state[state]) * 100))
            )
        except ZeroDivisionError:
            pass

    context = {
        'song_name': song_name,
        'show_list': show_list,
        'show_count': len(show_list),
        'avg_gap': avg_gap,
        'song_year_heat': sorted(song_year_heat),
        'song_month_heat': sorted(song_month_heat),
        'song_weekday_heat': sorted(song_weekday_heat),
        'song_state_heat': sorted(song_state_heat),
    }

    return render(request, 'songs/song.html', context)
