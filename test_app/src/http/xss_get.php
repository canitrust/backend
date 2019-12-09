<html>
  <head>
    <title>reflected XSS</title>
  </head>
  <body>
    <h1 id=headline>Hello World!</h1>
    <?php
      echo '<p>PHP is enabled</p>';
      echo '<p id="check">Check: 7*7 = ' . strval(7*7) . '</p>'
    ?>
    <?php echo $_GET['payload']; ?>
  </body>
</html>
