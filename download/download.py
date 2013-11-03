#!/usr/bin/python

import os
import urllib2

if not os.path.exists('dl'):
  os.makedirs('dl')

with open('teams.txt', 'r') as f:
  for teamRaw in f:
    team = teamRaw.strip()
    url = 'http://{}.nhl.com/schedule/full.csv'.format(team)

    print 'Downloading {}...'.format(url)

    response = urllib2.urlopen(url)
    csv = response.read()

    with open('dl/{}.csv'.format(team), 'w') as out:
      out.write(csv)
