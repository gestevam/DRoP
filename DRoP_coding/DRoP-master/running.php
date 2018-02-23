<?php
require("config.php");
$job=$_GET['job'];
$status=$_GET['status'];
print $job;
print "<br/><br/>";
print $status;
$res = mysql_query("UPDATE data_sets SET run_status = {$status} WHERE data_ID = {$job}",$link);
?>
