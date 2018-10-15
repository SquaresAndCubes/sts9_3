

#prints songs in order with set heading titles

for song in show.showsong_set.all().order_by('track'):
    if set_name == song.get_set_display():
        print(song.track, song.song.name)
    else:
        print(song.get_set_display())
        print(song.track, song.song.name)
        set_name = song.get_set_display()
