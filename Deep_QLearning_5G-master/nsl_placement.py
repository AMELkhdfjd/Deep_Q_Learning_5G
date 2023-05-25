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
    nslrs acceptance of another use cas
"""
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

def nsl_placement(nslr, substrate):  ## need to know why we are passing the substrate

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
    # ranked_nodes_cpu = nodes
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
            
                for n in ranked_nodes_cpu:
                    if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[vnodes[i-1]["backup"]]:
                        
                        already_backup[vnodes[i]["backup"]].append(n["id"])
                        
                        vnodes[i]["mapped_to"] = n["id"]
                        print("not_same_backup",vnodes[i] , "mapped to ", n["id"])
                        n["cpu"]  = n["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                        substrate.graph["centralized_cpu"] -= vnodes[i]["cpu"]
                        break
                
                    else: # insufficient resource, vnode rejected    

                        if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                            rejected = True    
                            print("enter to insufficient ressources")
                            #print("insufficient ressources")
                            break 
            else:   ### we have the same backup
                for n in ranked_nodes_cpu:
                    if(vnodes[i]["backup"] == 0):
                        if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[1]:
                            
                            already_backup[vnodes[i]["backup"]].append(n["id"])
                            vnodes[i]["mapped_to"] = n["id"]
                            print("same backup 0", vnodes[i] , "mapped to ", n["id"])
                            n["cpu"]  = n["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                            substrate.graph["centralized_cpu"] -= vnodes[i]["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
                    else:
                        if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[0]:
                            
                            already_backup[vnodes[i]["backup"]].append(n["id"])
                            vnodes[i]["mapped_to"] = n["id"] 
                            print("same backup 1", vnodes[i] , "mapped to ", n["id"])
                            n["cpu"]  = n["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                            substrate.graph["centralized_cpu"] -= vnodes["cpu"]

                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
        else:### here we are treating the first vnode, we dont have a previous one
            
            for n in ranked_nodes_cpu:
                    
                    if(vnodes[i]["backup"] == "0"):
                        if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[1]:
                            already_backup[vnodes[i]["backup"]].append(n["id"])
                            
                            vnodes[i]["mapped_to"] = n["id"]
                            print("the first node", vnodes[i] , "mapped to ", n["id"])
                            n["cpu"]  = n["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                            substrate.graph["centralized_cpu"] -= vnodes[i]["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
                    else:
                        if vnodes[i]["cpu"] <= n["cpu"] and n["id"] not in already_backup[0]:
                            
                            already_backup[vnodes[i]["backup"]].append(n["id"])
                            
                            vnodes[i]["mapped_to"] = n["id"]
                            print("the first node ", vnodes[i] , "mapped to ", n["id"])
                            n["cpu"]  = n["cpu"] - vnodes[i]["cpu"] ## to update the ressource of the node, new
                            substrate.graph["centralized_cpu"] -= vnodes[i]["cpu"]
                            break
                        else: # insufficient resource, vnode rejected    
                        
                            if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                                rejected = True    
                                print("enter to insufficient ressources")
                                #print("insufficient ressources")
                                break
    if rejected: ## free the ressources taken in the allocation process
        for vnf in vnodes:#the nodes of the reduced graph of the accepted nslr are traversed   
            if "mapped_to" in vnf:## the vnode is mapped to one of the phisical nodes
                n = next(n for n in nodes if (n["id"] == vnf["mapped_to"] and n["type"]==vnf["type"]) )## returns the phisical node mapped to the vnode                
                n["cpu"] = n["cpu"] + vnf["cpu"] ## kill will free the ressources, we will add the cpu taken to the phisical noode's cpu
                substrate.graph["centralized_cpu"] += vnf["cpu"] ## add the cpu freed to the sum of cpu ressource of all the graph
               
        
   
        





        """for n in ranked_nodes_cpu:  ## loop the list of vnodes sorted according to their ressources
            #if resource enough and node of the same type and node not used, vnode accepted  
             
            
            if v["cpu"] <= n["cpu"] and v["type"] == n["type"] and n["id"] not in already: 
                #mapping:

                v["mapped_to"] = n["id"]
                ### print(v["id"] , "mapped to ", n["id"])
                ### print(v)
                #print("enter to same type of vnfs backup or not")

                already.append(n["id"])
                #print("already", already)
                break
            else: # insufficient resource, vnode rejected    
                        
                if ranked_nodes_cpu.index(n) == len(ranked_nodes_cpu)-1: #slice rejection only when no node has enough resources
                                                                        ## we are in the last vnode
                    rejected = True    
                    print("enter to insufficient ressources")
                    #print("insufficient ressources")
                    break   """
    ################### ------------- #################                
    
    ################## vlinks admission #################ù
    print("placement done ! entering now to the analyse links function :")
    if not rejected:
        rejected, n_hops = analyze_links(nslr.nsl_graph,substrate)
        print("decision after analyse links", rejected, "number of hops", n_hops)
    else:
         print("\n\n","***rejected by the lack of node rsc","\n\n")
    ################### ------------- #################
    if rejected:
         print("\n\n","***rejected by the lack of link rsc","\n\n")

    return rejected, n_hops 

def sort_nodes(node_list,sortby):       
    sorted_list = sorted(node_list, key=itemgetter(sortby), reverse=True)#sorted list    
    return sorted_list

def calculate_resource_potential(substrate,resource_type):
    '''
        potential or importance of the node
        the potential of a node to embed vnfs in terms of cpu, str, and bw
        local_rsc_capacity  =  node resource * sum of bw of all links adjacent to the node
        degree_centrality = degree/(n-1)
        node potential = local_rsc_capacity + degree_centrality

    '''
    nodes = substrate.graph["nodes"]
    links = substrate.graph["links"]
    for i in range(len(nodes)):
        bw_sum = 0
 
        for l in range(len(links)):            
            if links[l]["source"] == i or links[l]["target"] == i: #links connected to node i
                bw_sum += links[l]["bw"] #sum of outgoing links bw 
        
        local_rsc_capacity = nodes[i].get(resource_type) * bw_sum
        # nodes[i]["node_potential"] = (local_rsc_capacity/10000) + (nodes[i]["degree_centrality"]*5)
        nodes[i]["node_potential"] = local_rsc_capacity #+ (nodes[i]["degree_centrality"]*5)
        #print("+++",local_rsc_capacity)
        #print("+++",nodes[i]["degree_centrality"])


"""def reduce_nslr_graph(nslr):
    '''
        Pre-processing of the nslr graph to reduce its size
        the vnfs that can be instantiated in the same physical node are grouped as a single virtual node
    '''
    centralized_vnfs = []
    
    # local_vnfs = []
    ###edge_vnfs = []

    #1. Group vnfs by node type: (fill the two above lists)
  

    #2. Sort the vnfs by backup:
    centralized_vnfs = sorted(centralized_vnfs, key=itemgetter("backup"))## order the vnfs according to backup from 0 to above to start first with the primary vnfs
    # local_vnfs = sorted(local_vnfs, key=itemgetter("backup"))
    ###edge_vnfs = sorted(edge_vnfs, key=itemgetter("backup"))

    #3. Group vnfs that will be instantiated in the same physical node:
    nsl_graph_red["vnodes"] = []
   
    group_vnfs(centralized_vnfs,0)
    # group_vnfs(local_vnfs,1)
    ###group_vnfs(edge_vnfs,1)

    #4. Create new vlinks considering the virtual nodes created
    nsl_graph_red["vlinks"] = []
    new_vlinks(nsl_graph_red,nslr.nsl_graph)

    #5. resulting graph is added to the nslr
    nslr.set_nsl_graph_reduced(nsl_graph_red) 
    # nslr["nsl_graph_red"] = nsl_graph_red
    # print("**",nsl_graph_red)

