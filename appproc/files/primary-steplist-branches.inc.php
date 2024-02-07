<?php 

if($keys[3]=="Branches")

{
    
$branches = count($arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['Branches']['branch']);

    echo "<table id='eum'>";
  
    $b = 0;
    while($b < $branches)
    {

    $identifier2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['Branches']['branch'][$b]['steps']['step']['@attributes']['identifier'];


    $type2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['Branches']['branch'][$b]['steps']['step']['StepBody']['@attributes']['type'];
    
    echo "<tr><td>$identifier2</td><td>$type2</td></tr>";

    $b++;
    }

    echo "</table>";

}

?>