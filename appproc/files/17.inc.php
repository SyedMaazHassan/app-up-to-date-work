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

$ProcedureFailureRecoveries = $arrOutput['ProcedureFailureRecoveries']; $ProcedureFailureRecoveries_count = count($ProcedureFailureRecoveries);

?>

<table id='eum2'>
<?php
echo "<tr><td>17</td><td>ProcedureFailureRecoveries</td><td>($ProcedureFailureRecoveries_count)</td></tr>";
?>
</table>