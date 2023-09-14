#!/bin/sh
echo "Checking Postgres"

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#doMigrate=${DB_MIGRATE:-false}
#if [ "$doMigrate" = true ] ;
#then
#  python manage.py flush --no-input #remove all data from database
#  python manage.py migrate
#fi

#exec "$@"

#python3 manage.py flush --no-input
#python3 manage.py makemigrations
#python3 manage.py migrate_schemas --share
#echo "Creating superuser"
#DJANGO_SUPERUSER_PASSWORD=testpass \
    #    python manage.py createsuperuser --username testuser --email admin@email.com --noinput
exec "$@"
