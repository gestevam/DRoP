<?php
session_start();
require("config.php");
if(isset($_GET['client'])) {
	$rem = mysql_query("SELECT Server_ID FROM p3_Server WHERE Client_ID = {$_GET['client']}",$link);
	while($remget = mysql_fetch_array($rem)) {
		$remip = mysql_query("UPDATE p3_IP Set Server_ID = null WHERE Server_ID = {$remget['Server_ID']}",$link);
	}
        $rem = mysql_query("DELETE FROM p3_Server WHERE Client_ID = {$_GET['client']}",$link);
	$rem = mysql_query("DELETE FROM p3_User WHERE Client_ID = {$_GET['client']}", $link);
	$rem = mysql_query("DELETE FROM p3_Client WHERE Client_ID = {$_GET['client']}",$link);
}
$query = "SELECT * FROM p3_Client ORDER BY Name";
$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<?php
	if(!session_is_registered('login'))
                print '<meta http-equiv="Refresh" content="0; URL=index.php" />';
?>
	<link type="text/css" media="screen" href="CSS/style.css" rel="stylesheet" />
	<link type="text/css" media="print" href="CSS/print.css" rel="stylesheet" />
	<title>CSC295W Project 3 - Clients</title>

</head>
<body>
	<div id="wrapper">
		<div id="logo" class="clearfix">
			<img src="images/serverrackwide.gif" width="184" height="93" class="headimg" alt = "" />
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
			<h1>Clients</h1>
			<br />
			
                      	<!--<form method="post" action="<?php //echo $_SERVER['PHP_SELF'];?>" />-->
<?php
	if(session_is_registered('login') && $_SESSION['login'] == 0) {

	while( $clients = mysql_fetch_array($results) ) {
		print "<ul>";
		print "<li>{$clients['Name']}";
		print '<div class="content">';
		print "<a href=\"clientDetails.php?client={$clients['Client_ID']}\">";
		print '<img src="images/view.gif" alt="View" width="30" height="30" class="linkimg" /></a>';
		print '&nbsp; &nbsp;';
		print "<a href=\"clients.php?client={$clients['Client_ID']}\">";
		print '<img src="images/delete.gif" alt="View" width="30" height="30" class="linkimg" /></a>';
		//print "<input type=\"image\" src=\"images/delete.gif\" alt=\"Delete Client\" name=\"{$clients['Client_ID']}\"/>";
		print "</div><ul>";
		$used = mysql_fetch_array(mysql_query("SELECT COUNT(p3_IP.IP_ID) AS Used FROM p3_IP JOIN p3_Server ON "
			."p3_Server.Server_ID = p3_IP.Server_ID JOIN p3_Client ON p3_Client.Client_ID = p3_Server.Client_ID "
			."WHERE p3_Client.Client_ID = '{$clients['Client_ID']}'",$link));
		print "<li>IP Addresses Used: {$used['Used']}<br /><br /></li>";
		print '</ul><br /></li>';
		print "</ul>";
	}

	}
	else Print "You are not authorized to view this page.";
?>
	 	<!--<input type="hidden" name="form_submit" />
                </form>-->
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
