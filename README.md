# conf-analysis
Analyzing the conference publication trend in CS

This repository contanins: 
- A Django local website for dataset visualization (Papers and papertracker folders)
- python scripts to produce plots
- python scripts to perfom API calls (apiloader.py apiloaderv2.py apitest.py)
- SQLite Database (2011-2020) of conference venues, papers, authors and institutions(not complete)

The most important plot scripts are:
- authorrank: plots the distribution of the two metrics for each conference
- authorrankp: plots the distribution of the metrics for a particular conference
- authorrankc: plots the distribution of the metrics for a particular category, linear regression
- allconf: plots all the conference distributions of first metric
- inter: plots all the conference distributions of second metric
- stdeval: plots the standard deviations of the metrics
