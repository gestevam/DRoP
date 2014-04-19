<?php
session_start();
require("config.php");
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
	<title>Mattos Lab Crystallography Database - Add Collection Trip</title>

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
                        $res = mysql_query("SELECT * FROM user WHERE Name = '{$_SESSION['name']}' AND "
                                ."Email = '{$_SESSION['mail']}'",$link);
                        $resset = mysql_fetch_array($res);
                        print "&nbsp; - &nbsp; &nbsp;<a href=\"users.php?user={$_SESSION['UID']}\">User Info</a>";
                        print '&nbsp; &nbsp; - &nbsp; &nbsp;<a href="logout.php">Logout</a></p>';
?>
		</div>
		<div id="top">
			<img src="images/top.gif" width="765" height="33" alt="" />
		</div>

		<div id="content">
<?php 
	if(isset($_POST['form_submit']))
	{
		$ymd="{$_POST['year']}-{$_POST['month']}-{$_POST['day']}";
		$query = "SELECT * FROM trip WHERE trip_date = '{$ymd}'";
		$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
		if(mysql_num_rows($results) > 0)
			print "Error. Trip for this date already exists!";
		else
		{
			$insert_query = "INSERT INTO trip VALUES (Default, '{$ymd}', ' ', Default)";
			$insert_results = mysql_query($insert_query, $link) or die('Invalid Query:'.mysql_error());
			print "Successfully added trip for {$ymd}";
		}	
	}
	else
	{
?>
			<h1>Add New Trip</h1>
			<br />
<?php
if(session_is_registered('login') && $_SESSION['access'] >= 10) {
?>
			<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
                    Month: 
					<select name="month"><option value="1">Jan&nbsp;&nbsp;</option>
					<option value="2">Feb&nbsp;&nbsp;</option>
					<option value="3">Mar&nbsp;&nbsp;</option>
					<option value="4">Apr&nbsp;&nbsp;</option>
					<option value="5">May&nbsp;&nbsp;</option>
					<option value="6">Jun&nbsp;&nbsp;</option>
					<option value="7">Jul&nbsp;&nbsp;</option>
					<option value="8">Aug&nbsp;&nbsp;</option>
					<option value="9">Sep&nbsp;&nbsp;</option>
					<option value="10">Oct&nbsp;&nbsp;</option>
					<option value="11">Nov&nbsp;&nbsp;</option>
					<option value="12">Dec&nbsp;&nbsp;</option></select>
                    Day: 
					<select name="day"><option value="1">1&nbsp;&nbsp;</option>
					<option value="2">2&nbsp;&nbsp;</option>
					<option value="3">3&nbsp;&nbsp;</option>
					<option value="4">4&nbsp;&nbsp;</option>
					<option value="5">5&nbsp;&nbsp;</option>
					<option value="6">6&nbsp;&nbsp;</option>
					<option value="7">7&nbsp;&nbsp;</option>
					<option value="8">8&nbsp;&nbsp;</option>
					<option value="9">9&nbsp;&nbsp;</option>
					<option value="10">10&nbsp;&nbsp;</option>
					<option value="11">11&nbsp;&nbsp;</option>
					<option value="12">12&nbsp;&nbsp;</option>
					<option value="13">13&nbsp;&nbsp;</option>
					<option value="14">14&nbsp;&nbsp;</option>
					<option value="15">15&nbsp;&nbsp;</option>
					<option value="16">16&nbsp;&nbsp;</option>
					<option value="17">17&nbsp;&nbsp;</option>
					<option value="18">18&nbsp;&nbsp;</option>
					<option value="19">19&nbsp;&nbsp;</option>
					<option value="20">20&nbsp;&nbsp;</option>
					<option value="21">21&nbsp;&nbsp;</option>
					<option value="22">22&nbsp;&nbsp;</option>
					<option value="23">23&nbsp;&nbsp;</option>
					<option value="24">24&nbsp;&nbsp;</option>
					<option value="25">25&nbsp;&nbsp;</option>
					<option value="26">26&nbsp;&nbsp;</option>
					<option value="27">27&nbsp;&nbsp;</option>
					<option value="28">28&nbsp;&nbsp;</option>
					<option value="29">29&nbsp;&nbsp;</option>
					<option value="30">30&nbsp;&nbsp;</option>
					<option value="31">31&nbsp;&nbsp;</option></select>
					Year: 
					<select name="year">
					<option value="2012">2012&nbsp;&nbsp;</option>
					<option value="2002">2002&nbsp;&nbsp;</option>
					<option value="2003">2003&nbsp;&nbsp;</option>
					<option value="2004">2004&nbsp;&nbsp;</option>
					<option value="2005">2005&nbsp;&nbsp;</option>
					<option value="2006">2006&nbsp;&nbsp;</option>
					<option value="2007">2007&nbsp;&nbsp;</option>
					<option value="2008">2008&nbsp;&nbsp;</option>
					<option value="2009">2009&nbsp;&nbsp;</option>
					<option value="2010">2010&nbsp;&nbsp;</option>
					<option value="2011">2011&nbsp;&nbsp;</option>
					</select>
			<br />
				<p align="center">
					<input type="image" src="images/check.gif" name="Add Trip" alt="Edit" />
				</p>
				<input type="hidden" name="form_submit" />
				</form>
			<br />
<?php 
	}
	else Print "You are not authorized to view this page. Please contact an administrator to add a trip.";
	}
?>
		</div>
<?php
if(session_is_registered('login') && $_SESSION['access'] >= 1) {
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
