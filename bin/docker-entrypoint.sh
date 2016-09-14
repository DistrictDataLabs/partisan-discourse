#!/usr/bin/env bash
set -e

if [[ ! -d /root/nltk_data ]]; then
    ./bin/install_nltk_data
fi
if [[ ! -f /etc/started ]]; then
    # startup tasks to make the app work and give us a local login
    python manage.py migrate --noinput
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('partisan', 'partisan@districtdatalabs.com', 'password')" | python manage.py shell
fi
# leave an artifact in the container to know we did the startup tasks
touch /etc/started
exec "$@"