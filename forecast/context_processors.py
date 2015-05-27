import ast

from django.template.defaulttags import register

from models import CustomUserProfile
from Peleus.settings import REGIONS, AREAS

FORECAST_REGIONS = dict(REGIONS)
FORECAST_AREAS = dict(AREAS)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def forecast_user(request):
    try:
        custom_user = CustomUserProfile.objects.select_related().get(user_id=request.user.id)

        custom_user.forecast_areas = [str(i) for i in ast.literal_eval(custom_user.forecast_areas)]
        custom_user.forecast_regions = [str(i) for i in ast.literal_eval(custom_user.forecast_regions)]
    except CustomUserProfile.DoesNotExist:
        custom_user = None
    return {'forecast_user': custom_user}

def forecast_interests(request):
    return {'FORECAST_REGIONS': FORECAST_REGIONS, 'FORECAST_AREAS': FORECAST_AREAS}