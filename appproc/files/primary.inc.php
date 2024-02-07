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


$PrimaryThread = $arrOutput['PrimaryThread']; $PrimaryThread_count = count($PrimaryThread);

$steps = $arrOutput['PrimaryThread']['StepList']['steps']['step'];
$steps = count($steps);

echo "<hr>";

// it appears there are 7 in all primary threads:

//  [@attributes] => Array
//  [description] => Array
//  [title] => Array
//  [ExecutionMode] => 0
//  [ReentrantFlag] => false
//  [EnabledOnStartFlag] => true
//  [StepList] => Array

echo "Admin-Info:<br />";

$label =  $arrOutput['PrimaryThread']['@attributes']['label'];
$description =  $arrOutput['PrimaryThread']['description'];
$title =  $arrOutput['PrimaryThread']['title'];
$execution_mode = $arrOutput['PrimaryThread']['ExecutionMode'];
$reentrant_flag = $arrOutput['PrimaryThread']['ReentrantFlag'];
$enabledonstart_flag = $arrOutput['PrimaryThread']['EnabledOnStartFlag'];

echo "<table>";
echo "<tr><td>label</td><td>$label</td></tr>";
echo "<tr><td>description</td><td>$description</td></tr>";
echo "<tr><td>title</td><td>$title</td></tr>";
echo "<tr><td>execution mode</td><td>$execution_mode</td></tr>";
echo "<tr><td>Reentrant flag</td><td>$reentrant_flag</td></tr>";
echo "<tr><td>Enabled on start flag</td><td>$enabledonstart_flag</td></tr>";
echo "</table>";

echo "<hr>";


echo "<h3>Steplist start</h3>";
include("primary-steplist.inc.php");
echo "<h3>Steplist end</h3>";

?>






<pre>
<b style='color:green;'>
<?php
print_r($PrimaryThread);
?>
</b>
</pre>

<?
// print_r($PrimaryThread);
?>