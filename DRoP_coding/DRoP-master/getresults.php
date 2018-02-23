<?php
session_start();
require("config.php");
$sample = $_GET['sample'];
$query = "SELECT * FROM data_sets WHERE data_ID = '{$sample}'";
$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
$resultset = mysql_fetch_array($results);
header('Content-type: text/plain');
header('Content-disposition: attachment; filename="test.txt"');
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<link type="text/css" media="screen" href="CSS/style.css" rel="stylesheet" />
	<link type="text/css" media="print" href="CSS/print.css" rel="stylesheet" />
<?php
	if(!session_is_registered('login'))
		print '<meta http-equiv="Refresh" content="0; URL=index.php" />';
	print "<title>Mattos Lab Crystallography Database - Sample Details: {$resultset['protein']}</title>";
?>
</head>
<body>
	<div id="wrapper">
		<div id="logo" class="clearfix">
			<img src="images/serverrackwide.gif" width="184" height="93" alt="" class="headimg" />
			<img src="images/logo2.gif" width="581" height="93" alt="CSC295W Project 3" class="nameimg" />
		</div>
		<div id="bar">
<?php
                        print "<p>&nbsp; Logged in as: {$_SESSION['name']} &nbsp;";
                        $res = mysql_query("SELECT * FROM user WHERE name = '{$_SESSION['name']}' AND "
                                ."email = '{$_SESSION['mail']}'",$link);
                        $resset = mysql_fetch_array($res);
                        print "&nbsp; - &nbsp; &nbsp;<a href=\"users.php?user={$resset['User_ID']}\">User Info</a>";
                        print '&nbsp; &nbsp; - &nbsp; &nbsp;<a href="logout.php">Logout</a></p>'; 
?>
		</div>
		<div id="top">
			<img src="images/top.gif" width="765" height="33" alt="" />
		</div>
		
		<!--<ul id="horizontal">
			<li><a href="http://courses.ncsu.edu/csc295w/lec/001/index.html">CSC295W</a></li>
			<li><a href="http://www.ncsu.edu">NC State Home</a></li>
			<li><a href="mailto:mtklawit@ncsu.edu">Contact Me</a></li>
		</ul>-->
		<div id="content">
<?php
	print "<h1>Sample Details: {$resultset['protein']}</h1><br />";
