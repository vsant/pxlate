#!/bin/sh

errlog="/var/log/pxlate/err.log"

if [ -f $errlog ]
then
  if [ `du -b $errlog | cut -f1` != "0" ]
  then
    /usr/bin/sendEmail -f "Pxlate <vsant@fas.harvard.edu>" -t "vsant@fas.harvard.edu" -u "crawler.py halted" -o message-file=$errlog -s smtp.fas.harvard.edu
    mv $errlog $errlog".1"
  fi
fi
