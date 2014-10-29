<html>
<body>

<?php

  #sudo -u username -p password my command
  #echo exec('whoami');  
  unlink("kat_sims.cfg");

  $CONFIG_FILE = "kat_sims.cfg";

  printArray($_POST);

  function printArray($array)
  {
     $file = "kat_sims.cfg";

     //echo $CONFIG_FILE;
     foreach ($array as $key => $value){
	if(!($key=="submit"))
	{	
        	$line = "$key=$value\n";
		echo "$line <br>";
		file_put_contents($file,$line, FILE_APPEND | LOCK_EX);
        	if(is_array($value)){ //If $value is an array, print it as well!
            	printArray($value);
        	}  
	}
    } 
  }

  #$script = "script.sh";
  $file = "meerkat_sims.cfg";
  
  //exec( " echo 'sh webkat.sh meerkat_sims.cfg'> file.txt " );
  //exec( "sh -i demo.sh" );

  #echo "start... <br>";
  #try
  #{
  #  echo "Run script...<br>";
  #  exec( "sh webkat.sh meerkat_sims.cfg" );
  #  echo "..Done.<br>";
  #}
  #catch (Exception $e)
  #{
  #  echo "Can't run the script", $e->getMessage(), "\n";
  #}
  #echo "...End.";

  $status = "ready.status";

  try
  {
    file_put_contents($status,"true");
  }
  catch (Exception $e)
  {
    echo "Can't change status!", $e->getMessage(),"\n";
  }

?>

</body>
</html>
