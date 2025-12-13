## Install

copy `.env.example` to `.env` and update env variables

```bash
docker-compose up -d
docker exec -it realworld_drf_api bash
python manage.py migrate
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