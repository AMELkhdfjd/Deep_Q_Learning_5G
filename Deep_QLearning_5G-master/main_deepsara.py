import numpy as np
import random
import math
import nsl_request
import nsl_placement
import substrate_graphs
import copy
import ql
import dql
import telegram_bot as bot
import time
import networkx as nx
import matplotlib.pyplot as plt
from SimGNN_DQL import SimGNNTrainer ## for the gcn
from param_parser import parameter_parser ## for the gcn





repetitions = 1 #33
twindow_length = 1

global last_reward
last_reward = 0

global episode 
episode = 0


global  list_attended_req 
global  list_accepted_req
global  list_terminated_req 
global  list_lost_r_issue 
global  list_lost_resc
global  list_acceptance_ratio 
global  list_epi_profit
global  list_epi_r2c_profit
global  list_epi_reability_profit 
global  list_epi_latency_profit 

list_attended_req = []
list_accepted_req = []
list_terminated_req  = []
list_lost_r_issue  = []
list_lost_resc = []
list_acceptance_ratio = []
list_epi_profit = []
list_epi_r2c_profit = []
list_epi_r2c_profit = []
#list_epi_reability_profit = []
list_epi_latency_profit = []


urllc_1_arrival_rate = 0
#urllc_2_arrival_rate = 0
#urllc_3_arrival_rate = 0 
arrival_rates = [20] #[100,80,60,40,30,25,20,15,10,7,5,3,1] #20 ## maybe the number of request to arrive in a time unit

mean_operation_time = 5 ## initially set to 15, the temination events are never executed
                          


centralized_initial = 0
bw_initial = 0
agente = None


#RL-specific parameters 
episodes = 1 #240##350



avble_central_size = 10
avble_bw_size = 10

pct_inst_urllc_1_size = 10 #percentage of instantiated slices of type urllc_1
                        ## maybe we need this percentage for the action vector


pct_arriv_urllc_1_size = 10



## class for the events
class Evento:
    def __init__(self, type, start, extra, function):
        self.type = type
        self.start = start ## need to figure out what means the start here !! maybe the time the event starts
        self.extra = extra
        self.function = function

    def __str__(self):
        return "("+self.type+","+str(self.start)+","+str(self.extra)+")"

##

## class for the controller
class Controlador:
    def __init__(self):
        self.cpt = 0
        #metricas
        self.total_profit = 0   ## profit for different types: node, links, services, type of nodes
        #self.reability_profit=0
        self.latency_profit=0
        self.urllc_1_profit = 0
        #self.urllc_2_profit = 0
        #self.urllc_3_profit = 0
        self.central_profit = 0
        

        self.acpt_rate = 0     ## we define acceptence rate
    
        
        self.total_utl = 0   ## here the utl means utilisation
        self.node_utl = 0    
        self.link_utl = 0
        self.central_utl = 0
        self.urllc_1_utl = 0
        #self.urllc_2_utl = 0
        #self.urllc_3_utl = 0

        self.simulation = Sim()
        self.substrate = {}
        self.agente = None


    def run(self):
        self.simulation.run(self)


