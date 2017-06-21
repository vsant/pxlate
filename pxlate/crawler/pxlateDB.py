#!/usr/bin/env python
#
# Copyright (C) 2009 Pxlate
# Author: Vivek Sant
#

from MySQLdb import connect, IntegrityError, escape_string
from namecolor import clr_arr as tables

tables = tables.keys()

def sqlQ(cmd):
  conn = connect (host = "localhost", user = "pxlate", passwd = "wyxacalaca78", db = "pxlate")
  cursor = conn.cursor()
  cursor.execute(cmd)
  rows = cursor.fetchall()
  #print "server version:", row[0]
  cursor.close()
  conn.close()
  return rows

def setupDB():
  for color in tables:
    cmd = """ CREATE TABLE IF NOT EXISTS %s (
              sig VARCHAR(255) NOT NULL,
              w int NOT NULL,
              h int NOT NULL,
              url varchar(255) NOT NULL PRIMARY KEY,
              tburl varchar(255) NOT NULL,
              tags varchar(255) NOT NULL
             );
          """ % color
    res = sqlQ(cmd)
    for row in res:
      print row

def cleanDB():
  for t in tables:
    cmd = "DROP TABLE IF EXISTS %s;" % t
    sqlQ(cmd)

def resetDB():
  cleanDB()
  setupDB()

if __name__ == "__main__":
  #for row in sqlQ("SELECT VERSION()"):
  #  print row
  import sys
  if len(sys.argv) != 2:
    print "usage: %s <num 1-3>" % sys.argv[0]
    sys.exit(-1)
  t = int(sys.argv[1])
  if t == 1:
    setupDB()
  elif t == 2:
    cleanDB()
  elif t == 3:
    resetDB()
  else:
    print "usage: %s <num 1-3>" % sys.argv[0]
