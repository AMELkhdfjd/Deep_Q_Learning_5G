"""
-If a graph is connected then edges >= n-1
-If a graph has more than (n-1)(n-2)/2 edges, then it is connected.
#G = nx.gnm_random_graph(n,(2*n)-1) # a graph is chosen uniformly at random from the set of all graphs with n nodes and m edges

barabasi_albert_graph returns a random graph according to the Barabasi-Albert preferential attachment model
A graph of n nodes is grown by attaching new nodes each with m edges that are preferentially attached to existing nodes with high degree. 1 <= m < n

"""

## this file contains prebuilt graphs and ready to use directly not like the graph generator in which we generate our own random graphs


import json
import networkx as nx
import random
import matplotlib.pyplot as plt





# Code Amel



substrate5 = {"directed": False, "multigraph": False, 
 "graph": {
 "min_cpu_cost": 2300.0, "max_cpu_revenue": 4600, 
 "edge_cpu": 700, "local_cpu": 0, "centralized_cpu": 900, "bw":80000,
 "min_bw_cost": 400.0, "max_bw_revenue": 3000.0, 
 "max_cpu_profit": 2300.0, "max_bw_profit": 2600.0, 
 "nodes": [
     {"type": 1, "cpu": 100, "id": 0}, 
     {"type": 1, "cpu": 100, "id": 1}, 
     {"type": 1, "cpu": 300, "id": 2}, 
     {"type": 1, "cpu": 100, "id": 3}, 
     {"type": 1, "cpu": 300, "id": 4}, 
 ],

 "links": [
     {"bw": 5000, "source": 0, "target": 2}, 
     {"bw": 5000, "source": 0, "target": 3}, 
     {"bw": 5000, "source": 1, "target": 2}, 
     {"bw": 5000, "source": 1, "target": 4}, 
     {"bw": 5000, "source": 2, "target": 3}, 
     {"bw": 5000, "source": 3, "target": 4}, 
     ]}}

#0:central, 1:edge

substrate10 = {"directed": False, "multigraph": False, 
 "graph": {
 "min_cpu_cost": 2300.0, "max_cpu_revenue": 4600, 
 "edge_cpu": 700, "local_cpu": 0, "centralized_cpu": 900, "bw":80000,
 "min_bw_cost": 400.0, "max_bw_revenue": 3000.0, 
 "max_cpu_profit": 2300.0, "max_bw_profit": 2600.0, 
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
     {"bw": 5000, "source": 0, "target": 2, "l": 0.055}, 
     {"bw": 5000, "source": 0, "target": 3, "l": 0.076}, 
     {"bw": 5000, "source": 0, "target": 5, "l": 0.055},
     {"bw": 5000, "source": 0, "target": 7, "l": 0.066}, 
     {"bw": 5000, "source": 1, "target": 2, "l": 0.075}, 
     {"bw": 5000, "source": 1, "target": 4, "l": 0.066}, 
     {"bw": 5000, "source": 2, "target": 3, "l": 0.055}, 
     {"bw": 5000, "source": 3, "target": 4, "l": 0.076}, 
     {"bw": 5000, "source": 3, "target": 5, "l": 0.055}, 
     {"bw": 5000, "source": 4, "target": 6, "l": 0.066}, 
     {"bw": 5000, "source": 4, "target": 9, "l": 0.055}, 
     {"bw": 5000, "source": 5, "target": 6, "l": 0.066}, 
     {"bw": 5000, "source": 5, "target": 7, "l": 0.055}, 
     {"bw": 5000, "source": 6, "target": 8, "l": 0.076}, 
     {"bw": 5000, "source": 6, "target": 9, "l": 0.055}, 
     {"bw": 5000, "source": 7, "target": 8, "l": 0.066}]}}

