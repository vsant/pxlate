<? include("common.php");
   include("getresults.php")
?>
<html>
<head>
<title>Pxlate Image Search - Results</title>
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
<div id="version">alpha 1</div>
<a href="/"><img src="logo.png" height=50 width=128/></a>
<br/><br/>
Search: <a href="<? echo htmlspecialchars($_POST['url']); ?>"><? echo htmlspecialchars($_POST['url']); ?></a>
<div class="results-header">
Results
</div>
<? echo getresults($_POST['url']); ?>
<? footer(); ?>
</body>
</html>
