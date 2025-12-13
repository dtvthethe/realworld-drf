# phiên bản slim (nhẹ hơn full version)
FROM python:3.14.2-slim

# PYTHONDONTWRITEBYTECODE=1: Không tạo file .pyc (bytecode)
#   - File .pyc là gì? Python tự tạo để chạy nhanh hơn lần sau
#   - Lợi ích: Docker image nhẹ hơn
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# gcc: Compiler để compile code C
# default-libmysqlclient-dev: Thư viện development để compile mysqlclient
# pkg-config: Tool hỗ trợ tìm thư viện khi compile
# rm -rf /var/lib/apt/lists/*: Xóa cache apt để giảm dung lượng image
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

# --upgrade pip: Cập nhật pip lên phiên bản mới nhất (tránh lỗi)
# -r requirements.txt: Flag -r (required) để đọc file danh sách packages
# --no-cache-dir: Không lưu cache pip, giúp image nhẹ hơn
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
