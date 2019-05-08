#!/usr/bin/env bash

$(python3 manage.py makemigrations)
$(python3 manage.py migrate)
yes yes | $(python3 manage.py flush)
$(python3 manage.py db_manager)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@polls.com', 'password')" | python3 manage.py shell
echo "from django.contrib.auth.models import Group; role = Group.objects.get(name='Gestor'); from django.contrib.auth.models import User; user = User.objects.get(username='admin'); user.groups.add(role)" | python3 manage.py shell
echo "DB successfully created. New achievement unlocked!"