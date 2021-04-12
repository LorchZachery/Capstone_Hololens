<?php

$type = intval(htmlspecialchars($_POST["type"]));
echo $type;

//$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

if( $type == 1){
	
	$filename = '../uploads/' . $_POST['fileName'];
	$fp = fopen($filename, 'wb');
	fwrite($fp, $_POST["fileToUpload"]);
	
	fclose($fp);
	
	
}
if( $type == 2){
	$filename = '../scripts/' . $_POST['fileName'];
	$fp = fopen($filename, 'wb');
	fwrite($fp, $_POST["fileToUpload"]);
	fclose($fp);
	echo "2";
}
if( $type == 3){
	$filename = '../' . $_POST['fileName'];
	$fp = fopen($filename, 'wb');
	fwrite($fp, $_POST["fileToUpload"]);
	fclose($fp);
	echo "3";
}



if( $type == 0){
	echo "You failed";
}
?>