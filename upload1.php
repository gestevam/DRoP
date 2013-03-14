<?php
session_start();
require("config.php");
$dir = 'upload/user2/';
#echo getcwd() . "\n";

if ((($_FILES["file"]["type"] == "application/zip")||($_FILES["file"]["type"] =="application/x-zip-compressed")||($_FILES["file"]["type"] =='application/x-compressed')||($_FILES["file"]["type"] =='multipart/x-zip')
)
&& ($_FILES["file"]["size"] > 1))
  {
  if ($_FILES["file"]["error"] > 0)
    {
    echo "Return Code: " . $_FILES["file"]["error"] . "<br />";
    }
  else
    {
	$name=pathinfo($_FILES["file"]["name"], PATHINFO_FILENAME);
	$insert_query = "INSERT INTO data_sets VALUES (Default, {$_SESSION['UID']}, '0', '{$name}' ,Default)";
	$insert_results = mysql_query($insert_query, $link) or die('Invalid Query:'.mysql_error());
	$runid = mysql_insert_id();
	$dir = 'upload/'.$runid.'/';
	if(!file_exists($dir))
	{
		mkdir($dir);
	}
    #echo "Upload: " . $_FILES["file"]["name"] . "<br />";
    #echo "Type: " . $_FILES["file"]["type"] . "<br />";
    #echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
    #echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />";

    if (file_exists($dir . $_FILES["file"]["name"]))
      {
      #echo $_FILES["file"]["name"] . " already exists. ";
      }
    else
      {
      move_uploaded_file($_FILES["file"]["tmp_name"],
      $dir . $_FILES["file"]["name"]);
      #echo "Stored in: " . $dir . $_FILES["file"]["name"];
      }
	  $test=$runid;
	  #print "<br />";
	  #print shell_exec('python callablepython.py '.$test);
          pclose(popen('python callablepython.py '.$test.' &','w'));
	  #echo getcwd() . "\n";
	  $test='4';
	  chdir('upload/'.$test.'/');
	  #echo getcwd() . "\n";
	  #print exec('python workingDRoP.py');
	  #print exec('whoami');
	  #print '<br />';
	  #print exec("alias python='/usr/bin/python'"); 
	  #print exec('whoami');
	  #print '<br />';
	  #print shell_exec('python2 callable2.py');
	  #print shell_exec('pymol -c');
	  #echo shell_exec('python2 cealign.py ND01PRESUPER.pdb ND02PRESUPER.pdb 2>&1');
	  #echo shell_exec('superpose 1.pdb 2.pdb foo.pdb 2>&1');
	  
	  #$out = shell_exec('ls -al');
	  #print $out;
	  #pclose(popen('python workingDRoP.py&','w'));
    }?><meta http-equiv="Refresh" content="0; URL=index.php" /><?php
  }
else
  {
  echo "Invalid file";
  echo $_FILES["file"]["type"];
  }

?> 