## simulation class
class Sim:
    def __init__(self):
        self.eventos = []## the list of events
        self.total_events = 0
        self.request = {} ## NEW: added to hold the arriving urllc request
        self.request_list = []
        self.window_req_list = [[],[],[]] #for the three services
        #self.window_req_list = []
        self.granted_req_list = []
        self.horario = 0 ## means the start of an nslr treatement
                         ## more likely its the start time of the current event that is being treated
        self.run_till = 1 ## initially was -1
        self.total_reqs = 0
        self.nb_steps =0
        #self.total_urllc_1_reqs = 0
        #self.total_urllc_2_reqs = 0
        #self.total_urllc_3_reqs = 0
        self.attended_reqs = 0
        self.list_profit_r2c = []
        self.list_profit_reability = []
        self.list_profit_latency = []
        self.list_profit = []

    
        self.reject_r_issue = 0
        self.reject_l_issue = 0
        self.reject_nslr = 0
        self.accepted_reqs = 0
        self.terminate_events = 0
  
                   

    def set_run_till(self, t):
        self.run_till = t 

    # def set_substrate(self,substrate):
    #     self.substrate = substrate

    def create_event(self, type, start, extra=None, f=None): ## creation of an event with parameters and its time must be greater than the schedule to take place
        if start<self.horario:
            #print("***false")
            return False
        # else:  
         
        e = Evento(type, start, extra, f)
        return e

    def binary_search (self, arr, l, r, x):   ## binary search for the index of the value x in the array arr returns the index in case found, else the left index l is returned
        if r >= l:       
            mid = int(l + (r - l)/2)
            if arr[mid].start == x: 
                return mid
            elif arr[mid].start > x: 
                return self.binary_search(arr, l, mid-1, x) 
            else: 
                return self.binary_search(arr, mid+1, r, x)   
        else:             
            return l


    def add_event(self, evt):  ## inserting a new event into the list of events evt in order and create the nslr and insert it in the appropriate window list according to its service 
        request = {}

        index = self.binary_search(self.eventos, 0, len(self.eventos)-1, evt.start) ## find where to insert the new event evt since its an ordered array
        self.eventos = self.eventos[:index] + [evt] + self.eventos[index:]  ## insert the new event


        if evt.type == "arrival":       ## if its an arrival type     
            #add nslrs in window list
            self.total_reqs += 1  ## increase the number of requests
            evt.extra["id"] = self.total_reqs
            
            service_type = evt.extra["service_type"]## maybe the extra means the additional parameters for the event here we are assigining the service_type





############################### Continue here ###################################


    def print_eventos(self):## print the infos about an event
        #print("HORARIO: ",self.horario,"\nTotal Events:",len(self.eventos))
    
        for i in range(len(self.eventos)): ## loop the events
            print(str(self.eventos[i]), end=" > \n")
           
           
        #print("++list: ",len(self.window_req_list[0])+len(self.window_req_list[1])+len(self.window_req_list[2]))

        print("\n")



    def get_next_evento(self):## maybe takes the next event from the list of events bcs in the list we will have only remaining events
        if len(self.eventos)==0:
            return None
        else:
            p = self.eventos.pop(0) ## remove the first element of the list which means the first event, since they are ordered
            self.horario = p.start  ## ATTT self.horario is the start of the event
                                    ## ATTT here we are changing the horario
            return p

    def run(self,c):  ## run all events from the list of events, one by one till we reach the end time of the simulation and execute a function for each event
                      ## need to figure out what the c represents here !!
        
        #self.print_eventos()
        while self.horario<self.run_till: ## while the start time of the event that we are going to teate is less than the time the simulation ends, its ok
            #self.print_eventos()

            #print("we are inside the run while", self.horario,"<",self.run_till)
            p = self.get_next_evento()
            if p==None:
                return    
            p.function(c,p)
 


def randoms(seed):  ## which means random just to not confuse
    m = 2**34
    c = 251
    a = 4*c+1
    b=351
    rand_number = (((a*seed)+b)%m)/m
    return rand_number


def get_interarrival_time(arrival_rate):  ## the same for all services
    seed = random.randint(10000000,8000000000)#cambiar solo para cada repetición
    p = randoms(seed) 
    # print(p)     
    inter_arrival_time = -math.log(1.0 - p)/arrival_rate #the inverse of the CDF of Exponential(_lamnbda)
    # inter_arrival_time = float('{0:,.2f}'.format(inter_arrival_time))

    return inter_arrival_time


def filtro(window_req_list,action): ## still ambigus
    
    granted_req_list = []
    auxiliar_list = []
    for req in window_req_list:
        ## ATT here bandera means flag, maybe here we are taking the requests with action flags <=(100,100,100)
        if (req.service_type == "urllc_1" and req.bandera <= actions[action][0]*100) or (req.service_type == "urllc_2" and req.bandera <= actions[action][1]*100) or (req.service_type == "urllc_3" and req.bandera <= actions[action][2]*100):
            # print("**agregando request...")
            granted_req_list.append(req)
    #     else:
    #         auxiliar_list.append(req)

    # granted_req_list = granted_req_list + auxiliar_list 

    return granted_req_list




