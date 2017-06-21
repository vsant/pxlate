#!/usr/bin/env python
#
# Copyright (C) 2009 Pxlate
# Author: Vivek Sant
#

from PIL import Image

# Expects 2 colors that look like (r,g,b)
# min dist will be 0
# max dist will be sqrt(255^2 * 3) = 441.673
def distance(c1, c2):
  return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2 )**(0.5)

# I: image object from Image.open
# O: freqlist - freq of similar colors (highest first)
def colors(im):
  # If the type is palette and colors are ints not 3-val tuples
  if im.mode == 'P' and type(im.getcolors(999999)[0][1]) == type(123):
    im = im.convert('RGB')
  colorlist = im.getcolors(999999)
  colorrank = sorted(colorlist, key=lambda a: -a[0])

  dims = im.size
  numpix = dims[0]*dims[1]
  sum, i, tooclose = 0, 0, 0
  newcolorfreqs = []

  while sum*100/numpix < 60: # Keep a threshhold of 60%
    for j in range(len(newcolorfreqs)):
      if distance(newcolorfreqs[j][1], colorrank[i][1]) < 15:
        newcolorfreqs[j][0] += colorrank[i][0]*100.0/numpix
        tooclose = 1
        break
      else:
        tooclose = 0
    if tooclose == 0:
      newcolorfreqs.append([ colorrank[i][0]*100.0/numpix, colorrank[i][1] ])
    sum += colorrank[i][0]
    i += 1

  newcolorfreqs = sorted(newcolorfreqs, key=lambda a: -a[0])
  newcolorfreqs = newcolorfreqs[:5]
  return map(lambda x: x[1], newcolorfreqs)

if __name__ == "__main__":
  import sys
  print colors(Image.open(sys.argv[1]))
