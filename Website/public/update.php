<?php

    $DB_USER=  "doadmin";
    $DB_PSWD = "AVNS_1OJ-Nk7eUgMXbec";
    $DB_HOST= "db-mysql-sfo2-96686-do-user-11317347-0.b.db.ondigitalocean.com:25060";
    $DATABASE = "peppetEMAIL";


    $dbcon = new mysqli($DB_HOST,$DB_USER,$DB_PSWD,$DATABASE);
    if ($dbcon->connect_error) {
        die("Connection failed: " . $dbcon->connect_error);
        
    }
    echo 'Connected!';

    $petid= $_POST['petid'];
    $update ="UPDATE parentTask SET done=true WHERE petID='".$petid. "';";

    if ($dbcon->query($update) == TRUE){
        echo "Task Completed!";
    }
    else{
        echo "Error: " . $update . " " . $dbcon->error;
    }

    $dbcon->close();
?>