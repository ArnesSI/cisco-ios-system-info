#!/usr/bin/env python
import sys
import re
import os
import subprocess
from optparse import OptionParser
import csv

__version__ = '1.0'
__author__ = 'Peter Ciber'
__date__ = '21.11.2016'

def main (hostslist):
  print "Gathering data for:"
  mydata = []
  for host in hostslist:
    host = host.rstrip()
    print host
    try:
      config = subprocess.check_output("rancid-restore " + host, shell=True)
    except:
      config = ''
    myhost = {}
    myinvent = {}
    for line in config.split('\n'):
      myinvent['hostname'] = host
      try:
        ctype = re.search(r"!Chassis type:\s+(.*)$", line)
        myinvent['Chassis type'] = ctype.group(1)
      except:
        pass
      try:
        cpu = re.search(r"!CPU:\s+(.*)$", line)
        myinvent['CPU'] = cpu.group(1)
      except:
        pass
      try:
        procid = re.search(r"!Processor ID:\s+(.*)$", line)
        myinvent['Processor ID'] = procid.group(1)
      except:
        pass
      try:
        image = re.search(r"!Image:\s+(.*)$", line)
        myinvent['image'] = image.group(1)
      except:
        pass
      try:
        pid = re.search(r"!PID:\s+(.*)$", line)
        myinvent['PID'] = pid.group(1)
      except:
        pass
      try:
        sn = re.search(r"!SN:\s+(.*)$", line)
        myinvent['SN'] = sn.group(1)
      except:
        pass
    myhost[host] = myinvent
    if not myinvent.has_key('Chassis type'):
      myinvent['Chassis type'] = 'None'
    if not myinvent.has_key('CPU'):
      myinvent['CPU'] = 'None'
    if not myinvent.has_key('Processor ID'):
      myinvent['Processor ID'] = 'None'
    if not myinvent.has_key('image'):
      myinvent['image'] = 'None'
    if not myinvent.has_key('PID'):
      myinvent['PID'] = 'None'
    if not myinvent.has_key('SN'):
      myinvent['SN'] = 'None'
    mydata.append(myhost)
  return mydata

def PrintToScreen(mydatadict):
  print "------------------------------------------"
  for mydict in mydatadict:
    for host, attrib in mydict.iteritems():
      print attrib['hostname'] + ' | ' + attrib['Chassis type'] + ' | ' + attrib['Processor ID'] + ' | ' + attrib['SN'] + ' | ' + attrib['image'] + ' | ' + attrib['PID'] + ' | ' + attrib['CPU']

def PrintToCSV(mylist,filename):
  print "------------------------------------------"
  print "Writing to CSV file " + filename
  with open(filename, 'w') as csvfile:
    fieldnames = ['hostname','SN','image','Chassis type', 'Processor ID','PID','CPU']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for mydict in mylist:
      for host,attrib in mydict.iteritems():
        writer.writerow(attrib)
    
if __name__ == '__main__':
  usage = 'usage: %prog'
  _parser = OptionParser(usage=usage, version='%prog '+__version__)
  _parser.add_option('-n', help='specify hostname', dest='hostname', default=None, type='str')
  _parser.add_option('-f', help='specify file with hostnames, separated with new line', dest='hostnames', default=False, type='str')
  _parser.add_option('-c', help='write data to CSV file', dest='csv', default=False, type='str')
  (FLAGS, args) = _parser.parse_args()
  if FLAGS.hostname:
    if FLAGS.csv:
      PrintToCSV(main([FLAGS.hostname]),FLAGS.csv)
    else:
      PrintToScreen(main([FLAGS.hostname]))
  elif FLAGS.hostnames:
    with open (FLAGS.hostnames, "r") as fileopen:
      hostslist = fileopen.readlines()
      if FLAGS.csv:
        PrintToCSV(main(hostslist),FLAGS.csv)
      else:
        PrintToScreen(main(hostslist))    
  else:
    _parser.print_help()
    sys.exit(0)    
