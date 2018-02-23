<?php 
session_start();
require("config.php");
if( session_is_registered('login') )
{
	print "<b>Server News: Nov 21, 2013</b> You can now upload .rar files for DRoP!<br /> <br />";
	print "<b>Special note from the admins:</b> If you are using a Mac OS, please use a separate zipping program than the one included with the OS. If you do not, you will receive a missing CRYST1 line error. We are working on a fix for this. <br /> <br />";
	print "<ul>";
	$query = "SELECT * FROM data_sets WHERE data_sets.user_ID={$_SESSION['UID']} ORDER BY data_ID DESC";
        if($_SESSION['UID']=='1')
	{
		 $query = "SELECT * FROM data_sets ORDER BY data_ID DESC";
	}
	$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
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
			if ($resultsArray['run_status']==667)
			{
				print "<li><font color=red>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
                                print "Run has failed. No PDB files were found in your upload.</font>";
			}
			if ($resultsArray['run_status']==666)
			{
				print "<li><font color=red>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
                                print "Run has failed. Did you upload a .zip file or a .rar file containing your .pdb files? You can't upload a single raw .pdb file.</font>";

			}
                        if ($resultsArray['run_status']==333)
                        {
				print "<font color=red><li>Run ID: {$resultsArray['data_ID']}   -   {$resultsArray['job_title']}<br />";
                                print "Run has failed. You're asking to superimpose only one structure. This will be fixed soon.</font>";
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

			}
if($_SESSION['UID']=='1')
        {
		$query="SELECT * FROM users WHERE users.user_ID = {$resultsArray['user_ID']}";
		$results2=mysql_query($query,$link) or die('BOOM');
		$rarray=mysql_fetch_array($results2);
                print "<br />User ID: {$resultsArray['user_ID']} ({$rarray['name']})<hr />";
        }

}
		}
		#print "Don't click this. I'm testing something. <a href=\"time.php\">test</a>";
	
	}
	else
	{
		echo "Welcome to DRoP! After uploading a zip file of PDBs, your history will appear here.";
	}
print "</ul>";
}
?>

