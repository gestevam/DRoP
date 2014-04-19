<?php
session_start();
require("config.php");
if( isset($_POST['id']) ) {
	
        $results = mysql_query("SELECT name, email, user_ID FROM users WHERE login = '{$_POST['id']}' AND password = MD5('{$_POST['psswrd']}')",$link);
        if(mysql_num_rows($results) == 1) {
                $resultsArray = mysql_fetch_array($results);
                $_SESSION['login']=1;
		$_SESSION['access']=50;
                $_SESSION['name'] = $resultsArray['name'];
                $_SESSION['mail'] = $resultsArray['email'];
		$_SESSION['UID'] = $resultsArray['user_ID'];
        }
	else {$error = "Incorrect User Name/Password"; }
	}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<link type="text/css" media="screen, handheld" href="CSS/style.css" rel="stylesheet" />
	<link type="text/css" media="print, projection" href="CSS/print.css" rel="stylesheet" />
	<title>Detection of Related Solvent Positions</title>

</head>
<body>

	<div id="wrapper">
		<div id="logo" class="clearfix">
			<img src="images/trypsin.png" width="184" height="93" alt="" class="headimg" />
			<img src="images/logo2.png" width="581" height="93" alt="Crystallography Database" class="nameimg" />
		</div>
		<div id="bar">
<?php
if( session_is_registered('login') ) {
                        print "<p>&nbsp; Logged in as: {$_SESSION['name']} &nbsp;";
                        print '&nbsp; - &nbsp; &nbsp;<a href="users.php">User Info</a>';
			print '&nbsp; &nbsp; - &nbsp; &nbsp;<a href="logout.php">Logout</a></p>';
}
else print "Please Log In."; 
?>
		</div>
		<div id="top">
			<img src="images/top.gif" width="765" height="33" alt="" />
		</div>
		
		<div id="content">
			<h1>Overview</h1>
			<br />
<?php


if( !$_SESSION['login'] ) { print $error;
	?>
	<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
	<?php
	print "<table><tr><td>Username: &nbsp; &nbsp;</td>";
	print '<td><input type="text" size="30" maxlength="50" name="id" autocomplete="off" value="" /></td></tr>';
	print "<tr><td>Password: </td>";
	print '<td><input type="password" size="20" maxlength="20" name="psswrd" value="" /></td></tr>';
	print '<tr><td>&nbsp;</td><td><input type="submit" name="submit" value="Submit" /></td></tr></table>';
	print '</form>';
}
else {
print "<ul>";
	$query = "SELECT * FROM data_sets WHERE data_sets.user_ID={$_SESSION['UID']} ORDER BY data_ID";
	$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	if(mysql_num_rows($results) > 0) 
	{
		while($resultsArray = mysql_fetch_array($results)) 
		{
			print "<li>Run ID: {$resultsArray['data_ID']}<br />";
			if ($resultsArray['run_status']==1)
			{
				print "Run is completed. <br />";
				print "Click <a href=\"getresults.php?run={$resultsArray['data_ID']}\">Here</a>";

			}
		}	
	}	
print "</ul>";
}
?>
		
		</div>
<?php
if($_SESSION['login']==1 && $_SESSION['access'] > 0) {
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
