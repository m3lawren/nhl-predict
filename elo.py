#!/usr/bin/python

import math
import re

divToTeams = { 
  'Atlantic': set(['Tampa Bay', 'Toronto', 'Detroit', 'Boston', 'Montreal', 'Ottawa', 'Florida', 'Buffalo']),
  'Metropolitan': set(['Pittsburgh', 'Washington', 'Ny Islanders', 'Ny Rangers', 'Carolina', 'Columbus', 'New Jersey', 'Philadelphia']),
  'Central': set(['Colorado', 'Chicago', 'Minnesota', 'St Louis', 'Nashville', 'Dallas', 'Winnipeg']),
  'Pacific': set(['Anaheim', 'San Jose', 'Phoenix', 'Vancouver', 'Los Angeles', 'Calgary', 'Edmonton'])
}
teamToDiv = {}
for div in divToTeams:
  for team in divToTeams[div]:
    teamToDiv[team] = div

teams = ['Anaheim','Boston','Buffalo','Calgary','Carolina','Chicago','Colorado','Columbus','Dallas','Detroit','Edmonton','Florida','Los Angeles','Minnesota','Montreal','Nashville','New Jersey','Ny Islanders','Ny Rangers','Ottawa','Philadelphia','Phoenix','Pittsburgh','San Jose','St Louis','Tampa Bay','Toronto','Vancouver','Washington','Winnipeg']
ratings = {}
homeAdv = {}
history = {}

scoreRe = re.compile('^[^,]*,([a-zA-Z ]+) ([0-9]+) - ([a-zA-Z ]+) ([0-9]+)$')

def expected(rHome, rAway):
  return 1.0 / (1.0 + math.pow(10.0, (rAway - rHome) / 400.0))

for t in teams:
  ratings[t] = 1500.0
  homeAdv[t] = 100.0
  history[t] = [('2013-09-30', 1500.0)]

with open('games-ordered.csv') as f:
  for line in f:
    date = line.strip().split(',')[0]
    (away, awayScoreStr, home, homeScoreStr) = scoreRe.match(line).groups()

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
    history[home].append((date, ratings[home]))
    history[away].append((date, ratings[away]))
    homeAdv[home] += homeDelta * 0.075

with open('rankings.txt', 'w') as f:
  for (team, rating) in sorted(ratings.items(), key=lambda x: -x[1]):
    f.write("{},{},{},{}\n".format(rating, team, teamToDiv[team], homeAdv[team]))
