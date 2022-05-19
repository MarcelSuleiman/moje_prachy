from django.contrib import admin

# Register your models here.

from .models import Venue
from .models import MyClubUser
from .models import Event
from .models import Items, Category, ReceiptsIds, SubCategory_01

#admin.site.register(Venue)
admin.site.register(MyClubUser)
admin.site.register(Event)
admin.site.register(Items)
admin.site.register(Category)
admin.site.register(ReceiptsIds)
admin.site.register(SubCategory_01)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'phone')
	ordering = ('name',)
	#ordering = ('-name',) # reverse
	search_fields = ('name', 'address')