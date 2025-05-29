from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Help)
admin.site.register(HelpReply)
admin.site.register(Ride)
admin.site.register(Drive)
admin.site.register(RideBook)