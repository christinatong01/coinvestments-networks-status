# Statuses of VC firms in co-investment networks

## File organization
`get_centrality.py` is the main code.

`coinvestments.csv` is the data.

`initial/` folder contains some initial calculations I did to understand beta centrality. This calculates values for the whole dataset without 5 year moving window for smoothing.

## Data
`coinvestments.csv` is a joined table between `investments`, `funding_rounds`, and `organizations`. 

`investments` and `funding_rounds` were merged based on `funding_round_uuid`, which was then merged with `organizations` on `investor_uuid` to add the `founded_on` column.

## Methods
### Overall approach: "DFS"
For each investor, calculate average beta centrality across all 5-year windows from founding date to interested year.

Example: find beta centralities of investors in year 2013
- Investor 1: founded in 2009, Investor 2: founded in 2006, Investor 3: founded in 2008

- Investor 1 DFS:
  - 2009-2013: build graph + beta centrality
- Investor 2 DFS:
  - 2006-2010: build graph + beta centrality
  - 2007-2011: build graph + beta centrality
  - 2008-2012: build graph + beta centrality
  - 2009-2013: build graph + beta centrality
  - calculate average beta centrality across 4 windows
- Investor 3 DFS:
  - 2008-2012: build graph + beta centrality
  - 2009-2013: build graph + beta centrality
  - calculate average beta centrality across 2 windows
 
Can index results for a specified investor.

### Data processing and manipulation
There are two important data structures being used. The first keeps track of investor id mapped to its corresponding founded date, sorted from earliest founded date. The second keeps track of every year in the dataset mapped to every funding round that happened in that year.

### Build graph and run beta centrality function
Using `investments_map`, get oldest founding date and create 5 year windows from that date to the year in question. Build graph with investors as nodes and edges based on shared funding rounds. Run beta centrality function on every 5 year window. Average beta centralities for each investor.

## Next steps
* How to set beta? From Pollock et al., 2015, "In our analysis, we set beta to 75% of the reciprocal of the largest eigenvalue" [p. 493]. The larger the beta, the more it reflects global structure. Currently, it is set at default beta of 0.1. 
* What to do with individuals? Currently, it filters them out.
* Need to fix windows when there are less than 5 years.