def takeFirst(elem):## i guess useless 
    return elem[0] 


def update_resources(substrate,nslr,kill):  ## updates the ressources consumed for the cpu of physical nodes and the bw of the links
    ### Problem !! why we dont update the ressources on the specific node rather than all the graph !?
    nodes = substrate.graph["nodes"]
    links = substrate.graph["links"]   
    #print("uppppppppdate the node of the nslr type: ", nslr.service_type)
    for vnf in nslr.nsl_graph["vnfs"]:#the nodes of the reduced graph of the accepted nslr are traversed   
        if "mapped_to" in vnf:## the vnode is mapped to one of the phisical nodes

            n = next(n for n in nodes if (n["id"] == vnf["mapped_to"] ) )## returns the phisical node mapped to the vnode
            ### ATTT; here we are taking the id of the phisical node not any node in order to update its ressources
              ## need to figure out the effect of next above
          
            if kill: #if it is kill process, resources are free again
                
                #print("before update the node: ", n["id"], n["cpu"])
                n["cpu"] = n["cpu"] + vnf["cpu"] ## kill will free the ressources, we will add the cpu taken to the phisical noode's cpu
                #print("after update the node: ", n["cpu"])
                substrate.graph["centralized_cpu"] += vnf["cpu"] ## add the cpu freed to the sum of cpu ressource of all the graph
          
    for vlink in nslr.nsl_graph["vlinks"]:
        try:#when two vnfs are instantiated in the same node there is no link
            path = vlink["mapped_to"]            
        except KeyError:
            path=[]
        for i in range(len(path)-1):
            try:
                l = next(l for l in links if ( (l["source"]==path[i] and l["target"]==path[i+1]) or (l["source"]==path[i+1] and l["target"]==path[i]) ) )              
                if kill:
                    l["bw"] += vlink["bw"]
                    substrate.graph["bw"] += vlink["bw"]
                
            except StopIteration:
                pass



def resource_allocation(cn, index, already_backup, a, reliability_total): #cn=controller
   #makes allocation for the set of nslrs captured in a time window ##and returns the profits calculated for the global allocations
    # the metrics calculated here correspond to a step
     
    sim = cn.simulation ## define the object of class Sim which is part of the Controller class
    substrate = cn.substrate ## substrate of the controller class

    
    req = sim.request
    vnfs = sim.request.nsl_graph["vnfs"]
    vnf = vnfs[index]
    reliability = 0    


    rejected, rejected_l, rejected_r, latency_totale, profit_reliability  = nsl_placement.nsl_placement(req, index, substrate, already_backup, a, reliability_total)#mapping  ## here try to allocate the nslr req in the substrate graph
        
    if not rejected: ## successfully mapped
         
        
            

            #step_latency_profit += profit_latency 
           

            if(len(vnfs) -1   == index ): ## check here if its index-1, which means its not rejected and its the last vnf, create a termination event
                sim.request.set_end_time(sim.horario+sim.request.operation_time)
               
                #print("the accepted reqs: ", sim.accepted_reqs)
                #print("END TIME:  ", sim.request.end_time)

                evt = sim.create_event(type="termination",start=sim.request.end_time, extra=sim.request, f=func_terminate) ## add the event to the list of events
                sim.add_event(evt)
                #print("TERMINATTION:   " )
                #print(str(evt), end=" > \n")


                ## add here the final reward to get
    else:
        profit_reliability = -1 ## the bad reward when we reject all the request due to non allocation of a vnf

                      
            
        
             
    return rejected, rejected_l, rejected_r, latency_totale, profit_reliability


