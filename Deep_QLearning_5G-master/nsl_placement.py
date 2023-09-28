


"""                                                                           *** RAM Module ***
    This code allows to determine if an  NSLR (Network Slice Request)
    can be granted or not based on the available resources from the substrate
    several vnfs can be accepted in the same node
    
    23 oct 19:
    function reduce_nslr_graph is added to reduce the size of the nslr graph

    04 nov 19:
    functionality is added to be able to map vnfs in nodes of another type
    in case the nodes of the required type have no resources available;
    In this way, accepting nslrs from a use case will have a greater influence on
    nslrs acceptance of another use cas"""

### type here is only centralised
## orderring the vnfs starting from the backup ones
## vnfs on the same node are groups and called virtual node to reduce the nslr graph

import copy
import networkx as nx
from operator import itemgetter, attrgetter, methodcaller 
import graph_generator as ggen

## amel
import nsl_request as nslr
import substrate_graphs as substrate_graph
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

ranked_nodes_cpu = []
nsl_graph_red = {} #reduced nsl graph


def nsl_placement(req, index, substrate, already_backup, a, reliability_total):  ## need to know why we are passing the substrate
   ## a is containing the id of the physical node the agent chosen 
    global ranked_nodes_cpu
    profit_nodes = 0
    profit_links = 0
    centralized_vnfs = []
  
    n_hops = 0   


    #calculate_resource_potential(substrate,"cpu") ## for each node, sum of its links bw * node's cpu ATTTT: to rank the nodes based on the ones with more conx links and cpu capacity
    nodes = substrate.graph["nodes"] #copy to temporarily work with it
    #ranked_nodes_cpu = sort_nodes(nodes,"node_potential") #ranked list of nodes by potential considering cpu and conections     
    links = substrate.graph["links"]
    rejected = False
    flag = False # to know if a vnode has not been mapped to nodes of the same type
    


      ###### Draw the reduced graph to see how we are grouping vnfs of different types, backup & primary
    
      
    """G = nx.Graph()

    # add nodes to the graph
    for vnf in nsl_graph_red["vnodes"]:
        G.add_node(vnf["id"], type=vnf["type"])

    # add edges to the graph
    for vlink in nsl_graph_red["vlinks"]:
        G.add_edge(vlink["source"], vlink["target"])

    # draw the graph
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.savefig("red_graph_test.png") # save as png """



    ################### vnfs admission #################  
    ## here we have only two vnodes according if the vnfs are primary or backup, then aleardy will be used to put them in different nodes 
    rejected = False
    rejected_r = False
    rejected_l = False

    node = substrate.graph["nodes"][a]
    reliability = 0
    latency_totale = 0

    #already_backup = [[],[]] #list of nodes that already hold a vnode
                             ## edit: getting the list from the ressource allocation function outside
    ### print("ranked nodes",ranked_nodes_cpu)
    #print("vnodes list: ", nsl_graph_red["vnodes"])
    vnfs = req.nsl_graph["vnfs"]
    vnf = req.nsl_graph["vnfs"][index]
    vlinks = req.nsl_graph["vlinks"]

    if vnf["cpu"] <= node["cpu"] :
                        
                        
                        
                        vnf["mapped_to"] = node["id"]
                        reliability  = node["p"]
                        #substrate.graph["nodes"][node["id"]]["cpu"]  = substrate.graph["nodes"][node["id"]]["cpu"] - vnf["cpu"] ## to update the ressource of the node, new
                        node["cpu"]  = node["cpu"] - vnf["cpu"] 
                        substrate.graph["centralized_cpu"] -= vnf["cpu"]
                        #print("ACCEPT VNF")
                        ## need to update the links here

                        
                
    else: # insufficient resource, vnode rejected    

                                                                ## we are in the last vnode
                            rejected = True    
                            #print("REJECT VNF")
                            #print("enter to insufficient ressources")

    if (index == len(vnfs)-1): ## we are on the last vnf
            #print("the total reliability:  ", reliability_total)
            if(reliability_total*reliability < req.nsl_graph["reliability"]):
                #print("coucou :", reliability_total*reliability)
                reliability = -1
                rejected = True
                rejected_r = True
               
                #print("REABIILTY ISSUE --------------------- ")
           



 

    if rejected: ## free the ressources taken in the allocation process
        """G = nx.Graph()

        for node in substrate.graph["nodes"]:
                G.add_node(node["id"], cpu=node["cpu"], p=node["p"])
            
        for link in substrate.graph["links"]:
                G.add_edge(link["source"], link["target"], bw=link["bw"])
        pos = nx.spring_layout(G, 0.5)
        plt.figure() 
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.9, edge_color='gray')
        node_labels = {node["id"]: f"ID: {node['id']}\nCPU: {node['cpu']}\nP: {node['p']}" for node in substrate.graph["nodes"]}
        nx.draw_networkx_labels(G, pos, node_labels, font_size=10, font_color='black', verticalalignment='center')
        edge_labels = {(link["source"], link["target"]): str(link["bw"]) for link in substrate.graph["links"]}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='black')
        plt.axis('off')
        plt.savefig("Before_UPdate.png")"""
        for vnf in vnfs:#the nodes of the reduced graph of the accepted nslr are traversed   
            if "mapped_to" in vnf:## the vnode is mapped to one of the phisical nodes
                n = next(n for n in nodes if (n["id"] == vnf["mapped_to"] ) )## returns the phisical node mapped to the vnode                
                n["cpu"] = n["cpu"] + vnf["cpu"] ## kill will free the ressources, we will add the cpu taken to the phisical noode's cpu
                #substrate.graph["nodes"][n["id"]]["cpu"] += vnf["cpu"]
                #print("recharge: ", n["cpu"], substrate.graph["nodes"][n["id"]] , n["id"])

                
                substrate.graph["centralized_cpu"] += vnf["cpu"] ## add the cpu freed to the sum of cpu ressource of all the graph
        






        #links = copy.deepcopy(substrate.graph["links"])
        links = substrate.graph["links"]
        ## update the links in case reject of the request
        for vlink in vlinks:
            try:#when two vnfs are instantiated in the same node there is no link
                path = vlink["mapped_to"]            
            except KeyError:
                path=[]
            for i in range(len(path)-1):
                try:
                    l = next(l for l in links if ( (l["source"]==path[i] and l["target"]==path[i+1]) or (l["source"]==path[i+1] and l["target"]==path[i]) ) )              
                  
                    l["bw"] += vlink["bw"]
                    substrate.graph["bw"] += vlink["bw"]
                   
                except StopIteration:
                    pass
        """G = nx.Graph()
        for node in substrate.graph["nodes"]:
                G.add_node(node["id"], cpu=node["cpu"], p=node["p"])

        for link in substrate.graph["links"]:
                G.add_edge(link["source"], link["target"], bw=link["bw"])
        pos = nx.spring_layout(G, 0.5)
        plt.figure() 
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.9, edge_color='gray')
        node_labels = {node["id"]: f"ID: {node['id']}\nCPU: {node['cpu']}\nP: {node['p']}" for node in substrate.graph["nodes"]}
        nx.draw_networkx_labels(G, pos, node_labels, font_size=10, font_color='black', verticalalignment='center')
        edge_labels = {(link["source"], link["target"]): str(link["bw"]) for link in substrate.graph["links"]}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='black')
        plt.axis('off')
        plt.savefig("After_update.png")"""
               
        
   
        


