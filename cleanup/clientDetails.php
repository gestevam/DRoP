<?php
session_start();
require("config.php");
$client = $_GET['client'];
$server = mysql_query("SELECT * FROM p3_Server WHERE Client_ID = '{$client}'",$link);
$query = "SELECT * FROM p3_Client WHERE Client_ID = '{$client}'";
$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
$resultset = mysql_fetch_array($results);
if( mysql_num_rows($server) > 0 ) 
{
	while ($servers = mysql_fetch_array($server)) 
	{
		$ip = mysql_query("SELECT * FROM p3_IP WHERE Server_ID = '{$servers['Server_ID']}'",$link);
		$ip_used=$ip_used+mysql_num_rows($ip);
	}
}
else $ip_used=0;
$errormessage = "";
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
<?php
	print "<title>CSC295W Project 3 - Client Details: {$resultset['Name']}</title>";
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
if(session_is_registered('login') && ($_SESSION['login'] == 0 || $_SESSION['login'] == $client)) {
    //if the form has been submitted
  	if(isset($_POST['form_submit'])){
	$query = "SELECT * FROM p3_Client WHERE (Client_ID = {$client})";
	$resultscheck = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
	if(mysql_num_rows($resultscheck) > 0)
	{
		print "User Information Updated.<br />";
		$update_query = "UPDATE p3_Client SET Name = '{$_POST['name']}' WHERE (Client_ID = {$client})";
		$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
		$update_query = "UPDATE p3_Client SET Addr = '{$_POST['street']}' WHERE (Client_ID = {$client})";
		$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
		$update_query = "UPDATE p3_Client SET City = '{$_POST['city']}' WHERE (Client_ID = {$client})";
		$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
		$update_query = "UPDATE p3_Client SET State = '{$_POST['state']}' WHERE (Client_ID = {$client})";
		$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
		$update_query = "UPDATE p3_Client SET Contact = '{$_POST['cName']}' WHERE (Client_ID = {$client})";
		$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
		$update_query = "UPDATE p3_Client SET Phone = '{$_POST['cTel']}' WHERE (Client_ID = {$client})";
		$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
		$update_query = "UPDATE p3_Client SET Email = '{$_POST['cEmail']}' WHERE (Client_ID = {$client})";
		$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
		$query = "SELECT * FROM p3_Client WHERE Client_ID = '{$client}'";
		$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
		$resultset = mysql_fetch_array($results);
	}	
}
	if(isset($_GET['del']) && $_SESSION['login'] == 0){
                $remip = mysql_query("UPDATE p3_IP Set Server_ID = null WHERE Server_ID = {$_GET['del']}",$link);
        	$rem = mysql_query("DELETE FROM p3_Server WHERE Server_ID = {$_GET['del']}",$link);
		print "Server Deleted";
	} 

$query = "SELECT * FROM p3_Client WHERE Client_ID = '{$client}'";
$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
$resultset = mysql_fetch_array($results);
$query = "SELECT * FROM p3_Server WHERE Client_ID = '{$client}'";
$results2 = mysql_query($query, $link) or die('Invalid Query: '.mysql_error()); 
}
?>	
			<h1>Details: <?php print "{$resultset['Name']}" ?></h1>

<?php
if(session_is_registered('login') && ($_SESSION['login'] == 0 || $_SESSION['login'] == $client)) {
?>
<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?client={$resultset['Client_ID']}"; ?>">
			<table>
				<tr>
					<th>Name</th>
					<td><input type="text" size="30" maxlength="50" name="name" value="<?php print "{$resultset['Name']}" ?>" /></td>
				</tr>
				<tr>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<th>Address</th>
				</tr>
				<tr>
					<td>Street</td> 
					<td><input type="text" size="30" maxlength="50" name="street" value="<?php print "{$resultset['Addr']}" ?>" /></td>
				</tr>
				<tr>
					<td>City</td>
					<td><input type="text" size="15" maxlength="30" name="city" value="<?php print "{$resultset['City']}" ?>" /></td>
				</tr>
				<tr>
                              <td>State</td>
					<td><input type="text" size="2" maxlength="2" name="state" value="<?php print "{$resultset['State']}" ?>" /></td>
				</tr>
				<tr>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<th>Primary Contact</th>
				</tr>
				<tr>
					<td>Name</td>
					<td><input type="text" size="50" maxlength="70" name="cName" value="<?php print "{$resultset['Contact']}" ?>" /></td>
				</tr>
				<tr>
					<td>Telephone</td>
					<td><input type="text" size="12" maxlength="20" name="cTel" value="<?php print "{$resultset['Phone']}" ?>" /></td>
				</tr>
				<tr>
					<td>E-mail</td>
					<td><input type="text" size="30" maxlength="50" name="cEmail" value="<?php print "{$resultset['Email']}" ?>" /></td>
				</tr>
				<tr>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<th>IP Allocation</th>
				</tr>
				<tr>
					<td>Used</td>
					<td><?php print "{$ip_used}"; ?></td>
				</tr>
			</table>
			<br /><input type="hidden" name="form_submit" />
				<p align="center"><input type="image" src="images/edit.gif" name="edit" alt="Edit" /></p>
			<br />
</form>
<?php
print "<ul>";
	if( mysql_num_rows($results2) > 0 ){
	while ($server_results = mysql_fetch_array($results2)) {
		print "<li>Server: <a href=\"serverDetails.php?server={$server_results['Server_ID']}\">{$server_results['Name']}</a>";

		if( $_SESSION['login'] == 0 ) {
                print "&nbsp; &nbsp; &nbsp;<a href=\"clientDetails.php?client={$client}&del={$server_results['Server_ID']}\">";
                print '<img src="images/delete.gif" alt="View" width="30" height="30" class="linkimg" /></a>';
		}

                print "<ul>";
                $rack = mysql_query("SELECT * FROM p3_Rack WHERE Rack_ID = '{$server_results['Rack_ID']}'",$link);
		if( mysql_num_rows($rack) > 0 ) {
		while ($racks = mysql_fetch_array($rack)) {
                        print "<li>Rack: <a href=\"rackDetails.php?rack={$racks['Rack_ID']}\">{$racks['Name']}</a></li>"; 
}
}
			else print "None";
                        print "</ul></li>";  
	}
	}
	else {print "<ul><li>No Servers Found</li>";
	print "</ul>";}
?>

<?php
}
else print "You are not authorized to view this page.";
if(session_is_registered('login') && $_SESSION['login'] == 0) {
?>
		</div>
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
