#!/usr/bin/perl
print "Content-type: text/html\n\n";
my @set = (a..z, A..Z, 0..9);
my $randomstring= join '' => map $set[rand scalar @set], 1 .. 30;
$html_template = qq{<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
</head>
<body>
  <span>$randomstring</span>
</body>
</html>
};
print "$html_template";