########                
    
    ################## vlinks admission #################ù
    #print("placement done ! entering now to the analyse links function :")
    if not rejected:
        #print("VNF n°:  ", index, "MAPPED TO : ",  n["id"], "with profit:  ", n["p"])
        rejected, n_hops = analyze_links(req.nsl_graph,index, substrate)
        if rejected:
            print("LIIIIIIINKS", rejected)
        
        ## Latency section
        else:
            if (index == len(vnfs)-1): 
                for v in vnfs:
                    latency_totale += nodes[v["mapped_to"]]["l"]
                    #print("the latency of node: ", nodes[v["mapped_to"]]["l"], v["mapped_to"])
                for vl in vlinks:
                  if "mapped_to" in vl:
                    path = vl["mapped_to"] ## path = [2, 3, 0, 7]
                    #print("the path:", path)
                    for i in range(len(path)-1):
                         source = path[i]
                         destination = path[i+1]
                         for j in range(len(links)):
                            if (links[j]["source"] == source and links[j]["target"] == destination) or (links[j]["source"] == destination and links[j]["target"] == source):
                                 latency_totale += links[j]["l"]
                                 #print("the latency of link: ", links[j]["l"])
                     
                #print("total latency: ", latency_totale)      
                if (latency_totale > req.nsl_graph["latency"]):
                       
                        rejected = True
                        rejected_l = True
                        latency_totale = -1
                        #print("Latency ISSUE --------------------- ")

                
                     
                     
                                                                                                                                                                                                                                                                             
             
        

    
    return rejected,  rejected_l, rejected_r, latency_totale, reliability 






