
d=`nslookup test_app | tail -n 2 | head -n 1 | awk -F ': ' '{print $2}'`
sed -i '/noexample/,+1 d' /etc/bind/noexample.mgm

echo "noexample.mgm.          IN      A       $d" >> /etc/bind/noexample.mgm
echo "test-canitrust.com.          IN      A       $d" >> /etc/bind/test-canitrust.com
echo "*.test-canitrust.com.          IN      A       $d" >> /etc/bind/test-canitrust.com

cat /etc/bind/test-canitrust.com
service bind9 start

tail -F /dev/null
