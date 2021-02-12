from django.contrib import admin
from .models import Profile,BetSlip,Game

class BetSlipAdmin(admin.ModelAdmin):
    list_display = [
        'profile',
        'accepted',
        'status'
    ]

admin.site.register(Profile)
admin.site.register(BetSlip,BetSlipAdmin)
admin.site.register(Game)

