<?php
	session_start();
	require("config.php");
	$server = $_GET['server'];
	$percentage = 0.9;
	$query = "SELECT * FROM p3_Server WHERE Server_ID = '{$server}'";
	$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	$resultset = mysql_fetch_array($results);
	$query = "SELECT * FROM p3_Client WHERE {$resultset['Client_ID']} = Client_ID";
	$client = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	$clientset = mysql_fetch_array($client); 
	$query = "SELECT * FROM p3_Rack WHERE {$resultset['Rack_ID']} = Rack_ID";
	$rack = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	$rackset = mysql_fetch_array($rack); 
	$query = "SELECT * FROM p3_IP";
	$ip = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	$ip_used = 0;
	$ip_checker = mysql_query("SELECT * FROM Server WHERE Client_ID = '{$clientset['Client_ID']}'",$link);
	if( mysql_num_rows($ip_checker) > 0 ) 
	{
		while ($ip_checking = mysql_fetch_array($ip_checker)) 
		{
			$ip_found = mysql_query("SELECT * FROM IP WHERE Server_ID = '{$ip_checking['Server_ID']}'",$link);
			$ip_used=$ip_used+mysql_num_rows($ip_found);
		}
	}
	$is_authorized = 0;
	$client2 = mysql_query("SELECT p3_Client.Client_ID FROM p3_Client JOIN p3_Server ON p3_Server.Client_ID = p3_Client.Client_ID WHERE "
			."p3_Server.Server_ID = '{$server}'",$link);
	while($clients2 = mysql_fetch_array($client2)){
		if( $clients2['Client_ID'] == $_SESSION['login'] ) $is_authorized = 1;
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
	<link type="text/css" media="screen" href="CSS/style.css" rel="stylesheet" />
	<link type="text/css" media="print" href="CSS/print.css" rel="stylesheet" />
	<title>CSC295W Project 3 - <?php print "{$resultset['Name']}" ?> Server Details</title>

</head>
<body>
	<div id="wrapper">
		<div id="logo" class="clearfix">
			<img src="images/serverrackwide.gif" width="184" height="93" alt="" class="headimg" />
			<img src="images/logo2.gif" width="581" height="93" alt="CSC295W Project 1" class="nameimg" />
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
    //if the form has been submitted
	if( session_is_registered('login') && (($_SESSION['login'] == 0) || ($is_authorized == 1))) 
{
	if(isset($_POST['form_submit3']))
	{	
			$ip_count = $_POST['deleteIP'];
			if($ip_count>0)
			{
				while(($ipset = mysql_fetch_array($ip)) && ($ip_count > 0)) 
				{
					if($ipset['Server_ID'] == $server)
					{
						$ip_count--;
						$update_query = "UPDATE p3_IP SET Server_ID = NULL WHERE (Address = '{$ipset['Address']}')";
						$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
					}
				}
				if($ip_count == 0)
				{
					print "All IPs requested to be freed released.<br/>";
				}
				else
				{
					$ip_allocated = $_POST['deleteIP']-$ip_count;
					print "{$ip_allocated} of {$_POST['deleteIP']} freed from server. Requested to remove more IPs than were on server.<br/>";
				}
			}	
	}
	else
  	if(isset($_POST['form_submit']) || isset($_POST['form_submit2']) || isset($_POST['form_submit4']))
	{

		if(isset($_POST['form_submit4']) && ($_POST['requestIP'] > 0) )
		{
			
			$query = "SELECT * FROM p3_User WHERE User_ID NOT IN (select User_ID from p3_User where Client_ID != 0)";
			$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
			print "Request for additional IPs submitted.";
	      		while( $resultsArray = mysql_fetch_array($results)){
                	$header = "From: {$_SESSION['name']} <{$_SESSION['mail']}>\n X-Mailer: PHP 5.x";
               		mail($resultsArray['Email'], "Request for Additional IPs","User {$_SESSION['name']} is requesting {$_POST['requestIP']} additional IPs for server {$resultset['Name']}. The reason for the request was: {$_POST['reason']}",$header);
        	}
		}
		if((isset($_POST['approveIP'])) && ($_SESSION['login'] == 0) )
		{
			$ip_count = $_POST['approveIP'];
			if($ip_count>0)
			{
				while(($ipset = mysql_fetch_array($ip)) && ($ip_count > 0)) 
				{
					if($ipset['Server_ID'] == 0)
					{
						$ip_count--;
						
						$update_query = "UPDATE p3_IP SET Server_ID = '{$server}' WHERE (Address = '{$ipset['Address']}')";
						$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
					}
				}
				if($ip_count == 0)
				{
					print "All requested IPs now allocated to server<br/>";
				}
				else
				{
					$ip_allocated = $_POST['approveIP']-$ip_count;
					print "{$ip_allocated} of {$_POST['approveIP']} allocated to server. Insufficient IPs to allocate all requested.<br/>";
				}
			}
			$luckychannel = 0;
			$query = "SELECT * FROM p3_IP";
			$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
			while( $resultsArray = mysql_fetch_array($results))
			{
				$luckychannel++;
			}
			$query = "SELECT * FROM p3_IP WHERE Server_ID != 0";
			$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
			$luckystar = 0;
			while( $resultsArray = mysql_fetch_array($results))
			{
				$luckystar++;
			}
			$luckystar = $luckychannel - $luckystar;
			if ($luckystar >= ($luckychannel * $percentage))
			{
				$query = "SELECT * FROM p3_User WHERE User_ID NOT IN (select User_ID from p3_User where Client_ID != 0)";
				$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
		      		while( $resultsArray = mysql_fetch_array($results)){
	                	$header = "From: {$_SESSION['name']} <{$_SESSION['mail']}>\n X-Mailer: PHP 5.x";
        	       		mail($resultsArray['Email'], "IP Allocation Critical","Free IPs available has fallen below 10%. FIX IT.",$header);}
			}
		}
		else if(isset($_POST['approveIP']))
		{
			print "NO HACKING";
		}

if(isset($_POST['form_submit']))
{
		$query = "SELECT * FROM Server WHERE (Server_ID = $server)";
		$results = mysql_query($query, $link) or die('Invalid Query:'.mysql_error());
		if(mysql_num_rows($results) > 0)
		{
			print "Server Details Updated.<br />";
			$update_query = "UPDATE Server SET Details = '{$_POST['Details']}' WHERE (Server_ID = $server)";
			$update_results = mysql_query($update_query, $link) or die('Invalid Query:'.mysql_error());
			
		}
}
	} 

	$query = "SELECT * FROM Server WHERE Server_ID = '{$server}'";
	$results = mysql_query($query, $link) or die('Invalid Query: '.mysql_error());
	$resultset = mysql_fetch_array($results);
?>	
			<h1>Server Details: <?php print "{$resultset['Name']}" ?></h1>
			<br /><form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?server={$resultset['Server_ID']}"; ?>">
			<table>
				<tr>
					<th>Name:</th>
					<td><?php print "{$resultset['Name']}" ?></td>
				</tr>
				<tr>
					<td>Rack:</td> 
					<td><a href="rackDetails.php?rack=<?php print "{$resultset['Rack_ID']}" ?>"><?php print "{$rackset['Name']}" ?></a></td>
				</tr>
				<tr>
					<td>Size:</td>
					<td><?php print "{$resultset['Size']}" ?>U</td>
				</tr>
				<tr>
                              <td>Client/Owner: </td>
					<td><a href="clientDetails.php?client=<?php print "{$resultset['Client_ID']}" ?>"><?php print "{$clientset['Name']}" ?> </a></td>
				</tr>
				<tr>
					<td>IP Addresses:</td>
					<td>
						<ul>
			
<?php
			$ip = mysql_query("SELECT * FROM p3_IP WHERE Server_ID = '{$server}'",$link);
			if( mysql_num_rows($ip) > 0) {
			while ($ips = mysql_fetch_array($ip)) {
				print "<li>{$ips['Address']}</li>";
			}
			}
			else print "None";
?>
						</ul>
					</td>
				</tr>
				<tr>
					<td>Details: </td>
					<td>
		<textarea name="Details" cols="50" rows="5"><?php print "{$resultset['Details']}" ?></textarea><input type="hidden" name="form_submit" /></td>
				</tr>
			</table>
			<br />
				<p align="center"><input type="image" src="images/edit.gif" name="edit" alt="Edit"/></p></form>

			<br /><?php if($_SESSION['login'] != 0) { ?><form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?server={$resultset['Server_ID']}"; ?>"><input type="hidden" name="form_submit2" />
			<table>
				<tr>
					<td>Request IP Addresses: &nbsp;</td>
					<td><input type="text" size="5" maxlength="3" name="requestIP" value="" /></td>
					<td><textarea name="reason" cols="50" rows="5">Reason for Request</textarea></td>
					<td>&nbsp; &nbsp;<input type="image" src="images/check.gif" name="request" alt="Request IP's" /></td>
				</tr></form>
				<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?server={$resultset['Server_ID']}"; ?>"><input type="hidden" name="form_submit3" /><tr>
			<td>Delete IP Addresses: &nbsp;</td>
					<td><input type="text" size="5" maxlength="3" name="deleteIP" value="" /></td>
					<td>&nbsp; &nbsp;<input type="image" src="images/delete.gif" name="request" alt="Remove IP's" /></td>
</tr></form>
			</table><?php } else { ?><form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?server={$resultset['Server_ID']}"; ?>"> <input type="hidden" name="form_submit4" /> <table>
				<tr>
					<td>Add IP Addresses: &nbsp;</td>
					<td><input type="text" size="5" maxlength="3" name="approveIP" value="" /></td>
					<td>&nbsp; &nbsp;<input type="image" src="images/check.gif" name="approve" alt="Add IP's" /></td>
				</tr></table></form>
<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}?server={$resultset['Server_ID']}"; ?>"><input type="hidden" name="form_submit3" /><table><tr>
			<td>Delete IP Addresses: &nbsp;</td>
					<td><input type="text" size="5" maxlength="3" name="deleteIP" value="" /></td>
					<td>&nbsp; &nbsp;<input type="image" src="images/delete.gif" name="request" alt="Remove IP's" /></td>
</tr></table></form>
			<?php } } else print "You are not Authorized to view this page.";?>
		
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
