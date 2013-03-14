<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title></title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
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
new loadXmlHttp('time.php', 'timeDiv');
setInterval(function(){new loadXmlHttp('time.php?t=' + new Date().getTime(), 'timeDiv');}, 1000);
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
</body>
</html>