ORGANIZATION_TYPE = (('1', 'School'),
                     ('2', 'Think Tank'),
                     ('3', 'Company'),
                     ('4', 'Government Agency'))

FORECAST_TYPE = (('1', 'Finite Event'),
                 ('2', 'Probability'),
                 ('3', 'Magnitude'),
                 ('4', 'Time Horizon Event'))

AREAS = (('1', "Elections"),
         ('2', "Conflicts/Wars"),
         ('3', "Social Events/Protests"),
         ('4', "Fiscal and Monetary Actions"),
         ('5', "Inter-State Negotiations"),
         ('6', "Trade Agreements"),
         ('7', "Private Sector Engagements"))

REGIONS = (('1', "Europe"),
           ('2', "Middle East"),
           ('3', "Africa"),
           ('4', "Asia"),
           ('5', "South Pacific"),
           ('6', "North America"),
           ('7', "South America"))

STATUS_CHOICES = (('u', "Unpublished"),
                  ('p', "Published"))

FORECAST_FILTER = "filter"
FORECAST_FILTER_MOST_ACTIVE = "mostactive"
FORECAST_FILTER_NEWEST = "newest"
FORECAST_FILTER_CLOSING = "closing"
FORECAST_FILTER_ARCHIVED = "archived"

FORECAST_FILTERS = {'FORECAST_FILTER_MOST_ACTIVE': FORECAST_FILTER_MOST_ACTIVE,
                    'FORECAST_FILTER_NEWEST': FORECAST_FILTER_NEWEST,
                    'FORECAST_FILTER_CLOSING': FORECAST_FILTER_CLOSING}

GROUP_TYPES = (('1', 'Public'),
               ('2', 'Private'))

