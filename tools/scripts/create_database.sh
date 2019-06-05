#!/usr/bin/env bash

$(python3 manage.py makemigrations)
$(python3 manage.py migrate)
yes yes | $(python3 manage.py flush)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@polls.com', 'password')" | python3 manage.py shell
$(python3 manage.py db_manager)
echo "DB successfully created. New achievement unlocked!"