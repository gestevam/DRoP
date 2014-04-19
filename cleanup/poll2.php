<?php 
session_start();
require("config.php");
if( session_is_registered('login') )
{
	print "<ul>";
	$start=10;
	$limit=10;
	print $link;
	$query = "SELECT * FROM data_sets WHERE data_sets.user_ID={$_SESSION['UID']} ORDER BY data_ID DESC LIMIT $start, $limit";
	$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	$page = $_GET['page'];
if(!$page || $page == 0 || !is_numeric($page)){
  $page = 1;
}
$limit = 10;
	if(mysql_num_rows($results) > 0) 
	{
		$count=0;
		//print $count;
		while($resultsArray = mysql_fetch_array($results)) 
		{
			$count=$count+1;
			if ($count<=10 or 1)
			{
			
			if ($resultsArray['run_status']==0)
			{
				print "<li>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
				print "File uploaded: Starting DRoP";
			}
			if ($resultsArray['run_status']==200)
			{
				print "<li>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
				print "Run is currently in Preprocessing.";
			}
			if ($resultsArray['run_status']==222)
			{
				print "<li><font color=red>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
				print "Run has failed. Error 222: Missing CRYST1 line.</font>";
			}
                        if ($resultsArray['run_status']==299)
                        {
				print "<li>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
				print "Run has completed Preprocess.";
                        }
                        if ($resultsArray['run_status']==300)
                        {
				print "<li>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
				print "Run is currently Superimposing.";
                        }
                        if ($resultsArray['run_status']==399)
                        {
				print "<li>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
				print "Run has completed Superimposing.";
                        }
                        if ($resultsArray['run_status']==400)
                        {
				print "<li>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
				print "Run is currently in main DRoP algorithm.";
                        }
                        if ($resultsArray['run_status']==-1)
                        {
				print "<li>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
				print "Run has failed. Please try running again. If the run consistently fails, please notify an administrator.";
                        }
			if ($resultsArray['run_status']==777)
			{
				print "<li><font color=green>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br /></font>";
				print "Run Complete. Click <a href=\"autosave.php?run={$resultsArray['data_ID']}\">Here</a> for your results.";

			}}
		}
		#print "Don't click this. I'm testing something. <a href=\"time.php\">test</a>";	
	}	
	else
	{
		echo "Huh.";
	}
print "</ul>";
}
?>

