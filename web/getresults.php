<?

function getresults($url) {
  $logcmd = "echo \"".date("F j, Y, g:i a")." ".$url."\" 2>&1 >> /var/log/pxlate/searches.log";
  `$logcmd`;
  $searchcmd = "cd /home/pxlate/pxlate/correlate; ./correlate.py \"".$url."\" 2>&1";
  return `$searchcmd`;
}

?>
