from datetime import date

from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from django_object_actions import DjangoObjectActions

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


class PublishedProposeFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'publication_status'
    YES = 'no'
    ALL = 'all'

    def lookups(self, request, model_admin):
        return (
            (None, 'Unpublished'),
            (self.YES, 'Published'),
            (self.ALL, 'All')
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        v = self.value()

        if v == None:
            return queryset.filter(status='u')
        elif v == self.YES:
            return queryset.filter(status='p')
        else:
            return queryset


@admin.register(models.Forecast)
class ForecastAdmin(ModelAdmin):
    list_display = ('forecast_question', 'forecast_type', 'start_date', 'end_date', 'votes_count')
    list_filter = ('forecast_type', IsActiveDisplayFilter,)
    # inlines = (TagsInline,)


@admin.register(models.ForecastPropose)
class ForecastProposeAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ('forecast_question', 'forecast_type', 'end_date', 'status')
    list_filter = (PublishedProposeFilter,)

    exclude = ('status',)

    def publish_propose(self, request, obj):
        obj.status = 'p'
        obj.save()

        f = models.Forecast(forecast_type=obj.forecast_type,
                            forecast_question=obj.forecast_question,
                            end_date=obj.end_date)
        f.save()

        for tag in obj.tags.all():
            f.tags.add(tag)
    publish_propose.label = 'Publish'
    publish_propose.attrs = {'class': 'btn btn-primary'}

    def get_object_actions(self, request, context, **kwargs):
        if 'original' in context and context['original'] and context['original'].status != 'p':
            return ['publish_propose']
        return []


@admin.register(models.ForecastVotes)
class ForecastVotesAdmin(ModelAdmin):
    list_display = ('user_display', 'forecast_question_display', 'vote', 'date',)

    def user_display(self, obj):
        return obj.user_id
    user_display.short_description = 'User'
    user_display.admin_order_field = 'user_id'

    def forecast_question_display(self, obj):
        return obj.forecast_id.forecast_question
    forecast_question_display.short_description = 'Question'


@admin.register(models.ForecastMedia)
class ForecastMediaAdmin(ModelAdmin):
    list_display = ('forecast', 'name', 'url', 'image')


@admin.register(models.ForecastAnalysis)
class ForecastAnalysis(ModelAdmin):
    list_display = ('title', 'body', 'forecast', 'user',)
    list_display_links = ('title', 'body',)