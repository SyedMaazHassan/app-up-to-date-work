<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="style.css">
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
    <title>Procedure overview</title>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>


	<!-- Favicon -->
	<link rel="shortcut icon" href="https://www-cdn.eumetsat.int/files/www_fav_icon_blue.png">

	<!-- Google Font -->
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Poppins:wght@400;500;700&display=swap">

	<!-- Plugins CSS -->
	<link rel="stylesheet" type="text/css" href="assets/vendor/font-awesome/css/all.min.css">
	<link rel="stylesheet" type="text/css" href="assets/vendor/bootstrap-icons/bootstrap-icons.css">
	<link rel="stylesheet" type="text/css" href="assets/vendor/overlay-scrollbar/css/overlayscrollbars.min.css">
	<link rel="stylesheet" type="text/css" href="assets/vendor/apexcharts/css/apexcharts.css">

	<!-- Theme CSS -->
	<link rel="stylesheet" type="text/css" href="assets/css/style.css">



</head>
<body>
<?php error_reporting(1); ?> 

<?php 

$procedure = $_REQUEST['procedure'];
if($procedure==""){$procedure = "N_AOC_I500.xml";}


echo "
<p>Select a procedure from the list.</p>
<form method='post' action='parse.php'>

<select name='procedure'>
";

if ($handle = opendir('procedures/')) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {

            $entry_show = substr("$entry", 0, -4);
            if($entry=="$procedure"){echo "<option selected value='$entry'>$entry_show</option>";}
            else{echo "<option value='$entry'>$entry_show</option>";}
        }
    }
    closedir($handle);
}

?>
</select>
<input type='submit'>
<br />

<!-- content 

00    [@attributes] => Array
01    [description] => Procedure Purpose:         FCI VNIR Calibration
02    [PrintScaling] => 100
03    [MaxInstances] => 1
04    [title] => FCI VNIR Calibration
05    [MaxExecutionTime] => Array
06    [UniqueId] => MTI1:NomSysSAT:N_FCI_I830
07    [author] => rogissart_OPRE
08    [LastModifiedDate] => 2023-04-06T12:31:47.642Z
09    [hierarchy] => Child Procedures:
10    [version] => 25.0
11    [history] => Version 1: (CT - 10.01.2023)
12    [duration] => Array
13    [VerificationVersion] => 03.07.05
14    [VerificationStatus] => Unverified
15    [ProcedureArguments] => Array
16    [ProcedureVariables] => Array
17    [ProcedureFailureRecoveries] => Array
18    [PrimaryThread] => Array
19    [SecondaryThreads] => Array

-->

<?php 

$procedure_short = substr($procedure, 0, -4);
echo "<hr /><h4>Procedure $procedure_short</h4><hr />";

 ?>


<ul class="nav nav-tabs" id="myTab" role="tablist">
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab_info" data-bs-toggle="tab" data-bs-target="#tab_info-pane" type="button" role="tab" aria-controls="profile-tab-pane" aria-selected="false">Info</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab_description" data-bs-toggle="tab" data-bs-target="#tab_description-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">Description</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab_history" data-bs-toggle="tab" data-bs-target="#tab_history-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">History</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab_procarg" data-bs-toggle="tab" data-bs-target="#tab_procarg-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">Procedure Arguments</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab_procvar" data-bs-toggle="tab" data-bs-target="#tab_procvar-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">Procedure Variables</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab17" data-bs-toggle="tab" data-bs-target="#tab17-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">ProcFailureRecov</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab_primary" data-bs-toggle="tab" data-bs-target="#tab_primary-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">primaryThread</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab19" data-bs-toggle="tab" data-bs-target="#tab19-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">secondaryThread</button></li>
</ul>


