<!DOCTYPE html>
<?php
	header("Access-Control-Allow-Origin: *");
?>
<html>
	<head>
		<script src="jquery-3.5.1.min.js"></script>
		<title>Supersichere Website</title>
	</head>
	<body>

		<div id="result"></div>
	</body>
<script>
	$(document).ready(function(){
		document.cookie = "secret=secret;SameSite=strict";
		$.ajax({
			url: "http://cors-cache-misc.test-canitrust.com/cors-cache-misc-websiteapi.php",
			success: function(result){
				$('#result').text(result);//html("<div id='scriptDiv'>"+result+"</div>");
			}
		});
	});
</script>
</html>
