#!/bin/sh

echo "Running Alembic Migrations"
alembic upgrade head

echo "Starting the application"
exec "$@"

