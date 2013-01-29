<?php

  /* create one master array of the records */
  $node = array();

  /* check for choice */
  if(isset($_GET['choice'])) {
    
    $node["__type"] = "DialogueNode";

    switch($_GET['choice']) {
	case 0:
	    $node["dialogue"] = "You ain't half bad yourself!";
	    break;
        case 1:
            $node["dialogue"] = "Geez, you're makin me blush.";
            break;
    }
  }
  else
  {
    $node["__type"] = "MenuNode";
    $node["choices"] = array("You are cool", "You are suuuper cool");
  }

  /* output in necessary format */
  header('Content-type: application/json');
  echo json_encode(array($node));

?>