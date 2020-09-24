<?php
$AUTH_USER = 'joe';
$AUTH_PW = '5ecr3t';

$template = '<html><body><div id="result">%s</div><body></html>';

if(
    isset($_GET['user']) && $AUTH_USER === $_GET['user'] &&
    isset($_GET['pw']) && $AUTH_PW === $_GET['pw']
) {
    setcookie('secret', '5ecr3t', [
        'expires' => time() + 86400,
        'path' => '/',
        'secure' => true,
        'httponly' => true,
        'samesite' => 'None',
    ]);
    printf($template, 'secret');
} else {
    printf($template, 'nosecret');
}
?>
