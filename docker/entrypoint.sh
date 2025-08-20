#!/usr/bin/env sh
set -e
mkdir -p /data
if [ ! -f /data/oc-lettings-site.sqlite3 ]; then
  echo "No runtime DB found. Seeding from image..."
  cp -f /seed/db.sqlite3 /data/oc-lettings-site.sqlite3
fi
chmod 664 /data/oc-lettings-site.sqlite3 || true
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn oc_lettings_site.wsgi:application \
  -b 0.0.0.0:${PORT:-8000} \
  --workers ${GUNICORN_WORKERS:-3} \
  --timeout ${GUNICORN_TIMEOUT:-60}
