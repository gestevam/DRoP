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
	if(!session_is_registered('login') and 0)
                print '<meta http-equiv="Refresh" content="0; URL=index.php" />';
?>
	<link type="text/css" media="screen" href="CSS/style.css" rel="stylesheet" />
	<link type="text/css" media="print" href="CSS/print.css" rel="stylesheet" />
	<title>Detection of Related Solvent Positions - User Registration</title>

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
                        $res = mysql_query("SELECT * FROM users WHERE name = '{$_SESSION['name']}' AND "
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
	if(isset($_POST['form_submit']))
	{
if(!empty($_POST['name']) && !empty($_POST['email']))
{
  
		$query = "SELECT * FROM users WHERE email = '{$_POST['email']}'";
		$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
		if(mysql_num_rows($results) > 0)
			print "Error. User with identical email already exists. Only one user may be associated with an email.";
		else 
		{
		$query = "SELECT * FROM users WHERE login = '{$_POST['login']}'";
		$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
		if(mysql_num_rows($results) > 0)
			print "Error. User with identical login already exists. Only one user may be associated with a login.";
		else
		{
			$pw = $_POST['password'];
			$insert_query = "INSERT INTO users VALUES (Default, '{$_POST['login']}', MD5('{$pw}'), '{$_POST['email']}', '{$_POST['name']}', Default)";
			$insert_results = mysql_query($insert_query, $link) or die('Invalid Query:'.mysql_error());
			print "Successfully added user {$_POST['name']}";
		}
		}
}
else
		print "Invalid input in one or more required fields.";
		
	}
	else
	{
?>
			<h1>Add New User</h1>
			<br />
<?php
if(session_is_registered('login') && $_SESSION['access'] >= 10 or 1) {
?>
			<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
			<table width="90%">
				<tr>
					<th width="20%">Name</th>
					<td><input type="text" size="30" maxlength="50" name="name" value="" /></td>
				</tr>
				<tr>
					<td>Email</td> 
					<td><input type="text" size="30" maxlength="50" name="email" value="" /></td>
				</tr>
				<tr>
					<td>Username</td> 
					<td><input type="text" size="30" maxlength="50" name="login" value="" /></td>
				</tr>
				<tr>
					<td>Password</td> 
					<td><input type="password" size="30" maxlength="50" name="password" value="" /></td>
				</tr>
			</table>
			<br />
				<p align="center">
					<input type="image" src="images/check.gif" name="Add User" alt="Edit" />
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
if(session_is_registered('login') && $_SESSION['access'] > 0) {
?>
		<div id="nav">
			<img src="images/side_top.gif" width="184" height="23" alt="" />
			<a href="index.php"><img border="0" src="images/button1.gif" width="184" height="31" alt="Home" /></a>
			<a href="clients.php"><img border="0" src="images/button2.gif" width="184" height="35" alt="Clients" /></a>
			<a href="addClient.php"><img border="0" src="images/button3.gif" width="184" height="36" alt="Add Client" /></a>
			<a href="addSample.php"><img border="0" src="images/button4.gif" width="184" height="31" alt="Add Server" /></a>
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
		<p>&copy; 2010 by Bradley Kearney.</p>
		<p>Feedback or questions? | E-mail the <a href="mailto:bmkearne@ncsu.edu">Webmaster</a>.</p>
	</div>
	</div>
	
</body>
</html>
