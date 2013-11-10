#!/usr/bin/python

import os
import urllib2
from datetime import datetime
import time
import sys

if not os.path.exists('dl'):
  os.makedirs('dl')

timestamp = 0
if os.path.exists('dl/timestamp.txt'):
  with open('dl/timestamp.txt', 'r') as ts_file:
    timestamp = float(ts_file.read().strip())

now = time.mktime(datetime.utcnow().timetuple())

if now - 60 * 60 * 2 <= timestamp:
  print 'Data up to date, last downloaded at {} UTC'.format(datetime.fromtimestamp(timestamp).isoformat())
  sys.exit(0)

with open('teams.txt', 'r') as f:
  for teamRaw in f:
    team = teamRaw.strip()
    url = 'http://{}.nhl.com/schedule/full.csv'.format(team)

    print 'Downloading {}...'.format(url)

    response = urllib2.urlopen(url)
    csv = response.read()

    with open('dl/{}.csv'.format(team), 'w') as out:
      out.write(csv)

with open('dl/timestamp.txt', 'w') as ts_file:
  ts_file.write(str(now))
