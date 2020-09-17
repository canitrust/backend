<?php
	#header('Access-Control-Allow-Origin: *');
	header('Content-Type: application/json');
	
	$httpHeaders = getallheaders();
	if(
		isset($_COOKIE['secret']) ||
		(isset($httpHeaders['Authorization']) && 'jwt-token' === $httpHeaders['Authorization'])
	){
		echo json_encode(['result' => 'secret']);
	} else if (isset($_COOKIE['secret']) && isset($httpHeaders['Authorization'])) {
		echo json_encode(['result' => 'Error: both cookie and jwt are sent']);
	} else {
		echo json_encode(['result' => 'nosecret']);
	}
?>
