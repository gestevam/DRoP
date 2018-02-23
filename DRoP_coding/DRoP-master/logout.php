<?php
session_start();
$_SESSION = array();
if (isset($_COOKIE[session_name()])) {
    setcookie(session_name(), '', time()-42000, '/');
}
session_destroy();
require("config.php");
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta http-equiv="Refresh" content="5; URL=index.php" />
	<link type="text/css" media="screen, handheld" href="CSS/style.css" rel="stylesheet" />
	<link type="text/css" media="print, projection" href="CSS/print.css" rel="stylesheet" />
	<title>Detection of Related Solvent Positions Server</title>

</head>
<body>
	<div id="wrapper">
		<div id="logo" class="clearfix">
			<img src="images/trypsin.png" width="184" height="93" alt="" class="headimg" />
			<img src="images/logo2.png" width="581" height="93" alt="DRoP" class="nameimg" />
		</div>
		<div id="bar">
			<p>&nbsp;</p>
		</div>
		<div id="top">
			<img src="images/top.gif" width="765" height="33" alt="" />
		</div>

		<div id="content">
			<h1>Logout Successful. Returning to index.</h1>
			<br />
		
		</div>
<?php
if(session_is_registered('login') && $_SESSION['login'] == 0 || 1) {
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
