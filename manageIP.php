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
	<title>CSC295W Project 3 - Manage IP Addresses</title>

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
		<h1>Manage IP Addresses</h1>
		<br />

<?php
if(!session_is_registered('login')){
	print "You do not have permission to view this page.";
}
else {
if(isset($_POST['form_submit'])) {
	//$one = explode('.', $_POST['ip']);
	$one = ip2long($_POST['ip']);
	//$two = explode('.', $_POST['ip2']);
	$two = ip2long($_POST['ip2']);
	if($one > $two){
		$temp = $one;
		$one = $two;
		$two = $temp;
	}
	print "Added IP Range: {$_POST['ip']} - {$_POST['ip2']}<br />";
	for($inc = $one; $inc <= $two; $inc += 1){
		$add = long2ip($inc);
		$count = 0;	
	$check = mysql_query("SELECT Address FROM p3_IP",$link);
	while($checks = mysql_fetch_array($check)){
		if( $add == $checks['Address'] )
			$count = 1;
	}
	if( $count == 0 ){
        	$ins = "INSERT INTO p3_IP VALUES(default, '{$add}', null);";
        	$res = mysql_query($ins, $link);
		//print "Added IP: {$add} <br />";
		
	}
	else print "&nbsp; &nbsp;EXCEPT IP: {$add}<br />";
	}
}
$query = "SELECT * FROM p3_IP ORDER BY Address";
$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
?>
			<table width="90%" class="ip">
				<thead>
				<tr>
					<th width="30%">IP Address</th>
					<th width="20%">Available</th>
					<th width="30%">IP Address</th>
					<th width="20%">Available</th>
				</tr>
				</thead>
<?php
        while( $resultset = mysql_fetch_array($results)) {
		print "<tr><td>{$resultset['Address']}</td>";
		if($resultset['Server_ID'] != 0)
			print '<td><img src="images/delete.gif" width="20" height="20" alt="Not Available" /></td>';
		else print '<td><img src="images/check.gif" width="20" height="20" alt="Available" /></td>';
		if( $resultset = mysql_fetch_array($results) ){
                print "<td>{$resultset['Address']}</td>";
                if($resultset['Server_ID'] != 0)
                        print '<td><img src="images/delete.gif" width="20" height="20" alt="Not Available" /></td>';
                else print '<td><img src="images/check.gif" width="20" height="20" alt="Available" /></td>';
		}
		else print "<td>&nbsp;</td><td>&nbsp;</td>";
        	print "</tr>";
	}
?>
			</table>
			<br />
			<form method="post" action="<?php echo $_SERVER['PHP_SELF'];?>" >
				<p>Add new IP Addresses from: &nbsp; &nbsp;
					<input type="text" size="15" maxlength="30" name="ip" value="" />
					&nbsp; &nbsp; &nbsp; to:
					&nbsp; &nbsp; <input type="text" size="15" maxlength="30" name="ip2" value="" />
					&nbsp; &nbsp; <input type="image" src="images/check.gif" name="Add" alt="Add IP" />
				</p>
				<input type="hidden" name="form_submit" />
			</form>
<?php
}
if(session_is_registered('login') && $_SESSION['access'] > 0) {
?>
		</div>
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
print "</div><div id=\"nav\">";
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
