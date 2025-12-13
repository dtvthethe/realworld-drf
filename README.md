## Install

copy `.env.example` to `.env` and update env variables

```bash
docker-compose up -d
docker exec -it realworld_drf_api bash
python manage.py migrate
```

## Save package to requirements.txt

```bash
pip3 freeze > requirements.txt
```