def group_vnfs(vnfs_list,node_type):  ## here we are grouping the backup vnfs and the primary ones (backups which are the first vnfs in the list after order)

    ## non-backup VNFs may have different functions and requirements, and grouping them together could limit their flexibility and performance.
    '''
        creates different vnodes and add them to the reduced graph
    '''
    vnode = {}
    vnode["vnfs"] = [] #ids of the vnfs that make up this vnode
    vnode["type"] = node_type
    
    if len(nsl_graph_red["vnodes"]) == 0:
        cont = 0
    else:
        cont = len(nsl_graph_red["vnodes"])
    #print("the vnfs_list:  ", vnfs_list)
    for i in range(len(vnfs_list)):
        
       
        
        if i==0: ## first vnf (backup maybe)
            vnode["cpu"] = vnfs_list[i]["cpu"]
            vnode["vnfs"].append(vnfs_list[i]["id"])
            if i == len(vnfs_list)-1: ## in case the list of vnfs contains only one, so add it directly to the list of vnodes nsl_graph_red[vnodes] since we wont have another vnf in this list
                vnode["id"]=cont  ## give it the id of the next index in the list of vnodes in the nsl_graph_red (since it might have previous vnodes)
                nsl_graph_red["vnodes"].append(vnode.copy())
                cont += 1

        elif vnfs_list[i]["backup"]==vnfs_list[i-1]["backup"]: ## we need to have the condition backup and primary vnfs are never put in the same node
            vnode["cpu"] += vnfs_list[i]["cpu"]  ## add the cpu ressources to the virtual node for the next vnf
            vnode["vnfs"].append(vnfs_list[i]["id"])  
            ### print("same backup",vnode["vnfs"])
            #print(vnfs_list[i], i)
            if i == len(vnfs_list)-1: ## we are on the last vnf, need to add it the vnodes list
                vnode["id"]=cont
                nsl_graph_red["vnodes"].append(vnode.copy())
                cont += 1

        else:            
            vnode["id"]=cont 
            nsl_graph_red["vnodes"].append(vnode.copy())
            
            cont += 1
            vnode["cpu"] = vnfs_list[i]["cpu"]
            vnode["vnfs"] = []
            vnode["vnfs"].append(vnfs_list[i]["id"])
            if i == len(vnfs_list)-1:
                vnode["id"]=cont
                nsl_graph_red["vnodes"].append(vnode.copy())
                cont += 1

    # return nsl_graph_red  ## maybe uncomment the return

