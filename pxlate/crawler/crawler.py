#!/usr/bin/env python
#
# Copyright (C) 2009 Pxlate
# Author: Vivek Sant
#

import urllib, simplejson
import sys
from pxlateDB import *
from namecolor import *
from signature import *
from time import time, ctime
from os import popen, remove
from os.path import getsize
from daemon import Daemon
import logging
from settings import *

input_text = "list.txt"
LOG_FILENAME = '/var/log/pxlate/crawler-stats.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

class MyDaemon(Daemon):
    def run(self):
      crawl(input_text)

def fetchResults(q, s, e):
  # Construct the url
  urlbase = "http://ajax.googleapis.com/ajax/services/search/images?"
  ver = "v=1.0"
  key = "&key="
  rsz = "&rsz=large"                 #large=8 resuls, small=4
  start = "&start=%d" % s
  safe = "&safe=active"              #active, moderate, off
  query = urllib.urlencode({'q' : q})
  url = urlbase + ver + key + API_KEY + rsz + start + safe + "&" + query
  
  # Make the query
  search_results = urllib.urlopen(url)
  json = simplejson.loads(search_results.read())
  results = json['responseData']['results']
  # Return the results, or cons with the next chunk
  if (s + 8) <= e:
    return results + fetchResults(q,s+8,e)
  else:
    return results

# Returns the signature, or -1 on error
def createSig(url):
  logging.info(ctime()+" wget'ing "+url)
  # Find file size, and return -1 if exceeds bounds
  wget_size_call = "wget --spider \""+url+"\" 2>&1 | grep \"Length: \" | cut -d' ' -f2"
  wget_type_call = "wget --spider \""+url+"\" 2>&1 | grep \"Length: \" | grep -i \"image\""
  size = "".join(popen(wget_size_call).readline()[:-1].split(","))
  type = popen(wget_type_call).readline()
  if size != '' and size != "unspecified":
      size = int(size)
  if size <= 4 or size >= 10485760: # 10mb limit (perhaps lower this?)
    return -1
  if type == '': # make sure it's an image, and not some funky HTML err page
    return -1
  # Dl the img (timeout -T 3 secs, retry -t 2 times)
  loc = "dls/" + str(time())
  popen("wget --quiet -T 3 -t 2 \""+url+"\" -O "+loc)
  # Make sure the img dl'ed (fully)
  if getsize(loc) != size:
    return -1
  # Calculate its signature
  sig = signature(loc)
  # rm the file
  remove(loc)
  # return sig
  return sig

def addToDB(sig, w, h, url, tburl, tags):
  if sig != -1:
    color = namecolor(eval(sig)[0][0])
    try:
      sqlQ("INSERT INTO %s VALUES ('%s', %d, %d, '%s', '%s', '%s')" 
          % (color, sig, int(w), int(h), escape_string(url), escape_string(tburl), escape_string(tags)))
    except IntegrityError, message:
      if message[0] != 1062:
        raise
    logging.info(ctime()+" Added to db "+url)

def crawl(filename):
  fp = open(filename, "r")
  words = fp.readlines()
  for w in words:
    # Get the first 8 images for each word
    results = fetchResults(w, 0, 47)
    for i in results:
      sig = createSig(i['unescapedUrl'])
      # Put it into the DB
      tags = i['contentNoFormatting'].encode('ascii', 'ignore').encode('latin-1', 'ignore')
      addToDB(sig, i['width'], i['height'], i['unescapedUrl'], i['tbUrl'], tags)

if __name__ == "__main__":
  import psyco
  psyco.full()
  #sys.exit(crawl(sys.argv[1]))
  
  daemon = MyDaemon('/tmp/pxlate-crawler.pid')
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.start()
    elif 'stop' == sys.argv[1]:
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      daemon.restart()
    else:
      print "Unknown command"
      sys.exit(2)
    sys.exit(0)
  else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)
