import csv
import networkx as nx
import numpy as np

# DESC: Beta centrality where adjacency matrices are constructed for the entire dataset. 

DEFAULT_BETA = 0.1

csv_file = "coinvestments_small.csv"

# Adjacency list that has funding round as the key and a list of investors
# as the value. This is used to build the graph of investor networks through
# funding round. 
funding_round_investor_map = {}

# Associate an investor ID with its name (done for clarity). 
investor_id_name_map = {}

# Every node in NetworkX graph represents an investor. Each investor is connected
# other investors based on funding round.
graph = nx.Graph()

# Open file
with open(csv_file, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Skip the header row
    next(csv_reader, None)

    # Iterate through each row
    for row in csv_reader:
        funding_round_id, investor_id, investor_name = row
        investor_id_name_map[investor_id] = investor_name
        
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
                
        
alpha = 0.1  # Scaling factor

# Get beta by building an adjacency matrix
# nodes = list(graph.nodes())
# num_nodes = len(nodes)
# adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
# for i, node in enumerate(nodes):
#     neighbors = graph[node]
#     for neighbor in neighbors:
#         j = nodes.index(neighbor)
#         adjacency_matrix[i, j] = 1
# eigenvalues = np.linalg.eigvals(adjacency_matrix)
# pollock_beta = 0.75 * 1/(max(eigenvalues))
# print(pollock_beta)

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

# Print important information
print("BONACICH'S CENTRALITY ASCENDING\n")
sorted_centrality = {k: v for k, v in sorted(centrality.items(), key=lambda item: item[1])}
for node, score in sorted_centrality.items():
    print(f"{investor_id_name_map[node]}: {score}")
    
max_centrality_value = max(centrality.values())
max_centrality_investor = [key for key, value in centrality.items() if value == max_centrality_value][0]
print(f"\nHighest network centrality is investor {investor_id_name_map[max_centrality_investor]} with value of {max_centrality_value}")
        
        