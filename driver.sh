#!/bin/bash

unlock_containers() {
  echo true > ./driver/config/container.lock
  while true; do
      lock=$(grep -E "browserstack|local" ./driver/config/container.lock)
      if [ "$lock" == "browserstack" ]; then
        docker-compose down  >> /dev/null 2>&1
        docker-compose up -d --build >> /dev/null 2>&1
        break
      elif [ "$lock" == "local" ]; then
        docker-compose -f docker-compose.local.yml down  >> /dev/null 2>&1
        docker-compose -f docker-compose.local.yml up -d --build >> /dev/null 2>&1
        break
      fi
  done
}

kill_docker() {
  docker-compose -f docker-compose.driver.yml down >> /dev/null 2>&1
  docker-compose down >> /dev/null 2>&1
}

docker-compose -f docker-compose.driver.yml down > /dev/null 2>&1
unlock_containers &
docker-compose -f docker-compose.driver.yml run -T driver python /driver/driver.py "$@" 
exit_status=$?
if [ $exit_status -ne 0 ]; then
    echo "Something wrong with Driver"
else
  echo "Driver DONE"
fi
kill_docker
exit $exit_status