# # substrate12 = {"directed": False, "multigraph": False, 
# # "graph": {
# #     "min_cpu_cost": 2500.0, "max_cpu_revenue": 5000, 
# #     "edge_cpu": 500, "local_cpu": 600, "centralized_cpu": 600, 
# #     "min_bw_cost": 500.0, "max_bw_revenue": 3750.0, 
# #     "max_cpu_profit": 2500.0, "max_bw_profit": 3250.0}, 
# # "nodes": [
# #     {"type": 2, "cpu": 100, "id": 0}, 
# #     {"type": 1, "cpu": 200, "id": 1}, 
# #     {"type": 1, "cpu": 150, "id": 2}, 
# #     {"type": 2, "cpu": 100, "id": 3}, 
# #     {"type": 1, "cpu": 150, "id": 4}, 
# #     {"type": 1, "cpu": 150, "id": 5}, 
# #     {"type": 1, "cpu": 200, "id": 6}, 
# #     {"type": 2, "cpu": 100, "id": 7}, 
# #     {"type": 1, "cpu": 150, "id": 8}, 
# #     {"type": 2, "cpu": 100, "id": 9}, 
# #     {"type": 1, "cpu": 200, "id": 10}, 
# #     {"type": 2, "cpu": 100, "id": 11}], 
# #     "links": [
# #     {"bw": 5000, "source": 0, "target": 2}, 
# #     {"bw": 5000, "source": 0, "target": 3}, 
# #     {"bw": 5000, "source": 1, "target": 2}, 
# #     {"bw": 5000, "source": 1, "target": 3}, 
# #     {"bw": 5000, "source": 1, "target": 4}, 
# #     {"bw": 5000, "source": 1, "target": 5}, 
# #     {"bw": 5000, "source": 1, "target": 6}, 
# #     {"bw": 5000, "source": 1, "target": 7}, 
# #     {"bw": 5000, "source": 1, "target": 9}, 
# #     {"bw": 5000, "source": 1, "target": 10}, 
# #     {"bw": 5000, "source": 3, "target": 4}, 
# #     {"bw": 5000, "source": 3, "target": 5}, 
# #     {"bw": 5000, "source": 3, "target": 6}, 
# #     {"bw": 5000, "source": 3, "target": 7}, 
# #     {"bw": 5000, "source": 3, "target": 8}, 
# #     {"bw": 5000, "source": 3, "target": 11}, 
# #     {"bw": 5000, "source": 7, "target": 8}, 
# #     {"bw": 5000, "source": 7, "target": 10}, 
# #     {"bw": 5000, "source": 7, "target": 11}, 
# #     {"bw": 5000, "source": 8, "target": 9}]}

# substrate12 = {"directed": False, "multigraph": False, 
# "graph": {
#     "min_cpu_cost": 3800.0, "max_cpu_revenue": 7600, 
#     "edge_cpu": 500, "local_cpu": 600, "centralized_cpu": 600, "bw":100000, 
#     "min_bw_cost": 500.0, "max_bw_revenue": 3750.0, 
#     "max_cpu_profit": 3800.0, "max_bw_profit": 3250.0}, 
# "nodes": [
#     {"type": 2, "cpu": 100, "id": 0}, 
#     {"type": 1, "cpu": 150, "id": 1}, 
#     {"type": 1, "cpu": 200, "id": 2}, 
#     {"type": 1, "cpu": 200, "id": 3}, 
#     {"type": 1, "cpu": 150, "id": 4}, 
#     {"type": 2, "cpu": 100, "id": 5}, 
#     {"type": 1, "cpu": 200, "id": 6}, 
#     {"type": 2, "cpu": 100, "id": 7}, 
#     {"type": 1, "cpu": 150, "id": 8}, 
#     {"type": 2, "cpu": 100, "id": 9}, 
#     {"type": 2, "cpu": 100, "id": 10}, 
#     {"type": 1, "cpu": 150, "id": 11}], 
# "links": [
#     {"bw": 5000, "source": 0, "target": 2}, 
#     {"bw": 5000, "source": 0, "target": 3}, 
#     {"bw": 5000, "source": 0, "target": 4}, 
#     {"bw": 5000, "source": 0, "target": 5}, 
#     {"bw": 5000, "source": 0, "target": 6}, 
#     {"bw": 5000, "source": 0, "target": 8}, 
#     {"bw": 5000, "source": 1, "target": 2}, 
#     {"bw": 5000, "source": 1, "target": 4}, 
#     {"bw": 5000, "source": 1, "target": 5}, 
#     {"bw": 5000, "source": 1, "target": 9}, 
#     {"bw": 5000, "source": 2, "target": 3}, 
#     {"bw": 5000, "source": 3, "target": 7}, 
#     {"bw": 5000, "source": 4, "target": 6}, 
#     {"bw": 5000, "source": 6, "target": 7}, 
#     {"bw": 5000, "source": 6, "target": 8}, 
#     {"bw": 5000, "source": 6, "target": 9}, 
#     {"bw": 5000, "source": 6, "target": 10}, 
#     {"bw": 5000, "source": 6, "target": 11}, 
#     {"bw": 5000, "source": 9, "target": 10}, 
#     {"bw": 5000, "source": 10, "target": 11}]}

