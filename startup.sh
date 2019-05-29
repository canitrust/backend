dnsval=$(dig +short dns_server)
echo "nameserver $dnsval" >> /etc/resolv.conf


if [[ $RUN_ENV == 'local' ]]; then
  echo -e 'Running test with \033[1;33mlocal pre-defined\033[0m driver!'
  bash /testcases/test.sh $1;
else
  echo -e 'Running test with \033[1;33mBrowserStack\033[0m drivers!'
  bash /testcases/test.sh $1 $2 $3;
fi
