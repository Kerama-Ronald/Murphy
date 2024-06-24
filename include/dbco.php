<?php

$host="localhost";
$user="root";
$password="";
$dbname="lb_pcea_makupa";

$conn=mysqli_connect($host,$user,$password,$dbname);

if(!$conn){

    echo "Failed to connect";
}

?>