# substrate14 = {"directed": False, "multigraph": False, 
# "graph": {
#     "min_cpu_cost": 4600.0, "max_cpu_revenue": 9200, 
#     "edge_cpu": 700, "local_cpu": 600, "centralized_cpu": 600, "bw":120000,
#     "min_bw_cost": 600.0, "max_bw_revenue": 4500.0, 
#     "max_cpu_profit": 4600.0, "max_bw_profit": 3900.0}, 
# "nodes": [
#     {"type": 2, "cpu": 100, "id": 0}, 
#     {"type": 2, "cpu": 100, "id": 1}, 
#     {"type": 1, "cpu": 150, "id": 2}, 
#     {"type": 1, "cpu": 200, "id": 3}, 
#     {"type": 2, "cpu": 100, "id": 4}, 
#     {"type": 2, "cpu": 100, "id": 5}, 
#     {"type": 1, "cpu": 150, "id": 6}, 
#     {"type": 1, "cpu": 200, "id": 7}, 
#     {"type": 1, "cpu": 150, "id": 8}, 
#     {"type": 1, "cpu": 200, "id": 9}, 
#     {"type": 2, "cpu": 100, "id": 10}, 
#     {"type": 1, "cpu": 150, "id": 11}, 
#     {"type": 2, "cpu": 100, "id": 12}, 
#     {"type": 2, "cpu": 100, "id": 13}], 
# "links": [
#     {"bw": 5000, "source": 0, "target": 2}, 
#     {"bw": 5000, "source": 1, "target": 2}, 
#     {"bw": 5000, "source": 1, "target": 3}, 
#     {"bw": 5000, "source": 1, "target": 4}, 
#     {"bw": 5000, "source": 1, "target": 5}, 
#     {"bw": 5000, "source": 1, "target": 7}, 
#     {"bw": 5000, "source": 1, "target": 8}, 
#     {"bw": 5000, "source": 1, "target": 11}, 
#     {"bw": 5000, "source": 2, "target": 3}, 
#     {"bw": 5000, "source": 3, "target": 4}, 
#     {"bw": 5000, "source": 3, "target": 6}, 
#     {"bw": 5000, "source": 3, "target": 7}, 
#     {"bw": 5000, "source": 4, "target": 5}, 
#     {"bw": 5000, "source": 4, "target": 6}, 
#     {"bw": 5000, "source": 4, "target": 10}, 
#     {"bw": 5000, "source": 5, "target": 8}, 
#     {"bw": 5000, "source": 5, "target": 9}, 
#     {"bw": 5000, "source": 5, "target": 10}, 
#     {"bw": 5000, "source": 5, "target": 11}, 
#     {"bw": 5000, "source": 5, "target": 12}, 
#     {"bw": 5000, "source": 5, "target": 13}, 
#     {"bw": 5000, "source": 6, "target": 9}, 
#     {"bw": 5000, "source": 6, "target": 12}, 
#     {"bw": 5000, "source": 6, "target": 13}]}

'''
    node cost = edge*3 + central 
'''

