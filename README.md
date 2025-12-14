## Install

copy `.env.example` to `.env` and update env variables

```bash
docker-compose up -d
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
```

## Run server
```bash
docker-compose up -d
source .venv/bin/activate
python3 manage.py runserver
```
The server at http://127.0.0.1:8000/


## Save package to requirements.txt

```bash
pip3 freeze > requirements.txt
```

## Error install
1. Mysql client
```
RROR: Failed to build 'mysqlclient' when getting requirements to build wheel
```

Fix:


```bash
sudo apt update
sudo apt install -y build-essential python3-dev default-libmysqlclient-dev pkg-config
```