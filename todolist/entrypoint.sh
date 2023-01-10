#!/bin/bash
python manage.py migrate --check
if [[ $? != 0 ]] ; then
  python manage.py migrate
fi
exec "$@"