substrate16 = {"directed": False, "multigraph": False, 
"graph": {
    "min_cpu_cost": 4800, "max_cpu_revenue": 9600, 
    "edge_cpu": 1200, "local_cpu": 0, "centralized_cpu": 1200, "bw":1400, 
    "min_bw_cost": 700.0, "max_bw_revenue": 5250.0, 
    "max_cpu_profit": 4800, "max_bw_profit": 4550.0,


"nodes": [
    { "p":0.974,  "cpu": 80, "id": 0, "l": 0.0578}, ## all initially set to 100
    { "p":0.996,  "cpu": 80, "id": 1 , "l": 0.0578}, 
    { "p":0.982,  "cpu": 80, "id": 2, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 3,  "l": 0.0578}, 
    { "p":0.975,  "cpu": 80, "id": 4, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 5, "l": 0.0578}, #0.991
    { "p":0.995,  "cpu": 80, "id": 6, "l": 0.0578}, 
    { "p":0.989,  "cpu": 80, "id": 7, "l": 0.0578}, 
    { "p":0.982,  "cpu": 80, "id": 8, "l": 0.0578}, 
    { "p":0.995,  "cpu": 80, "id": 9, "l": 0.0578}, 
    { "p":0.976,  "cpu": 80, "id": 10, "l": 0.0578}, 
    { "p":0.999,  "cpu": 80, "id": 11, "l": 0.0578}, #0.976
    { "p":0.991,  "cpu": 80, "id": 12, "l": 0.0578}, #0.991
    { "p":0.982,  "cpu": 80, "id": 13, "l": 0.0578}, 
    { "p":0.996,  "cpu": 80, "id": 14, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 15, "l": 0.0578}], #0.974
    
"links": [
    {"bw": 50, "source": 0, "target": 2}, 
    {"bw": 50, "source": 0, "target": 8}, 
    {"bw": 50, "source": 0, "target": 10},
    {"bw": 50, "source": 0, "target": 12}, 
    {"bw": 50, "source": 1, "target": 2}, 
    {"bw": 50, "source": 1, "target": 3}, 
    {"bw": 50, "source": 1, "target": 5}, 
    {"bw": 50, "source": 1, "target": 6}, 
    {"bw": 50, "source": 1, "target": 11}, 
    {"bw": 50, "source": 1, "target": 13}, 
    {"bw": 50, "source": 1, "target": 14}, 
    {"bw": 50, "source": 2, "target": 3}, 
    {"bw": 50, "source": 2, "target": 4}, 
    {"bw": 50, "source": 2, "target": 7}, 
    {"bw": 50, "source": 2, "target": 12}, 
    {"bw": 50, "source": 2, "target": 15}, 
    {"bw": 50, "source": 3, "target": 4}, 
    {"bw": 50, "source": 3, "target": 15}, 
    {"bw": 50, "source": 4, "target": 5}, 
    {"bw": 50, "source": 5, "target": 6}, 
    {"bw": 50, "source": 5, "target": 7}, 
    {"bw": 50, "source": 5, "target": 9}, 
    {"bw": 50, "source": 6, "target": 8}, 
    {"bw": 50, "source": 7, "target": 11}, 
    {"bw": 50, "source": 8, "target": 9}, 
    {"bw": 50, "source": 8, "target": 14}, 
    {"bw": 50, "source": 9, "target": 10}, 
    {"bw": 50, "source": 9, "target": 13}]
    }
}






