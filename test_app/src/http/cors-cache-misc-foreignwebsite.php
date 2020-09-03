<!DOCTYPE html>
<html>
	<head>
		<script src="jquery-3.5.1.min.js"></script>
		<title>Arbitrary Website</title>
	</head>
	<body>

		<div id="result"></div>
	</body>
<script>
(function(){


	fetch('http://cors-cache-misc.test-canitrust.com/cors-cache-misc-websiteapi.php',
		{
			'cache': 'force-cache',
			'credentials': 'omit'
	})
	.then(function(res){
		return res.text();
	})
	.then(function(data){
		console.log(data);
		document.getElementById('result').innerText = data; //"<div id='scriptDiv'>"+data+"</div>";
	});
})();
</script>
</html>
