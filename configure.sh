#!/bin/bash

mkdir -p data
chmod +x manage.py

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

crontab -l > mycron
echo "5 0 * * * bash "$DIR"/cron.sh" >> mycron
crontab mycron
rm mycron

