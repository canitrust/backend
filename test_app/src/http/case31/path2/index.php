<html>
<head>
<title>Cookie Path Testing</title>
</head>
<body>
    <p id="cookie_path">
        <?php
             echo (sizeof($_COOKIE) > 0) ?  "YES" : "NO";
        ?>
    </p>
</body>
</html>
 