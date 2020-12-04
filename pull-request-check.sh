#!/bin/bash

testcases=()
testcase_numb_regex="driver/testcases/case([0-9]+).py"
o1_testcase_regex=("(testCase.py|Dockerfile|docker-compose*|driver.sh|pull-request-check.sh|deriver.py|helper.py|driver_cli.py|workflows)")

while read line
do
  changed_files=("${changed_files[@]}" $line)
done

# if all changed files are not in o1_testcase_regex and testcase_numb_regex, run localtest with --all_live param
for file in ${changed_files[@]}
do
  if [[ $file =~ $testcase_numb_regex ]]; then
    testcases+=("${BASH_REMATCH[1]}")
  else
    if [[ $file =~ $o1_testcase_regex ]]; then
      o1_testcase=39
    else
      run_all=1
    fi
  fi
done

if [ -z ${run_all+x} ]; then
  if [ ${#testcases[@]} -ne 0 ]; then
    echo "Run localtest with testcases: ${testcases[@]}"
    ./driver.sh runlocal -t $(printf "%s," "${testcases[@]}" | cut -d "," -f 1-${#testcases[@]}) --catch_fail
  else
    if [ -z ${o1_testcase+x} ]; then
      echo "Something went wrong!"
    else
      echo "Run localtest with testcases: $o1_testcase"
      ./driver.sh runlocal -t $o1_testcase --catch_fail
    fi
  fi
else
  echo "Run all live"
  ./driver.sh runlocal --all_live --catch_fail
fi
