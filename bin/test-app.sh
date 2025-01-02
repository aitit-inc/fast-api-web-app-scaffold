#!/bin/sh
set -eux

DC_YML=docker-compose.db.test.yml

# Change directory to the root of the project
SCRIPT_DIR=$(
  cd "$(dirname "$0")"
  pwd
)
cd "$SCRIPT_DIR/.."

# Check if docker-compose command exists, if not, fallback to docker compose
if command -v docker-compose >/dev/null 2>&1; then
  DOCKER_COMPOSE_CMD="docker-compose"
else
  DOCKER_COMPOSE_CMD="docker compose"
fi

$DOCKER_COMPOSE_CMD -f $DC_YML "$@"
