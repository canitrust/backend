<html>
<head>
<title>SameSite Attribute Testing</title>
</head>
<body>
    <p>SameSite Attribute Testing</p>
    <iframe src="http://samesite1.test-canitrust.com"></iframe>
    <p>Is the cookie sent? </p>
    <p id="cookie_samesite">
        <?php
             echo (sizeof($_COOKIE) > 0) ?  "YES" : "NO";
        ?>
    </p>
</body>
</html>
 