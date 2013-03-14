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
	<title>Mattos Lab Crystallography Database - Add Sample</title>
	<link type="text/css" media="print" href="CSS/print.css" rel="stylesheet" />

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
                        print "&nbsp; - &nbsp; &nbsp;<a href=\"users.php?user={$resset['User_ID']}\">User Info</a>";
                        print '&nbsp; &nbsp; - &nbsp; &nbsp;<a href="logout.php">Logout</a></p>'; 
?>
		</div>
		<div id="top">
			<img src="images/top.gif" width="765" height="33" alt="" />
		</div>

		<div id="content">
<?php
	if(isset($_POST['form_submit']) ) 
		if (empty($_POST['protein']))
			print "You have failed to enter your protein.";
		else if (empty($_POST['number']))
			print "You have failed to enter the cane number.";
		else
		{
			//Now Find if the cane position is taken for this trip.
			$query = "SELECT * FROM sample WHERE ((trip_ID = {$_POST['trip']}) && (cane_color = '{$_POST['color']}')&& (cane_number = {$_POST['number']}) &&(cane_position = {$_POST['position']}))";
			//$query = "SELECT * FROM sample WHERE ((trip_ID = {$_POST['trip']}) && (cane_color = {$_POST['color']}) && (cane_number = {$_POST['number']}) &&(cane_position = {$_POST['position']}))";
			$sample = mysql_query($query, $link) or die('Invalid Query - '.mysql_error());
			$sampleset = mysql_fetch_array($sample);
			if(mysql_num_rows($sample)>0||$_POST['trip']==0)
			{
				print "Uh oh! Something already exists in this position!";
			}
			else
			{
				$valid = 1;
				$query = "INSERT INTO sample VALUES (Default, '{$_POST['trip']}', {$_SESSION['UID']}, '{$_POST['protein']}', '{$_POST['e_notes']}', 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{$_POST['color']}', '{$_POST['number']}', '{$_POST['position']}', NULL, '{$resset['PI']}')";
				$insert_results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
			}
			/*$query = "SELECT * FROM p3_Client WHERE Client_ID = {$_POST['owner']}";
			$client = mysql_query($query, $link) or die('Invalid Query1: '.mysql_error());
			$clientset = mysql_fetch_array($client); 
			$query = "SELECT * FROM p3_IP";
			$ip = mysql_query($query, $link) or die('Invalid Query3: '.mysql_error());
			$ip_used = 0;
			$ip_checker = mysql_query("SELECT * FROM p3_Server WHERE Client_ID = '{$clientset['Client_ID']}'",$link)or die('Invalid Query3: '.mysql_error());
			if( mysql_num_rows($ip_checker) > 0 ) 
			{
				while ($ip_checking = mysql_fetch_array($ip_checker)) 
				{
					$ip_found = mysql_query("SELECT * FROM p3_IP WHERE Server_ID = '{$ip_checking['Server_ID']}'",$link);
					$ip_used=$ip_used+mysql_num_rows($ip_found);
				}
			}
		$query = "SELECT * FROM p3_Server WHERE ((Rack_ID = '{$_POST['rack']}') && (Name = '{$_POST['name']}'))";
		$namecheck = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
		$total = mysql_fetch_array(mysql_query("SELECT * FROM p3_Rack WHERE Rack_ID = '{$_POST['rack']}';",$link)); 
		$free = mysql_fetch_array(mysql_query("SELECT SUM(p3_Server.Size) AS Size FROM p3_Server"
		." WHERE p3_Server.Rack_ID = '{$_POST['rack']}';",$link));
		$freeunits = $total['Size'] - $free['Size'];
 if($freeunits < $_POST['size'])
	print "Not enough physical space on rack.<br/>";
else
{
		if(mysql_num_rows($namecheck) == 0)//No Server with that name on server
		{	
			$insert_query = "INSERT INTO p3_Server VALUES (Default, '{$_POST['rack']}', '{$_POST['owner']}', '{$_POST['name']}', {$_POST['size']}, '{$_POST['details']}')";
			$insert_results = mysql_query($insert_query, $link) or die('Invalid Query:'.mysql_error());
			print "Successfully added server {$_POST['name']}<br/>";
			$ip_count = $_POST['requestIP'];
			$query = "SELECT * FROM p3_Server WHERE ((Rack_ID = '{$_POST['rack']}') && (Name = '{$_POST['name']}'))";
			$newserver = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
			$newservers = mysql_fetch_array($newserver);
			$ip_count = $_POST['requestIP'];
				if($ip_count>0)
				{
					while(($ipset = mysql_fetch_array($ip)) && ($ip_count > 0)) 
					{
						if($ipset['Server_ID'] == null)
						{
							$ip_count--;
							$update_query = "UPDATE p3_IP SET Server_ID = '{$newservers['Server_ID']}' WHERE (Address = '{$ipset['Address']}')";
							$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
						}//endif
					}//endwhile
					if($ip_count == 0)
					{
						print "<br/>All requested IPs now allocated to server<br/>";
					}//endif	
					else
					{
						$ip_allocated = $_POST['requestIP']-$ip_count;
						print "{$ip_allocated} of {$_POST['requestIP']} allocated to server. Insufficient IPs to allocated all requested.<br/>";
					}//end while
		}//end if
}
		else 
			print "Server with same name already exists on this rack";
		}*/
	}


