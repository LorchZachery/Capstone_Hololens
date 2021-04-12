<?php
    include_once "config.php";

    // Outputs Debug Text
    function debug ($text, $verbose = false) {
        if ($verbose) {
            echo $text;
        }
    }

    // Connects to the Database (or dies trying)
    // Thanks to https://www.binpress.com/using-php-with-mysql/
    function db_connect($db_name = _DB_NAME) {
        // Connection is static -- i.e., only one should exist for the lifetime of the script
        static $conn;
        
        if (!isset($conn)) {
            // Attempts to connect
            $conn = new mysqli(_DB_SERVERNAME, _DB_USERNAME, _DB_PASSWORD, $db_name);

            // Checks to see if an error occurred
            if ($conn->connect_error) { 
                die("DB Connection failed: " . $conn->connect_error); 
            }     
        }
        // Returns the connection
        return $conn;
    }

    // Returns the Error Message if a query goes bad
    function db_error() {
        $connection = db_connect();
        return mysqli_error($connection);
    }

    // Executes an INSERT, REMOVE Database Query
    function db_query($query, $verbose = false) {
        // Connect to the database
        $conn = db_connect();

        // Query the database
        debug('<br>' . $query . '<br>', $verbose);
        $result = mysqli_query($conn, $query);
        
        if ($result === false) {
            debug('SQL FAILURE: ' . mysqli_error($conn) . '<br>', $verbose);
        }
        else {
            debug('SQL SUCCESS<br>', $verbose);
        }
        
        return $result;
    }

    // Surrounds a value with the ' characters, and escapes code characters to prevent injection attacks
    function db_quote($value) {
        
        $conn = db_connect();
        return "'" . mysqli_real_escape_string($conn, $value) . "'";
        
    }

    // Executes a SELECT statement
    // Returns an array with the rows, OR false if something bad happened
    function db_select($query) {
        
        $rows   = array();
        $result = db_query($query);

        // If query failed, return `false`
        if($result === false) {
            return false;
        }

        // If query was successful, retrieve all the rows into an array
        while ($row = mysqli_fetch_assoc($result)) {
            $rows[] = $row;
        }
        
        return $rows;
        
    }

?>