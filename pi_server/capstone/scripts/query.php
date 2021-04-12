<?php

	include 'database.php';
	
	$value = (htmlspecialchars($_POST['query']));
	$type =  (htmlspecialchars($_POST['type']));
	$result = 'error';
	if($type == 'SELECT'){
	$result = db_select($value);
	//$query = 'SELECT * FROM bombs WHERE field=' . db_quote("VALUE") . ;
	}
	if($type == 'EDIT'){
		
		$result = db_query($value);
	}
	print_r(json_encode($result));


?>