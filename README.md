# Statuses of VC firms in co-investment networks

## Data
`co-investments.csv` is a joined table between `organizations`, `investments`, and `funding_rounds`. 

`investments` and `funding_rounds` were merged based on `funding_round_uuid`, which was then merged with `organizations` on `investor_uuid` to add the `founded_on` column.

## Methods
### Data processing and manipulation

### Build graph and run beta centrality function

## Notes
The `initial/` folder contains some initial calculations I did to understand beta centrality. This calculates values for the whole dataset without 5 year moving window for smoothing.

## Next steps
* From Pollock et al., 2015, "In our analysis, we set beta to 75% of the reciprocal of the largest eigenvalue" [p. 493]. Currently, it is set at default beta of 0.1.
* What to do with individuals? Currently, it filters them out.
