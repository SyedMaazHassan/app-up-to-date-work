<?php

if($keys[2]=="StepList"){$substeps = count($arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step']);

    echo "<table id='eum'>";
    $b = 0;
    while($b < $substeps)
    {

           $identifier2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['@attributes']['identifier'];
           $title2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['title'];
           $type2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['StepBody']['@attributes']['type'];
    
           $expression2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['StepBody']['WaitCondition']['expression'];
           $window2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['StepList']['steps']['step'][$b]['StepBody']['WaitCondition']['window'];


    echo "<tr>
        <td>$identifier2</td>
        <td>$title2</td>
        <td>$type2</td>
        <td>$expression2</td>
        <td>$window2</td>
       <td>$variable2</td> 
        <td>$variable2_value</td>
        </tr>";
    $b++;
    }
    echo "</table>";
}

?>