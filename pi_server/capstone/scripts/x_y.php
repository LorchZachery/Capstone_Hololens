<?php
	include 'database.php';
	
	
	//get from form
	$curr_lat = deg2rad((htmlspecialchars($_POST["lat"]))); //deg2rad(39.008935 );
	
	$curr_lon =  deg2rad((htmlspecialchars($_POST["lon"]))); //deg2rad(-104.882653);
	
	echo "lat: " . rad2deg($curr_lat) . " lon: " . rad2deg($curr_lon) . "\n";
	$R = 6371*1000; //could make more exact if wanted not sure yet
	$query = 'SELECT lat FROM current_location WHERE ID=1';
	$curr_loc_lat = db_select($query);
	$query = 'SELECT lon FROM current_location WHERE ID=1';
	$curr_loc_lon = db_select($query);
	echo "curr_loc_lat: " . $curr_loc_lat[0]['lat'] . "  curr_loc_lon: " . $curr_loc_lon[0]['lon'] . "\n";
	$distance = distanceBetweenEarthCoordinates($curr_loc_lat[0]['lat'], $curr_loc_lon[0]['lon'], rad2deg($curr_lat),rad2deg($curr_lon));
	$distance = $distance * 1000.0;
	echo "distance: " . $distance . " m";
	
	if(($distance > 5 && $distance < 1000)){
			to_currentLocation(rad2deg($curr_lat), rad2deg($curr_lon));
			$data = db_select('SELECT ID from bombs');
	
			foreach ($data as $innerArray){
					foreach($innerArray as $key => $ID){
						$lat_query = 'SELECT lat FROM bombs WHERE ID=' . db_quote($ID);
						$lon_query = 'SELECT lon FROM bombs WHERE ID=' . db_quote($ID);
						$bomb_lat = -1;
						$bomb_lon = -1;
						$lat_query = (db_select($lat_query));
						foreach($lat_query as $inner){
							foreach($inner as $lat){
								$bomb_lat = deg2rad(doubleval($lat));
							}
						}
						
						$lon_query = (db_select($lon_query));
						foreach($lon_query as $inner){
							foreach($inner as $lon){
								$bomb_lon = deg2rad(doubleval($lon));
							}
						}
						
						$dlat =  $bomb_lat - $curr_lat;
						$dlon = $bomb_lon - $curr_lon;
						$a = (sin($dlat / 2) * sin($dlat/2)) + cos($curr_lat) * cos($bomb_lat) * (sin($dlon/2) * sin($dlon/2));
						$c = 2 * atan2(sqrt($a), sqrt(1-$a));
						$d = $R * $c;
						$y = sin($dlon) * cos($bomb_lat);
						$x = cos($curr_lat) * sin($bomb_lat) - sin($curr_lat) * cos($bomb_lat) * cos($dlon); 
						$theta = atan2($y,$x);
						$x_coord = $d * cos($theta);
						$y_coord = $d * sin($theta);
						print_r($x_coord);
						echo '\n';
						
						print_r($y_coord);
						echo '\n';
						$result = add_coor($y_coord, 'y', $ID);
						//print_r($result);
						
						$result = add_coor($x_coord, 'x', $ID);
						//print_r($result);
				}
			}
		}
	function add_coor($coord, $type, $id){
		$query = 'UPDATE bombs SET ' . $type . ' = ' . $coord . ' WHERE ID= ' . $id . ';';
		$result = db_query($query, true);
		return $result;
	}
	
	function to_currentLocation($lat, $lon){
		
				$query = 'UPDATE current_location SET lat = '. round($lat,6) . ' WHERE ID=1;';
				db_query($query, true);
				$query = 'UPDATE current_location SET lon = ' . round($lon,6) . 'WHERE ID=1;' ;
				db_query($query, true);
		
		return;
	}
	

	function distanceBetweenEarthCoordinates($lat1, $lon1, $lat2, $lon2) {
		
		
		$dLat = deg2rad($lat2-$lat1);
		$dLon = deg2rad($lon2-$lon1);
		
		$lat1 = deg2rad($lat1);
		$lat2 = deg2rad($lat2);
		
		$a = sin(dLat/2) * sin(dLat/2) + sin($dLon/2) * sin($dLon/2) * cos($lat1) * cos($lat2); 
		$c = 2 * atan2(sqrt($a), sqrt(1-$a));
		
		return 6371.0 * $c;
	}
	
	
	
?>