<html>
<?php
#header('Content-Type: text/html');
#header('X-XSS-Protection: 0');
#header('X-Content-Type-Options: nosniff');
#header('Cache-Control: no-cache, no-store, must-revalidate')
header('Content-Type: ' . $_GET['content_type']);
header('X-XSS-Protection: 0');
if ($_GET['nosniff'] == "true"){
    header('X-Content-Type-Options: nosniff');
}
?>
  <head>
    <title>sniffing test</title>
  </head>
  <body>
    <h1 id=headline>Hello World!</h1>
    <?php
      echo '<p>PHP is enabled</p>';
      echo '<p id="check">Check: 7*7 = ' . strval(7*7) . '</p>'
    ?>
    <br/>
    <script>document.getElementById("headline").innerHTML = "XSS exploited";</script>
  </body>
</html>
