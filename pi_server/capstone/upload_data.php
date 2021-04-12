<?php

    include_once("libs/config.php");

    // Extracts Relevant POST Info
    $api_key = $_POST['api_key'];
    $dev_id  = $_POST['device_id'];
    $data    = json_decode($_POST['data'], true);
    
    // Returns the Column Names from a Table (or an empty array if the table does not exist)
    function get_table_columns($table_name) {
        $table_info = db_query("SHOW COLUMNS FROM " . strtolower($table_name));
        
        $result = array();
        
        if ($table_info != false) {
            foreach ($table_info as $column_info) {
                array_push($result, $column_info['Field']);
            }
        }
        
        return $result;
    }

    // Determines what SQL Data Type a Value Is
    function get_data_type($value) {        
        // By default, all data is assumed to be a string
        $datatype = "VARCHAR(64)";
                    
        // Looks for floats, integers, etc.
        if (is_int($value)) {
            $datatype = "INT";
        }
        elseif (is_float($value)) {
            $datatype = "FLOAT";
        }
        elseif (is_bool($value)) {
            $datatype = "BOOLEAN";
        }
        
        return $datatype;
    }

    // Creates (or Updates) the Table as Needed
    function create_or_update_table($data) {
        $table_columns = get_table_columns(strtolower($data['type']));
        
        // Creates a New Table
        if (sizeof($table_columns) == 0 && sizeof($data) > 1) {
            $sql = "CREATE TABLE " . strtolower($data['type']) . " (";
            $sql .= "id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,";
            $sql .= "device_id VARCHAR(64) NOT NULL,";
            $sql .= "time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,";
            
            foreach (array_keys($data) as $column) {
                if ($column != 'type') {
                    
                    $datatype = get_data_type($data[$column]);
                    
                    $sql .= strtolower($column) . ' ' . $datatype . ', ';
                }
            }
            
            $sql = substr($sql, 0, -2);
            $sql .= ")";
            
            //echo "Creating Table";
            db_query($sql);
        }
        elseif (sizeof($table_columns) > 0) {
            
            $sql = "ALTER TABLE " . strtolower($data['type']) . " ";
            $run_query = false;
            
            // Determines if new columns need to be added to the table
            foreach (array_keys($data) as $column) {    
                if (!in_array(strtolower($column), $table_columns) && strtolower($column) != 'type') {
                    echo $column . " not in table";
                    $run_query = true;
                    $sql .= "ADD " . strtolower($column) . ' ' . get_data_type($data[$column]) . ', ';
                }
            }
            
            $sql = substr($sql, 0, -2);
            
            if ($run_query == true) {
                //echo "Updating Table";
                //echo $sql;
                db_query($sql);
            }
            else {
                //echo "No Need to Update Table";
            }
        }
    }

    // Adds a New Record in the Database Table
    function insert_data($device_id, $data) {
        $sql = "INSERT INTO " . strtolower($data['type']) . " (device_id, ";
        
        foreach (array_keys($data) as $column) {  
            $column_name = strtolower($column);

            if ($column_name != 'type') {
                $sql .= $column_name . ", ";    
            }
        }
     
        $sql = substr($sql, 0, -2);
        $sql .= ") VALUES (" . db_quote($device_id) . ', ';
        
        foreach (array_keys($data) as $column) {  
            $column_name = strtolower($column);

            if ($column_name != 'type') {
                if (is_numeric($data[$column])) {
                    $sql .= $data[$column] . ", ";  
                }
                else {
                    $sql .= db_quote($data[$column]) . ", ";  
                }
            }
        }
        
        $sql = substr($sql, 0, -2);
        $sql .= ")";
        
        //print_r($sql);
        db_query($sql);
    }

    // Creates an Array to Store the Response
    $response = array(RESPONSE => RESPONSE_UNKNOWN, MESSAGE => "Unknown Condition Reached.  This is not good or bad, just unexpected.");

    // Processes the POST Operation and Generates an Appropriate Response Message
    if (validate_api_key($api_key)) {
        $response[RESPONSE] = RESPONSE_SUCCESS;
        $response[MESSAGE]  = "Valid API Key";
        
        // TODO:  Examines the Data Message and Tries to Determine What Tables to Create
        //print_r($data);
            
        // Step 1:  Determines if a New Table Needs to be Created
        create_or_update_table($data);
        
        // Step 2:  Adds the Value to the Database Table
        insert_data($dev_id, $data);
    }
    else {
        $response[RESPONSE] = RESPONSE_FAILURE;
        $response[MESSAGE]  = "Invalid API Key";
    }

    echo json_encode($response);
?>