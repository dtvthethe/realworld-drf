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

## Save package to requirements.txt

```bash
pip3 freeze > requirements.txt
```
