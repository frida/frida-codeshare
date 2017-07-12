release: python manage.py createcachetable; python manage.py migrate
web: gunicorn fridasnippits.wsgi --log-file - --access-logfile - --access-logformat='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Forwarded-For}i)s"'
