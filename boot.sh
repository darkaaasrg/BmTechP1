#!/bin/bash
# Чекаємо, поки MySQL стане доступним
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo "База ще не готова, чекаємо 5 секунд..."
    sleep 5
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app

chmod a+x /vagrant/boot.sh


