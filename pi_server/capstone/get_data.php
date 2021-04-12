<?php
    // ----------------------------------------------------------------------
    // Obtains Data Values from the Database
    //
    // USAGE: HTTP POST OR GET with the following variables:
    //    1.  api_key
    //    2.  type
    //    3.  time_start (optional)
    //    4.  time_end (optional)
    //    5.  limit (optional)
    //    6.  device_ids (optional)
    //
    // Returns:  JSON
    // ----------------------------------------------------------------------

    include_once("libs/config.php");

    // Stores the result of the transaction
    $response = array();

    // ---------------------------------------------------
    // Gets a Value from the $_POST or $_GET arrays
    // ---------------------------------------------------
    function get_value($key) {
        if (isset($_POST[$key])) {
            return $_POST[$key];
        }
        elseif (isset($_GET[$key])) {
            return $_GET[$key];
        }
        else {
            return null;
        }
    }

    // Gets Mandatory Parameters
    $api_key = get_value('api_key'); 
    $type = get_value('type');

    if ($api_key != null && $type != null) {
        // Gets Optional Parameters
        $time_start = (get_value('time_start') == null) ? "1969-01-01 00:00:00" : get_value('time_start');
        $time_end   = (get_value('time_end') == null) ? "2099-01-01 00:00:00" : get_value('time_end');
        $limit      = (get_value('limit') == null) ? 10 : get_value('limit');
        $device_ids = (get_value('device_ids') == null) ? array() : get_value('device_ids');
        
        if (validate_api_key($api_key)) {  
            $start = new DateTime($time_start);
            $start = $start->format('Y-m-d H:i:s');
            $end   = new DateTime($time_end);
            $end   = $end->format('Y-m-d H:i:s');
            
            // Performs the Query
            $search_query = "SELECT * from " . strtolower($type) . " WHERE " .
                "time>=" . db_quote($start) . " AND time<=" . db_quote($end);
            
            if (sizeof($device_ids) > 0) {
                $search_query .= ' AND (';
                
                foreach ($device_ids as $device) {
                    $search_query .= "device_id=" . db_quote($device) . ' OR ';
                }
                
                $search_query = substr($search_query, 0, -3);
                
                $search_query .= ')';
            }
            
            // Sorts by Descending Time
            $search_query .= " ORDER BY time DESC LIMIT " . $limit;
            
            //echo $search_query . '<br><br>';
            $search_results =  db_select($search_query);
            
            if ($search_results == false) {
                // If we get here, the operation was (hopefully) a success
                $response[RESPONSE] = RESPONSE_FAILURE;  
                $response[MESSAGE] = $search_query;
            }
            else {
                // If we get here, the operation was (hopefully) a success
                $response[RESPONSE] = RESPONSE_SUCCESS;  
                $response[MESSAGE] = $search_results;    
            }
        }
        else {
            $response[RESPONSE] = RESPONSE_FAILURE;
            $response[MESSAGE]  = "Invalid API Key " . $api_key;
        }
    }
    else {
        $response[RESPONSE] = RESPONSE_FAILURE;
        $response[MESSAGE] = "Missing parameters. Expecting api_key and type.";
    }

    # Returns a Success Message
    echo json_encode($response);
?>