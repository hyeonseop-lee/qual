# qual

### Requirements
- Python 2.7
- virtualenv

### Setup
```sh
virtualenv env
source env/bin/activate
pip install -r requirements.txt
sudo -u postgres createdb qual
# need to create settings.py
python manage.py db upgrade
```

### Run for debug
```sh
python manage.py runserver
```

### Run for production
```sh
uwsgi uwsgi.ini
```

### Migrate after changing models
```sh
python manage.py db migrate
python manage.py db upgrade
```
