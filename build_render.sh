#!/bin/bash

pip install -r requirements.txt
cd ssmanager/
python ./manage.py makemigrations
python ./manage.py migrate

exit 0