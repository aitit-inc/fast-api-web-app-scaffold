#!/bin/sh
set -eux

# Input arguments
# $1: down - stop the database container

DOCKER_COMPOSE_CMD=bin/test-app.sh
VOLUME_NAME=fast-api-web-app-scaffold_fawapp_test_postgresdb

# docker-compose service name
APP_SERVICE=test-app

# Change directory to the root of the project
SCRIPT_DIR=$(
  cd "$(dirname "$0")"
  pwd
)
cd "$SCRIPT_DIR/.."

# Stop and remove database if it exists
$DOCKER_COMPOSE_CMD down || true
if [ $# = 1 ] && [ "$1" = "down" ]; then
  exit 0
fi

docker volume rm $VOLUME_NAME || true

# Start test database container
$DOCKER_COMPOSE_CMD up --build -d

sleep 3

RUN_APP_CMD="$DOCKER_COMPOSE_CMD run --rm $APP_SERVICE"

# Create database
$RUN_APP_CMD bash -c "USE_TEST_DB=True alembic upgrade head"

# Import seed data
$RUN_APP_CMD python app/load_seeds.py --test
