l =       [0.898, 0.896, 0.894, 0.892, 0.890, 0.888, 0.886, 0.884, 0.882, 0.880,0.878, 0.876, 0.874, 0.872, 0.870, 0.868, 0.866, 0.864, 0.862, 0.860,0.858, 0.856, 0.854, 0.852, 0.850, 0.848, 0.846, 0.844, 0.842, 0.840,0.838, 0.836, 0.834, 0.832, 0.830, 0.828, 0.826, 0.824, 0.822, 0.820,0.818, 0.816, 0.814, 0.812, 0.810, 0.808, 0.806, 0.804, 0.802, 0.800,0.798, 0.796, 0.794, 0.792, 0.790, 0.788, 0.786, 0.784, 0.782, 0.780,0.778, 0.776, 0.774, 0.772, 0.770, 0.768, 0.766, 0.764, 0.762, 0.760,0.758, 0.756, 0.754, 0.752, 0.750, 0.748, 0.746, 0.744, 0.742, 0.740,    0.738, 0.736, 0.734, 0.732, 0.730, 0.728, 0.726, 0.724, 0.722, 0.722,0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722,0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722,0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722,0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722,0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722, 0.722,0.722, 0.722, 0.722, 0.722, 0.722

]
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plot
import csv
import math
import numpy as np
from scipy.signal import convolve





first_60_values = l[:65]
print(first_60_values)


graph = {
"nodes": [
      {"p":0.974, "cpu": 120, "id": 0, "l": 0.0473}, 
      {"p":0.996, "cpu": 120, "id": 1, "l": 0.0847}, 
      {"p":0.982, "cpu": 120, "id": 2, "l": 0.0527}, 
      {"p":0.991, "cpu": 120, "id": 3, "l": 0.0443}, 
      {"p":0.975, "cpu": 120, "id": 4, "l": 0.0676}, 
      {"p":0.991, "cpu": 120, "id": 5, "l": 0.0987}, 
      {"p":0.995, "cpu": 120, "id": 6, "l": 0.0902}, 
      {"p":0.989, "cpu": 120, "id": 7, "l": 0.0423}, 
      {"p":0.982, "cpu": 120, "id": 8, "l": 0.0498}, 
      {"p":0.976, "cpu": 120, "id": 9, "l": 0.0578}],  
 "links": [
     {"bw": 50, "source": 0, "target": 2, "l": 0.055}, 
     {"bw": 50, "source": 0, "target": 3, "l": 0.076}, 
     {"bw": 50, "source": 0, "target": 5, "l": 0.055},
     {"bw": 60, "source": 0, "target": 7, "l": 0.066}, 
     {"bw": 50, "source": 1, "target": 2, "l": 0.075}, 
     {"bw": 70, "source": 1, "target": 4, "l": 0.066}, 
     {"bw": 100, "source": 2, "target": 3, "l": 0.055}, 
     {"bw": 55, "source": 3, "target": 4, "l": 0.076}, 
     {"bw": 69, "source": 3, "target": 5, "l": 0.055}, 
     {"bw": 80, "source": 4, "target": 6, "l": 0.066}, 
     {"bw": 90, "source": 4, "target": 9, "l": 0.055}, 
     {"bw": 76, "source": 5, "target": 6, "l": 0.066}, 
     {"bw": 54, "source": 5, "target": 7, "l": 0.055}, 
     {"bw": 100, "source": 6, "target": 8, "l": 0.076}, 
     {"bw": 90, "source": 6, "target": 9, "l": 0.055}, 
     {"bw": 65, "source": 7, "target": 8, "l": 0.066}]}



import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

for node in graph["nodes"]:
    G.add_node(node["id"], cpu=node["cpu"], p=node["p"])
            
for link in graph["links"]:
    G.add_edge(link["source"], link["target"], bw=link["bw"])
pos = nx.spring_layout(G, 0.5)
plt.figure() 
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')
nx.draw_networkx_edges(G, pos, width=1, alpha=0.9, edge_color='gray')
node_labels = {node["id"]: f"{node['id']}" for node in graph["nodes"]}
nx.draw_networkx_labels(G, pos, node_labels, font_size=11, font_color='black', verticalalignment='center')
edge_labels = {(link["source"], link["target"]): str(link["bw"]) for link in graph["links"]}
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='black')
plt.axis('off')
plt.savefig("Before_UPdate_2.png")


