<?php
$datas = $_POST['rdata'];
echo $datas;
$datafile='data.txt';
$fh = fopen("data.txt", 'a') or die("can't open file"); 
  fwrite($fh,$datas);
  fclose($fh);
?>
