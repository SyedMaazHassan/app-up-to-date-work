<?php 

if($keys[2]=="arguments"){$arguments = count($arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument']);

 
   echo "<table id='eum' style='font-size:11px;'>";
    
    echo "<tr>
        <th>name</th>
        <th>description</th>
        <th>type</th>
        <th>value</th>
        <th>EnumValues</th>
        <th>DefaultValue</th>
        <th>required</th>
        <th>modifiable</th>
        
        
    echo </tr>";
    
    
    $b = 0;
 
    while($b < $arguments)
    {
    $name2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument'][$b]['name'];
    $description2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument'][$b]['description'];
    $type2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument'][$b]['type'];
    $value2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument'][$b]['value'];

    $enumvalues2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument'][$b]['EnumValues'];
    $defaultvalue2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument'][$b]['DefaultValue'];
    $required2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument'][$b]['required'];
    $modifiable2 = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['arguments']['argument'][$b]['modifiable'];
   
   if($required2=="true"){$required2 = "&#9989;";}else{$required2 = "#10060";}
   if($modifiable2=="true"){$modifiable2 = "&#9989;";}else{$modifiable2 = "#10060";}

       echo "<tr>
        <td>$name2</td>
        <td>$description2</td>
        <td>$type2</td>
        <td>$value2</td>

        <td>$enumvalues2</td>
        <td>$defaultvalue2</td>
        <td>$required2</td>
        <td>$modifiable2</td>
        </tr>";
    $b++;
    
    }
    echo "</table>";


}

?>