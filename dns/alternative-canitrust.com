$TTL	604800
@	IN	SOA	localhost. root.localhost. (
			      2		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	localhost.
; name servers - A records
alternative-canitrust.com.          IN      CNAME test_app.
*.alternative-canitrust.com.          IN      CNAME test_app.