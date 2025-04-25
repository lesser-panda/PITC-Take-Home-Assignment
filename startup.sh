cd /usr/src/app 
python manage.py migrate
python manage.py createsuperuser --noinput --username "admin" --email "pitc_demo" || true
gunicorn core.wsgi:application --bind 0.0.0.0:8000
