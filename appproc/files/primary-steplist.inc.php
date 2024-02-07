

<?php

$steplist = $arrOutput['PrimaryThread']['StepList'];
// steplist consists of title (empty) and steps



$testvalue = count($arrOutput['PrimaryThread']['StepList']['steps']);

echo "<p>Test value: $testvalue</p>";



echo "<div class='accordion' id='accordionExample'>";

$a = 0;

while($a < $steps) {

$step_name = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['@attributes']['identifier'];
$step_title = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['title'];

$step_body = count($arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']);
$step_type = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['@attributes']['type'];

          $variable = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['variable'];
           $variable_value = $arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']['VariableValue'];


$keys = array_keys($arrOutput['PrimaryThread']['StepList']['steps']['step'][$a]['StepBody']);



echo "

    <div class='accordion-item'>
        <h2 class='accordion-header'>
        <button class='accordion-button' type='button' data-bs-toggle='collapse' data-bs-target='#collapse$a' aria-expanded='false' aria-controls='collapse$a'>
        $step_name - $step_title</button></h2>

        <div id='collapse$a' class='accordion-collapse collapse' data-bs-parent='#accordionExample'>
            <div class='accordion-body'>
                <strong>Stepbody: $step_body $step_type"; print_r($keys); echo "$variable $variable_value</strong>

";



if($keys[3]=="SubThreads"){$subthreads = "test";}


include("primary-steplist-branches.inc.php");
include("primary-steplist-arguments.inc.php");
include("primary-steplist-steplist.inc.php");


echo "<p>$substeps substeps / subthreads = $subthreads / $branches branches / $arguments arguments </p>";


echo "




            </div>
        </div>
    
    </div>
  
	
";

$a++;

}

echo "</div>";

?>