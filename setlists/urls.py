from django.urls import path
from . import views
from setlists.views import ShowsByYearView

urlpatterns = [


    #Home Landing Page
    path('', views.home, name='home'),
    #Setlists by year
    path('setlists/<int:year>/', ShowsByYearView.as_view(), name='setlists by year'),
    #single setlist
    path('setlist/<int:show_id>', views.show, name='setlist'),
    #Songs List Landing Page
    path('songs/', views.songs, name='songs play count'),
    #Specific Song Page
    path('songs/<int:song_id>', views.song, name='song details'),
    #Stats Landing Page
    path('stats/', views.stats, name='stats'),
    #about section landing page
    path('about/', views.about, name='about'),

    path('myshows/', views.my_shows, name='my shows')
]