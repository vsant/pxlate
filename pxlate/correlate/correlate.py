#!/usr/bin/env python
#
# Copyright (C) 2009 Pxlate
# Author: Vivek Sant
#

import sys
sys.path.append("../crawler/")
sys.path.append("../signature/")
from os import popen, remove
from time import time
from signature import *
from colors import distance
from pxlateDB import *
from namecolor import *

def smallestDist(clr, clrs):
  currSmallest = 1000000
  for i in clrs:
    d = distance(clr, i)
    if d < currSmallest:
      currSmallest = d
  return currSmallest

# I: 2 signatures (lists)
# O: A score of closeness (lower means closer match)
def compareSigs(s1, s2):
  score = 0
  # Go through each color in s1, and find the closest ea gets to a color in s2
  for clr in s1[0]:
    score += smallestDist(clr, s2[0])
  # Add the diff between contrasts
  score += abs(s1[1] - s2[1])
  return score

def compareAspectRatio(ar1, ar2):
  return 100.0*abs(ar1-ar2)

# I: Local file loc
# O: Sorted arr of best matches

def searchDBextern(url):
  # Wget the img
  # Find file size, and return -1 if exceeds bounds
  wget_size_call = "wget --spider \""+url+"\" 2>&1 | grep \"Length: \" | cut -d' ' -f2"
  size = "".join(popen(wget_size_call).readline()[:-1].split(","))
  if size != '' and size != "unspecified":
      size = int(size)
  if size <= 4 or size >= 10485760: # 10mb limit (perhaps lower this?)
    return -1
  # Dl the img (timeout -T 3 secs, retry -t 2 times)
  loc = "dls/" + str(time())
  popen("wget --quiet -T 3 -t 2 \""+url+"\" -O "+loc)
  # searchDBlocal on the local img now!
  res = searchDBlocal(loc)
  # delete the local file
  remove(loc)
  return res

def searchDBlocal(loc):
  results = []
  loc_sig = eval(signature(loc))
  primary_color = namecolor(loc_sig[0][1])
  loc_AR = 1 #TODO Find aspect ratio of input im
  res = sqlQ("SELECT * FROM %s" % primary_color)
  for r in res:
    score = 0
    score += compareSigs(loc_sig, eval(r[0]))
    score += compareAspectRatio(loc_AR, 1.0*r[1]/r[2])
    url, tburl = r[3], r[4]
    entry = (score, url, tburl)
    # TODO Do something with the TAGS
    if score < 1000: # TODO Find a nice max val threshhold for score
      results.append(entry)
  results = sorted(results, key=lambda a: a[0])[:100] # TODO make a cutoff val for results
  return results

# I: Array of results
# O: Results in nice HTML format
def formatResults(res):
  html = ""
  html += "<table id='results'>"
  for i in range(len(res)):
    entry = res[i]
    if i == 0:
      html += "<tr>"
    elif i % 5 == 0:
      html += "</tr><tr>"
    html_entry = "<a href='%s'><img src='%s' /><br/>%s</a>" % (entry[1], entry[2], str(entry[0])[:3])
    html += "<td>"+html_entry+"</td>"
  html += "</table>"
  return html

if __name__ == "__main__":
  import psyco
  psyco.full()
  print formatResults(searchDBextern(sys.argv[1]))
