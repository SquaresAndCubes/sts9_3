from django.contrib import admin
from setlists.models import *



class ShowAdmin(admin.ModelAdmin):

    ordering = ('-date',)

# Register your models here.


admin.site.register(Song)
admin.site.register(ShowSong)
admin.site.register(Show, ShowAdmin)
admin.site.register(Artist)
admin.site.register(Tour)
admin.site.register(Venue)
admin.site.register(Album)
admin.site.register(UserProfile)
