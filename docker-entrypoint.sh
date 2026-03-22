#!/bin/bash
set -e

VENV_PATH="/app/.venv"
MARKER="$VENV_PATH/.installed_marker"

echo "🐍 Checking .venv..."

# Cần install nếu:
# 1. Chưa có marker (lần đầu chạy)
# 2. requirements.txt mới hơn marker (có thêm package)
if [ ! -f "$MARKER" ] || [ /app/requirements.txt -nt "$MARKER" ]; then
    echo "📦 Installing packages vào .venv (lần này hơi lâu chút nha...)"

    # Tạo venv nếu chưa có
    python -m venv "$VENV_PATH"

    # Upgrade pip
    "$VENV_PATH/bin/pip" install --upgrade pip --quiet

    # Install tất cả packages vào .venv
    "$VENV_PATH/bin/pip" install -r /app/requirements.txt

    # Đánh dấu đã install xong
    touch "$MARKER"

    echo "✅ Done! Packages đã sẵn sàng."
else
    echo "✅ .venv đã có rồi, skip install."
fi

# Kích hoạt venv
source "$VENV_PATH/bin/activate"

# Chạy lệnh được truyền vào (ví dụ: python manage.py runserver)
exec "$@"
