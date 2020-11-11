<?php 

// Initialize a file URL to the variable 
$url = 'http://127.0.0.1/files/0017SET/000/IMG_0111_2.tif'; 

// Use basename() function to return the base name of file 
$file_name = basename($url); 

// Use file_get_contents() function to get the file 
// from url and use file_put_contents() function to 
// save the file by using base name 
if(file_put_contents( $file_name,file_get_contents($url))) { 
	echo "File downloaded successfully"; 
} 
else { 
	echo "File downloading failed."; 
} 

?> 
