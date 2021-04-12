<?php

    // Libraries
    include_once "libs/database.php";

    // Database
    define("_DB_SERVERNAME", "localhost");
    define("_DB_NAME", "ieddfcsc_mldb");
    define("_DB_USERNAME", "ieddfcsc_mldbuser");
    define("_DB_PASSWORD", "B7PbWFa4sUm1");

    // Response JSON Components
    define("RESPONSE", "response");
    define("MESSAGE", "message");

    // Response Codes
    define("RESPONSE_SUCCESS", 200);
    define("RESPONSE_FAILURE", 400);
    define("RESPONSE_UNKNOWN", 999);

    // This function determines if an API key is stored within the database
    // Returns TRUE if in the credentials table, and FALSE otherwise
    function validate_api_key($apikey) {
        $query = "SELECT * from credentials WHERE api_key=" . db_quote($apikey);
        $result = db_select($query);
        return sizeof($result) > 0;
    }

?>