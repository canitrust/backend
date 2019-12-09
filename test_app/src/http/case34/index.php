<?php header("Content-Security-Policy: script-src 'none'; report-uri /security-alert?source=" . $_SERVER['REQUEST_URI']); ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1>CSP with an invalid directive</h1>
    <p id="content">safe</p>
    <script>
        document.getElementById('content').innerHTML = 'exploited';
    </script>
</body>
</html>
