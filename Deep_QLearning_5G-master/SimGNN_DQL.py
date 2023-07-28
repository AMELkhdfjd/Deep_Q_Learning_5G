"""SimGNN class and runner."""

import glob
import torch
import random
import numpy as np
from tqdm import tqdm, trange
from torch_geometric.nn import GCNConv
from layers import AttentionModule, TenorNetworkModule
from utils import process_pair, calculate_loss, calculate_normalized_ged
from param_parser import parameter_parser
from utils import tab_printer

class SimGNN(torch.nn.Module):
    """
    SimGNN: A Neural Network Approach to Fast Graph Similarity Computation
    https://arxiv.org/abs/1808.05689
    """
    def __init__(self, args, number_of_labels):
        """
        :param args: Arguments object.
        :param number_of_labels: Number of node labels.
        """
        super(SimGNN, self).__init__()
        self.args = args
        self.number_labels = number_of_labels ## att need to search about the labels
        self.setup_layers()



    def setup_layers(self): ## prepare the layers
        """
        Creating the layers.
        """
        
        self.convolution_1 = GCNConv(self.number_labels, self.args.filters_1)
        self.convolution_2 = GCNConv(self.args.filters_1, self.args.filters_2)
        self.convolution_3 = GCNConv(self.args.filters_2, self.args.filters_3)
        self.attention = AttentionModule(self.args) ## initialise the weight matrix
        self.tensor_network = TenorNetworkModule(self.args) ## initialise the weights matrices



    def convolutional_pass(self, edge_index, features): ## GCN module
        """
        Making convolutional pass.
        :param edge_index: Edge indices.
        :param features: Feature matrix.
        :return features: Absstract feature matrix.
        """
        features = self.convolution_1(features, edge_index)
        features = torch.nn.functional.relu(features)
        features = torch.nn.functional.dropout(features,
                                               p=self.args.dropout,
                                               training=self.training)

        features = self.convolution_2(features, edge_index)
        features = torch.nn.functional.relu(features)
        features = torch.nn.functional.dropout(features,
                                               p=self.args.dropout,
                                               training=self.training)

        features = self.convolution_3(features, edge_index)
        return features

    def forward(self, data, index): ## this forward is used when we call the model with data paramter
        """
        Forward pass with graphs.
        :param data: Data dictiyonary.
        :return score: Similarity score.
        """
        edge_index_1 = data["edge_index_1"]
        edge_index_2 = data["edge_index_2"]
        features_1 = data["features_1"]
        features_2 = data["features_2"]

        ## Node Embedding
        abstract_features_1 = self.convolutional_pass(edge_index_1, features_1) ## the Us matrix from article
        abstract_features_2 = self.convolutional_pass(edge_index_2, features_2) ## the Uv matrix from the article

        ## Graph Embedding
        pooled_features_1 = self.attention.forward_1(abstract_features_1)   ### ATTTT: calls the forward from the attention class
        pooled_features_2 = self.attention.forward_2(abstract_features_2, index)   ## here we pass the GCN result

        ## NTN step
        scores = self.tensor_network(pooled_features_1, pooled_features_2)  ## a vector of similarity
        scores = torch.t(scores) ## transposition
        #print(" the final result:    ", scores)
   
       
        return scores

class SimGNNTrainer(object):
    """
    SimGNN model trainer.
    """
    def __init__(self, args, graph_1, graph_2):
        """
        :param args: Arguments object.
        """
        self.args = args
        ##
        self.graph_1 = graph_1
        self.graph_2 = graph_2
        self.initial_label_enumeration()
        self.setup_model()
        

    def setup_model(self):
        """
        Creating a SimGNN.
        """
        self.model = SimGNN(self.args, self.number_of_labels) ## the class above

    def initial_label_enumeration(self): ## groups all the labels of the two  graphs into one sorted indexed list
        """
        Collecting the unique node idsentifiers.
        """
        #print("\nEnumerating unique labels.\n")
        self.global_labels = set()
        
        #data = process_pair(str(self.graphs))
        
        
        data = {
            "labels_1": self.graph_1["labels_1"],
            "labels_2": self.graph_2["labels_2"],
            "graph_1": self.graph_1["graph_1"],
            "graph_2": self.graph_2["graph_2"]
            }
        self.graphs = data

        self.global_labels = data["labels_1"] + data["labels_2"]
        
        unique_labels = set(map(tuple, self.global_labels))
        

