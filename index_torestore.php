
<?php
session_start();
require("config.php");
if( isset($_POST['id']) ) {
	
        $results = mysql_query("SELECT name, email, user_ID FROM users WHERE login = '{$_POST['id']}' AND password = MD5('{$_POST['psswrd']}')",$link);
        if(mysql_num_rows($results) == 1) {
                $resultsArray = mysql_fetch_array($results);
                $_SESSION['login']=1;
				$_SESSION['access']=50;
                $_SESSION['name'] = $resultsArray['name'];
                $_SESSION['mail'] = $resultsArray['email'];
		$_SESSION['UID'] = $resultsArray['user_ID'];
	print '<meta http-equiv="Refresh" content="0; URL=redirect.php" />';
        }
	else {$error = "Incorrect User Name/Password"; }
	}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<link type="text/css" media="screen, handheld" href="CSS/style.css" rel="stylesheet" />
	<link type="text/css" media="print, projection" href="CSS/print.css" rel="stylesheet" />
	<title>Detection of Related Solvent Positions Server</title>

</head>
<body>
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon"/>
	<div id="wrapper">
		<div id="logo" class="clearfix">
			<img src="images/trypsin.png" width="184" height="93" alt="" class="headimg" />
			<img src="images/logo2.png" width="581" height="93" alt="DRoP" class="nameimg" />
		</div>
		<div id="bar">
<?php
if( session_is_registered('login') ) {
                        print "<p>&nbsp; Logged in as: {$_SESSION['name']} &nbsp;";
			$res = mysql_query("SELECT * FROM users WHERE name = '{$_SESSION['name']}' AND "
                                ."email = '{$_SESSION['mail']}'",$link);
                        $resset = mysql_fetch_array($res);
                        print "&nbsp; - &nbsp; &nbsp;<a href=\"users.php?user={$_SESSION['UID']}\">User Info</a>";
                        print '&nbsp; &nbsp; - &nbsp; &nbsp;<a href="logout.php">Logout</a></p>';
}
else print "Please Log In."; 
?>
		</div>
		<div id="top">
			<img src="images/top.gif" width="765" height="33" alt="" />
		</div>
		
		<div id="content">

<?php


if( !$_SESSION['login'] ) { print $error;
	?>
	<h1>Please login</h1>
	<br />
	<form method="post" action="<?php print "{$_SERVER['PHP_SELF']}"; ?>">
	<?php
	print "<table><tr><td>Username: &nbsp; &nbsp;</td>";
	print '<td><input type="text" size="30" maxlength="50" name="id" autocomplete="off" value="" /></td></tr>';
	print "<tr><td>Password: </td>";
	print '<td><input type="password" size="20" maxlength="20" name="psswrd" value="" /></td></tr>';
	print '<tr><td>&nbsp;</td><td><input type="submit" name="submit" value="Submit" /></td></tr></table>';
	print '</form>';
	print "<a href='./registration.php'>New user registration</a>";
}
else { ?>
<h1>Overview</h1>
<br />
<script type="text/javascript">
function loadXmlHttp(url, id) {
var f = this;
f.xmlHttp = null;
/*@cc_on @*/ // used here and below, limits try/catch to those IE browsers that both benefit from and support it
/*@if(@_jscript_version >= 5) // prevents errors in old browsers that barf on try/catch & problems in IE if Active X disabled
try {f.ie = window.ActiveXObject}catch(e){f.ie = false;}
@end @*/
if (window.XMLHttpRequest&&!f.ie||/^http/.test(window.location.href))
f.xmlHttp = new XMLHttpRequest(); // Firefox, Opera 8.0+, Safari, others, IE 7+ when live - this is the standard method
else if (/(object)|(function)/.test(typeof createRequest))
f.xmlHttp = createRequest(); // ICEBrowser, perhaps others
else {
f.xmlHttp = null;
 // Internet Explorer 5 to 6, includes IE 7+ when local //
/*@cc_on @*/
/*@if(@_jscript_version >= 5)
try{f.xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");}
catch (e){try{f.xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");}catch(e){f.xmlHttp=null;}}
@end @*/
}
if(f.xmlHttp != null){
f.el = document.getElementById(id);
f.xmlHttp.open("GET",url,true);
f.xmlHttp.onreadystatechange = function(){f.stateChanged();};
f.xmlHttp.send(null);
}
}


loadXmlHttp.prototype.stateChanged=function () {
if (this.xmlHttp.readyState == 4 && (this.xmlHttp.status == 200 || !/^http/.test(window.location.href)))
	this.el.innerHTML = this.xmlHttp.responseText;
}

var requestTime = function(){
new loadXmlHttp('poll.php', 'timeDiv');
setInterval(function(){new loadXmlHttp('poll.php?t=' + new Date().getTime(), 'timeDiv');}, 1000);
}

if (window.addEventListener)
 window.addEventListener('load', requestTime, false);
else if (window.attachEvent)
 window.attachEvent('onload', requestTime);
</script>
</head>
<body>
<div id="timeDiv">

</div>
<?php
}
?>
		
		</div>
<?php
if(1 or $_SESSION['login']==1 && $_SESSION['access'] > 0) {
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
		<p>&copy; 2010-2013 by Bradley Kearney.</p>
		<p>Feedback or questions? | E-mail the <a href="mailto:bmkearne@ncsu.edu">Author</a>.</p>
	</div>
	</div>
	
</body>
</html>
