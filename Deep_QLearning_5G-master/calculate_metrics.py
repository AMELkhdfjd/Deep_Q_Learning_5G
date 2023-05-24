### definition of functions to calculate the profit for nodes and links used in the deep main file ###
def calculate_profit_latency(nslr, n_hops):
    L_max = 4
    if(nslr.service_type == "urllc_1"):
        if(n_hops < L_max):
            return 5
        else:
            return -5
    elif(nslr.service_type == "urllc_2"):
        if(n_hops < L_max):
            return 4
        else:
            return -4
    elif(nslr.service_type == "urllc_3"):
        if(n_hops < L_max):
            return 3
        else:
            return -3
    


def calculate_profit_reability(num_urllc_1,num_urllc_2,num_urllc_3, urllc_1_accepted_reqs,urllc_2_accepted_reqs,urllc_3_accepted_reqs):

    perc_urllc_1_accepted =0
    perc_urllc_2_accepted =0
    perc_urllc_3_accepted =0
    r1=0
    r2=0
    r3=0
    a = 1.0  # Weighting factor for the first URLLC service
    a_ = 0.8  # Weighting factor for the second URLLC service
    a__ = 0.6  # Weighting factor for the third URLLC service




    if urllc_1_accepted_reqs != 0:
        perc_urllc_1_accepted = num_urllc_1 * 100 / urllc_1_accepted_reqs
    else:
        perc_urllc_1_accepted = 0 

    if urllc_2_accepted_reqs != 0:
        perc_urllc_2_accepted = num_urllc_2 * 100 / urllc_2_accepted_reqs
    else:
        perc_urllc_2_accepted = 0 

    if urllc_3_accepted_reqs != 0:
        perc_urllc_3_accepted = num_urllc_3 * 100 / urllc_3_accepted_reqs
    else:
        perc_urllc_3_accepted = 0 


    r1 = perc_urllc_1_accepted*a -(100 - perc_urllc_1_accepted)
    r2 = perc_urllc_2_accepted*a_ -(100 - perc_urllc_2_accepted)
    r3 = perc_urllc_3_accepted*a__ -(100 - perc_urllc_3_accepted)
    step_reability_profit = r1+r2 +r3
    return step_reability_profit, r1, r2, r3









def calculate_profit_nodes(nslr,end_simulation_time):

    #Calculates profit per time unit and then multiplies it by the nslr op. time
    #profit = revenue-cost 
    cost = 0
    revenue = 0    
    vnfs = nslr.nsl_graph_reduced["vnodes"]
    time = 0.0

    cf_cpu = 0 #cost factor of physical nodes(depends on node type)
    for vnf in vnfs:
        if vnf["type"] == 0:#central
            cf_cpu = 1
        elif vnf["type"] == 1:#edge
            cf_cpu = 3 ## edge nodes are more valuable
        # else:
        #     cf_cpu = 4 
        cost += vnf["cpu"]*cf_cpu  ## att: vnodes not the phisical nodes
        revenue += vnf["cpu"]*cf_cpu*2#revenue is twice the cost (so far)

    if nslr.end_time > end_simulation_time:
        #if it is greater, the portion of time until the end of the simulation is considered 
        time = nslr.operation_time - (nslr.end_time-end_simulation_time) ## if the time of the nslr is greater than the simulation time, we need to substrate this time since we are not consuming it, the simulation ends before that

    else:
        time = nslr.operation_time ## if the end time is smaller than the simulation time than take all the operation time since the nslr will have the time to

    profit = (revenue-cost)*time 
    return profit

def calculate_profit_links(nslr,end_simulation_time):
    #Calculates profit per time unit and then multiplies it by the nslr op. time
    #profit = revenue-cost 
    cost = 0
    revenue = 0        
    vlinks = nslr.nsl_graph_reduced["vlinks"]    
    cf_bw =  0.5#cost factor of physical links    
    time = 0.0

    for vlink in vlinks:
        try:
            hops = len(vlink["mapped_to"])-1
        except KeyError:
            hops=0
        cost += vlink["bw"]*cf_bw*hops #cost is proportional to the number of hops
        revenue += vlink["bw"]*cf_bw*5*1.5 #(5: charged considering the maximum number of hops allowed and 1.5: an additional 50% to the cost with 5hops)

    if nslr.end_time > end_simulation_time:
        #si es mayor, se considera la porcion de tiempo hasta acabar la simulacao  
        time = nslr.operation_time - (nslr.end_time-end_simulation_time)
    else:
        time = nslr.operation_time## same as above

    profit = (revenue-cost)*time
    return profit

def calculate_request_utilization(nslr,end_simulation_time,substrate):## returns how much cpu*time consumed (the cpu and bw consumed) for contral nodes and links
    vnfs = nslr.nsl_graph_reduced["vnodes"]
    vlinks = nslr.nsl_graph_reduced["vlinks"]
    time = 0.0
    central_sum = 0
    bw_sum = 0 
    
    for vnf in vnfs:
        if vnf["type"] == 0:#central
            central_sum += vnf["cpu"]
      

    for vlink in vlinks:
        bw_sum += vlink["bw"]      
        

    if nslr.end_time > end_simulation_time:
        #si es mayor, se considera la porcion de tiempo hasta acabar la simulacion  
        time = nslr.operation_time - (nslr.end_time-end_simulation_time)
    else:
        time = nslr.operation_time## same as above

    central_utl = central_sum*time
    links_utl = bw_sum*time  

    return  central_utl, links_utl

# def calculate_request_utilization(nslr,end_simulation_time,substrate):
#     '''
#         Calculates resource utilization of the current requests
#         utilization: the time the resource was busy
#         profit = revenue-cost 
#     '''
#     utl = 0 
#     vnfs = nslr.nsl_graph_reduced["vnodes"]
#     vlinks = nslr.nsl_graph_reduced["vlinks"]  
#     time = 0.0
#     central_sum = 0
#     # local_sum = 0 
#     edge_sum = 0
#     bw_sum = 0
#     # print("substrate",substrate["nodes"])
#     # print("vnfs",vnfs)
#     for vnf in vnfs:
#         # print("**+",substrate["nodes"][vnf["mapped_to"]]["type"])
#         if substrate["graph"]["nodes"][vnf["mapped_to"]]["type"] == 0:
#             central_sum += vnf["cpu"]
#         # elif substrate["nodes"][vnf["mapped_to"]]["type"] == 1:
#         #     local_sum += vnf["cpu"]
#         elif substrate["graph"]["nodes"][vnf["mapped_to"]]["type"] == 1:
#             edge_sum += vnf["cpu"]
        
#         # else:
#         #     edge_sum += vnf["cpu"]  
    
#     for vlink in vlinks:
#         bw_sum += vlink["bw"]        

#     if nslr.end_time > end_simulation_time:
#         #si es mayor, se considera la porcion de tiempo hasta acabar la simulacion  
#         time = nslr.operation_time - (nslr.end_time-end_simulation_time)
#     else:
#         time = nslr.operation_time
#     # print("**++",edge_sum)
#     edge_utl = edge_sum*time 
#     # local_utl = local_sum*time 
#     central_utl = central_sum*time
#     # print("**++",central_utl)
#     links_utl = bw_sum*time 
#     # print("**++",edge_utl)
#     return edge_utl, central_utl, links_utl



