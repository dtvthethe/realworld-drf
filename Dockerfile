FROM python:3.12-slim

# mysqlclient cần các system packages này để compile
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ⭐ Set PATH để mọi shell trong container đều dùng .venv/bin/python
# Kể cả khi `docker exec` vào tay, không cần activate .venv thủ công
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements trước (tận dụng Docker layer cache)
COPY requirements.txt .

# KHÔNG pip install ở đây!
# Việc install sẽ do entrypoint.sh làm lúc container start
# → để packages được ghi vào .venv trên host

COPY . .
