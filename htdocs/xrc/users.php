<?php
session_start();
require("config.php");
if( isset($_POST['email']) ) {
        $results = mysql_query("SELECT name, user_ID FROM user WHERE email = '{$_POST['email']}' AND password = md5('{$_POST['psswrd']}')",$link);
        if(mysql_num_rows($results) == 1) {
                $resultsArray = mysql_fetch_array($results);
                session_register('login');
                $_SESSION['access'] = $resultsArray['level'];
                $_SESSION['name'] = $resultsArray['name'];
                $_SESSION['mail'] = $resultsArray['email'];
				$_SESSION['UID'] = $resultsArray['user_ID'];
        }
}
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
	<link type="text/css" media="screen, handheld" href="CSS/style.css" rel="stylesheet" />
	<link type="text/css" media="print, projection" href="CSS/print.css" rel="stylesheet" />
	<title>Mattos Lab Crystallography Database - User Management</title>

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
			$res = mysql_query("SELECT * FROM User WHERE Name = '{$_SESSION['name']}' AND "
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
			<h1>User Details</h1>
			<br />
			
<?php
if( !session_is_registered('login') ) {
	print 'You are not authorized to view this page.';
}
else {
	if( isset($_POST['setmanpw']))
	{
		$res = mysql_query("UPDATE user SET password = '{$_POST['manpw']}' WHERE user_ID = {$_GET['user']}",$link);
		print "New Password Set.";
	}
	if( isset($_POST['submit'])){
		$res = mysql_query("SELECT user_ID FROM user WHERE name = '{$_SESSION['name']}' AND "
			."email = '{$_SESSION['mail']}'",$link);
		$resset = mysql_fetch_array($res);
		if( $resset['user_ID'] == $_GET['user'] ) {
			print "You cannot edit your own details.";
		}
		else {
		$res = mysql_query("UPDATE user SET name = '{$_POST['name']}', email = '{$_POST['email']}', "
			."Client_ID = {$_POST['client']} WHERE user_ID = {$_GET['user']}",$link);
		print "User Details Updated";
		}
	}
	if( isset($_POST['reset'])){
		$res = mysql_query("UPDATE User SET Password = '{$_POST['pswd']}' WHERE User_ID = {$_GET['user']}",$link);
		$res = mysql_query("SELECT Name, Email From User WHERE User_ID = {$_GET['user']}",$link);
		$resarray = mysql_fetch_array($res);
		$header = "From: {$_SESSION['name']} <{$_SESSION['mail']}>\n X-Mailer: PHP 5.x";
                mail($resarray['Email'], "CSC295w Project 3 Password Reset","Mr./Ms. {$resarray['name']}:  This is an automated email to notify you that your password has been reset.  Your new password is:  {$_POST['pswd']}",$header);
		print "Password Reset";
	}
	if(session_is_registered('login') && isset($_GET['del']) && $_SESSION['access'] == 50){
                $rem = mysql_query("DELETE FROM user WHERE user_ID = {$_GET['del']}",$link);
                print "User Deleted";
        }


	
	$check = mysql_query("SELECT user_ID FROM user WHERE name = '{$_SESSION['name']}' AND email = '{$_SESSION['mail']}'",$link);
	$checks = mysql_fetch_array($check);
	if( $_SESSION['login'] == 0 ) {if($_SESSION['access']==50)
{
?>
		<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?user={$_GET['user']}"; ?>">
<?php		
			$res = mysql_Query("SELECT * FROM user WHERE user_ID = '{$_GET['user']}'",$link);
			$resset = mysql_fetch_array($res);
			/*print "<table><tr><td>Name: </td><td><input type=\"text\" name=\"name\" value=\"{$resset['name']}\" /></td></tr>";
			print "<tr><td>Email: </td><td><input type=\"text\" name=\"email\" value=\"{$resset['email']}\" /></td></tr>";
			print "<tr><td>Client: </td><td>";
			print "</td></tr></table>";
			print "<input type=\"submit\" name=\"submit\" value=\"Update Client\" />";
		print "</form>";
		print "<form method=\"post\" action=\"{$_SERVER['PHP_SELF']}?user={$_GET['user']}\" >";
			$ps = "hi2ucreateRandomPassword()";
			print "<input type=\"hidden\" name=\"pswd\" value=\"{$ps}\" />";
			print "<br /><input type=\"submit\" name=\"reset\" value=\"Reset Password\" />";*/
?>
		</form>
		<!--<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?user={$_GET['user']}"; ?>">
		Set New password: <input type="password" name="manpw" /> <input type="hidden" name="setmanpw" /><br/>
		<input type="submit" name="submitnewpw" value="Submit" />
		</form>-->
<?php
		print "<br /><br /><a href=\"addUser.php\">Add New User</a>";
		print '<br /><hr /><ul>';

		$results = mysql_query("SELECT * FROM user ORDER BY name", $link);
		while($resultset = mysql_fetch_array($results)){
			print "<li>User: <a href=\"users.php?user={$resultset['user_ID']}\">{$resultset['name']}</a>";
			print "&nbsp; &nbsp; &nbsp;<a href=\"users.php?user={$_GET['user_ID']}&del={$resultset['user_ID']}\">";
	                print '<img src="images/delete.gif" alt="Delete" width="30" height="30" class="linkimg" /></a>';
			print "<br />Email: {$resultset['email']}<br /><br /></li>";
		}
		}
	}
	else if($checks['user_ID'] == $_GET['user']){
?>
		<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?user={$_GET['user']}"; ?>">
<?php
			$res = mysql_Query("SELECT * FROM user WHERE user_ID = '{$_GET['user']}'",$link);
            $resset = mysql_fetch_array($res);
            print "<table><tr><td>Name: </td><td>{$resset['name']}</td></tr>";
            print "<tr><td>Email: </td><td>{$resset['email']}</td></tr>";
			$ps = "hi2ucreateRandomPassword";
                        print "<input type=\"hidden\" name=\"pswd\" value=\"{$ps}\" />";
                        print "</tr><td><input type=\"submit\" name=\"reset\" value=\"Reset Password\" /></td></tr></table>";

?>
		</form>
		<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?user={$_GET['user']}"; ?>">
		Set New password: <input type="password" name="manpw" /> <input type="hidden" name="setmanpw" /><br/>
		<input type="submit" name="submitnewpw" value="Submit" />
		</form>
<?php
	}
	print '</ul>';
}
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
