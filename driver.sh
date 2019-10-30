#!/bin/bash

unlock_containers() {
  while true; do
      lock=$(grep false ./driver/config/container.lock)
      if [ "$lock" == "false" ]; then
        docker-compose down  >> /dev/null 2>&1
        docker-compose up -d --build >> /dev/null 2>&1
        break
      fi
  done
}

kill_docker() {
  docker-compose -f docker-compose.driver.yml down >> /dev/null 2>&1
  docker-compose down >> /dev/null 2>&1
}


docker-compose -f docker-compose.driver.yml down > /dev/null 2>&1
SECONDS=0
docker-compose -f docker-compose.driver.yml up -d --build

while true; do
  if [ "$SECONDS" -gt "180" ]; then
    echo "Starting driver FAILED (waited for 3 minutes)"
    exit 1
  fi
  sleep 2
  driver=$(docker ps --filter 'status=running' --format '{{.Names}}' | grep driver)
  echo "Waiting for driver...in ($SECONDS seconds)"
  if [ "$driver" == "driver" ]; then
    echo "Driver UP"
    break
  fi
done
unlock_containers &
docker exec -it $driver python /driver/driver.py "$@"
echo "Driver DONE"
kill_docker