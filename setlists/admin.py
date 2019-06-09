from django.contrib import admin
from setlists.models import *


# adds ordering to admin Show class
class ShowAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    list_per_page = 2000

# Register your models here.


admin.site.register(Song)
admin.site.register(ShowSong)
# add ShowAdmin class for ordering
admin.site.register(Show, ShowAdmin)
admin.site.register(Artist)
admin.site.register(Tour)
admin.site.register(Venue)
admin.site.register(Album)
admin.site.register(UserProfile)
