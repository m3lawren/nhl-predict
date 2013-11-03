NHL Predict
===========

An elo rating system for the current NHL season.

### Running 


1. `./download.py` to download all teams schedules
2. `./process.sh` to merge the schedules into one file with results from the regular season
3. `./elo.py` to dump the rankings to rankings.txt and write the rating changes to stdout