def analyze_links(nsl_graph, index, substrate): ## returns the length of the path in addition in order to calculate the latency

    ## ATT: the virtual link vlink, can be more than one link in the physical representation
    '''
   Makes the accept or reject decision based on the shortest path
    Find the shortest path and with enough bw in each link to instantiate
    a v.link. Max number of hops allowed is 5
    If there is no path with hops <= 5 and enough bw, the nslr is rejected
    '''
 
    G = nx.node_link_graph(substrate.graph)#graph format
    links = copy.deepcopy(substrate.graph["links"])#copy to temporarily work with it
    reject = False
    max_hops = 6
    chosen_path =[]
    n_hops = 0
    vlinks = nsl_graph["vlinks"]

    vnf = nsl_graph["vnfs"][index] ## att: we work only with vnodes 
    vnfs = nsl_graph["vnfs"]
    path = []
    #print("the vnf to place is : ", vnf["id"])
    #print("the vnfs: ", vnfs)
    for vlink in vlinks:
        #print("the target vlink : ", vlink["target"])
        #print("the error here: ", vnf["id"], vlink["source"], vlink["target"])
        if vnf["id"] == vlink["target"]: 
            substrate_dst = vnf["mapped_to"]
            #print("the substrate_dst :", vnf["mapped_to"])
            substrate_src = vnfs[vlink["source"]]["mapped_to"]

           
            #print("source", substrate_src, "destination", substrate_dst)
            # print("\n***vlink:",vlink)
            paths = nx.all_simple_paths(G,source=substrate_src,target=substrate_dst)
            path_list = [p for p in paths]
            path_list.sort(key=len)
            #print("the path list ", path_list)
            for path in path_list:
                #check if all the links in the path have sufficient resource
                enough = True
                # print("*PATH:",path)
                if len(path) >= max_hops:
                    reject = True
                    # print("hops number is 5 or higher")
                    break
                else:    
                    for l in range(len(path)-1):

                        link = next(lk for lk in links if ( (lk["source"]==path[l] and lk["target"]==path[l+1]) or (lk["source"]==path[l+1] and lk["target"]==path[l]) ) )
                        # print("*",path[l],path[l+1])
                        # print("link:",link["bw"])
                        if vlink["bw"] <= link["bw"]: #hay suficiente bw                        
                            link["bw"] -= vlink["bw"] #resource is updated
                            substrate.graph["bw"] -= vlink["bw"]
                            #enough bw    
                            ##enough = True                   
                        else:# not enough bw
                            enough = False

                    if enough:
                        # print("MAPEAR")
                        vlink["mapped_to"] = path#if there was enough bw on each link of the path, it is mapp
                        #print("the path choosen", path)
                        chosen_path = path
                        break
                    elif enough == False and path_list.index(path) == len(path_list)-1:
                            reject = True 
        

        


                     
                
        if reject:
            break

    if reject: ## free the resources taken during the allocation process
        for vlink in vlinks:
            try:#when two vnfs are instantiated in the same node there is no link
                path = vlink["mapped_to"]            
            except KeyError:
                path=[]
            for i in range(len(path)-1):
                try:
                    l = next(l for l in links if ( (l["source"]==path[i] and l["target"]==path[i+1]) or (l["source"]==path[i+1] and l["target"]==path[i]) ) )              
                  
                    l["bw"] += vlink["bw"]
                    substrate.graph["bw"] += vlink["bw"]
                   
                except StopIteration:
                    pass
    
    for vlink in vlinks:
        try:#when two vnfs are instantiated in the same node there is no link
            if(vnf["id"] == vlink["target"]):
                path = vlink["mapped_to"]  
                #print("the smaaaaaaal path:  ", path)          
        except KeyError:
                path=[]
        n_hops += len(path) - 1

    return reject, n_hops


