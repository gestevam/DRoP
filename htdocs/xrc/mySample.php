<?php
session_start();
require("config.php");
$sample = $_GET['sample'];
$query = "SELECT * FROM sample WHERE sample_ID = '{$sample}'";
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

		<div id="content">
		<?php
		if(isset($_POST['form2_submit']))
		{
			$valid=3;
			
		}
		else
		if(isset($_POST['form3_submit']))
		{	
		if($_POST['screen']=="on")
			$screen=1;
		else
			$screen=0;
		if($_POST['collect']=="on")
			$collect=1;
		else
			$collect=0;
		if($_POST['process']=="on")
			$process=1;
		else
			$process=0;
		/*	print "Screened  {$screen} <br/>";
			print "Collected  {$collect}<br/>";
			print "Processed  {$process}<br/>";
			print "a  {$screen} <br/>";
			print "b  {$collect}<br/>";
			print "c  {$process}<br/>";
			print "alpha  {$screen} <br/>";
			print "beta  {$collect}<br/>";
			print "gamma  {$process}<br/>";
			print "{$_POST['e_notes']}";*/
			$query = "UPDATE sample SET e_notes=\"{$_POST['e_notes']}\", screen={$screen}, collect={$collect}, process={$process}, a=\"{$_POST['a']}\", b=\"{$_POST['b']}\", c=\"{$_POST['c']}\", alpha=\"{$_POST['alpha']}\", beta=\"{$_POST['beta']}\", gamma=\"{$_POST['gamma']}\",resolution=\"{$_POST['res']}\", space_group=\"{$_POST['sg']}\", beamline=\"{$_POST['beamline']}\", detector=\"{$_POST['detector']}\", completeness=\"{$_POST['completeness']}\", reflections=\"{$_POST['reflections']}\", time=\"{$_POST['time']}\", c_notes=\"{$_POST['c_notes']}\" WHERE sample_ID={$_POST['SID']}";
			$update = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
			$valid=4;
		}
		else
	if(isset($_POST['form1_submit']) ) 
		if (!isset($_POST['form2_submit']))
			$valid=1;
