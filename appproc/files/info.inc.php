<?

// contains 00, 02, 03, 04, 05 - 06, 07, 08, 09, 10, 12, 13, 14

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

$identifier = $arrOutput['@attributes']['identifier'];
$PrintScaling = $arrOutput['PrintScaling'];
$MaxInstances = $arrOutput['MaxInstances'];
$title = $arrOutput['title'];
$MaxExecutionTime = $arrOutput['MaxExecutionTime'];
$MaxExecutionTime_count = count($MaxExecutionTime);
$UniqueId = $arrOutput['UniqueId'];
$author = $arrOutput['author'];
$LastModifiedDate = $arrOutput['LastModifiedDate'];
$hierarchy = $arrOutput['hierarchy']; $hierarchy = nl2br($hierarchy);
$version = $arrOutput['version'];
$duration = $arrOutput['duration'];

// check if variable duration exists

if (isset($duration)) {
   $duration_count  = count($duration);
}

$VerificationVersion = $arrOutput['VerificationVersion'];
$VerificationStatus = $arrOutput['VerificationStatus'];

?>


<h6>Info</h6>

<table id='eum'>
<?php
echo "<tr><td>identifier</td><td>$identifier</td></tr>";
echo "<tr><td>PrintScaling</td><td>$PrintScaling</td></tr>";
echo "<tr><td>MaxInstances</td><td>$MaxInstances</td></tr>";
echo "<tr><td>title</td><td>$title</td></tr>";
echo "<tr><td>MaxExecutionTime</td><td>$MaxExecutionTime_count</td></tr>";
echo "<tr><td>UniqueId</td><td>$UniqueId</td></tr>";
echo "<tr><td>author</td><td>$author</td></tr>";
echo "<tr><td>LastModifiedDate</td><td>$LastModifiedDate</td></tr>";
echo "<tr><td>hierarchy</td><td>$hierarchy</td></tr>";
echo "<tr><td>version</td><td>$version</td></tr>";
echo "<tr><td>12</td><td>duration</td><td>($duration_count)</td></tr>";
echo "<tr><td>13</td><td>VerificationVersion</td><td>$VerificationVersion</td></tr>";
echo "<tr><td>14</td><td>VerificationStatus</td><td>$VerificationStatus</td></tr>";
?>
</table>




}
