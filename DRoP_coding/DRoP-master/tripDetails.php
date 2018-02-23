<?php
session_start();
require("config.php");
$rack = $_GET['rack'];
$query = "SELECT * FROM Rack WHERE Rack_ID = '{$rack}'";
$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
$resultset = mysql_fetch_array($results);
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
	print "<title>CSC295W Project 3 - Rack Details: {$resultset['Name']}</title>";
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
                        $res = mysql_query("SELECT * FROM p3_User WHERE Name = '{$_SESSION['name']}' AND "
                                ."Email = '{$_SESSION['mail']}'",$link);
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
	print "<h1>Rack Details: {$resultset['Name']}</h1><br />";
	if( isset($_POST['notify']) ){
        $result = mysql_query("SELECT DISTINCT p3_User.Email AS Email, p3_User.Name AS Name FROM p3_User JOIN p3_Server ON "
				."p3_Server.Client_ID = p3_User.Client_ID WHERE p3_Server.Rack_ID = '{$rack}'", $link);
        while( $resultsArray = mysql_fetch_array($result)){
                $header = "From: {$_SESSION['name']} <{$_SESSION['mail']}>\n X-Mailer: PHP 5.x";
                mail($resultsArray['Email'], "CSC295w Project Servers Down for Maintenance","Mr./Ms. {$resultsArray['Name']}:  This is an automated email to notify you of maintenance on your server for the CSC295w Project.  Please check with the admins for notification of maintenance completion.",$header);
        }
}
	$check = 0;
        $client2 = mysql_query("SELECT p3_Client.Client_ID FROM p3_Client JOIN p3_Server ON p3_Server.Client_ID = p3_Client.Client_ID WHERE "
			."p3_Server.Rack_ID = '{$rack}'",$link);
	while($clients2 = mysql_fetch_array($client2)){
		if( $clients2['Client_ID'] == $_SESSION['login'] ) $check = 1;
	}
	if(session_is_registered('login') && $_SESSION['login'] == 0) {
        ?>
        <form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?rack={$rack}"; ?>">
        <input type="submit" name="notify" value="Notify This Rack of Maintenance" />
        <br />
        <br />
        </form>
        <?php
	}
	if( session_is_registered('login') && ($_SESSION['login'] == 0) || ($check == 1)) {
	if( $_SESSION['login'] == 0 )
	$client = mysql_query("SELECT p3_Client.* FROM p3_Client JOIN p3_Server ON p3_Server.Client_ID = p3_Client.Client_ID WHERE "
			."p3_Server.Rack_ID = '{$rack}' GROUP BY p3_Server.Client_ID ORDER BY p3_Client.Name",$link);
	else $client = mysql_query("SELECT p3_Client.* FROM p3_Client JOIN p3_Server ON p3_Server.Client_ID = p3_Client.Client_ID WHERE "
			."p3_Server.Rack_ID = {$rack} AND p3_Client.Client_ID = {$_SESSION['login']} GROUP BY p3_Server.Client_ID "
			."ORDER BY p3_Client.Name", $link);
	if( mysql_num_rows($client) > 0 ){ print "<ul>";
	while ($clients = mysql_fetch_array($client)) {
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
	else print "<li>No Clients Found</li>";
	print "</ul>";
	}
	else print "You are not Authorized to view this page.";
?>
		</div>
<?php
if(session_is_registered('login') && $_SESSION['login'] == 0) {
?>
		<div id="nav">
			<img src="images/side_top.gif" width="184" height="23" alt="" />
			<a href="index.php"><img border="0" src="images/button1.gif" width="184" height="31" alt="Home" /></a>
			<a href="clients.php"><img border="0" src="images/button2.gif" width="184" height="35" alt="Clients" /></a>
			<a href="addClient.php"><img border="0" src="images/button3.gif" width="184" height="36" alt="Add Client" /></a>
			<a href="addServer.php"><img border="0" src="images/button4.gif" width="184" height="31" alt="Add Server" /></a>
			<a href="manageIP.php"><img border="0" src="images/button5.gif" width="184" height="35" alt="Manage IP's" /></a>
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
		<p>&copy; 2007 by Matt Klawiter and Brad Kearney.</p>
		<p>Feedback or questions? | E-mail the <a href="mailto:mtklawit">Webmaster</a>.</p>
	</div>
	</div>
	
</body>
</html>