?>
			<h1>Add New Sample</h1>
			<br />
<?php
if(session_is_registered('login') && $_SESSION['access'] > 0 && $valid!=1) {
?>
			<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
			<table width="90%">
				<tr>
					<td width="20%">Trip: </td> 
					<td><select name="trip"><?php
					$query = "SELECT * FROM trip ORDER BY trip_date DESC";
					$rackresult = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
					while ($results = mysql_fetch_array($rackresult))
					{	
						print "<option value=\"{$results['trip_ID']}\">{$results['trip_date']} &nbsp;&nbsp;</option>";
					} ?>
					</select></td>
				</tr>
				<tr>
					<td>Protein: </td>
					<td><input type="text" size="15" maxlength="30" name="protein" value="<?php print $_POST['protein']; ?>" /></td>
				</tr>
				<tr>
					<td>Experimental Notes: </td>
					<td><textarea name="e_notes" cols="50" rows="5">Details</textarea></td>
				</tr>
				<tr>
                    <td>Cane Color: </td>
					<td><select name="color"><option value="Red"<?php if($_POST['color']=='Red') print "selected=yes"; ?>>Red&nbsp;&nbsp;</option>
					<option value="Yellow" <?php if($_POST['color']=='Yellow') print "selected=yes"; ?>>Yellow&nbsp;&nbsp;</option>
					<option value="White" <?php if($_POST['color']=='White') print "selected=yes"; ?>>White&nbsp;&nbsp;</option>
					<option value="Silver" <?php if($_POST['color']=='Silver') print "selected=yes"; ?>>Silver&nbsp;&nbsp;</option></select></td>
				</tr>
				<tr>
					<td>Cane Number: </td>
					<td><input type="text" size="15" maxlength="3" name="number" value="<?php print $_POST['number']; ?>" /></td>
				</tr>
				<tr>
					<td>Cane Position: </td>
					<td><select name="position"><option value="1" <?php if($_POST['position']==1) print "selected=yes"; ?>>1 (Top)&nbsp;&nbsp;</option>
					<option value="2" <?php if($_POST['position']==2) print "selected=yes"; ?>>2&nbsp;&nbsp;</option>
					<option value="3" <?php if($_POST['position']==3) print "selected=yes"; ?>>3&nbsp;&nbsp;</option>
					<option value="4" <?php if($_POST['position']==4) print "selected=yes"; ?>>4&nbsp;&nbsp;</option>
					<option value="5" <?php if($_POST['position']==5) print "selected=yes"; ?>>5&nbsp;&nbsp;</option>
					<option value="6" <?php if($_POST['position']==6) print "selected=yes"; ?>>6 (Bottom)&nbsp;&nbsp;</option></select></td>

				</tr>
			</table>
			<br />
				<p align="center"><input type="image" src="images/check.gif" name="Add Sample" /></p>
			<br />
				<input type="hidden" name="form_submit" />
				</form>
<?php
}
else if($valid==1) print "Sample added successfully.";
else print "You are not authorized to view this page.";
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