#substrate = ggen.ba_graph("amel_test",15) 
#print(substrate)
#decision = nsl_placement(NSLR, substrate)

## Amel code

"""substrate = substrate_graph.get_graph(10)

NSLR = nslr.get_nslr(1,"urllc_1",50)

decision = nsl_placement(NSLR, substrate)
print(decision)





## to draw the graph:
# create an empty graph
G = nx.Graph()

# add nodes
for node in substrate.graph["nodes"]:
    G.add_node(node["id"], cpu=node["cpu"], type=node["type"])

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
plt.savefig("substrate_graph.png") # save as png   



## to draw the NSLR:


# create an empty graph
G = nx.Graph()

# add nodes to the graph
for vnf in NSLR.nsl_graph["vnfs"]:
    G.add_node(vnf["id"], function=vnf["function"], type=vnf["type"], backup=vnf["backup"])

# add edges to the graph
for vlink in NSLR.nsl_graph["vlinks"]:
    G.add_edge(vlink["source"], vlink["target"])

# draw the graph
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
plt.savefig("NSLR_graph.png") # save as png  """






"""def nsl_placement(nslr, substrate):  ## need to know why we are passing the substrate

    global ranked_nodes_cpu
    profit_nodes = 0
    profit_links = 0
    centralized_vnfs = []
    # local_vnfs = []
    #edge_vnfs = []   
    n_hops = 0   

    vnfs = nslr.nsl_graph["vnfs"] #considerar rankear vnfs tambien
    ##reduce_nslr_graph(nslr) #builds a reduced version of the nsl_graph to reduce the size of it based on if we have seccessor backups we put them in one virtual node
    
    ##vnodes = nslr.nsl_graph_reduced["vnodes"]    ## !! if its not working check here for the return of the above function


    #Amel code to avoid reducing the nslr graph
    vnodes=vnfs
    nslr.set_nsl_graph_reduced(nslr.nsl_graph) 
    nsl_graph_red=nslr.nsl_graph

    ## end code


  
    calculate_resource_potential(substrate,"cpu") ## for each node, sum of its links bw * node's cpu ATTTT: to rank the nodes based on the ones with more conx links and cpu capacity
    nodes = copy.deepcopy(substrate.graph["nodes"]) #copy to temporarily work with it
    ranked_nodes_cpu = sort_nodes(nodes,"node_potential") #ranked list of nodes by potential considering cpu and conections     

    rejected = False
    flag = False # to know if a vnode has not been mapped to nodes of the same type
    


      ###### Draw the reduced graph to see how we are grouping vnfs of different types, backup & primary
    
      
    """"""G = nx.Graph()

    # add nodes to the graph
    for vnf in nsl_graph_red["vnodes"]:
        G.add_node(vnf["id"], type=vnf["type"])

    # add edges to the graph
    for vlink in nsl_graph_red["vlinks"]:
        G.add_edge(vlink["source"], vlink["target"])

    # draw the graph
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.savefig("red_graph_test.png") # save as png """"""







      



    ################### vnfs admission #################  
    ## here we have only two vnodes according if the vnfs are primary or backup, then aleardy will be used to put them in different nodes 
    rejected = False
    already_backup = [[],[]] #list of nodes that already hold a vnode
    ### print("ranked nodes",ranked_nodes_cpu)
    #print("vnodes list: ", nsl_graph_red["vnodes"])
    for i in range(len(vnodes)):
        if rejected:
            break
        if i > 0:
            pre_vnf = vnodes[i - 1]
            pre_backup = pre_vnf["backup"]
            #print("backup type of previous node",pre_backup)
            if(pre_backup != vnodes[i]["backup"]):  ## we have diff types of backup, need to find another physical node to map it
            
                for j, n in enumerate(ranked_nodes_cpu):
                    if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[vnodes[i-1]["backup"]]:
                        
                        already_backup[vnodes[i]["backup"]].append(n["id"])
                        
                        vnodes[i]["mapped_to"] = n["id"]
                        #print("not_same_backup",vnodes[i] , "mapped to ", n["id"])
                        substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                        n["cpu"]  = n["cpu"] - vnodes[i]["cpu"] 
                        substrate.graph["centralized_cpu"] -= vnodes[i]["cpu"]
                        break
                
                    else: # insufficient resource, vnode rejected    

                        if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                            rejected = True    
                            #print("enter to insufficient ressources")
                            #print("insufficient ressources")
                            break 
            else:   ### we have the same backup
                for j, n in enumerate(ranked_nodes_cpu):
                    if(vnodes[i]["backup"] == 0):
                        if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[1]:
                            
                            already_backup[vnodes[i]["backup"]].append(n["id"])
                            vnodes[i]["mapped_to"] = n["id"]
                            #print("same backup 0", vnodes[i] , "mapped to ", n["id"])
                            substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                            n["cpu"]  = n["cpu"] - vnodes[i]["cpu"] 
                            substrate.graph["centralized_cpu"] -= vnodes[i]["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                #print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
                    else:
                        if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[0]:
                            
                            already_backup[vnodes[i]["backup"]].append(n["id"])
                            vnodes[i]["mapped_to"] = n["id"] 
                            #print("same backup 1", vnodes[i] , "mapped to ", n["id"])
                            substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                            n["cpu"]  = n["cpu"] - vnodes[i]["cpu"]                            
                            substrate.graph["centralized_cpu"] -= vnodes["cpu"]

                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                #print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
        else:### here we are treating the first vnode, we dont have a previous one
            
            for j, n in enumerate(ranked_nodes_cpu):
                    
                    if(vnodes[i]["backup"] == "0"):
                        if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[1]:
                            already_backup[vnodes[i]["backup"]].append(n["id"])
                            
                            vnodes[i]["mapped_to"] = n["id"]
                            #print("the first node", vnodes[i] , "mapped to ", n["id"])
                            substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                            n["cpu"]  = n["cpu"] - vnodes[i]["cpu"]                            
                            substrate.graph["centralized_cpu"] -= vnodes[i]["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                #print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
                    else:
                        if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[0]:
                            
                            already_backup[vnodes[i]["backup"]].append(n["id"])
                            
                            vnodes[i]["mapped_to"] = n["id"]
                            #print("the first node ", vnodes[i] , "mapped to ", n["id"])
                            substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                            n["cpu"]  = n["cpu"] - vnodes[i]["cpu"]                            
                            substrate.graph["centralized_cpu"] -= vnodes[i]["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                #print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
    if rejected: ## free the ressources taken in the allocation process
        for vnf in vnodes:#the nodes of the reduced graph of the accepted nslr are traversed   
            if "mapped_to" in vnf:## the vnode is mapped to one of the phisical nodes
                n = next(n for n in nodes if (n["id"] == vnf["mapped_to"] and n["type"]==vnf["type"]) )## returns the phisical node mapped to the vnode                
                n["cpu"] = n["cpu"] + vnf["cpu"] ## kill will free the ressources, we will add the cpu taken to the phisical noode's cpu
                substrate.graph["centralized_cpu"] += vnf["cpu"] ## add the cpu freed to the sum of cpu ressource of all the graph
               
        
   
        


########                
    
    ################## vlinks admission #################ù
    #print("placement done ! entering now to the analyse links function :")
    if not rejected:
        rejected, n_hops = analyze_links(nslr.nsl_graph,substrate)
        #print("decision after analyse links", rejected, "number of hops", n_hops)
    #else:
         #print("\n\n","***rejected by the lack of node rsc","\n\n")
    ################### ------------- #################
    #if rejected:
         #print("\n\n","***rejected by the lack of link rsc","\n\n")

    return rejected, n_hops """










