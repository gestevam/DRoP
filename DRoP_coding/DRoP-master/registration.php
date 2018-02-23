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
			<img src="images/trypsin.png" width="184" height="93" alt="" class="headimg" />
			<img src="images/logo2.png" width="581" height="93" alt="DRoP" class="nameimg" />
		</div>
		<div id="bar">
<?php
    print "New User Registration";
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
		if(isset($_POST['password']) && empty($_POST['password']))
			print "No password entered.";
		else
		{
			$pw = $_POST['password'];
			$insert_query = "INSERT INTO users VALUES (Default, '{$_POST['login']}', MD5('{$pw}'), '{$_POST['email']}', '{$_POST['name']}', Default,'{$_POST['organization']}','{$_POST['department']}','{$_POST['address']}','{$_POST['city']}','{$_POST['state']}','{$_POST['zip']}','{$_POST['country']}')";
			$insert_results = mysql_query($insert_query, $link) or die('Invalid Query:'.mysql_error());
			print "Successfully added user {$_POST['login']}. Now redirecting to main page.";
			unset($_POST);
			$done=True;
			print '<meta http-equiv="Refresh" content="5; URL=index.php" />';
		}
		}
		}
}
else
		print "Invalid input in one or more required fields.";
		
	}
	//else
	{
?>

<?php
if(!$done && (session_is_registered('login') && $_SESSION['access'] >= 10 or 1)) {
?>
			<h1>Add New User</h1>
			<br />
			<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
			<table width="90%">
				<tr>
					<th width="20%">Name</th>
					<td><input type="text" size="30" maxlength="50" name="name" value="<?php print "{$_POST['name']}";?>" /></td>
				</tr>
				<tr>
					<td>Email</td> 
					<td><input type="text" size="30" maxlength="50" name="email" value="<?php print "{$_POST['email']}";?>" /></td>
				</tr>
				<tr>
					<td>Username</td> 
					<td><input type="text" size="30" maxlength="50" name="login" value="<?php print "{$_POST['login']}";?>" /></td>
				</tr>
				<tr>
					<td>Password</td> 
					<td><input type="password" size="30" maxlength="50" name="password" value="" /></td>
				</tr>
				<tr>
					<td>Organization</td> 
					<td><input type="text" size="30" maxlength="100" name="organization" value="<?php print "{$_POST['organization']}";?>" /></td>
				</tr>
				<tr>
					<td>Department</td> 
					<td><input type="text" size="30" maxlength="100" name="department" value="<?php print "{$_POST['department']}";?>" /></td>
				</tr>
				<tr>
					<td>Street Address</td> 
					<td><input type="text" size="30" maxlength="100" name="address" value="<?php print "{$_POST['address']}";?>" /></td>
				</tr>
				<tr>
					<td>City</td> 
					<td><input type="text" size="30" maxlength="25" name="city" value="<?php print "{$_POST['city']}";?>" /></td>
				</tr>
				<tr>
					<td>State/Province </td> 
					<td><input type="text" size="30" maxlength="35" name="state" value="<?php print "{$_POST['state']}";?>" /></td>
				</tr>
				<tr>
					<td>Postal Code</td> 
					<td><input type="text" size="30" maxlength="15" name="zip" value="<?php print "{$_POST['zip']}";?>" /></td>
				</tr>
				<tr>
					<td>Country</td> 
					<td><input type="text" size="30" maxlength="36" name="country" value="<?php print "{$_POST['country']}";?>" /></td>
				</tr>
			</table>
			<br />
				<p>
					<input type="image" src="images/check.gif" name="Add User" alt="Edit" /><br />
					Register Account
				</p>
				<input type="hidden" name="form_submit" />
				</form>
			<br />
<?php 
	}
	else
	if (!$done)
		print "You are not authorized to view this page.";
	}
?>
		</div>
<?php
if(1 or session_is_registered('login') && $_SESSION['access'] > 0) {
?>
		<div id="nav">
			<img src="images/side_top.gif" width="184" height="23" alt="" />
			<a href="index.php"><img border="0" src="images/button1.png" width="184" height="31" alt="Home" /></a>
			<a href="upload.php"><img border="0" src="images/button2.png" width="184" height="35" alt="Upload Files" /></a>
			<a href="server.php"><img border="0" src="images/button3.png" width="184" height="36" alt="Server Status" /></a>
			<a href="examples.php"><img border="0" src="images/button4.png" width="184" height="31" alt="Examples/Help" /></a>
			<a href="publications.php"><img border="0" src="images/button5.png" width="184" height="35" alt="Publications" /></a>
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
		<p>&copy; 2010-2013</p>
		<p>Feedback or questions? | E-mail <a href="mailto:c.mattos@neu.edu">Carla Mattos</a>.</p>
	</div>
	</div>
	
</body>
</html>
