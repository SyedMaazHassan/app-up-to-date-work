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



echo "<h6>Procedure variables</h6>";


$y = 0;

echo "<table id='eum2'><tr><th>Name</th><th>Description</th><th>Type</th><th>EnumValues</th><th>&nbsp;</th><th>&nbsp;</th></tr>";
while($y < $ProcedureVariables_count) {


  $ProcedureVariable_name = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['name'];
  $ProcedureVariable_description = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['description'];
  $ProcedureVariable_type = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['type'];
  $ProcedureVariable_value = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['value'];
  
  $ProcedureVariable_EnumValues = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['EnumValues'];


  $ProcedureVariable_EnumValue = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['EnumValues']['EnumValue'];
    


$enumvalues = is_array($ProcedureVariable_EnumValue);
if($enumvalues=="1"){$amount = count($ProcedureVariable_EnumValue);}else{$amount = "";}

    echo "<tr>";
    echo "<td>$ProcedureVariable_name</td>";
    echo "<td>$ProcedureVariable_description</td>";
    echo "<td>$ProcedureVariable_type</td>";
    echo "<td>$ProcedureVariable_value</td>";
    echo "<td>$ProcedureVariable_EnumValues</td>";
    echo "<td>";

if($amount>0){
    echo "<details>";
    echo "<summary>details</summary>";
    echo "<table id='eum2'><tr><th>key</th><th>value</th></tr>";
}

$w = 0;

    while($w < $amount) {

$key = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['EnumValues']['EnumValue'][$w]['key'];
$value = $arrOutput['ProcedureVariables']['ProcedureVariable'][$y]['EnumValues']['EnumValue'][$w]['value'];

        echo "<tr><td>$key</td><td>$value</td></tr>";
        $w++;
    }

if($amount>0)
{
        echo "</table>";
}
    
    
    echo "</td>";
    echo "</tr>";


    $y++;}

echo "</table>";








}




?>
