FROM httpd:2.4

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		libapache2-mod-php \
	; \
	rm -rf /var/lib/apt/lists/*

RUN mkdir /var/log/httpd
COPY src/http/.  /usr/local/apache2/htdocs/
RUN rm -rf /usr/local/apache2/conf/
COPY src/config/* /usr/local/apache2/conf/extra/

COPY src/httpd.conf /usr/local/apache2/conf/
COPY src/http/cache3.cgi /usr/local/apache2/htdocs/cgi-bin/
RUN chmod a+x /usr/local/apache2/htdocs/cgi-bin/cache3.cgi
COPY src/mime.types /usr/local/apache2/conf/
COPY src/magic /usr/local/apache2/conf/
COPY src/modules/. /usr/local/apache2/modules/

COPY src/certs-local/. /usr/local/apache2/certs-local/
RUN bash /usr/local/apache2/certs-local/changeLocal.sh
RUN ls /usr/local/apache2/conf/