substrate32 = {"directed": False, "multigraph": False, 
"graph": {
    "min_cpu_cost": 4800, "max_cpu_revenue": 9600, 
    "edge_cpu": 1200, "local_cpu": 0, "centralized_cpu": 1200, "bw":1400, 
    "min_bw_cost": 700.0, "max_bw_revenue": 5250.0, 
    "max_cpu_profit": 4800, "max_bw_profit": 4550.0,


"nodes": [
    { "p":0.974,  "cpu": 80, "id": 0, "l": 0.0578}, ## all initially set to 100
    { "p":0.996,  "cpu": 80, "id": 1 , "l": 0.0578}, 
    { "p":0.982,  "cpu": 80, "id": 2, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 3,  "l": 0.0578}, 
    { "p":0.975,  "cpu": 80, "id": 4, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 5, "l": 0.0578}, #0.991
    { "p":0.995,  "cpu": 80, "id": 6, "l": 0.0578}, 
    { "p":0.989,  "cpu": 80, "id": 7, "l": 0.0578}, 
    { "p":0.982,  "cpu": 80, "id": 8, "l": 0.0578}, 
    { "p":0.995,  "cpu": 80, "id": 9, "l": 0.0578}, 
    { "p":0.976,  "cpu": 80, "id": 10, "l": 0.0578}, 
    { "p":0.999,  "cpu": 80, "id": 11, "l": 0.0578}, #0.976
    { "p":0.991,  "cpu": 80, "id": 12, "l": 0.0578}, #0.991
    { "p":0.982,  "cpu": 80, "id": 13, "l": 0.0578}, 
    { "p":0.996,  "cpu": 80, "id": 14, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 15, "l": 0.0578},
    { "p":0.974,  "cpu": 80, "id": 16, "l": 0.0578}, ## all initially set to 100
    { "p":0.996,  "cpu": 80, "id": 17 , "l": 0.0578}, 
    { "p":0.982,  "cpu": 80, "id": 18, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 19,  "l": 0.0578}, 
    { "p":0.975,  "cpu": 80, "id": 20, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 21, "l": 0.0578}, #0.991
    { "p":0.995,  "cpu": 80, "id": 22, "l": 0.0578}, 
    { "p":0.989,  "cpu": 80, "id": 23, "l": 0.0578}, 
    { "p":0.982,  "cpu": 80, "id": 24, "l": 0.0578}, 
    { "p":0.995,  "cpu": 80, "id": 25, "l": 0.0578}, 
    { "p":0.976,  "cpu": 80, "id": 26, "l": 0.0578}, 
    { "p":0.999,  "cpu": 80, "id": 27, "l": 0.0578}, #0.976
    { "p":0.991,  "cpu": 80, "id": 28, "l": 0.0578}, #0.991
    { "p":0.982,  "cpu": 80, "id": 29, "l": 0.0578}, 
    { "p":0.996,  "cpu": 80, "id": 30, "l": 0.0578}, 
    { "p":0.991,  "cpu": 80, "id": 31, "l": 0.0578}
    
      
    ], #0.974
    
"links": [
    {"bw": 50, "source": 0, "target": 2}, 
    {"bw": 50, "source": 0, "target": 8}, 
    {"bw": 50, "source": 0, "target": 10},
    {"bw": 50, "source": 0, "target": 12}, 
    {"bw": 50, "source": 1, "target": 2}, 
    {"bw": 50, "source": 1, "target": 3}, 
    {"bw": 50, "source": 1, "target": 5}, 
    {"bw": 50, "source": 1, "target": 6}, 
    {"bw": 50, "source": 1, "target": 11}, 
    {"bw": 50, "source": 1, "target": 13}, 
    {"bw": 50, "source": 1, "target": 14}, 
    {"bw": 50, "source": 2, "target": 3}, 
    {"bw": 50, "source": 2, "target": 4}, 
    {"bw": 50, "source": 2, "target": 7}, 
    {"bw": 50, "source": 2, "target": 12}, 
    {"bw": 50, "source": 2, "target": 15}, 
    {"bw": 50, "source": 3, "target": 4}, 
    {"bw": 50, "source": 3, "target": 15}, 
    {"bw": 50, "source": 4, "target": 5}, 
    {"bw": 50, "source": 5, "target": 6}, 
    {"bw": 50, "source": 5, "target": 7}, 
    {"bw": 50, "source": 5, "target": 9}, 
    {"bw": 50, "source": 6, "target": 8}, 
    {"bw": 50, "source": 7, "target": 11}, 
    {"bw": 50, "source": 8, "target": 9}, 
    {"bw": 50, "source": 8, "target": 14}, 
    {"bw": 50, "source": 9, "target": 10}, 
    {"bw": 50, "source": 9, "target": 13},




# link the two 16 nodes graphs

{"bw": 50, "source": 9, "target": 13},
{"bw": 50, "source": 14, "target": 16},
{"bw": 50, "source": 5, "target": 19},
{"bw": 50, "source": 4, "target": 29},
{"bw": 50, "source": 10, "target": 20},
{"bw": 50, "source": 0, "target": 31},
{"bw": 50, "source": 13, "target": 28},
{"bw": 50, "source": 8, "target": 17},
{"bw": 50, "source": 7, "target": 18},
{"bw": 50, "source": 2, "target": 25},
{"bw": 50, "source": 3, "target": 27},
{"bw": 50, "source": 17, "target": 19},
{"bw": 50, "source": 8, "target": 29},









{'bw': 50, 'source': 16, 'target': 18},
 {'bw': 50, 'source': 16, 'target': 24}, 
 {'bw': 50, 'source': 16, 'target': 26}, 
 {'bw': 50, 'source': 16, 'target': 28}, 
 {'bw': 50, 'source': 17, 'target': 18}, 
 {'bw': 50, 'source': 17, 'target': 19}, 
 {'bw': 50, 'source': 17, 'target': 21}, 
 {'bw': 50, 'source': 17, 'target': 22}, 
 {'bw': 50, 'source': 17, 'target': 27}, 
 {'bw': 50, 'source': 17, 'target': 29}, 
 {'bw': 50, 'source': 17, 'target': 30}, 
 {'bw': 50, 'source': 18, 'target': 19}, #
 {'bw': 50, 'source': 18, 'target': 20}, 
 {'bw': 50, 'source': 18, 'target': 23}, 
 {'bw': 50, 'source': 18, 'target': 28},# 
 {'bw': 50, 'source': 18, 'target':31}, 
 {'bw': 50, 'source': 19, 'target': 20}, #
 {'bw': 50, 'source': 19, 'target': 31}, #
 {'bw': 50, 'source': 20, 'target': 21},# 
 {'bw': 50, 'source': 21, 'target': 22}, #
 {'bw': 50, 'source': 21, 'target': 23},# 
 {'bw': 50, 'source': 21, 'target': 25}, 
 {'bw': 50, 'source': 22, 'target': 24}, #
 {'bw': 50, 'source': 23, 'target': 27}, #
 {'bw': 50, 'source': 24, 'target': 25},
 {'bw': 50, 'source': 24, 'target': 30}, #
 {'bw': 50, 'source': 25, 'target': 26}, #
 {'bw': 50, 'source': 25, 'target': 29} ]
    }
}




