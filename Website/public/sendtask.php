<?php
    
    // $DB_USER=  "doadmin";
    // $DB_PSWD = "AVNS_1OJ-Nk7eUgMXbec";
    // $DB_HOST= "db-mysql-sfo2-96686-do-user-11317347-0.b.db.ondigitalocean.com:25060";
    // $DATABASE = "peppetEMAIL";


    // $dbcon = new mysqli($DB_HOST,$DB_USER,$DB_PSWD,$DATABASE);
    // if ($dbcon->connect_error) {
    //     die("Connection failed: " . $dbcon->connect_error);
        
    // }
    // echo 'Connected!';

    // $petid= $_POST['petid'];
    // $task= $_POST['task'];
    // $reward= $_POST['reward'];

    // echo $petid;
    // echo $task;
    // echo $reward;

    // $task = "INSERT INTO parentTask (petID,task,done)
    //         VALUES ('" .$petid."','" . $task . "', false);";
    // if ($dbcon->query($task) == TRUE){
    //     echo "task sent sucessfully!";
    // }
    // else{
    //     echo"Error: " . $task . " " . $dbcon->error;
    // }
    $dbcon->close();
?>