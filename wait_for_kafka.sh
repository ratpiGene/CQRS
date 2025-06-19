#!/bin/bash
set -e

host="$1"
port="$2"

echo "⏳ Attente de Kafka sur $host:$port..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "✅ Kafka est prêt sur $host:$port"
exec "${@:3}"
