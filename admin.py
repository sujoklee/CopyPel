from app.models import Forecast

class ForecastAdmin(admin.ModelAdmin):
      list_display    = ['forecast_id', 'forecast_type', 'forecast_question']

admin.site.register(Forecast,ForecastAdmin)