abilene = {'directed': False, 'multigraph': False, 
'graph': {
    'DateObtained': '3/02/11', 'GeoLocation': 'US', 'GeoExtent': 'Country', 'Network': 'Abilene', 
    'Provenance': 'Primary', 'Access': 0, 'Source': 'http://www.internet2.edu/pubs/200502-IS-AN.pdf', 
    'Version': '1.0', 'Type': 'REN', 'DateType': 'Historic', 'Backbone': 1, 'Commercial': 0, 'label': 
    'Abilene', 'ToolsetVersion': '0.3.34dev-20120328', 'Customer': 0, 'IX': 0, 'SourceGitVersion': 'e278b1b', 
    'DateModifier': '=', 'DateMonth': '02', 'LastAccess': '3/02/11', 'Layer': 'IP', 'Creator': 'Topology Zoo Toolset', 
    'Developed': 0, 'Transit': 0, 'NetworkDate': '2005_02', 'DateYear': '2005', 'LastProcessed': '2011_09_01', 
    'Testbed': 0,
    "min_cpu_cost": 3300, "max_cpu_revenue": 6600, 
    "edge_cpu": 800, "local_cpu": 0, "centralized_cpu": 900, "bw":700, 
    "min_bw_cost": 350.0, "max_bw_revenue": 2625.0, 
    "max_cpu_profit": 3300, "max_bw_profit": 2275.0, 
'nodes': [
    {"type": 1, "cpu": 100,'Country': 'United States', 'Longitude': -74.00597, 'Internal': 1, 'Latitude': 40.71427, 'id': 'New York'}, 
    {"type": 1, "cpu": 300,'Country': 'United States', 'Longitude': -87.65005, 'Internal': 1, 'Latitude': 41.85003, 'id': 'Chicago'}, 
    {"type": 1, "cpu": 100,'Country': 'United States', 'Longitude': -77.03637, 'Internal': 1, 'Latitude': 38.89511, 'id': 'Washington DC'}, 
    {"type": 1, "cpu": 100,'Country': 'United States', 'Longitude': -122.33207, 'Internal': 1, 'Latitude': 47.60621, 'id': 'Seattle'}, 
    {"type": 1, "cpu": 100,'Country': 'United States', 'Longitude': -122.03635, 'Internal': 1, 'Latitude': 37.36883, 'id': 'Sunnyvale'}, 
    {"type": 1, "cpu": 300,'Country': 'United States', 'Longitude': -118.24368, 'Internal': 1, 'Latitude': 34.05223, 'id': 'Los Angeles'}, 
    {"type": 1, "cpu": 100,'Country': 'United States', 'Longitude': -104.9847, 'Internal': 1, 'Latitude': 39.73915, 'id': 'Denver'}, 
    {"type": 1, "cpu": 100,'Country': 'United States', 'Longitude': -94.62746, 'Internal': 1, 'Latitude': 39.11417, 'id': 'Kansas City'}, 
    {"type": 1, "cpu": 300,'Country': 'United States', 'Longitude': -95.36327, 'Internal': 1, 'Latitude': 29.76328, 'id': 'Houston'}, 
    {"type": 1, "cpu": 100,'Country': 'United States', 'Longitude': -84.38798, 'Internal': 1, 'Latitude': 33.749, 'id': 'Atlanta'}, 
    {"type": 1, "cpu": 100,'Country': 'United States', 'Longitude': -86.15804, 'Internal': 1, 'Latitude': 39.76838, 'id': 'Indianapolis'}
], 
'links': [
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'New York', 'target': 'Chicago'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'New York', 'target': 'Washington DC'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Chicago', 'target': 'Indianapolis'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Washington DC', 'target': 'Atlanta'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Seattle', 'target': 'Sunnyvale'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Seattle', 'target': 'Denver'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Sunnyvale', 'target': 'Los Angeles'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Sunnyvale', 'target': 'Denver'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Los Angeles', 'target': 'Houston'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Denver', 'target': 'Kansas City'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Kansas City', 'target': 'Houston'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Kansas City', 'target': 'Indianapolis'},
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Houston', 'target': 'Atlanta'}, 
    {"bw": 50,'LinkType': 'OC-192', 'LinkLabel': 'OC-192c', 'LinkNote': 'c', 'source': 'Atlanta', 'target': 'Indianapolis'}
 ]}
 }

