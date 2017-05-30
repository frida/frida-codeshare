release: python manage.py createcachetable; python manage.py migrate
web: gunicorn fridasnippits.wsgi --log-file -
