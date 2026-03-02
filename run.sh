#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Projekt mappa: $(pwd)"

if [ ! -d "venv" ]; then
  echo "venv nincs, létrehozom..."
  python3 -m venv venv
fi

echo "Függőségek telepítése..."
./venv/bin/python -m ensurepip --upgrade >/dev/null 2>&1 || true
./venv/bin/python -m pip install -r requirements.txt

echo "Migrációk futtatása..."
./venv/bin/python manage.py migrate

echo "Szerver indul: http://127.0.0.1:8000"
echo "Leállítás: Ctrl+C"
./venv/bin/python manage.py runserver 0.0.0.0:8000