def new_vlinks(nsl_graph_red, nsl_graph): ## create the virtual links between the vnodes created before
    vnfs = nsl_graph["vnfs"]
    vnodes = nsl_graph_red["vnodes"]
    new_vlink = {}
    for vlink in nsl_graph["vlinks"]:     
        source = next(vnf for vnf in vnfs if vnf["id"]==vlink["source"])
        target = next(vnf for vnf in vnfs if vnf["id"]==vlink["target"])
        #if src and target are of the same type and are from the same backup, then do nothing (vlink is not considered)
        if source["type"] == target["type"] and source["backup"] == target["backup"]:
            pass
        else: #otherwise vlink is considered, since the pair of vnfs are in different vnodes
            new_src = next(vnode for vnode in vnodes if source["id"] in vnode["vnfs"])
            new_tgt = next(vnode for vnode in vnodes if target["id"] in vnode["vnfs"]) 
            new_vlink = {"source":new_src["id"],"target":new_tgt["id"],"bw":vlink["bw"]}
            nsl_graph_red["vlinks"].append(new_vlink)"""


def analyze_links(nsl_graph,substrate): ## returns the length of the path in addition in order to calculate the latency

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
    max_hops = 5
    chosen_path =[]
    
    vlinks = nsl_graph["vlinks"]
    vnfs = nsl_graph["vnfs"] ## att: we work only with vnodes 
    for vlink in vlinks:
        substrate_src = next(vnf["mapped_to"] for vnf in vnfs if vnf["id"] == vlink["source"]) 
        substrate_dst = next(vnf["mapped_to"] for vnf in vnfs if vnf["id"] == vlink["target"])
        print("source", substrate_src, "destination", substrate_dst)
        # print("\n***vlink:",vlink)
        # que hacer con las vnfs que se instancian en el mismo nodo? cobrar por vlink? cuanto?
        paths = nx.all_simple_paths(G,source=substrate_src,target=substrate_dst)
        path_list = [p for p in paths]
        path_list.sort(key=len)
        print("the path list ", path_list)
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
                    print("the path choosen", path)
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


    return reject, len(chosen_path)


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




