from django.urls import path
from . import views



urlpatterns = [

    # Home Landing Page
    path('', views.home, name='home'),

    # Setlists landing page most recent year
    path('setlists/', views.ShowsByYearView.as_view(), name='setlists landing'),
    # setlists by year from URL
    path('setlists/<int:year>/', views.ShowsByYearView.as_view(),
         name='setlists by year'),
    # single setlist
    path('setlist/<int:show_id>', views.show, name='setlist'),
    # Songs List Landing Page
    path('songs/', views.songs, name='songs play count'),
    # Specific Song Page
    path('songs/<int:song_id>', views.song, name='song details'),
    # Stats Results page
    path('stats/', views.stats_view, name='stats'),
    path('mystats/', views.my_stats, name='my stats'),
    # about section landing page
    path('about/', views.about, name='about'),
    # view of users shows
    path('myshows/', views.my_shows, name='my shows'),
    #all venues list
    path('venues/', views.venues, name='venues'),
    #single venue list
    path('venue/<int:venue_id>', views.venue, name='venue'),



]


