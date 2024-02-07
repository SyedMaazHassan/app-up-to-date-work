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

$LastModifiedDate = $arrOutput['LastModifiedDate'];

?>

<table id='eum'>
<?php
echo "<tr><td>08</td><td>LastModifiedDate</td><td>$LastModifiedDate</td></tr>";
?>
</table>