"""
def analyze_links(nsl_graph, index, substrate): ## returns the length of the path in addition in order to calculate the latency

    ## ATT: the virtual link vlink, can be more than one link in the physical representation
    '''
   Makes the accept or reject decision based on the shortest path
    Find the shortest path and with enough bw in each link to instantiate
    a v.link. Max number of hops allowed is 5
    If there is no path with hops <= 5 and enough bw, the nslr is rejected
    '''
 
    G = nx.node_link_graph(substrate.graph)#graph format
    links = copy.deepcopy(substrate.graph["links"])#copy to temporarily work with it
    reject = False
    max_hops = 6
    chosen_path =[]
    n_hops = 0

    vlinks = nsl_graph["vlinks"]
    vnfs = nsl_graph["vnfs"] ## att: we work only with vnodes 
    for vlink in vlinks:
        substrate_src = next(vnf["mapped_to"] for vnf in vnfs if vnf["id"] == vlink["source"]) 
        substrate_dst = next(vnf["mapped_to"] for vnf in vnfs if vnf["id"] == vlink["target"])
        #print("source", substrate_src, "destination", substrate_dst)
        # print("\n***vlink:",vlink)
        # que hacer con las vnfs que se instancian en el mismo nodo? cobrar por vlink? cuanto?
        paths = nx.all_simple_paths(G,source=substrate_src,target=substrate_dst)
        path_list = [p for p in paths]
        path_list.sort(key=len)
        #print("the path list ", path_list)
        for path in path_list:
            #check if all the links in the path have sufficient resource
            enough = True
            # print("*PATH:",path)
            if len(path) >= max_hops:
                reject = True
                # print("hops number is 5 or higher")
                break
            else:    
                for l in range(len(path)-1):

                    link = next(lk for lk in links if ( (lk["source"]==path[l] and lk["target"]==path[l+1]) or (lk["source"]==path[l+1] and lk["target"]==path[l]) ) )
                    # print("*",path[l],path[l+1])
                    # print("link:",link["bw"])
                    if vlink["bw"] <= link["bw"]: #hay suficiente bw                        
                        link["bw"] -= vlink["bw"] #resource is updated
                        substrate.graph["bw"] -= vlink["bw"]
                        #enough bw    
                        ##enough = True                   
                    else:# not enough bw
                        enough = False

                if enough:
                    # print("MAPEAR")
                    vlink["mapped_to"] = path#if there was enough bw on each link of the path, it is mapp
                    #print("the path choosen", path)
                    chosen_path = path
                    break
                elif enough == False and path_list.index(path) == len(path_list)-1:
                        reject = True              
                
        if reject:
            break

    if reject: ## free the resources taken during the allocation process
        for vlink in vlinks:
            try:#when two vnfs are instantiated in the same node there is no link
                path = vlink["mapped_to"]            
            except KeyError:
                path=[]
            for i in range(len(path)-1):
                try:
                    l = next(l for l in links if ( (l["source"]==path[i] and l["target"]==path[i+1]) or (l["source"]==path[i+1] and l["target"]==path[i]) ) )              
                  
                    l["bw"] += vlink["bw"]
                    substrate.graph["bw"] += vlink["bw"]
                   
                except StopIteration:
                    pass

    for vlink in vlinks:
        try:#when two vnfs are instantiated in the same node there is no link
                path = vlink["mapped_to"]  
                #print("the smaaaaaaal path:  ", path)          
        except KeyError:
                path=[]
        n_hops += len(path) - 1

    return reject, n_hops"""









