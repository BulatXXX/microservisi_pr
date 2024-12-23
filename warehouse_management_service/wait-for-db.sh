#!/bin/sh

set -e

host="$1"
shift
cmd="$@"

until pg_isready -h staff_management_db -p 5432 -U postgres; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
