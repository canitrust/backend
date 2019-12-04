#!/bin/bash

unlock_containers() {
  echo true > ./driver/config/container.lock
  while true; do
      lock=$(grep -E "browserstack|local|exit" ./driver/config/container.lock)
      if [ "$lock" == "browserstack" ]; then
        docker-compose down  >> /dev/null 2>&1
        docker-compose up -d --build >> /dev/null 2>&1
        break
      elif [ "$lock" == "local" ]; then
        docker-compose -f docker-compose.local.yml down  >> /dev/null 2>&1
        docker-compose -f docker-compose.local.yml up -d --build >> /dev/null 2>&1
        break
      elif [ "$lock" == "exit" ]; then
        break
      fi
  done
}

kill_docker() {
  docker-compose -f docker-compose.driver.yml down >> /dev/null 2>&1
  docker-compose down >> /dev/null 2>&1
}
exit_lock() {
  echo exit > ./driver/config/container.lock
}

docker-compose -f docker-compose.driver.yml down > /dev/null 2>&1
docker-compose -f docker-compose.driver.yml build  > /dev/null 2>&1
unlock_containers &
docker-compose -f docker-compose.driver.yml run -T driver python /driver/driver.py "$@" 
exit_status=$?
if [ $exit_status -ne 0 ]; then
    echo "Something wrong with Driver"
else
  echo "Driver DONE"
fi
exit_lock
kill_docker
exit $exit_status

