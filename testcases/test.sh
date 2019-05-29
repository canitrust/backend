if [[ $RUN_ENV == 'bs' ]]; then
  touch /tmp/log_bs.log
  echo -e "Testcase number: \033[0;31m$3\033[0m, waiting for BrowserstackLocal"
  /testcases/BrowserStackLocal --key $1 --force-local > /tmp/log_bs.log 2>&1 &
  tail -F /tmp/log_bs.log  | 
  grep --line-buffered 'exit' | 
  while read ; do python3 /testcases/test_bs.py $3 ; done
else
  echo -e "Testcase number: \033[0;31m$1\033[0m, running local geckodriver"
  python3 /testcases/test_local.py $1
fi