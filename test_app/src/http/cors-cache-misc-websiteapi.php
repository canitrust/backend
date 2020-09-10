<?php
	#header('Access-Control-Allow-Origin: *');
	header('Content-Type: text/plain');
	

	if(isset($_COOKIE['secret'])){
		#echo json_encode($response);
		echo "secret";
	}else{
		#echo json_encode($badresponse);
		echo "nosecret";
	}
?>
