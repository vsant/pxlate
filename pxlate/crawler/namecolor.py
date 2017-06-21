#!/usr/bin/env python
#
# Copyright (C) 2009 Pxlate
# Author: Vivek Sant
#

import sys
sys.path.append("../signature/")
from colors import distance

clr_arr = {'red':(255,0,0),
           'orange':(255,50,0),
           'yellow':(255,255,0),
           'green':(0,192,0),
           'blue':(0,0,255),
           'purple':(160,32,240),
           'black': (0,0,0),
           'white': (255,255,255),
           'brown': (139,69,19),
           'gray': (84,84,84) }

def namecolor(rgb):
  col, dist = "", 500

  for c in clr_arr.keys():
    d = distance(clr_arr[c],rgb)
    if d < dist:
      dist = d
      col = c
  return col

if __name__ == "__main__":
  print namecolor((106, 88, 86))