# Convert the unique tuples back to lists
        self.global_labels = [list(label) for label in unique_labels]
        
        ## global_labels will contain labels of the two graphs without duplicate since its a set
        self.global_labels = sorted(self.global_labels) ## att here its sorting alphabitacly considering as strings
        #self.global_labels = {val:index  for index, val in enumerate(self.global_labels)} ## puting indexes for the list of elements
        self.number_of_labels = len(self.global_labels)
    


    def transfer_to_torch(self, data):
        """
        Transferring the data to torch and creating a hash table.
        Including the indices, features and target.
        :param data: Data dictionary.
        :return new_data: Dictionary of Torch Tensors.
        """
        new_data = dict()
        ## remaining the same
        edges_1 = data["graph_1"] + [[y, x] for x, y in data["graph_1"]] ## list of edges of graph 1

        edges_2 = data["graph_2"] + [[y, x] for x, y in data["graph_2"]] ## list of edges of graph 2

        edges_1 = torch.from_numpy(np.array(edges_1, dtype=np.int64).T).type(torch.long) ## transpose the vectors to match the dimensions
        edges_2 = torch.from_numpy(np.array(edges_2, dtype=np.int64).T).type(torch.long) ## creating torch tensors here

        features_1, features_2 = [], []

    
        for n in data["labels_1"]:
            features_1.append([1.0 if n == label else 0.0 for label in self.global_labels])


        for n in data["labels_2"]:
            features_2.append([1.0 if n == label else 0.0 for label in self.global_labels])
            

        features_1 = torch.FloatTensor(np.array(features_1))
        features_2 = torch.FloatTensor(np.array(features_2))
        

        new_data["edge_index_1"] = edges_1
        new_data["edge_index_2"] = edges_2

        new_data["features_1"] = features_1
        new_data["features_2"] = features_2

        ## new_data will contain the dict of graphs
        return new_data

    def process_batch(self, index): ## return the loss
        """
        Forward pass with a batch of data.
        :param batch: Batch of graph pair locations.
        :return loss: Loss on the batch.
        """
        data = self.graphs
        data = self.transfer_to_torch(data) ## get the dict of infos
        scores = self.model(data, index) ## returns the score similarity

    
        return scores

    def fit(self, index):
        """
        Fitting a model.
        """
        #print("\nModel training.\n")
        
        self.model.train() ## here its a default function, set the params for training phase for the GNN model, maybe it will remain
        #index=3 ## for ex: we are instanciating the third vnf
        vector = self.process_batch(index) ## apply this funciton on the file of the two graphs as input
        #print("the vector is : ", vector)
        return vector
              
                
           


    




"""args = parameter_parser()
tab_printer(args)

graph_1 = {"labels_1": [[0.9,200], [0.1,100], [0.2,300], [0.3,200], [0.5,100], [0.8,400], [0.6,100], [0.2,300], [0.7,300], [0.3,400], [0.5,200], [0.9,400], [0.8,300], [0.7,200], [0.2,700], [0.9,400]], "graph_1": [[0, 3], [0, 4], [0, 5], [0, 6], [0, 10], [0, 11], [0, 12], [0, 14], [0, 15], [1, 2], [1, 3], [1, 4], [1, 5], [1, 7], [1, 9], [1, 10], [1, 11], [1, 12], [1, 13], [2, 3], [2, 5], [2, 6], [2, 7], [2, 9], [2, 10], [2, 11], [2, 13], [2, 14], [3, 9], [3, 10], [3, 12], [3, 13], [3, 15], [4, 5], [4, 7], [4, 8], [4, 9], [4, 10], [4, 15], [5, 6], [5, 7], [5, 9], [5, 10], [5, 11], [5, 14], [5, 15], [6, 7], [6, 8], [6, 9], [6, 10], [6, 15], [7, 11], [7, 12], [7, 14], [8, 11], [8, 12], [8, 13], [8, 14], [8, 15], [9, 10], [9, 11], [9, 13], [9, 15], [10, 11], [10, 12], [10, 13], [10, 14], [10, 15], [11, 12], [11, 14], [12, 13], [12, 14], [12, 15], [13, 14], [13, 15]]}
graph_2 = {"labels_2": [[0.7,100], [0.9,300], [0.4,100], [0.5,100], [0.3,300], [0.8,100], [0.7,200], [0.1,100], [0.7,200], [0.4,300], [0.5,100], [0.5,200], [0.4,300], [0.5,400], [0.3,300], [0.3,500]], "graph_2": [[0, 2], [0, 3], [0, 5], [0, 6], [0, 7], [0, 9], [0, 12], [0, 14], [0, 15], [1, 2], [1, 3], [1, 6], [1, 8], [1, 9], [1, 11], [1, 13], [1, 14], [1, 15], [2, 6], [2, 7], [2, 8], [2, 10], [2, 11], [2, 15], [3, 4], [3, 5], [3, 7], [3, 8], [3, 9], [3, 10], [3, 12], [3, 14], [3, 15], [4, 5], [4, 6], [4, 7], [4, 11], [4, 13], [4, 15], [5, 6], [5, 9], [5, 10], [5, 12], [5, 13], [5, 14], [5, 15], [6, 8], [6, 9], [6, 10], [6, 11], [6, 15], [7, 11], [7, 12], [7, 14], [7, 15], [8, 9], [8, 11], [8, 12], [8, 13], [8, 14], [9, 10], [9, 14], [10, 11], [10, 15], [11, 14], [11, 15], [12, 13], [12, 14], [12, 15], [13, 14]]}


trainer = SimGNNTrainer(args, graph_1, graph_2)
trainer.fit()"""