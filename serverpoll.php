<?php 
session_start();
require("config.php");
if( session_is_registered('login') or 1 )
{
	$uptime = shell_exec("cut -d. -f1 /proc/uptime");
	$days = floor($uptime/60/60/24);
	$hours = $uptime/60/60%24;
	$mins = $uptime/60%60;
	$secs = $uptime%60;
	echo "DRoP server uptime: $days days $hours hours $mins minutes";
	print "<br><br>";

	//$query = "UPDATE data_sets SET run_status=-1 WHERE data_sets.run_status!=777";
	//$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	print "<ul>";
	$query = "SELECT * FROM data_sets ORDER BY data_ID DESC";
	$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	if(mysql_num_rows($results) > 0) 
	{
		$count=0;
		//print $count;
		$now=date("'Y-m-d H:i:s'");
		//print $now;
		$query="SELECT * FROM data_sets WHERE data_sets.job_time > (DATE_SUB($now, INTERVAL 1 DAY))";
		$last24 = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
		//print mysql_num_rows($last24);
		$successful=0;
		$inprogress=0;
		while($resultsArray = mysql_fetch_array($results)) 
		{
			if ($resultsArray['run_status']==777)
			{
				$successful=$successful+1;
			}
			if ($resultsArray['run_status']!=222 and $resultsArray['run_status']!=-1 and $resultsArray['run_status']!=777 and $resultsArray['run_status']!=333 and $resultsArray['run_status']!=666)
			{
				$inprogress=$inprogress+1;
			}
		}
		print "Successful runs: ";
		print $successful;
		print "<br>Runs in progress: ";
		print $inprogress;
		print "<br>Runs in the last 24 hours: ";
		print mysql_num_rows($last24);
		#print "Don't click this. I'm testing something. <a href=\"time.php\">test</a>";
	}	
	else
	{
		echo "Welcome to DRoP! If you are viewing this, that means nobody has used the live DRoP server yet. Try it out!";
	}
print "</ul>";
}
?>