/*	if( isset($_POST['notify']) ){
        $result = mysql_query("SELECT DISTINCT p3_User.Email AS Email, p3_User.Name AS Name FROM p3_User JOIN p3_Server ON "
				."p3_Server.Client_ID = p3_User.Client_ID WHERE p3_Server.Rack_ID = '{$rack}'", $link);
        while( $resultsArray = mysql_fetch_array($result)){
                $header = "From: {$_SESSION['name']} <{$_SESSION['mail']}>\n X-Mailer: PHP 5.x";
                mail($resultsArray['Email'], "CSC295w Project Servers Down for Maintenance","Mr./Ms. {$resultsArray['Name']}:  This is an automated email to notify you of maintenance on your server for the CSC295w Project.  Please check with the admins for notification of maintenance completion.",$header);
        }
}*/
	$check = 0;
        $client2 = mysql_query("SELECT user.user_ID FROM user JOIN sample ON sample.user_ID = user.user_ID WHERE "
			."sample.sample_ID = '{$sample}'",$link);
	while($clients2 = mysql_fetch_array($client2)){
		if( $clients2['user_ID'] == $_SESSION['UID'] ) $check = 1;
	}
	if(session_is_registered('login') && $_SESSION['access'] == 9001) {
        ?>
        <form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?rack={$rack}"; ?>">
        <input type="submit" name="notify" value="Notify This Rack of Maintenance" />
        <br />
        <br />
        </form>
        <?php
	}
	if( session_is_registered('login') && ($_SESSION['access'] >= 10) || ($check == 1)) 
	{
	$tripinfo=mysql_fetch_array(mysql_query("SELECT * FROM trip WHERE trip_ID={$resultset['trip_ID']}"));
	$userinfo=mysql_fetch_array(mysql_query("SELECT * FROM user WHERE user_ID={$resultset['user_ID']}"));
	print "<b>Sample ID:</b> {$resultset['sample_ID']}<br />";
	print "<b>Trip Date:</b> {$tripinfo['trip_date']}<br />";
	print "<b>User:</b> {$userinfo['name']}<br />";
	print "<b>Experiment Notes:</b> {$resultset['e_notes']}<br />";
	print "<b>Collection Notes:</b> {$resultset['c_notes']}<br />";
	if($resultset['screen']==1)
		$didscreen="checked";
	else
	 	$didscreen=" ";
	if($resultset['collect']==1)
		$didcollect="checked";
	else
	 	$didcollect=" ";
	if($resultset['process']==1)
		$didprocess="checked";
	else
	 	$didprocess=" ";
	print "<b>Screened:</b> <INPUT TYPE=CHECKBOX {$didscreen} disabled=\"disabled\"/><br />";
	print "<b>Collected:</b> <INPUT TYPE=CHECKBOX {$didcollect} disabled=\"disabled\"/><br />";
	print "<b>Processed:</b> <INPUT TYPE=CHECKBOX {$didprocess} disabled=\"disabled\"/><br />";
	print "<b>Resolution:</b> {$resultset['resolution']}<br />";
	print "<b>Spacegroup:</b> {$resultset['space_group']}<br />";
	print "<b><u>Unit Cell Parameters</b></u><br />";
	print "<b>a:</b> {$resultset['a']} <b>alpha:</b> {$resultset['alpha']}<br />";
	print "<b>b:</b> {$resultset['b']} <b>beta:</b> {$resultset['beta']}<br />";
	print "<b>c:</b> {$resultset['c']} <b>gamma:</b> {$resultset['gamma']}<br />";
	print "<b>Beamline:</b> {$resultset['beamline']}<br />";
	print "<b>Detector:</b> {$resultset['detector']}<br />";
	print "<b>Completeness:</b> {$resultset['completeness']}<br />";
	print "<b>Reflections:</b> {$resultset['reflections']}<br />";
	print "<b>Exposure Time:</b> {$resultset['time']} second(s)<br />";
	print "<b>Cane Label:</b> {$resultset['cane_color']} {$resultset['cane_number']} <b>Position:</b> {$resultset['cane_position']}"; 
	/* $samples = mysql_query("SELECT p3_Client.* FROM p3_Client JOIN p3_Server ON p3_Server.Client_ID = p3_Client.Client_ID WHERE "
			."p3_Server.Rack_ID = {$rack} AND p3_Client.Client_ID = {$_SESSION['login']} GROUP BY p3_Server.Client_ID "
			."ORDER BY p3_Client.Name", $link);
	if( mysql_num_rows($client) > 0 )
	{ print "<ul>";
	while ($samples = mysql_fetch_array($client)) {
		print "<li>Client: <a href=\"clientDetails.php?client={$clients['Client_ID']}\">{$clients['Name']}</a>";
                print "<ul>";
                $server = mysql_query("SELECT * FROM p3_Server WHERE ((Client_ID = '{$clients['Client_ID']}') && (Rack_ID = {$rack})) ORDER BY p3_Server.Name",$link);
		if( mysql_num_rows($server) > 0 ) {
		while ($servers = mysql_fetch_array($server)) {
                        print "<li>Server: <a href=\"serverDetails.php?server={$servers['Server_ID']}\">{$servers['Name']}</a>"; 
                        print "<p>IP Addresses: </p><ul>";
			$ip = mysql_query("SELECT * FROM p3_IP WHERE Server_ID = '{$servers['Server_ID']}' ORDER BY p3_IP.Address",$link);
			if( mysql_num_rows($ip) > 0) {
			while ($ips = mysql_fetch_array($ip)) {
				print "<li>{$ips['Address']}</li>";
			}
			}
			else print "<li>None</li>";
                        print "</ul></li>";  
              	}
		}
		else print "<li><ul><li>No Servers Found</li>";
                print "</ul><br /></li>";
	}
	}
	else print "<li>No Samples Found</li>";*/
	print "</ul>";
	}
	else print "You are not Authorized to view this page.";
?>
		</div>
<?php
if(session_is_registered('login') && $_SESSION['access'] > 0) {
?>
		<div id="nav">
			<img src="images/side_top.gif" width="184" height="23" alt="" />
			<a href="index.php"><img border="0" src="images/button1.gif" width="184" height="31" alt="Home" /></a>
			<a href="addSample.php"><img border="0" src="images/button2.gif" width="184" height="35" alt="Add Sample" /></a>
			<a href="mySample.php"><img border="0" src="images/button3.gif" width="184" height="36" alt="View my samples" /></a>
			<a href="addTrip.php"><img border="0" src="images/button4.gif" width="184" height="31" alt="Add Trip" /></a>
		<!--	<a href="manageIP.php"><img border="0" src="images/button5.gif" width="184" height="35" alt="Manage IP's" /></a>-->
			<img src="images/side_bottomcopy.gif" alt="" />
		</div>
<?php
}
else {
print "<div id=\"nav\">";
print '<img src="images/side_top.gif" width="184" height="23" alt="" />';
print '<a href="index.php"><img border="0" src="images/button1.gif" width="184" height="31" alt="Home" /></a>';
print '<img src="images/side_bottomcopy.gif" alt="" /></div>';
}
?>

	<div id="footer">
		<hr />
		<p>&copy; 2010 by Bradley Kearney.</p>
		<p>Feedback or questions? | E-mail the <a href="mailto:bmkearne@ncsu.edu">Webmaster</a>.</p>
	</div>
	</div>
	
</body>
</html>
