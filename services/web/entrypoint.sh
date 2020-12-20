#!/bin/sh

if [ "$FLASK_ENV" = "development" ]
then
    echo "Seeding Redis database..."
    python seed_redis.py
    echo "Redis ready"
fi

exec "$@"
