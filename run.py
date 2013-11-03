#!/usr/bin/python

import math
import re

teams = ['Anaheim','Boston','Buffalo','Calgary','Carolina','Chicago','Colorado','Columbus','Dallas','Detroit','Edmonton','Florida','Los Angeles','Minnesota','Montreal','Nashville','New Jersey','Ny Islanders','Ny Rangers','Ottawa','Philadelphia','Phoenix','Pittsburgh','San Jose','St Louis','Tampa Bay','Toronto','Vancouver','Washington','Winnipeg']
ratings = {}
homeAdv = {}
newRatings = {}

scoreRe = re.compile('^([a-zA-Z ]+) ([0-9]+) - ([a-zA-Z ]+) ([0-9]+)$')

def expected(rHome, rAway):
  return 1.0 / (1.0 + math.pow(10.0, (rAway - rHome) / 400.0))

dumpedHeader = False
def dumpData():
  global dumpedHeader, newRatings
  if not dumpedHeader:
    print 'Date,{}'.format(','.join(teams))
    dumpedHeader = True
  print '{},{}'.format(lastDate,','.join([str(newRatings[t]) for t in teams]))

  for t in teams:
    newRatings[t] = ''

for t in teams:
  ratings[t] = 1500.0
  homeAdv[t] = 100.0
  newRatings[t] = 1500.0

lastDate = '20130930'

with open('games-ordered.csv') as f:
  for line in f:
    date = line.strip().split(',')[0]
    if date != lastDate:
      dumpData()
      lastDate = date
    (away, awayScoreStr, home, homeScoreStr) = scoreRe.match(line.strip().split(',')[1]).groups()

    awayScore = int(awayScoreStr)
    homeScore = int(homeScoreStr)

    homeRating = ratings[home] + homeAdv[home]
    awayRating = ratings[away]

    eHome = expected(homeRating, awayRating)

    sHome = 1.0
    if (awayScore > homeScore):
      sHome = 0.0

    diffMult = math.sqrt(abs(homeScore - awayScore))

    homeDelta = diffMult * 32.0 * (sHome - eHome)
    
    ratings[home] += homeDelta
    ratings[away] -= homeDelta
    newRatings[home] = ratings[home]
    newRatings[away] = ratings[away]
    homeAdv[home] += homeDelta * 0.075
  dumpData()
