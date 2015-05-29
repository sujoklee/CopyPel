from datetime import date

from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

import models


admin.site.site_header = 'Peleus administration'
admin.site.site_title = 'Peleus site admin'


class CustomUserProfileInline(StackedInline):
    model = models.CustomUserProfile
    verbose_name = 'forecast user'
    verbose_name_plural = 'forecast users'

UserAdmin.inlines = (CustomUserProfileInline,)


class IsActiveDisplayFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'is_active_status'
    ACTIVE = 'active'
    ARCHIVED = 'archived'

    def lookups(self, request, model_admin):
        return (
            (self.ACTIVE, 'Active'),
            (self.ARCHIVED, 'Archived'),
        )

    def queryset(self, request, qs):
        v = self.value()
        qs = qs.annotate(votes_count=Count('votes'))

        if v == self.ACTIVE:
            return qs.filter(end_date__gte=date.today())
        elif v == self.ARCHIVED:
            return qs.filter(end_date__lt=date.today())
        else:
            return qs


@admin.register(models.Forecast)
class ForecastAdmin(ModelAdmin):
    list_display = ('forecast_question', 'forecast_type', 'start_date', 'end_date', 'votes_count')
    list_filter = ('forecast_type', IsActiveDisplayFilter,)

admin.site.register(models.ForecastVotes)