def get_code(value):## maps the input value to one of ten codes (0, 1, 2, 3, 4, 5, 6, 7, 8, or 9) based on the range of values that value falls within.
    cod = 0
    value = value*100
    # #para granularidad de 5 (100/5) -> (20,40,60,80,100)
    # if value <= 20:
    #     cod = 0
    # elif value <= 40:
    #     cod = 1
    # elif value <= 60:
    #     cod = 2
    # elif value <= 80:
    #     cod = 3    
    # else:
    #     cod = 4
    # return cod

    #for granularity of 10 (100/10) -> (10,20,30,...100)
    if value <= 10:
        cod = 0
    elif value <= 20:
        cod = 1
    elif value <= 30:
        cod = 2
    elif value <= 40:
        cod = 3
    elif value <= 50:
        cod = 4
    elif value <= 60:
        cod = 5        
    elif value <= 70:
        cod = 6
    elif value <= 80:
        cod = 7
    elif value <= 90:
        cod = 8
    else:
        cod = 9
    return cod
    
    #return value



def get_state(substrate,simulation, index): ## returns the state of 9 parmas   
    args = parameter_parser()

    #labels_1 = [[node["p"], node["cpu"]] for node in substrate.graph["nodes"]]
    # Latency solution
    labels_1 = [[node["p"], node["cpu"], node["l"]] for node in substrate.graph["nodes"]]


# Extract links' "source" and "target" values into "graph_1"
    graph_1 = [[link["source"], link["target"]] for link in substrate.graph["links"]]

# Create the desired format in the "graph" variable
    graph_s = {
    "labels_1": labels_1,
    "graph_1": graph_1
    }
    labels_2 = [[node["cpu"]] for node in simulation.request.nsl_graph["vnfs"]]

# Extract links' "source" and "target" values into "graph_1"
    graph_2 = [[link["source"], link["target"]] for link in simulation.request.nsl_graph["vlinks"]]

# Create the desired format in the "graph" variable
    graph_v = {
    "labels_2": labels_2,
    "graph_2": graph_2
    }


    trainer = SimGNNTrainer(args, graph_s, graph_v)
    state = trainer.fit(index)
   

    return state

