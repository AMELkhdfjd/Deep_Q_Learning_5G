"""Classes for SimGNN modules."""

import torch

class AttentionModule(torch.nn.Module):
    """
    SimGNN Attention Module to make a pass on graph.
    """
    def __init__(self, args):
        """
        :param args: Arguments object.
        """
        super(AttentionModule, self).__init__()
        self.args = args
        self.setup_weights()
        self.init_parameters()

    def setup_weights(self):
        """
        Defining weights.
        """

        self.weight_matrix = torch.nn.Parameter(torch.Tensor(self.args.filters_3,
                                                             self.args.filters_3)) ## att: here we set the filter_3 to 32 bcz we have 16 labels like graphs features, in our case it should be updated

    def init_parameters(self):
        """
        Initializing weights.
        """
        torch.nn.init.xavier_uniform_(self.weight_matrix) ## initialise the weight matrix with xavier methode

    def forward_1(self, embedding):  ## returns the graph embedding from the node embedding
                                    ## need to know the embedding if its all the nodes embedding
        """
        Making a forward propagation pass to create a graph level representation.
        :param embedding: Result of the GCN.
        :return representation: A graph level representation vector.
        """
        
        global_context = torch.mean(torch.matmul(embedding, self.weight_matrix), dim=0)
        #print("the embedding is :", embedding)
        #print("the weight matrix is :", self.weight_matrix)

        transformed_global = torch.tanh(global_context) ## the Context defined in the article
        sigmoid_scores = torch.sigmoid(torch.mm(embedding, transformed_global.view(-1, 1)))
        representation = torch.mm(torch.t(embedding), sigmoid_scores)
        return representation
    

## here we define the forward function for the VNE embedding, which is diff from the physical graph embedding
    def forward_2(self, embedding, index):  ## returns the graph embedding from the node embedding
                                    ## need to know the embedding if its all the nodes embedding
        """
        Making a forward propagation pass to create a graph level representation.
        :param embedding: Result of the GCN.
        :return representation: A graph level representation vector.
        """
        global_context = torch.matmul(embedding[index], self.weight_matrix)
        transformed_global = torch.tanh(global_context) ## the Context defined in the article
        sigmoid_scores = torch.sigmoid(torch.mm(embedding, transformed_global.view(-1, 1)))
        representation = torch.mm(torch.t(embedding), sigmoid_scores)
        return representation

class TenorNetworkModule(torch.nn.Module):
    """
    SimGNN Tensor Network module to calculate similarity vector.
    """
    def __init__(self, args):
        """
        :param args: Arguments object.
        """
        super(TenorNetworkModule, self).__init__()
        self.args = args
        self.setup_weights()
        self.init_parameters()

    def setup_weights(self):
        """
        Defining weights.
        """
        self.weight_matrix = torch.nn.Parameter(torch.Tensor(self.args.filters_3,
                                                             self.args.filters_3,
                                                             self.args.tensor_neurons))

        self.weight_matrix_block = torch.nn.Parameter(torch.Tensor(self.args.tensor_neurons,
                                                                   2*self.args.filters_3))
        self.bias = torch.nn.Parameter(torch.Tensor(self.args.tensor_neurons, 1))

    def init_parameters(self):
        """
        Initializing weights.
        """
        torch.nn.init.xavier_uniform_(self.weight_matrix)
        torch.nn.init.xavier_uniform_(self.weight_matrix_block)
        torch.nn.init.xavier_uniform_(self.bias)

    def forward(self, embedding_1, embedding_2): ## returns a vector for similarity
        """
        Making a forward propagation pass to create a similarity vector.
        :param embedding_1: Result of the 1st embedding after attention.
        :param embedding_2: Result of the 2nd embedding after attention.
        :return scores: A similarity score vector.
        """
        scoring = torch.mm(torch.t(embedding_1), self.weight_matrix.view(self.args.filters_3, -1))
        scoring = scoring.view(self.args.filters_3, self.args.tensor_neurons)
        scoring = torch.mm(torch.t(scoring), embedding_2)
        combined_representation = torch.cat((embedding_1, embedding_2))
        block_scoring = torch.mm(self.weight_matrix_block, combined_representation)
        scores = torch.nn.functional.relu(scoring + block_scoring + self.bias)
        return scores
