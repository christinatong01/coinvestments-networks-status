# Statuses of VC firms in co-investment networks

## File organization
`get_centrality.py` is the main code.

`coinvestments.csv` is the data.

`initial/` folder contains some initial calculations I did to understand beta centrality. This calculates values for the whole dataset without 5 year moving window for smoothing.

## Data
`coinvestments.csv` is a joined table between `organizations`, `investments`, and `funding_rounds`. 

`investments` and `funding_rounds` were merged based on `funding_round_uuid`, which was then merged with `organizations` on `investor_uuid` to add the `founded_on` column.

## Methods
### Data processing and manipulation
There are two important data structures being used. The first keeps track of investor id mapped to its corresponding founded date, sorted from earliest founded date. The second keeps track of every year in the dataset mapped to every funding round that happened in that year.

### Build graph and run beta centrality function
Using `investments_map`, get oldest founding date and create 5 year windows from that date to the year in question. Build graph with investors as nodes and edges based on shared funding rounds. Run beta centrality function on every 5 year window. Average beta centralities for each investor.

## Next steps
* How to set beta? From Pollock et al., 2015, "In our analysis, we set beta to 75% of the reciprocal of the largest eigenvalue" [p. 493]. Currently, it is set at default beta of 0.1.
* What to do with individuals? Currently, it filters them out.
