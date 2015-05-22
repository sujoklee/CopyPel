from django.contrib import admin
import models


admin.site.register(models.CustomUserProfile)
admin.site.register(models.Forecast)
admin.site.register(models.ForecastVotes)