def func_arrival(c,evt): #NSL arrival, we will treate the one URLLC request arrived


    global counter_windows
    global last_reward
    global episode
    sim = c.simulation 
    

    already_backup =[[], []]
    reliability_total = 1
    actions = c.substrate.graph["nodes"]  ### NEW: defenition of the new action here
    revenue = 0
    cout  =0




    sim.request = nsl_request.get_nslr(evt.extra["id"],evt.extra["service_type"],mean_operation_time)
   
    vnfs = sim.request.nsl_graph["vnfs"]
    vlinks = sim.request.nsl_graph["vlinks"]
    sim.attended_reqs = sim.attended_reqs +1
    #print("TYPE  : ", evt.extra["service_type"])
    ## here we should take the action and state from the last request placement:
    """if(evt.extra["first_event"] == True):
            r = 0
            #a = agente.step(state,0) ## this returns the action taken, here we call the function step from the dql file, give state, reward, training=true, 
           
    else:
            #r = evt.extra["current_reward"]
            r = last_reward"""
            #print("the reward outside the loop is : ", r)

    r = last_reward
    #print("the last reward of nslr", last_reward)

    for index, vnf in enumerate(vnfs):

        
        state = get_state(c.substrate,c.simulation, index)


        state = state.tolist()[0]
        sim.nb_steps +=1
        a = agente.step(state,r)  
      
       

        rejected, rejected_l, rejected_r, latency_totale, profit_reliability = resource_allocation(c, index, already_backup, a, reliability_total)
        #r = profit_reliability  #here for the first solution
        #print("ACTION : ", a,"REAB VNF: ", profit_reliability)
        r = 0
         
        if (rejected):  ##rejected due to resc or due to latency
            #print("ENTER TO REJECT")
            

            if (index != len(vnfs)-1): ## its not the last episode, ressources forcly
                r = -1
                sim.reject_nslr = sim.reject_nslr +1
                #print("VNF REJECT --- RSC")
                last_reward = r
                break
            else: ## its the last one
                if(rejected_r): ## reliability issue
                    r = -1
                    sim.reject_r_issue = sim.reject_r_issue+1
                    #print("VNF REJECT --- REA", r)
                    last_reward = r
                    break
                elif(rejected_l):
                    r = -1
                    sim.reject_l_issue = sim.reject_l_issue+1
                    #print("VNF REJECT --- LAT", r)
                    last_reward = r
                    break

                else: ## last vnf and ressource issue
                    r = -1
                    sim.reject_nslr = sim.reject_nslr +1
                    last_reward = r
                    #print("VNF REJECT --- RSC LAST")
                    break

                 
                   

                

        else:
            reliability_total = reliability_total*profit_reliability ##### ATT erreur grave
            #print("the reability till now: ", reliability_total)
            if (index == len(vnfs)-1):

                
                sim.accepted_reqs = sim.accepted_reqs +1
                #print("ACCEPT")

                ## define the new reward here:
                for i in range(len(vnfs)):
                    revenue += vnfs[i]["cpu"] 
                    cout += vnfs[i]["cpu"] 
                    #print("the cpu is  : ",vnfs[i]["cpu"])
                    
                for j in range(len(vlinks)):
                    revenue += vlinks[j]["bw"]
                   
                    if "mapped_to" in vlinks[j]:

                        cout +=  vlinks[j]["bw"] * (len(vlinks[j]["mapped_to"])-1)
                        #print("the bw is : ", vlinks[j]["bw"], "mapped_to", vlinks[j]["mapped_to"], len(vlinks[j]["mapped_to"]))

                    else:
                        cout += 0
                #print("revenu: ", revenue)
                #print("cout: ", cout)
                #r = 0.6*(revenue/cout) + 0.4*reliability_total

                r = 0.9*(revenue/cout) + 0.1*(reliability_total/latency_totale)
                #print("the reward ", r)
                sim.list_profit_reability.append(reliability_total)
                sim.list_profit_latency.append(latency_totale)
                sim.list_profit_r2c.append(revenue/cout)
                sim.list_profit.append(r)
                last_reward = r


        if sim.nb_steps == 200:

            #f = open("deepsara_"+ "_10BA_300epi_run-time4.txt","a+")
            episode_profit = sum(sim.list_profit) / len(sim.list_profit) 
            episode_profit_r2c = sum(sim.list_profit_r2c) / len(sim.list_profit_r2c) 
            episode_profit_reability = sum(sim.list_profit_reability) / len(sim.list_profit_reability) 
            episode_profit_latency = sum(sim.list_profit_latency) / len(sim.list_profit_latency) 


          

            list_attended_req.append(sim.attended_reqs)
            list_accepted_req.append(sim.accepted_reqs)
            list_terminated_req.append(sim.terminate_events)
            list_lost_r_issue.append(sim.reject_l_issue)
            list_lost_resc.append(sim.reject_nslr)
            list_acceptance_ratio.append((sim.accepted_reqs/ sim.attended_reqs)*100)
            list_epi_profit.append(episode_profit)
            list_epi_r2c_profit.append(episode_profit_r2c)
            #list_epi_reability_profit.append(episode_profit_reability)
            list_epi_latency_profit.append(episode_profit_latency)
            print("episode: ", episode)
            print("attended requests:", sim.attended_reqs)
            print("accepted requests:", sim.accepted_reqs)
            print("rejected requests:", sim.reject_r_issue+sim.reject_l_issue)
        
            print("acceptance_ratio:", (sim.accepted_reqs/ sim.attended_reqs)*100)
            print("episode reability:", episode_profit_reability)
            print("episode latency:", episode_profit_latency, "\n")
            
           
            sim.nb_steps = 0
            episode +=1
            sim.reject_l_issue =0
            sim.reject_nslr =0
            sim.attended_reqs =0
            sim.accepted_reqs =0
            sim.terminate_events =0
            sim.list_profit =[]
            sim.list_profit_r2c =[]
            #sim.list_profit_reability =[]
            sim.list_profit_latency =[]
            #print("the small episode: ", episode)


     
       
        
               


        

            


   

    arrival_rate = evt.extra["arrival_rate"]
    service_type = evt.extra["service_type"]
    inter_arrival_time = get_interarrival_time(arrival_rate)
    sim.add_event(evt = sim.create_event(type="arrival",start=sim.horario+inter_arrival_time, extra={"service_type":service_type,"arrival_rate":arrival_rate, "current_reward":r, "first_event": False}, f=func_arrival))