##################### the part for the last version of nsl_placement #######################


"""def nsl_placement(req, index, substrate, already_backup):  ## need to know why we are passing the substrate

    global ranked_nodes_cpu
    profit_nodes = 0
    profit_links = 0
    centralized_vnfs = []
  
    n_hops = 0   

 


  
    calculate_resource_potential(substrate,"cpu") ## for each node, sum of its links bw * node's cpu ATTTT: to rank the nodes based on the ones with more conx links and cpu capacity
    nodes = copy.deepcopy(substrate.graph["nodes"]) #copy to temporarily work with it
    ranked_nodes_cpu = sort_nodes(nodes,"node_potential") #ranked list of nodes by potential considering cpu and conections     

    rejected = False
    flag = False # to know if a vnode has not been mapped to nodes of the same type
    


      ###### Draw the reduced graph to see how we are grouping vnfs of different types, backup & primary
    
      
    """"""G = nx.Graph()


    # add nodes to the graph
    for vnf in nsl_graph_red["vnodes"]:
        G.add_node(vnf["id"], type=vnf["type"])

    # add edges to the graph
    for vlink in nsl_graph_red["vlinks"]:
        G.add_edge(vlink["source"], vlink["target"])

    # draw the graph
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.savefig("red_graph_test.png") # save as png """







      



    ################### vnfs admission #################  
    ## here we have only two vnodes according if the vnfs are primary or backup, then aleardy will be used to put them in different nodes 
