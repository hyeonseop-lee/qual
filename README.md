# qual

### Requirements

- Python 2.7
- virtualenv
- PostgreSQL Instance

### Setup

```sh
virtualenv env
source env/bin/activate
pip install -r requirements.txt
cp settings.py.default settings.py
```

You should modify settings.py with your PostgreSQL configuration.

```
python manage.py db upgrade
```

### Run for debug

```sh
python manage.py runserver
```

### Run for production

Make sure you have your unique `SECRET_KEY` and `REGISTER_KEY` in settings.py.

```sh
uwsgi uwsgi.ini
```

### Migrate after changing models

```sh
python manage.py db migrate
python manage.py db upgrade
```
