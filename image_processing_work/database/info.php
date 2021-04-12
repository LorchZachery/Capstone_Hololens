<?php

$type = intval(htmlspecialchars($_POST["type"]));

if( $type == 1){

	$image_name = htmlspecialchars($_POST["imageName"]);	
	$macaddress = $_POST["MAC"] ; 
	date_default_timezone_set("America/denver");
	$time_of_upload =  date("H:i:s");
	echo $macaddress;
	
	//$jsonString = file_get_contents('current_status.json');
	//$curr_data = json_decode($jsonString, true);
	
	$file = file_get_contents('current_status.json');
	$tempArray = json_decode($file, true);
	
	$tempArray[$macaddress] = array("file"=>$image_name, "time"=>$time_of_upload);
	//$data[$macaddress] = array("file"=>$image_name, "time"=>$time_of_upload);
	
	//print_r($data);
	
	$jsonData = json_encode($tempArray, true);
	file_put_contents('current_status.json',$jsonData);
}

if( $type == 2){
	$file = file_get_contents('current_status.json');
	$json = json_decode($file, true); // decode the JSON into an associative array
	foreach($json as $field => $value) {
		$index  = 0; 
		foreach( $json[$field] as $feild1 => $value1){
			if($index%2 == 0){
				echo $value1;
				echo " ";
			}
			$index = $index  +1;
		}
	}
	//print_r($current_images);

}
/*
ip_addr1 image_name time
ip_addr2 image_name time

*/

?>