#!/usr/bin/env python
#
# Copyright (C) 2009 Pxlate
# Author: Vivek Sant
#

import sys
from PIL import Image
from colors import *
from contrast import *

def signature(loc):
  im = Image.open(loc)
  # TODO should we be so harsh and only allow RGBs
  #      or instead just filter out 'L's (BW)?
  if im.mode != "RGB":
    return -1
  # Forbid interlaced images (pngs?)
  if im.info.has_key("interlace"):
    if im.info['interlace'] == 1:
      return -1
  sig = [ colors(im), contrast(im) ]
  return str(sig)

if __name__ == "__main__":
  print signature(sys.argv[1])
