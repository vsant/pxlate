<? include("common.php"); ?>
<html>
<head>
<title>Pxlate Image Search</title>
<link rel="stylesheet" type="text/css" href="style.css" />

<script type="text/javascript">
function c(w) { if (!w._haschanged) { w.value=''; document.getElementsByName("url")[0].className = "active";} w._haschanged=true; }
function r(w) { if (w.value == '') { w.value='URL of an image'; w._haschanged=false; document.getElementsByName("url")[0].className = "inactive"; } }

function showTinypicPlugin() {
    var el = document.getElementById('tinypic');
    el.style.display = '';
    if (el.src != '')
        return;
    var tpurl = "http://plugin.tinypic.com/plugin/index.php?popts=l,narrow|t,images|c,url|i,en|s,false";
    el.src = tpurl;
}

function hideTinypicPlugin() {
    var el = document.getElementById('tinypic');
    el.style.display = 'none';
}
</script>

</head>
<body>
<div id="version">alpha 1.0</div>
<center>
<!-- height=75 width=192 onLoad="document.forms.q.url.focus()"> -->
<img src="logo.png"/>
<div class="header1">search the web for similar pics with pxlate</div>

<form action="results.php" method="POST" name="q">
	<input type="text" name="url" size="50" maxlength="100" class="inactive"
				value="URL of an image" onfocus="c(this)" onblur="r(this)"/>
	<br/><input type="submit" value="Pxlate Search"/>
</form>
<div style="margin-top:20px;margin-bottom:-10px;">or <button onClick="showTinypicPlugin()">Upload a Picture</button> to <a href="http://tinypic.com/">tinypic</a> and paste the URL above.</div>
<br/>
<iframe width='260' height='260' id='tinypic' frameborder='0' style='display: none;' scrolling='no'></iframe>
</center>

<? footer(); ?>
</body>
</html>
