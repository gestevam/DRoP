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
	<title>CSC295W Project 3 - Add New Client</title>

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
	if(isset($_POST['form_submit']))
	{
if(!empty($_POST['name']) && !empty($_POST['street']) && !empty($_POST['city']) && !empty($_POST['state']) && !empty($_POST['cName']) && !empty($_POST['cTel']) && !empty($_POST['cEmail']))
{
  
		$query = "SELECT * FROM p3_Client WHERE Name = '{$_POST['name']}'";
		$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
		if(mysql_num_rows($results) > 0)
			print "Error. Client with identical name already exists. Please use the Edit Client page to edit information.";
		else
		{
			$insert_query = "INSERT INTO p3_Client VALUES (Default, '{$_POST['name']}', '{$_POST['street']}', '{$_POST['city']}', '{$_POST['state']}', '{$_POST['cName']}', '{$_POST['cTel']}', '{$_POST['cEmail']}', 10 )";
			$insert_results = mysql_query($insert_query, $link) or die('Invalid Query:'.mysql_error());
			print "Successfully added client {$_POST['name']}";
		}
}
else
		print "Invalid input in one or more required fields.";
		
	}
	else
	{
?>
			<h1>Add New Client</h1>
			<br />
<?php
if(session_is_registered('login') && $_SESSION['login'] == 0) {
?>
			<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
			<table width="90%">
				<tr>
					<th width="20%">Name</th>
					<td><input type="text" size="30" maxlength="50" name="name" value="" /></td>
				</tr>
				<tr>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<th>Address</th>
				</tr>
				<tr>
					<td>Street</td> 
					<td><input type="text" size="30" maxlength="50" name="street" value="" /></td>
				</tr>
				<tr>
					<td>City</td>
					<td><input type="text" size="15" maxlength="30" name="city" value="" /></td>
				</tr>
				<tr>
                              <td>State</td>
					<td><input type="text" size="2" maxlength="2" name="state" value="" /></td>
				</tr>
				<tr>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<th>Primary Contact</th>
				</tr>
				<tr>
					<td>Name</td>
					<td><input type="text" size="50" maxlength="70" name="cName" value="" /></td>
				</tr>
				<tr>
					<td>Telephone</td>
					<td><input type="text" size="12" maxlength="20" name="cTel" value="" /></td>
				</tr>
				<tr>
					<td>E-mail</td>
					<td><input type="text" size="30" maxlength="50" name="cEmail" value="" /></td>
				</tr>
				<tr>
					<td>&nbsp;</td>
				</tr>
			</table>
			<br />
				<p align="center">
					<input type="image" src="images/check.gif" name="Add Client" alt="Edit" />
				</p>
				<input type="hidden" name="form_submit" />
				</form>
			<br />
<?php 
	}
	else Print "You are not authorized to view this page.";
	}
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
