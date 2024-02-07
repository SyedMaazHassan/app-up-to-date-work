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

$hierarchy = $arrOutput['hierarchy']; $hierarchy = nl2br($hierarchy);

?>

<table id='eum'>
<?php
echo "<tr><td>09</td><td>hierarchy</td><td>$hierarchy</td></tr>";
?>
</table>