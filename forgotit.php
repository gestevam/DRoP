<?php
echo "boo";
require 'PHPMailerAutoload.php';
echo "ok";
$mail = new PHPMailer(); // create a new object
echo "how about now";
$mail->IsSMTP(); // enable SMTP
$mail->SMTPDebug = 1; // debugging: 1 = errors and messages, 2 = messages only
$mail->SMTPAuth = true; // authentication enabled
$mail->SMTPSecure = 'ssl'; // secure transfer enabled REQUIRED for GMail
$mail->Host = "smtp.gmail.com";
$mail->Port = 465; // or 587
$mail->IsHTML(true);
$mail->Username = "dropinthemattoslab@gmail.com";
$mail->Password = "r@$B10chem";
$mail->SetFrom('dropinthemattoslab@gmail.com');
$mail->Subject = "Test";
$mail->Body = "hello";
$mail->AddAddress('dropinthemattoslab@gmail.com');
echo "huh";
if(!$mail->send()) {
   echo 'Message could not be sent.';
   echo 'Mailer Error: ' . $mail->ErrorInfo;
   exit;
}

echo 'Message has been sent';
echo "wedone";
?>