def func_terminate(c,evt):   ## terminates a request, updates the ressources and reduced the number of instantiated reqs list
    
    sim = c.simulation
    
    sim.terminate_events += 1
    
    G = nx.Graph()
   

############## BEFORE 

    
    """if sim.terminate_events == 50:
        for node in c.substrate.graph["nodes"]:
            G.add_node(node["id"], cpu=node["cpu"], p=node["p"])
            #print("node:, ", node["id"])
        for link in c.substrate.graph["links"]:
            G.add_edge(link["source"], link["target"], bw=link["bw"])
        pos = nx.spring_layout(G, 0.5)
        plt.figure() 
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.9, edge_color='gray')
        node_labels = {node["id"]: f"ID: {node['id']}\nCPU: {node['cpu']}\nP: {node['p']}" for node in c.substrate.graph["nodes"]}
        nx.draw_networkx_labels(G, pos, node_labels, font_size=10, font_color='black', verticalalignment='center')
        edge_labels = {(link["source"], link["target"]): str(link["bw"]) for link in c.substrate.graph["links"]}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='black')
        plt.axis('off')
        plt.savefig("BEFORE.png") # save as png """
       
    request = evt.extra
    update_resources(c.substrate,request,True)

############ REQUEST
    

    """if sim.terminate_events == 50:
        for node in request.nsl_graph["vnfs"]:
            G.add_node(node["id"], cpu=node["cpu"], mapped=node["mapped_to"])
            
        for link in request.nsl_graph["vlinks"]:
            G.add_edge(link["source"], link["target"], bw=link["bw"])
        pos = nx.spring_layout(G, 0.5)
        plt.figure() 
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightgrey')
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.9, edge_color='gray')
        node_labels = {node["id"]: f"ID: {node['id']}\nCPU: {node['cpu']}\nmpped_to: {node['mapped_to']}" for node in request.nsl_graph["vnfs"]}
        nx.draw_networkx_labels(G, pos, node_labels, font_size=10, font_color='black', verticalalignment='center')
        edge_labels = {(link["source"], link["target"]): str(link["bw"]) for link in request.nsl_graph["vlinks"]}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='black')
        plt.axis('off')
        plt.savefig("req.png")""" # save as png """


################ AFTER
    
"""if sim.terminate_events == 50:
        for node in c.substrate.graph["nodes"]:
            G.add_node(node["id"], cpu=node["cpu"], p=node["p"])
            #print("node:, ", node["id"])
        for link in c.substrate.graph["links"]:
            G.add_edge(link["source"], link["target"], bw=link["bw"])
        pos = nx.spring_layout(G, 0.5)
        plt.figure() 
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.9, edge_color='gray')
        node_labels = {node["id"]: f"ID: {node['id']}\nCPU: {node['cpu']}\nP: {node['p']}" for node in c.substrate.graph["nodes"]}
        nx.draw_networkx_labels(G, pos, node_labels, font_size=10, font_color='black', verticalalignment='center')
        edge_labels = {(link["source"], link["target"]): str(link["bw"]) for link in c.substrate.graph["links"]}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='black')
        plt.axis('off')
        plt.savefig("AFTER.png") # save as png 
        c.cpt +=1"""
        
    
  

  
def prepare_sim(s):## prepares the simulation object for all services and sets the params for them
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_1_arrival_rate),extra={"service_type":"urllc_1","arrival_rate":urllc_1_arrival_rate, "first_event": True},f=func_arrival) 
    s.add_event(evt)
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_1_arrival_rate),extra={"service_type":"urllc_2","arrival_rate":urllc_1_arrival_rate, "first_event": True},f=func_arrival)    
    s.add_event(evt)
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_1_arrival_rate),extra={"service_type":"urllc_3","arrival_rate":urllc_1_arrival_rate, "first_event": True},f=func_arrival)    
    s.add_event(evt)
  
                         
