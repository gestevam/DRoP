<?php
session_start();
require("config.php");
if( isset($_POST['id']) ) {
        $results = mysql_query("SELECT name, level, email, PI, user_ID FROM user WHERE login = '{$_POST['id']}' AND password = MD5('{$_POST['psswrd']}')",$link);
        if(mysql_num_rows($results) == 1) {
                $resultsArray = mysql_fetch_array($results);
                $_SESSION['login']=1;
                $_SESSION['access'] = $resultsArray['level'];
                $_SESSION['name'] = $resultsArray['name'];
                $_SESSION['mail'] = $resultsArray['email'];
				$_SESSION['UID'] = $resultsArray['user_ID'];
				$_SESSION['PI'] = $resultsArray['PI'];
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
	if( $_SESSION['access'] == 50) {
	?>
	<!--<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
	<input type="submit" name="notify" value="Notify All Users of Maintenance" />-->
	</form>
	<?php
	}
	if($_SESSION['access'] == 50)
		$query = "SELECT * FROM trip ORDER BY trip_date DESC";
	else $query = "SELECT * FROM trip ORDER BY trip_date DESC";
	$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
print "<ul>";
	if(mysql_num_rows($results) > 0) {
		while($resultsArray = mysql_fetch_array($results)) {
			if($resultsArray['trip_ID']==0)
			{
			/*<a href=\"tripDetails.php?trip={$resultsArray['trip_ID']}\">*/
			print "<li>Trip: In House Collection</a>";
			if($_SESSION['access'] == 50)
			$samples = (mysql_query("SELECT * FROM sample WHERE sample.trip_ID = '{$resultsArray['trip_ID']}'"));
			else if($_SESSION['access'] == 10) $samples = (mysql_query("SELECT * FROM sample WHERE sample.trip_ID = '{$resultsArray['trip_ID']}' AND sample.PI='{$_SESSION['PI']}'"));
			else $samples = (mysql_query("SELECT * FROM sample WHERE sample.trip_ID = '{$resultsArray['trip_ID']}' AND sample.user_ID={$_SESSION['UID']}"));
			if(mysql_num_rows($samples) > 0)
			{
				while($sampleArray = mysql_fetch_array($samples))
				{
					$currentuser=mysql_fetch_array(mysql_query("SELECT name FROM user WHERE user_ID={$sampleArray['user_ID']}"));
					print "<p><a href=\"sampleDetails.php?sample={$sampleArray['sample_ID']}\">{$sampleArray['sample_ID']} User: {$currentuser['name']} Protein: {$sampleArray['protein']}</a> Cane: {$sampleArray['cane_color']} {$sampleArray['cane_number']} <b>Position:</b> {$sampleArray['cane_position']} </p>";
				}
			}
			print "</li>";
			}
			else
			{
			/*<a href=\"tripDetails.php?trip={$resultsArray['trip_ID']}\">*/
			print "<li>Trip: {$resultsArray['trip_date']}</a>";
			if($_SESSION['access'] == 50)
			$samples = (mysql_query("SELECT * FROM sample WHERE sample.trip_ID = '{$resultsArray['trip_ID']}'"));
			else if($_SESSION['access'] == 10) $samples = (mysql_query("SELECT * FROM sample WHERE sample.trip_ID = '{$resultsArray['trip_ID']}' AND sample.PI='{$_SESSION['PI']}'"));
			else $samples = (mysql_query("SELECT * FROM sample WHERE sample.trip_ID = '{$resultsArray['trip_ID']}' AND sample.user_ID={$_SESSION['UID']}"));
			if(mysql_num_rows($samples) > 0)
			{
				while($sampleArray = mysql_fetch_array($samples))
				{
					$currentuser=mysql_fetch_array(mysql_query("SELECT name FROM user WHERE user_ID={$sampleArray['user_ID']}"));
					print "<p><a href=\"sampleDetails.php?sample={$sampleArray['sample_ID']}\">{$sampleArray['sample_ID']} User: {$currentuser['name']} Protein: {$sampleArray['protein']} Cane: {$sampleArray['cane_color']} {$sampleArray['cane_number']} <b>Pos:</b> {$sampleArray['cane_position']}</a></p>";
				}
			}
			print "</li>";
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
