sed -i 's/CustomLog/#CustomLog/g' /usr/local/apache2/conf/extra/httpd-canitrust.conf
sed -i 's/        \"\%t/#        \"\%t/g' /usr/local/apache2/conf/extra/httpd-canitrust.conf
sed -i 's/        \"\%t/#        \"\%t/g' /usr/local/apache2/conf/extra/httpd-canitrust.conf
sed -i '/SSLCertificateChainFile/d' /usr/local/apache2/conf/extra/httpd-canitrust.conf
sed -i 's/SSLCertificateFile.*/SSLCertificateFile \"\/usr\/local\/apache2\/certs-local\/test-canitrust.com\/root.cert.pem\"/g' /usr/local/apache2/conf/extra/httpd-canitrust.conf
sed -i 's/SSLCertificateKeyFile.*/SSLCertificateKeyFile \"\/usr\/local\/apache2\/certs-local\/test-canitrust.com\/root.privkey.pem\"/g' /usr/local/apache2/conf/extra/httpd-canitrust.conf