def calculate_degree_centrality(substrate): ## calculate the degree of each node
    links = substrate.graph["links"]
    nodes = substrate.graph["nodes"]
    for i in range(len(substrate.graph["nodes"])):
        degree = 0
        for l in range(len(links)):            
            if links[l]["source"] == i or links[l]["target"] == i:
                degree += 1
        nodes[i]["degree_centrality"] = degree/(len(links)-1)      

def get_graph(n): ## returns a substrate of graph depending on the number of nodes
    substrate = Substrate()
    if n == 10:
        substrate.set_graph(substrate10["graph"])
    elif n == 12:
        #substrate.set_graph(substrate12["graph"])
        pass#amel
    elif n == 5:
        substrate.set_graph(substrate5["graph"])
        pass#amel
    elif n == 14:
        #substrate.set_graph(substrate14["graph"])
        pass#amel
    elif n == 16:        
        substrate.set_graph(substrate16["graph"])           
    elif n == 32:        
        substrate.set_graph(substrate32["graph"])
    elif n == "abilene":
        substrate.set_graph(abilene["graph"])
    else:   
        return "no substrate"
    calculate_degree_centrality(substrate)    

    ## to draw the graph:
# create an empty graph
    """G = nx.Graph()

# add nodes
    for node in substrate.graph["nodes"]:
        G.add_node(node["id"], cpu=node["cpu"], p=node["p"])

# add edges
    for link in substrate.graph["links"]:
        G.add_edge(link["source"], link["target"], bw=link["bw"])

# set positions of nodes
    pos = nx.spring_layout(G)

# draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')

# draw edges
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.7, edge_color='gray')

# add node labels
    labels = {node["id"]: node["id"] for node in substrate.graph["nodes"]}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='black')

# add edge labels
    edge_labels = {(link["source"], link["target"]): str(link["bw"]) for link in substrate.graph["links"]}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='black')

# show plot
    plt.axis('off')
    plt.savefig("substrate_graph.png") # save as png   """

    return substrate 

class Substrate:
    def __init__(self):
        # self.id=id
        self.graph = {}

    def set_graph(self,graph):
        self.graph = graph


    # def set_run_till(self, t):
    #     self.run_till = t

#otras topos: NSF, ANSNET