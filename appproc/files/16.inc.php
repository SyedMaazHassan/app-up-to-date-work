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

$ProcedureVariables = $arrOutput['ProcedureVariables']['ProcedureVariable']; 

if (isset($ProcedureVariables)) {
  $ProcedureVariables_count = count($ProcedureVariables);


echo "<table id='eum'>";

echo "<tr><td>16</td><td><a id='ProcedureVariables'>ProcedureVariables</a></td><td>($ProcedureVariables_count)";



$y = 0;

echo "<table id='eum2'><tr><th>Name</th><th>Description</th><th>Type</th><th>EnumValues</th></tr>";
while($y < $ProcedureVariables_count) {


  $ProcedureVariable_name = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['name'];
  $ProcedureVariable_description = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['description'];
  $ProcedureVariable_type = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['type'];
  $ProcedureVariable_EnumValues = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['EnumValues'];
    
    echo "<tr>";
    echo "<td>$ProcedureVariable_name</td>";
    echo "<td>$ProcedureVariable_description</td>";
    echo "<td>$ProcedureVariable_type</td>";
    echo "<td>$ProcedureVariable_EnumValues</td>";
    echo "</tr>";


    $y++;}

echo "</table>";


echo "</td></tr>";


echo "</table>";


}




?>
