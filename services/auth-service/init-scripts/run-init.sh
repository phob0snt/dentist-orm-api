#!/bin/bash
set -e

FLAG_FILE="/app/.initialized"

if [ -f "$FLAG_FILE" ]; then
    echo "Инициализация уже была выполнена"
else
    echo "Создание таблиц"
    python /app/init-scripts/init_db.py

    echo "Создание админа"
    python /app/init-scripts/create_admin.py

    touch "$FLAG_FILE"

    echo "Инициализация выполнена"
fi

exec "$@"