"""rejected = False
    #already_backup = [[],[]] #list of nodes that already hold a vnode
                             ## edit: getting the list from the ressource allocation function outside
    ### print("ranked nodes",ranked_nodes_cpu)
    #print("vnodes list: ", nsl_graph_red["vnodes"])
    vnfs = req.nsl_graph["vnfs"]
    vnf = req.nsl_graph["vnfs"][index]

    if index > 0:
            pre_vnf = vnfs[index - 1]
            pre_backup = pre_vnf["backup"]
            #print("backup type of previous node",pre_backup)
            if(pre_backup != vnf["backup"]):  ## we have diff types of backup, need to find another physical node to map it
            
                for j, n in enumerate(ranked_nodes_cpu):
                    if vnf["cpu"] <= n["cpu"] and n["id"] not in already_backup[vnfs[index-1]["backup"]]:
                        
                        already_backup[vnf["backup"]].append(n["id"])
                        
                        vnf["mapped_to"] = n["id"]
                        reliability  = n["p"]
                        #print("not_same_backup",vnodes[i] , "mapped to ", n["id"])
                        substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnf["cpu"] ## to update the ressource of the node, new
                        #n["cpu"]  = n["cpu"] - vnf["cpu"] 
                        substrate.graph["centralized_cpu"] -= vnf["cpu"]
                        break
                
                    else: # insufficient resource, vnode rejected    

                        if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                            rejected = True    
                            #print("enter to insufficient ressources")
                            #print("insufficient ressources")
                            break 
            else:   ### we have the same backup
                for j, n in enumerate(ranked_nodes_cpu):
                    if(vnf["backup"] == 0):
                        if vnf["cpu"] <= n["cpu"] and n["id"] not in already_backup[1]:
                            
                            already_backup[vnf["backup"]].append(n["id"])
                            vnf["mapped_to"] = n["id"]
                            reliability  = n["p"]
                            #print("same backup 0", vnf , "mapped to ", n["id"])
                            substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnf["cpu"] ## to update the ressource of the node, new
                            #n["cpu"]  = n["cpu"] - vnf["cpu"] 
                            substrate.graph["centralized_cpu"] -= vnf["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                #print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
                    else:
                        if vnf["cpu"] <= n["cpu"] and n["id"] not in already_backup[0]:
                            
                            already_backup[vnf["backup"]].append(n["id"])
                            vnf["mapped_to"] = n["id"] 
                            reliability  = n["p"]
                            #print("same backup 1", vnf , "mapped to ", n["id"])
                            substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnf["cpu"] ## to update the ressource of the node, new
                            #n["cpu"]  = n["cpu"] - vnf["cpu"]                            
                            substrate.graph["centralized_cpu"] -= vnf["cpu"]

                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                #print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
    else:### here we are treating the first vnode, we dont have a previous one
            
            for j, n in enumerate(ranked_nodes_cpu):
                    
                    if(vnf["backup"] == "0"):
                        if vnf["cpu"] <= n["cpu"] and n["id"] not in already_backup[1]:
                            already_backup[vnf["backup"]].append(n["id"])
                            
                            vnf["mapped_to"] = n["id"]
                            reliability  = n["p"]
                            #print("the first node", vnodes[i] , "mapped to ", n["id"])
                            substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnf["cpu"] ## to update the ressource of the node, new
                            #n["cpu"]  = n["cpu"] - vnf["cpu"]     ## NEW: no need since we are placing only one vnf here                      
                            substrate.graph["centralized_cpu"] -= vnf["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                #print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
                    else:
                        if vnf["cpu"] <= n["cpu"] and n["id"] not in already_backup[0]:
                            
                            already_backup[vnf["backup"]].append(n["id"])
                            
                            vnf["mapped_to"] = n["id"]
                            reliability  = n["p"]
                            #print("the first node ", vnodes[i] , "mapped to ", n["id"])
                            substrate.graph["nodes"][n["id"]]["cpu"]  = substrate.graph["nodes"][n["id"]]["cpu"] - vnf["cpu"] ## to update the ressource of the node, new
                            #n["cpu"]  = n["cpu"] - vnodes[i]["cpu"]      ## NEW: no need since we are placing only one vnf here                         
                            substrate.graph["centralized_cpu"] -= vnf["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                #print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break


    if rejected: ## free the ressources taken in the allocation process
        for vnf in vnfs:#the nodes of the reduced graph of the accepted nslr are traversed   
            if "mapped_to" in vnf:## the vnode is mapped to one of the phisical nodes
                n = next(n for n in nodes if (n["id"] == vnf["mapped_to"] and n["type"]==vnf["type"]) )## returns the phisical node mapped to the vnode                
                n["cpu"] = n["cpu"] + vnf["cpu"] ## kill will free the ressources, we will add the cpu taken to the phisical noode's cpu
                substrate.graph["centralized_cpu"] += vnf["cpu"] ## add the cpu freed to the sum of cpu ressource of all the graph
               
        
   
        


########                
    
    ################## vlinks admission #################ù
    #print("placement done ! entering now to the analyse links function :")
    if not rejected:
        rejected, n_hops = analyze_links(req,index, substrate)
        #print("decision after analyse links", rejected, "number of hops", n_hops)
    #else:
         #print("\n\n","***rejected by the lack of node rsc","\n\n")
    ################### ------------- #################
    #if rejected:
         #print("\n\n","***rejected by the lack of link rsc","\n\n")

    return rejected, reliability, already_backup

"""