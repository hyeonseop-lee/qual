# qual

### Requirements
- Python 2.7
- virtualenv

### Setup
```sh
virtualenv env
source env/bin/activate
pip install -r requirements.txt
./manage.py db init
./manage.py db migrate
```

### Run
```sh
./run.py
```

### Migrate after changing models
```sh
./manage.py db migrate
./manage.py db upgrade
```
