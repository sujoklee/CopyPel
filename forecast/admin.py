from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

import models


class CustomUserProfileInline(admin.StackedInline):
    model = models.CustomUserProfile
    verbose_name = 'forecast user'
    verbose_name_plural = 'forecast users'


class UserAdmin(UserAdmin):
    inlines = (CustomUserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models.Forecast)
admin.site.register(models.ForecastVotes)
