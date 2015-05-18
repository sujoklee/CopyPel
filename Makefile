MANAGE=django-admin.py
test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=forecast.settings $(MANAGE) test
run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=forecast.settings $(MANAGE) runserver
syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=forecast.settings $(MANAGE) syncdb --noinput
migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=forecast.settings $(MANAGE) migrate