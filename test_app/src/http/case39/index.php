<?php
$AUTH_USER = 'joe';
$AUTH_PW = '5ecr3t';

$template = '<html><body><div id="result">%s</div><body></html>';

if (!isset($_SERVER['PHP_AUTH_USER']) || !isset($_SERVER['PHP_AUTH_PW'])) {
    header('WWW-Authenticate: Basic realm="CIT Case 39"');
    header('HTTP/1.1 401 Unauthorized');
    printf($template, 'please authenticate');
    exit;
} else if (
    $AUTH_USER === $_SERVER['PHP_AUTH_USER'] &&
    $AUTH_PW === $_SERVER['PHP_AUTH_PW']
) {
    printf($template, 'secret');
} else {
    printf($template, 'nosecret');
}
?>
