<?php
session_start();
require("config.php");
$sample = $_GET['run'];
$yourfile="results/";
$yourfile.=$sample;
$yourfile.='/results';
$yourfile.=".zip";
$yourfile2="DRoP_Results_".$sample.".zip";
#print $sample;
$query = "SELECT * FROM data_sets WHERE data_ID = '{$sample}'";
$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
$resultset = mysql_fetch_array($results);
if($resultset['user_ID']==$_SESSION['UID'])
{
header ("Content-Type: application/download");
header ("Content-Disposition: attachment; filename=$yourfile2");
header("Content-Length: " . filesize("$yourfile"));
$fp = fopen("$yourfile", "r");
fpassthru($fp);
}
else
{
  print "This event is being logged. You tried to access someone else's results. Repeated offenses may result in your banning from the server!<br />";
  $ip = $_SERVER['REMOTE_ADDR'];
  print "Your IP Address is ".$ip;
  print "<br />Your User Name is: ".$_SESSION['name'];
}
?>

