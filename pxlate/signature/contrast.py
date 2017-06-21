#!/usr/bin/env python
#
# Copyright (C) 2009 Pxlate
# Author: Vivek Sant
#

from PIL import Image
from scipy import sum

# I: image object from Image.open
# O: contrast as a number between 0-100

def contrast(im):
  a = im.histogram()
  r = a[0:256]
  g = a[256:512]
  b = a[512:768]
  # Create a threshhold (grab first t and last t vals from the histogram
  t = 52
  total = sum(r[0:t])+sum(r[256-t:256])+sum(g[0:t])+sum(g[256-t:256])+sum(b[0:t])+sum(b[256-t:256])
  # This is really a percentage, so has to be 0-100
  # Q: What percentage are the first and last t buckets of the histogram?
  # A: We are taking top t/255 = (in this case, top/bottom ~20% of histogram)
  return total*100/(sum(a))

if __name__ == "__main__":
  import sys
  print contrast(Image.open(sys.argv[1]))
