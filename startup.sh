cd /usr/src/app 
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser --noinput --username "admin" --email "pitc_demo" || true
gunicorn seqseek.wsgi:application --bind 0.0.0.0:8000
