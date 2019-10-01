<html>
 <head>
  <title>reflected XSS</title>
 </head>
 <body>
<h1 id=headline>Hello World!</h1>
 <?php echo '<p>PHP is enabled</p>'; ?>
 <?php echo $_GET['payload']; ?>
 </body>
</html>