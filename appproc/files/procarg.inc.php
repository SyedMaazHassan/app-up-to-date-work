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

$ProcedureArguments = $arrOutput['ProcedureArguments'];
$ProcedureArgument = $arrOutput['ProcedureArguments']['ProcedureArgument'];
$ProcedureArguments_count = count($ProcedureArgument); 

?>

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

$description = $arrOutput['description']; $description = nl2br($description);

?>

<table id='eum'>
<?php
echo "<tr>";
echo "<td>15</td>";
echo "<td><a id='ProcedureArgument'>ProcedureArgument</a></td>";
echo "<td>";



$w = 0;



echo "<table id='eum2'><tr><th>&nbsp;</th><th>Name</th><th>Description</th><th>Type</th><th>Value</th></tr>";
while($w < $ProcedureArguments_count) {

	$argument_name = $arrOutput['ProcedureArguments']['ProcedureArgument'][$w]['name'];
	$argument_description = $arrOutput['ProcedureArguments']['ProcedureArgument'][$w]['description'];
    $argument_type = $arrOutput['ProcedureArguments']['ProcedureArgument'][$w]['type'];
    $argument_value = $arrOutput['ProcedureArguments']['ProcedureArgument'][$w]['value'];
 
    $EnumValues = $arrOutput['ProcedureArguments']['ProcedureArgument'][$w]['EnumValues']['EnumValue'];


$ab = is_array($EnumValues) ? count($EnumValues) : 0 ;



    echo "<tr>
        <td>$w</td>
        <td>$argument_name</td>
        <td>$argument_description</td>
        <td>$argument_type</td>
        <td>$argument_value";

    if($ab!="0"){
    
    $x = 0;

    echo "<details>";
    echo "<summary>details</summary>";
    echo "<table id='eum2'><tr><th>key</th><th>value</th></tr>";

echo "


    

";

    while($x < $ab) {

$key = $arrOutput['ProcedureArguments']['ProcedureArgument'][$w]['EnumValues']['EnumValue'][$x]['key'];
$value = $arrOutput['ProcedureArguments']['ProcedureArgument'][$w]['EnumValues']['EnumValue'][$x]['value'];


        echo "<tr><td>$key</td><td>$value</td></tr>";
        $x++;
    }
        
    echo "</table>";
    echo "</details>";
    }
    else{};


        echo "</td>";
        echo "</tr>";
    
    $w++;
}
echo "</table>";





echo "</td></tr>";

?>
</table>

