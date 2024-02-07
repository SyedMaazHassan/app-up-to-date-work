<?php

libxml_use_internal_errors(TRUE);
$objXmlDocument = simplexml_load_file("procedures/$procedure");
if ($objXmlDocument === FALSE) {
    echo "There were errors parsing the XML file.\n";
    foreach(libxml_get_errors() as $error) {
        echo $error->message;
    }
    exit;
}
$objJsonDocument = json_encode($objXmlDocument);
$arrOutput = json_decode($objJsonDocument, TRUE);

$duration = $arrOutput['duration'];

// check if variable duration exists

if (isset($duration)) {
   $duration_count  = count($duration);

echo "<table id='eum'>";
echo "<tr><td>12</td><td>duration</td><td>($duration_count)</td></tr>";
echo "</table>";


}




?>