?>
<?php
if(session_is_registered('login') && $_SESSION['access'] > 0 && $valid==0) {
?>
<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
			<table width="90%">
				<tr>
					<td width="20%">Trip: </td> 
					<td><select name="trip"><?php
					/*WHERE active = 1*/
					$query = "SELECT * FROM trip ORDER BY trip_date DESC";
					$rackresult = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
					while ($results = mysql_fetch_array($rackresult))
					{	
						if($results['trip_ID']==0)
						print "<option value=\"{$results['trip_ID']}\">In House Collection &nbsp;&nbsp;</option>";
						else
						print "<option value=\"{$results['trip_ID']}\">{$results['trip_date']} &nbsp;&nbsp;</option>";
					} ?>
					</select></td>
				</tr>
			</table>
			<br />
				<p align="center"><input type="image" src="images/check.gif" name="Add Sample" /></p>
			<br />
				<input type="hidden" name="form1_submit" />
				</form>
<?php } 
else if(session_is_registered('login') && $_SESSION['access'] > 0 && $valid==1) {?>
			<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
			<table width="90%">
			<tr>
					<td width="20%">Sample: <select name="sample"><?php
					$query = "SELECT * FROM sample WHERE trip_ID = {$_POST['trip']}";
					$rackresult = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
					while ($results = mysql_fetch_array($rackresult))
					{	
/*						if($results['screen']==0)*/
						print "<option value=\"{$results['sample_ID']}\">{$results['sample_ID']} - {$results['protein']} &nbsp;&nbsp;</option>";
					} ?>
					</select></td>
				</tr>
			</table>
			<br />
				<p align="center"><input type="image" src="images/check.gif" name="Add Sample" /></p>
			<br />
				<input type="hidden" name="form2_submit" />
				</form>
<?php
}
else if($valid==3)
{ ?>
<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
			<table width="90%">
			<tr>
					<td width="20%">Sample: <select name="sample"><?php
					$query = "SELECT * FROM sample WHERE sample_ID = {$_POST['sample']}";
					$rackresult = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
					$results = mysql_fetch_array($rackresult);
					print "<option value=\"\">{$results['sample_ID']} - {$results['protein']} &nbsp;&nbsp;</option>";
					 ?>
					</td>
				</tr>
				<tr>
				<td>
						Collection Information<BR/>
<?php 	if($results['screen']==1)
		$didscreen="checked";
	else
	 	$didscreen=" ";
	if($results['collect']==1)
		$didcollect="checked";
	else
	 	$didcollect=" ";
	if($results['process']==1)
		$didprocess="checked";?>
						<b>Screened:</b> <INPUT TYPE=CHECKBOX name="screen" <?php print "{$didscreen}"; ?>><br/>
						<b>Collected:</b> <INPUT TYPE=CHECKBOX name="collect" <?php print "{$didcollect}"; ?>><br/>
						<b>Processed:</b> <INPUT TYPE=CHECKBOX name="process" <?php print "{$didprocess}"; ?>>
				</tr>
				<tr>
					<td>Experimental Notes: </td>
					<td><textarea name="e_notes" cols="50" rows="5"><?php print "{$results['e_notes']}"; ?></textarea></td>
				</tr>
				<tr>
					<td>Collection Notes: </td>
					<td><textarea name="c_notes" cols="50" rows="5"><?php print "{$results['c_notes']}"; ?></textarea></td>
				</tr>
				<tr>
                    <td>Crystal Information: </td>
					<td>a <input type="text" size="7" maxlength="7" name="a" value="<?php print "{$results['a']}"; ?>" /> alpha &nbsp;&nbsp;&nbsp;<input type="text" size="7" maxlength="7" name="alpha" value="<?php print "{$results['alpha']}"; ?>" /></td>
					<tr><td /><td>b <input type="text" size="7" maxlength="7" name="b" value="<?php print "{$results['b']}"; ?>" /> beta&nbsp;&nbsp;&nbsp;&nbsp; <input type="text" size="7" maxlength="7" name="beta" value="<?php print "{$results['beta']}"; ?>" /></td></tr>
					<tr><td /><td>c <input type="text" size="7" maxlength="7" name="c" value="<?php print "{$results['c']}"; ?>" /> gamma <input type="text" size="7" maxlength="7" name="gamma" value="<?php print "{$results['gamma']}"; ?>" /></td></tr>
					<tr><td /><td>Resolution <input type="text" size="7" maxlength="7" name="res" value="<?php print "{$results['resolution']}"; ?>" /> Space Group <input type="text" size="15" maxlength="15" name="sg" value="<?php print "{$results['space_group']}"; ?>" /></td></tr>
				</tr>
				<tr>
					<td>Other: </td>
					<td>Detector <input type="text" size="7" maxlength="7" name="detector" value="<?php print "{$results['detector']}"; ?>" /> Beamline &nbsp;&nbsp;&nbsp;<input type="text" size="7" maxlength="7" name="beamline" value="<?php print "{$results['beamline']}"; ?>" /></td>
					<tr><td /><td>Completeness <input type="text" size="7" maxlength="7" name="completeness" value="<?php print "{$results['completeness']}"; ?>" /> Reflections&nbsp;&nbsp;&nbsp;&nbsp; <input type="text" size="7" maxlength="7" name="reflections" value="<?php print "{$results['reflections']}"; ?>" /></td></tr>
					<tr><td /><td>Exposure Time <input type="text" size="7" maxlength="7" name="time" value="<?php print "{$results['time']}"; ?>" /></td></tr>
				</tr>
				<tr>
					<td>Cane Info: </td>
					<td>Label: <?php print "{$results['cane_color']} {$results['cane_number']}"; ?> Position: <?php print "{$results['cane_position']}"; ?></td>
					<td>
			</table>
			<br />
				<p align="center"><input type="image" src="images/check.gif" name="Add Sample" /></p>
			<br />
				<input type="hidden" name="form3_submit" />
				<input type="hidden" name="SID" value="<?php print "{$results['sample_ID']}";?>">
				</form>
<?php }
else if($valid==4) print "Updated Sucessfully";
else print "You are not authorized to view this page.";
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