def main():
                                              
# ▀████▄     ▄███▀     ██     ▀████▀███▄   ▀███▀
#   ████    ████      ▄██▄      ██   ███▄    █  
#   █ ██   ▄█ ██     ▄█▀██▄     ██   █ ███   █  
#   █  ██  █▀ ██    ▄█  ▀██     ██   █  ▀██▄ █  
#   █  ██▄█▀  ██    ████████    ██   █   ▀██▄█  
#   █  ▀██▀   ██   █▀      ██   ██   █     ███  
# ▄███▄ ▀▀  ▄████▄███▄   ▄████▄████▄███▄    ██ 
                                                  
                                                      
    global centralized_initial
    global bw_initial
    global agente
    global urllc_1_arrival_rate
  
    
    for m in arrival_rates:  ### the most global loop, arrival_rates = [100,80,60,40,30,25,20,15,10,7,5,3,1]
        #urllc_1_arrival_rate = m/3 ##  calculate the rate arrival for each service, its logical we devide by 3 here
        urllc_1_arrival_rate = m   ## we have only one service type, logically take the arival rate as it is

        
        for i in range(1): ## repetitions=33 global 
                                     ## 1


            #print("################ REPITITION LOOP #####################", i)                       
            #agente = ql.Qagent(0.9, 0.9, 0.9, episodes, n_states, n_actions) #(alpha, gamma, epsilon, episodes, n_states, n_actions)
            agente = dql.Agent(16,10) ## here we pass the state size and the action size
                                            ## 
                                            ## the action size is the number of nodes in the phisical graph, we take it 10
            for j in range(episodes): ## 1
                agente.handle_episode_start() ## sets last_state and last_action to none


                #print("\n","episode:",j,"\n")
                print("################ EPISODE LOOP #####################")
                controller = None
                controller = Controlador()                   
                controller.substrate = copy.deepcopy(substrate_graphs.get_graph(10)) #get substrate  with 16 nodes
                                                                                              ## maybe we dont need to pass the agent to the controller


                # controller.substrate = copy.deepcopy(substrate_graphs.get_graph("abilene")) #get substrate    
                centralized_initial = controller.substrate.graph["centralized_cpu"]
                bw_initial = controller.substrate.graph["bw"]

                controller.simulation.set_run_till(6)   ## set the run_till variable of SIm to 15, the end of the simulatin is after 15 time units
                                                        ## initially was 15
                prepare_sim(controller.simulation)   ## creates the arrival events and the twindow_end event to prepare the environment          
                controller.run()    ## runs all the events of the list one by one, here we execute the run of the class SIm, and a function for each event  
               




              

        f = open("Results_10BA_15epi_run-time6.txt","a+")
        f.write("attended req "+  str(list_attended_req)+"\n\n")
        f.write("accepted req "+  str(list_accepted_req)+"\n\n")
        f.write("terminated_req "+  str(list_terminated_req)+"\n\n")
        f.write("lost_r_issue "+  str(list_lost_r_issue)+"\n\n")
        f.write("list_lost_resc "+  str(list_lost_resc)+"\n\n")
        f.write("list_acceptance_ratio "+  str(list_acceptance_ratio)+"\n\n")
        f.write("list_epi_profit "+  str(list_epi_profit)+"\n\n")
        f.write("list_epi_r2c_profit "+  str(list_epi_r2c_profit)+"\n\n")
        #f.write("list_epi_reability_profit "+  str(list_epi_reability_profit)+"\n\n")
        f.write("list_epi_latency_profit "+  str(list_epi_latency_profit)+"\n\n")
    



            #bot.sendMessage("Repetition " + str(i) + " finishes!")

  
            

if __name__ == '__main__':
    #bot.sendMessage("Simulation starts!")
    start = time.time()## in order to receive the current time
    print("start time: ",start)
    main()
    end = time.time()
    print("end time: ",end)
    #bot.sendMessage("Simulation finishes!")

    #bot.sendMessage("total time: " + str(end-start))