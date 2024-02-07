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

?>



<table id='eum'>
<?php
echo "<tr><td>18</td><td><a id='PrimaryThread'></td><td>";


$a = 0;

echo "<table id='eum2'><tr><th>&nbsp;</th><th>no.</th><th>title</th><th>&nbsp;</th><th>&nbsp;</th></tr>";
while($a < $steps) {

	$step_name = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['@attributes']['identifier'];
	$step_title = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['title'];
	$step_label = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['label'];
	

	$substep = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'];

    echo "<tr><td>$a</td><td>$step_name</td><td>$step_title</td><td>$step_table</td>";
    
    echo "<td>";


$what = isset($substep); // checks if array exists  
    
    if($what=="1")
    {

        echo "<details>";
        echo "<summary>details</summary>";

  

        echo "<table>";

        $count_substep = count($substep);

            $b = 0;    
            while($b < $count_substep) {

            $identifier2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['@attributes']['identifier'];
            $description2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['description'];
            $title2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['title'];
            $label2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['label'];

$type2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['StepBody']['@attributes']['type'];


            $maxexec2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['StepBody']['MaxExecutionTime'];

            $expression2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['StepBody']['WaitCondition']['expression'];
            $window2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['StepBody']['WaitCondition']['window'];

 


            echo "<tr>
                <td>$b</td>
                <td>$identifier2</td>
                <td>$description2</td>
                <td>$title2</td>
                <td>$label2</td>
                <td>
                    <table>
                    <tr><td><b>type</b></td>               
                    <tr><td><small>$type2</small></td><td><small>$maxexec2</small></td><td><small>$expression2</small></td><td><small>$window2</small></td></td></tr>
                    </table>
                </tr>";
        
            $b++; 
            }

        echo "</table>";

        echo "</details>";
    }


    
    
    echo "</td></tr>";
    
    $a++;
}
echo "</table>";

echo "</td></tr>";

?>
</table>


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