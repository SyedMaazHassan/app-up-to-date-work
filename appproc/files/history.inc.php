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

$history = $arrOutput['history']; $history = nl2br($history);

?>

<h6>History</h6>
<table id='eum'>
<?php
echo "<tr><td>history</td><td>$history</td></tr>";
?>
</table>