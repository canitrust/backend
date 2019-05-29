FROM sameersbn/bind:9.11.3-20190315
 
COPY setup-and-run.sh .

RUN rm /etc/bind/named.conf.options
RUN rm /etc/bind/named.conf.default-zones

COPY noexample.mgm /etc/bind/noexample.mgm
COPY test-canitrust.com /etc/bind/test-canitrust.com
COPY named.conf.default-zones /etc/bind/named.conf.default-zones
COPY named.conf.options /etc/bind/named.conf.options

CMD ["./setup-and-run.sh"]
