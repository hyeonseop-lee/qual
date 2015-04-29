# qual

### Requirements
- Python 2.7
- virtualenv

### Setup
```sh
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py db upgrade
```

### Run
```sh
python manage.py runserver
```

### Migrate after changing models
```sh
python manage.py db migrate
python manage.py db upgrade
```
