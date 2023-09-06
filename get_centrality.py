import csv
import networkx as nx
import numpy as np
import sys
import datetime

# Round class
class Round:
    def __init__(self, funding_round_uuid, investor_uuid, investor_name, founded_on):
        self.funding_round_uuid = funding_round_uuid
        self.investor_uuid = investor_uuid
        self.investor_name = investor_name
        self.founded_on = founded_on

    # def __str__()

# Constants
DEFAULT_BETA = 0.1
DEFAULT_ALPHA = 0.1
WINDOW_SIZE = 5
NULL_DATE = datetime.datetime(1000, 1, 1)
csv_file = "coinvestments.csv"

# Calculate beta centrality for a given graph. 
# Returns centralities map for nodes in the graph.
def calculate_beta_centrality(graph):
    alpha = DEFAULT_ALPHA
    beta = DEFAULT_BETA   # Constant
    max_iterations = 100  # Maximum number of iterations

    # Initialize centrality scores
    centrality = {node: 1.0 for node in graph.nodes()}

    # Iterate to calculate Bonacich's centrality
    for _ in range(max_iterations):
        new_centrality = {}
        for node in graph.nodes():
            new_centrality[node] = beta
            for neighbor in graph.neighbors(node):
                new_centrality[node] += alpha * centrality[neighbor]
        centrality = new_centrality
    
    return centrality

def build_graph(rounds):
    graph = nx.Graph()
    funding_round_investor_map = {}
    
    for round in rounds:
        funding_round_id = round.funding_round_uuid
        investor_id = round.investor_uuid
        
        # Create node
        graph.add_node(investor_id)
        
        # Update funding round to investor adjacency list
        if funding_round_id not in funding_round_investor_map:
            funding_round_investor_map[funding_round_id] = []
        
        # Connect edges
        for inv in funding_round_investor_map[funding_round_id]:
            # Avoid self loops
            if investor_id != inv:
                graph.add_edge(investor_id, inv)
                
        funding_round_investor_map[funding_round_id].append(investor_id)
    
    return graph

# Parse date
def parse_date(date_string, date_formats):
    if date_string == 'NULL':
        return NULL_DATE
    for date_format in date_formats:
        try:
            date_object = datetime.datetime.strptime(date_string, date_format)
            return date_object
        except ValueError:
            continue
        
    raise ValueError(f"Unable to parse the date with any of the provided formats: {date_string}")

# Get arguments
if len(sys.argv) != 2:
    print("Error: provide year")
    sys.exit(1)  # Exit with an error code

interested_year = int(sys.argv[1])

# Set up vars
funding_round_investor_map = {}
investor_id_name_map = {}
graph = nx.Graph()
investor_map = {} # investor_uuid to founding date
yearly_rounds_map = {} # year to rounds that happened that year
centralities_map = {} # investment firm to beta centrality
results_map = {} # results map with investment firm to averaged beta centrality

# Another hashmap to map years to list of rounds that happened that year.
# Update map investor_uuid to map to founding date
# Get oldest founding date and create 5 year windows (append the 5 lists together) from that date up until year in question. Build graph/calc centrality for every 5 year window. 

# Read from CSV
with open(csv_file, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Skip the header row
    next(csv_reader, None)
    
    for row in csv_reader:
        cleaned_row = [value.strip() for value in row]
        funding_round_id, created_at, investor_id, investor_name, founded_on = cleaned_row
        
        if founded_on == 'NULL':
            continue
        
        # Format dates
        date_formats = ["%Y-%m-%d %H:%M:%S", "%m/%d/%Y", "%m-%d-%Y", "%m/%d/%y", "%Y-%m-%d"]
        founded_date = parse_date(founded_on, date_formats)
        created_at_date = parse_date(created_at, date_formats)
        
        # Add investor founded date 
        if investor_id not in investor_map:
            investor_map[investor_id] = founded_date
        # else:
        #     investor_map[investor_id] = min(founded_date, investor_map[investor_id])

        # Add created year
        if created_at_date.year not in yearly_rounds_map:
            yearly_rounds_map[created_at_date.year] = []
            
        yearly_rounds_map[created_at_date.year].append(Round(funding_round_id, investor_id, investor_name, founded_date))
# print(yearly_rounds_map)

# Sort both maps by year 
yearly_rounds_map = dict(sorted(yearly_rounds_map.items()))
investor_map = dict(sorted(investor_map.items(), key=lambda item: item[1]))
print(yearly_rounds_map.keys())
# print(investor_map)
for investor_id, founded_date in investor_map.items():
    if investor_id not in centralities_map:
        centralities_map[investor_id] = []
    
    for year in range(founded_date.year, interested_year - WINDOW_SIZE):
        # print(founded_date.year)
        rounds = []
        for i in range(year, year + WINDOW_SIZE):
            # print(yearly_rounds_map[i] if i in yearly_rounds_map else [])
            rounds += yearly_rounds_map[i] if i in yearly_rounds_map else []
        # print(rounds)
        centralities = calculate_beta_centrality(build_graph(rounds))
        
        # Add the items from centralities into centralities_map
        for inv, score in centralities.items():
            if inv not in centralities_map:
                centralities_map[inv] = []
            centralities_map[inv].append(score)
            
for inv, scores in centralities_map.items():
    if inv not in results_map:
        results_map[inv] = sum(centralities_map[inv]) / len(centralities_map[inv]) # Take average
        print(f"{inv}: {results_map[inv]}")