<!--

 <ul class="nav nav-tabs" id="myTab" role="tablist">
  <li class="nav-item" role="presentation"><button class="nav-link active" id="tab00" data-bs-toggle="tab" data-bs-target="#tab00-pane" type="button" role="tab" aria-controls="tab00-pane" aria-selected="true">Ident.</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab01" data-bs-toggle="tab" data-bs-target="#tab01-pane" type="button" role="tab" aria-controls="profile-tab-pane" aria-selected="false">Desc.</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab02" data-bs-toggle="tab" data-bs-target="#tab02-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">Print</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab03" data-bs-toggle="tab" data-bs-target="#tab03-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">MaxInst.</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab04" data-bs-toggle="tab" data-bs-target="#tab04-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">title</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab05" data-bs-toggle="tab" data-bs-target="#tab05-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">MaxEcexT</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab06" data-bs-toggle="tab" data-bs-target="#tab06-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">UniqueId</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab07" data-bs-toggle="tab" data-bs-target="#tab07-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">author</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab08" data-bs-toggle="tab" data-bs-target="#tab08-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">LastModDate</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab09" data-bs-toggle="tab" data-bs-target="#tab09-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">hierarchy</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab10" data-bs-toggle="tab" data-bs-target="#tab10-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">version</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab11" data-bs-toggle="tab" data-bs-target="#tab11-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">history</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab12" data-bs-toggle="tab" data-bs-target="#tab12-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">duration</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab13" data-bs-toggle="tab" data-bs-target="#tab13-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">VerifVers.</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab14" data-bs-toggle="tab" data-bs-target="#tab14-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">VerifStatus</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab15" data-bs-toggle="tab" data-bs-target="#tab15-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">ProcArg</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab16" data-bs-toggle="tab" data-bs-target="#tab16-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">ProcVar</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab17" data-bs-toggle="tab" data-bs-target="#tab17-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">ProcFailureRecov</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab18" data-bs-toggle="tab" data-bs-target="#tab18-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">primaryThread</button></li>
  <li class="nav-item" role="presentation"><button class="nav-link" id="tab19" data-bs-toggle="tab" data-bs-target="#tab19-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">secondaryThread</button></li>
</ul>


-->


<div class="tab-content" id="myTabContent">


  <div class="tab-pane fade" id="tab_description-pane" role="tabpanel" aria-labelledby="tab_description" tabindex="1"><?php require("files/description.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab_info-pane" role="tabpanel" aria-labelledby="tab_info" tabindex="2"><?php require("files/info.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab_history-pane" role="tabpanel" aria-labelledby="tab_history" tabindex="11"><?php include("files/history.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab_procarg-pane" role="tabpanel" aria-labelledby="tab15" tabindex="15"><?php include("files/procarg.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab_procvar-pane" role="tabpanel" aria-labelledby="tab16" tabindex="16"><?php include("files/procvar.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab17-pane" role="tabpanel" aria-labelledby="tab17" tabindex="17"><?php include("files/17.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab_primary-pane" role="tabpanel" aria-labelledby="tab_primary" tabindex="18"><?php include("files/primary.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab19-pane" role="tabpanel" aria-labelledby="tab19" tabindex="19"><?php include("files/19.inc.php"); ?></div>




<!--
  <div class="tab-pane fade show active" id="tab00-pane" role="tabpanel" aria-labelledby="tab00" tabindex="0"><?php include("files/00.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab01-pane" role="tabpanel" aria-labelledby="tab01" tabindex="1"><?php require("files/01.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab02-pane" role="tabpanel" aria-labelledby="tab02" tabindex="2"><?php include("files/02.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab03-pane" role="tabpanel" aria-labelledby="tab03" tabindex="3"><?php include("files/03.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab04-pane" role="tabpanel" aria-labelledby="tab04" tabindex="4"><?php include("files/04.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab05-pane" role="tabpanel" aria-labelledby="tab05" tabindex="5"><?php include("files/05.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab06-pane" role="tabpanel" aria-labelledby="tab06" tabindex="6"><?php include("files/06.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab07-pane" role="tabpanel" aria-labelledby="tab07" tabindex="7"><?php include("files/07.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab08-pane" role="tabpanel" aria-labelledby="tab08" tabindex="8"><?php include("files/08.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab09-pane" role="tabpanel" aria-labelledby="tab09" tabindex="9"><?php include("files/09.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab10-pane" role="tabpanel" aria-labelledby="tab10" tabindex="10"><?php include("files/10.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab11-pane" role="tabpanel" aria-labelledby="tab11" tabindex="11"><?php include("files/11.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab12-pane" role="tabpanel" aria-labelledby="tab12" tabindex="12"><?php include("files/12.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab13-pane" role="tabpanel" aria-labelledby="tab13" tabindex="13"><?php include("files/13.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab14-pane" role="tabpanel" aria-labelledby="tab14" tabindex="14"><?php include("files/14.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab15-pane" role="tabpanel" aria-labelledby="tab15" tabindex="15"><?php include("files/15.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab16-pane" role="tabpanel" aria-labelledby="tab16" tabindex="16"><?php include("files/16.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab17-pane" role="tabpanel" aria-labelledby="tab17" tabindex="17"><?php include("files/17.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab18-pane" role="tabpanel" aria-labelledby="tab18" tabindex="18"><?php include("files/18.inc.php"); ?></div>
  <div class="tab-pane fade" id="tab19-pane" role="tabpanel" aria-labelledby="tab19" tabindex="19"><?php include("files/19.inc.php"); ?></div>
-->


</div>
    
   
    <!-- End Example Code -->

<?php

echo "<br /><br /><br /><hr>";



?>




<details>
    <summary>show full XML</summary>
<pre>
<br /><br />
<?php print_r($arrOutput); ?>
<br /><br />
</pre>

</details>














