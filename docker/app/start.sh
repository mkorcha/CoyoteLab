#!/bin/bash
source /var/app/set_host.sh

cd /var/app/project

# install/update npm dependencies for frontend
npm update
npm install --save-dev

# install/update pip dependencies for backend
pip install -r requirements.txt

# run migrations
python manage.py db upgrade
python manage.py lxd_init
python manage.py run

