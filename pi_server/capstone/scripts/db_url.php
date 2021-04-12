<?php

	include 'database.php';
	
	$value = (htmlspecialchars($_GET['query']));
	
	
	$result = db_select($value);
	//$query = 'SELECT * FROM bombs WHERE field=' . db_quote("VALUE") . ;
	
	
	
	print_r(json_encode($result));
	

	

?>