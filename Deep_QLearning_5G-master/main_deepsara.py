import numpy as np
import random
import math
import nsl_request
import nsl_placement
import substrate_graphs
import copy
import calculate_metrics 
import ql
import dql
import telegram_bot as bot
import time



# import bisect
#simulation parameters
# seed = 0
repetitions = 1 #33
twindow_length = 1
# urllc_1_arrival_rate = 10 #5#1#2 #reqXsecond
# urllc_2_arrival_rate = 40 #5#2.5 #reqXsecond
# urllc_3_arrival_rate = 10 #5#1#2 #reqXsecond

urllc_1_arrival_rate = 0
urllc_2_arrival_rate = 0
urllc_3_arrival_rate = 0 
arrival_rates = [20] #[100,80,60,40,30,25,20,15,10,7,5,3,1] #20 ## maybe the number of request to arrive in a time unit

mean_operation_time = 15 ## initially set to 15, the temination events are never executed
                          


centralized_initial = 0
bw_initial = 0
agente = None


#RL-specific parameters 
episodes = 1 #240##350



avble_central_size = 10
avble_bw_size = 10

pct_inst_urllc_1_size = 10 #percentage of instantiated slices of type urllc_1
                        ## maybe we need this percentage for the action vector
pct_inst_urllc_2_size = 10
pct_inst_urllc_3_size = 10

pct_arriv_urllc_1_size = 10
pct_arriv_urllc_2_size = 10
pct_arriv_urllc_3_size = 10

# n_states = avble_edge_size*avble_central_size
#n_states = avble_edge_size*avble_central_size*avble_bw_size
#n_states = avble_edge_size*avble_central_size*avble_bw_size*pct_inst_urllc_1_size*pct_inst_urllc_size*pct_inst_urllc_3_size
n_states = avble_central_size*avble_bw_size*pct_inst_urllc_1_size*pct_inst_urllc_2_size*pct_inst_urllc_3_size*pct_arriv_urllc_1_size*pct_arriv_urllc_2_size*pct_arriv_urllc_3_size

# #30 actions:
# actions = [
# (1,1,1),(0.75,1,1),(1,0.75,1),(1,1,0.75),(0.75,0.75,1),(1,0.75,0.75),(0.75,1,0.75),
# (0.75,1,0.5),(0.5,1,0.75),(1,0.75,0.5),(0.5,0.75,1),
# (0.5,1,1),(1,1,0.5),(1,0.5,1),(0.5,1,0.5),(0.5,0.5,1),(1,0.5,0.5),
# (0.25,1,1),(1,1,0.25),(0.25,1,0.25),(0.1,1,1),(1,1,0.1),(0.1,1,0.1),(0.1,1,0.75),
# (0.75,1,0.25),(0.25,1,0.75),(1,0.75,0.25),(0.25,0.75,1),(0.5,1,0.25),(0.25,1,0.5)
# ]

#30actsv2.2
actions = [
(1,1,1),
(0.75,1,1),(1,0.75,1),(1,1,0.75),(1,0.75,0.75),(0.75,1,0.75),
(0.75,1,0.5),(0.5,1,0.75),(1,0.75,0.5),
(0.5,1,1),(1,1,0.5),(1,0.5,1),(0.5,1,0.5),(1,0.5,0.5),
(0.25,1,1),(1,1,0.25),(0.25,1,0.25),(0.1,1,1),(1,1,0.1),(0.1,1,0.1),
(0.25,1,0.1), (0.1,1,0.25), (0.5,1,0.1), (0.1,1,0.5), (0.75,1,0.1), (0.1,1,0.75),
(0.25,1,0.5), (0.5,1,0.25), (0.25,1,0.75), (0.75,1,0.25)  
]


#20 actions:
#actions = [(1,1,1),(0.75,1,1),(1,0.75,1),(1,1,0.75),(0.75,0.75,1),(1,0.75,0.75),(0.75,1,0.75),(0.75,1,0.5),(0.5,1,0.75),(1,0.75,0.5),(0.5,0.75,1),
#(0.5,1,1),(1,1,0.5),(0.5,1,0.5),(0.75,1,0.25),(0.25,1,0.75),(1,0.75,0.25),(0.25,0.75,1),(0.5,1,0.25),(0.25,1,0.5)]

#19 actions:
#actions =  [(1,1,1),(0.75,1,1),(1,0.75,1),(1,1,0.75),(0.75,0.75,1),(1,0.75,0.75),(0.75,1,0.75),
            #(0.5,1,1),(1,0.5,1),(1,1,0.5),(0.5,0.5,1),(1,0.5,0.5),(0.5,1,0.5),
            #(0.75,0.5,1),(0.75,1,0.5),(0.5,0.75,1),(1,0.75,0.5),(0.5,1,0.75),(1,0.5,0.75)]

#15 actions:
# actions =  [(1,1,1),(0.75,1,1),(1,0.75,1),(1,1,0.75),(0.75,0.75,1),(1,0.75,0.75),(0.75,1,0.75),
#             (0.5,1,1),(1,0.5,1),(1,1,0.5),(0.5,1,0.5),
#             (0.75,1,0.5),(0.5,0.75,1),(1,0.75,0.5),(0.5,1,0.75)]

# 13 actions:
#actions =  [(1,1,1),(0.75,1,1),(1,0.75,1),(1,1,0.75),(0.75,0.75,1),(1,0.75,0.75),(0.75,1,0.75),
             #(0.5,1,1),(1,0.5,1),(1,1,0.5),(0.5,0.5,1),(1,0.5,0.5),(0.5,1,0.5)]

#10 actions:
# actions =  [(1,1,1),(0.75,1,1),(1,1,0.75),(1,0.75,1),(0.75,1,0.75),
#             (0.75,1,0.5),(0.5,1,0.75),(0.5,1,1),(1,1,0.5),(0.5,1,0.5)]
#actions = [(1,1,1),(0.75,1,1),(1,1,0.75),(0.75,1,0.75),(0.75,1,0.5),(0.5,1,0.75),(0.5,1,1),(1,1,0.5),(0.5,1,0.5),(0.5,1,0.25)]

#7actions:
#actions = [(1,1,1),(0.75,1,1),(1,1,0.75),(0.75,1,0.75),(0.75,1,0.5),(0.5,1,0.5),(0.5,1,0.25)] #list of tuples

n_actions = len(actions)


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
        #metricas
        self.total_profit = 0   ## profit for different types: node, links, services, type of nodes
        self.reability_profit=0
        self.latency_profit=0
        self.urllc_1_profit = 0
        self.urllc_2_profit = 0
        self.urllc_3_profit = 0
        self.central_profit = 0

        self.acpt_rate = 0     ## we define acceptence rate
        self.urllc_1_acpt_rate = 0
        self.urllc_2_acpt_rate = 0
        self.urllc_3_acpt_rate = 0
        
        self.total_utl = 0   ## here the utl means utilisation
        self.node_utl = 0    
        self.link_utl = 0
        self.central_utl = 0
        self.urllc_1_utl = 0
        self.urllc_2_utl = 0
        self.urllc_3_utl = 0

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
        self.window_req_list = [[],[],[]] #for the three services
        #self.window_req_list = []
        self.granted_req_list = []
        self.horario = 0 ## means the start of an nslr treatement
                         ## more likely its the start time of the current event that is being treated
        self.run_till = 1 ## initially was -1
        self.total_reqs = 0
        self.total_urllc_1_reqs = 0
        self.total_urllc_2_reqs = 0
        self.total_urllc_3_reqs = 0
        self.attended_reqs = 0
        self.accepted_reqs = 0
        self.urllc_1_accepted_reqs = 0
        self.urllc_2_accepted_reqs = 0
        self.urllc_3_accepted_reqs = 0
        self.current_instatiated_reqs = [0,0,0] #[urllc_1,urllc_2,urllc_3]
                   

    def set_run_till(self, t):
        self.run_till = t 

    # def set_substrate(self,substrate):
    #     self.substrate = substrate

    def create_event(self, type, start, extra=None, f=None): ## creation of an event with parameters and its time must be greater than the schedule to take place
        if start<self.horario:
            print("***false")
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
        #encontrar indice y adicionar evt en esa posicion
        # index = 0
        # for i in range(len(self.eventos)):
        #     if self.eventos[i].start > evt.start: 
        #         index = i 
        #         break
        #     else:
        #         index = i+1 
        index = self.binary_search(self.eventos, 0, len(self.eventos)-1, evt.start) ## find where to insert the new event evt since its an ordered array
        self.eventos = self.eventos[:index] + [evt] + self.eventos[index:]  ## insert the new event
        # self.eventos.insert(index,evt)
        # self.eventos[index:index] = [evt]  ## maybe here its another alternative

        if evt.type == "arrival":       ## if its an arrival type     
            #add nslrs in window list
            self.total_reqs += 1  ## increase the number of requests
            service_type = evt.extra["service_type"]## maybe the extra means the additional parameters for the event here we are assigining the service_type
            request = nsl_request.get_nslr(self.total_reqs,service_type,mean_operation_time)## here we are calling the fonction from the file imported ATT
            
              ## self.total_reqs: to define the id of the new nslr, 
              ## mean_operation_time = 15 as a global variable


            if evt.extra["service_type"] == "urllc_1":
                self.total_urllc_1_reqs += 1
                self.window_req_list[0].append(copy.deepcopy(request))## add the request to the window list according to the type of the service
            elif evt.extra["service_type"] == "urllc_2":
                self.total_urllc_2_reqs += 1
                self.window_req_list[1].append(copy.deepcopy(request))#
            else: #evt.extra["service_type"] == "urllc_3":
                self.total_urllc_3_reqs += 1
                self.window_req_list[2].append(copy.deepcopy(request))#
            
        print("print details events:  ")
        self.print_eventos()

        print()
            #service_type = evt.extra["service_type"]
            #request = nsl_request.get_nslr(self.total_reqs,service_type,mean_operation_time)
            #self.window_req_list.append(copy.deepcopy(request))



############################### Continue here ###################################


    def print_eventos(self):## print the infos about an event
        print("HORARIO: ",self.horario,"\nTotal Events:",len(self.eventos))
    
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

            print("we are inside the run while", self.horario,"<",self.run_till)
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


def prioritizer_v1(window_req_list,action_index): ## in order to prioritize the request lists of the window list based on the action choosed before
                   ## returns the granted list containing the requests that must be sutistied and chosen according to the action passed in argument
                   ## we will loop all the requests of the window list and store the chosen requests in the granted list
       
    #print("****prioritizing...")
    action = actions[action_index]
    # urllc_1_list = []
    # urllc_2_list = []
    # urllc_3_list = []
    granted_req_list = []

    #Conversion of action in proportion eg: #action = (0.75,1,0.25) -> (3,4,1) represents 3:4:1
    translated_action = [] ## will contain the numbers 1,2,3,4 instead of 0.5,...
    for i in action:  ## ATT translates only one action, the action passed to the function
        if i == 1:
            translated_action.append(4)
        elif i == 0.75:
            translated_action.append(3)
        elif i == 0.5:
            translated_action.append(2)
        else:
            translated_action.append(1)
    
    #se agrupan las NSLRs por service_type
    # for req in window_req_list: 
    #     if req.service_type == "urllc_1":
    #         urllc_1_list.append(req)
    #     elif req.service_type == "urllc_2":
    #         urllc_2_list.append(req)
    #     else:
    #         urllc_3_list.append(req)

    urllc_1_list = window_req_list[0]
    urllc_2_list = window_req_list[1]
    urllc_3_list = window_req_list[2]
    
    #While there are requests in the lists, they are added to the prioritized list        

    while urllc_1_list or urllc_2_list or urllc_3_list:
        #for value in action:
        for i in range(0,translated_action[0]):
            if urllc_1_list:
                granted_req_list.append(urllc_1_list[0]) ## att: fills the granted_list will the respective number of requests epecified in the translated action for ex: 3
                urllc_1_list.pop(0) ## remove the request taken from the list, leave only untreated events or requests

        for i in range(0,translated_action[1]):
            if urllc_2_list:
                granted_req_list.append(urllc_2_list[0])
                urllc_2_list.pop(0)
   
        for i in range(0,translated_action[2]):
            if urllc_3_list: 
                granted_req_list.append(urllc_3_list[0])
                urllc_3_list.pop(0)        

    return granted_req_list 

def takeFirst(elem):## i guess useless 
    return elem[0]


############################### Continue here ###################################

def prioritizer(window_req_list,action_index): #v2  ## the two versions do the same thing but with different manners
    #print("****prioritizing...")
    action = actions[action_index]## taken the action passed in argument action=(0.75,1,0.25)
    action2 = []
    granted_req_list = []
    remaining_req_list = []
    num_urllc_1 =0
    num_urllc_2 =0
    num_urllc_3 =0
    
    #action = (0.75,1,0.25) -> (cant1,cant2,cant3) 
    #translate action in percentage to quantities (nearest integer)
    action2.append([action[0],round(action[0]*len(window_req_list[0])),0]) #[pctg,cant,type] ej:[0.75,75,0]
    action2.append([action[1],round(action[1]*len(window_req_list[1])),1]) ## the length depends on each execution, we need to have more reqs to take some
    action2.append([action[2],round(action[2]*len(window_req_list[2])),2])
   ## ex: action2=([0.75,75,0],[0.5,50,1],[0.25,25,2])
    #according to "action", sort "action2"
    action2.sort(key=takeFirst,reverse=True)## action2 will be sorted in descending order based on the first element of each element in the list.
    ## it sorts according to the percentage of the services 0.75 descending order
    print("action2 containts", action2)
    for j in action2:
        
        if j[0]==1:## contains the percentage for each element of the list, ex: 0.5
            granted_req_list += window_req_list[j[2]]## add all requests for the type to the granted list since the percentage is 100%
            if(j[2]== 0): ## urllc_1 type
                        num_urllc_1 = len(window_req_list[j[2]])
            elif(j[2]== 1):
                        num_urllc_2 = len(window_req_list[j[2]])
            elif(j[2]== 2):
                        num_urllc_3 = len(window_req_list[j[2]])
            
        else:    
            for i in range(len(window_req_list[j[2]])):            
                if i < j[1]:## in order to take for ex 75 requests from the windows list and leave in the remaining list the remaining requests
                    granted_req_list.append(window_req_list[j[2]][i])
                    if(j[2]== 0): ## urllc_1 type
                        num_urllc_1+=1
                    elif(j[2]== 1):
                        num_urllc_2+=1
                    elif(j[2]== 2):
                        num_urllc_3+=1
                else:
                    remaining_req_list.append(window_req_list[j[2]][i])      
    print("granted_req_list contains from the prioritizer function", granted_req_list)
    print("remaining_req_list contains from the prioritizer function", remaining_req_list)
    
    return granted_req_list, remaining_req_list, num_urllc_1, num_urllc_2, num_urllc_3 #v6
    #return granted_req_list+remaining_req_list, remaining_req_list #v1

def update_resources(substrate,nslr,kill):  ## updates the ressources consumed for the cpu of physical nodes and the bw of the links
    ### Problem !! why we dont update the ressources on the specific node rather than all the graph !?
    nodes = substrate.graph["nodes"]
    links = substrate.graph["links"]   
    for vnf in nslr.nsl_graph_reduced["vnfs"]:#the nodes of the reduced graph of the accepted nslr are traversed   
        if "mapped_to" in vnf:## the vnode is mapped to one of the phisical nodes
            n = next(n for n in nodes if (n["id"] == vnf["mapped_to"] and n["type"]==vnf["type"]) )## returns the phisical node mapped to the vnode
            ### ATTT; here we are taking the id of the phisical node not any node in order to update its ressources
              ## need to figure out the effect of next above
            if vnf["type"] == 1: #
                type = "centralized_cpu"
            if kill: #if it is kill process, resources are free again
                
                n["cpu"] = n["cpu"] + vnf["cpu"] ## kill will free the ressources, we will add the cpu taken to the phisical noode's cpu
                substrate.graph[type] += vnf["cpu"] ## add the cpu freed to the sum of cpu ressource of all the graph
            else:
                
                n["cpu"] = n["cpu"] - vnf["cpu"] ## reduce the cpu of the nodes in the graph maybe
                substrate.graph[type] -= vnf["cpu"]
    for vlink in nslr.nsl_graph_reduced["vlinks"]:
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
                else:
                    l["bw"] -= vlink["bw"] ## reduce the bw consumed 
                    substrate.graph["bw"] -= vlink["bw"]
            except StopIteration:
                pass

def resource_allocation(cn): #cn=controller
   #makes allocation for the set of nslrs captured in a time window ##and returns the profits calculated for the global allocations
    # the metrics calculated here correspond to a step
     
    sim = cn.simulation ## define the object of class Sim which is part of the Controller class
    substrate = cn.substrate ## substrate of the controller class
    step_urllc_1_profit_latency = 0 
    step_urllc_2_profit_latency = 0
    step_urllc_3_profit_latency = 0
    step_latency_profit=0
    end_simulation_time = sim.run_till
    """max_node_profit = substrate.graph["max_cpu_profit"]*sim.run_till
    max_link_profit = substrate.graph["max_bw_profit"]*sim.run_till
    max_profit = max_link_profit + max_node_profit"""
    print("granted req list contains: ",sim.granted_req_list)




    for req in sim.granted_req_list: 
        
        # print("**",req.service_type,req.nsl_graph)

        sim.attended_reqs += 1   
        n_hops = 0 ## this variable will contain the nmber of hops for each request     
        rejected, n_hops = nsl_placement.nsl_placement(req,substrate)#mapping  ## here try to allocate the nslr req in the substrate graph
        if not rejected: ## successfully mapped
            #instantiation and addition of termination event
            req.set_end_time(sim.horario+req.operation_time)## the start time + the time of the operation
            graph = req.nsl_graph_reduced 
            update_resources(substrate,req,False)#instantiation, occupy resources
            evt = sim.create_event(type="termination",start=req.end_time, extra=req, f=func_terminate) ## add the event to the list of events
            print("added a termination event")
            sim.add_event(evt) 
           

            #calculation of metrics (profit, acpt_rate, counters)           
            sim.accepted_reqs += 1
            ## implementation of the new rewared function call for reability and latency
            profit_latency = calculate_metrics.calculate_profit_latency(req, n_hops)

            #profit_nodes = calculate_metrics.calculate_profit_nodes(req,end_simulation_time)  ## from the functions of the calculate_metrics file to have the profit gained for node and links
            #profit_links = calculate_metrics.calculate_profit_links(req,end_simulation_time)*10    
            #step_profit += (profit_nodes + profit_links)/max_profit #the total profit in this step is the reward

            step_latency_profit += profit_latency 
           
         

            if req.service_type == "urllc_1":
                sim.current_instatiated_reqs[0] += 1 ## the total of requests accepted for the specific service for each step
                sim.urllc_1_accepted_reqs += 1 ## the accepted for the specific service in general not in the step i think
                step_urllc_1_profit_latency += profit_latency 
            elif req.service_type == "urllc_2":
                sim.current_instatiated_reqs[1] += 1
                sim.urllc_2_accepted_reqs += 1
                step_urllc_2_profit_latency += profit_latency 
            else:
                sim.current_instatiated_reqs[2] += 1
                sim.urllc_3_accepted_reqs += 1
                step_urllc_3_profit_latency += profit_latency                       
            
            """b,c = calculate_metrics.calculate_request_utilization(req,end_simulation_time,substrate)## returns edge_utl, central_utl, links_utl for the request treated
            step_central_cpu_utl += b/(centralized_initial*end_simulation_time)
            step_links_bw_utl += c*10/(bw_initial*end_simulation_time)## links profit and utilistion are always *10
            step_node_utl += (b)/((centralized_initial)*end_simulation_time)
            step_total_utl += (step_node_utl + step_links_bw_utl)/2"""
             
    return step_latency_profit,step_urllc_1_profit_latency,step_urllc_2_profit_latency,step_urllc_3_profit_latency, sim.urllc_1_accepted_reqs, sim.urllc_2_accepted_reqs, sim.urllc_3_accepted_reqs 

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

def translateStateToIndex(state): ## still ambigus
    '''
    returns state index from a given state code
    '''
    cod_avble_central = state[1]
    cod_avble_bw = state[2]
    
    cod_pct_urllc_1 = state[3]
    cod_pct_urllc_2= state[4]
    cod_pct_urllc_3 = state[5]
    
    cod_pct_arriv_urllc_1 = state[6]
    cod_pct_arriv_urllc_2= state[7]
    cod_pct_arriv_urllc_3 = state[8]

    #index = cod_avble_edge*avble_central_size + cod_avble_central
    
    #index for a 3-parameter state
    #index = cod_avble_edge*avble_central_size*avble_bw_size + cod_avble_central*avble_bw_size + cod_avble_bw
    
    #index for a 6-parameter state
    # index = cod_avble_edge*avble_central_size*avble_bw_size*pct_inst_urllc_1_size*pct_inst_urllc_size*pct_inst_urllc_3_size 
    # + cod_avble_central*avble_bw_size*pct_inst_urllc_1_size*pct_inst_urllc_size*pct_inst_urllc_3_size
    # + cod_avble_bw*pct_inst_urllc_1_size*pct_inst_urllc_size*pct_inst_urllc_3_size
    # + cod_pct_urllc_1*pct_inst_urllc_size*pct_inst_urllc_3_size
    # + cod_pct_urllc*pct_inst_urllc_3_size 
    # + cod_pct_urllc_3

    #index for a 9-parameter state
    index = avble_central_size*avble_bw_size*pct_inst_urllc_1_size*pct_inst_urllc_2_size*pct_inst_urllc_3_size*pct_arriv_urllc_1_size*pct_arriv_urllc_2_size*pct_arriv_urllc_3_size 
    + cod_avble_central*avble_bw_size*pct_inst_urllc_1_size*pct_inst_urllc_2_size*pct_inst_urllc_3_size*pct_arriv_urllc_1_size*pct_arriv_urllc_2_size*pct_arriv_urllc_3_size
    + cod_avble_bw*pct_inst_urllc_1_size*pct_inst_urllc_2_size*pct_inst_urllc_3_size*pct_arriv_urllc_1_size*pct_arriv_urllc_2_size*pct_arriv_urllc_3_size
    + cod_pct_urllc_1*pct_inst_urllc_2_size*pct_inst_urllc_3_size*pct_arriv_urllc_1_size*pct_arriv_urllc_2_size*pct_arriv_urllc_3_size
    + cod_pct_urllc_2*pct_inst_urllc_3_size *pct_arriv_urllc_1_size*pct_arriv_urllc_2_size*pct_arriv_urllc_3_size
    + cod_pct_urllc_3*pct_arriv_urllc_1_size*pct_arriv_urllc_2_size*pct_arriv_urllc_3_size
    + cod_pct_arriv_urllc_1*pct_arriv_urllc_2_size*pct_arriv_urllc_3_size
    + cod_pct_arriv_urllc_2*pct_arriv_urllc_3_size
    + cod_pct_arriv_urllc_3

    return int(index)


def get_state(substrate,simulation): ## returns the state of 9 parmas   
    cod_avble_central = get_code(substrate.graph["centralized_cpu"]/centralized_initial)
    cod_avble_bw = get_code(substrate.graph["bw"]/bw_initial)
    

    total = 0   ## for all the requests from current instantiated req list for the step
    for i in simulation.current_instatiated_reqs:
        total += i
    if total == 0:
        pct_urllc_1, pct_urllc_2, pct_urllc_3 = 0,0,0
    else:
        pct_urllc_1, pct_urllc_2, pct_urllc_3 = simulation.current_instatiated_reqs[0]*100/total,simulation.current_instatiated_reqs[1]*100/total,simulation.current_instatiated_reqs[2]*100/total 
    cod_pct_urllc_1 = get_code(pct_urllc_1)
    cod_pct_urllc_2= get_code(pct_urllc_2)
    cod_pct_urllc_3 = get_code(pct_urllc_3)

    
    counter = [0,0,0] ## counts the number of reqs for each type of the granted req list
                      ## here we are doing the same thing above except for the granted list req
    n = len(simulation.granted_req_list)
    
    if n == 0:
        pct_arriv_urllc_1, pct_arriv_urllc_2, pct_arriv_urllc_3 = 0,0,0
    else:
        for req in simulation.granted_req_list:
            if req.service_type == "urllc_1":
                counter[0] += 1
            elif req.service_type == "urllc_2":
                counter[1] += 1
            else:
                counter[2] += 1
        pct_arriv_urllc_1, pct_arriv_urllc_2, pct_arriv_urllc_3 = counter[0]*100/n, counter[1]*100/n, counter[2]*100/n

    cod_pct_arriv_urllc_1 = get_code(pct_arriv_urllc_1)
    cod_pct_arriv_urllc_2= get_code(pct_arriv_urllc_2)
    cod_pct_arriv_urllc_3 = get_code(pct_arriv_urllc_3)


    #3-parameter state:
    #state = [np.float32(cod_avble_edge),np.float32(cod_avble_central),np.float32(cod_avble_bw)]

    #6-parameter state:    
    # state = [
    #             np.float32(cod_avble_edge),
    #             np.float32(cod_avble_central),
    #             np.float32(cod_avble_bw),
    #             np.float32(cod_pct_urllc_1),
    #             np.float32(cod_pct_urllc_2),
    #             np.float32(cod_pct_urllc_3)
    #         ]

    #9-parameter state:
    state = [
                np.float32(cod_avble_central),
                np.float32(cod_avble_bw),
                np.float32(cod_pct_urllc_1),
                np.float32(cod_pct_urllc_2),
                np.float32(cod_pct_urllc_3),
                np.float32(cod_pct_arriv_urllc_1),
                np.float32(cod_pct_arriv_urllc_2),
                np.float32(cod_pct_arriv_urllc_3)
            ]

    return state

def func_arrival(c,evt): #NSL arrival  ## creates an arrival event of NSLR and inserts it in the list of events
    s = c.simulation
    # print("**/",evt.extra["arrival_rate"])
    arrival_rate = evt.extra["arrival_rate"]
    service_type = evt.extra["service_type"]
    inter_arrival_time = get_interarrival_time(arrival_rate)
    print("teated arrival event ---> creration of another arrival event")
    s.add_event(s.create_event(type="arrival",start=s.horario+inter_arrival_time, extra={"service_type":service_type,"arrival_rate":arrival_rate}, f=func_arrival))
    


counter_termination = 0

def func_terminate(c,evt):   ## terminates a request, updates the ressources and reduced the number of instantiated reqs list
    global counter_termination
    sim = c.simulation
    counter_termination +=1
    print("terminating")
    request = evt.extra
    update_resources(c.substrate,request,True)
    if request.service_type == "urllc_1":
        sim.current_instatiated_reqs[0] -= 1  ## att current_instatiated reqs means the req in this moment occuping ressources in the graph and not yet terminated
    elif request.service_type == "urllc_2":
        sim.current_instatiated_reqs[1] -= 1
    else:
        sim.current_instatiated_reqs[2] -= 1


counter_windows = 0
def func_twindow(c,evt):  ## recursive function need to understand it more
    #the time sale has expired. The nslrs collected so far will be analyzed for admission.
    global counter_windows
    sim = c.simulation 
    counter_windows += 1
    num_urllc_1 = 0
    num_urllc_2 = 0
    num_urllc_3 = 0
    step_urllc_1_profit_reability =0
    step_urllc_2_profit_reability =0
    step_urllc_3_profit_reability =0
    
    if evt.extra["first_state"]: ## if its the first state
        #first state index
        #all resources at 100% (with granularity of 5)
        print("entered in the first state section of func_twindow")
        state = get_state(c.substrate,c.simulation)
        
        #s = translateStateToIndex(state)
        #a = agente.take_action(s,True)
        
        a = agente.step(state,0) ## this returns the action taken, here we call the function step from the dql file, give state, reward, training=true, 
        print("the action taken",actions[a])
    else:## its not the first state, still ambigus why we dont call the step function 
                                    ##edit: we dont need to calculate the next step bcz we have the action here, before we dont have since its the first state
        s = evt.extra["current_state"] ## the state
        a = evt.extra["action"]  ## the action of the event
        print("the action taken",a)
        #print("##agent",agente.last_state," ",agente.last_action)    
        print("entered in the else of first state of func_twindow")    
      
    sim.granted_req_list, remaining_req_list, num_urllc_1, num_urllc_2, num_urllc_3 = prioritizer(sim.window_req_list, a) #the list of reqs is filtered depending on the action
    #the list is sent to the Resource Allocation module
    #step_profit_latency,step_latency_profit,step_reability_profit,step_urllc_1_profit,step_urllc_2_profit,step_urllc_3_profit = resource_allocation(c)
    step_latency_profit,step_urllc_1_profit_latency,step_urllc_2_profit_latency,step_urllc_3_profit_latency, urllc_1_accepted_reqs, urllc_2_accepted_reqs, urllc_3_accepted_reqs = resource_allocation(c)

    


    step_reability_profit, step_urllc_1_profit_reability, step_urllc_2_profit_reability, step_urllc_3_profit_reability = calculate_metrics.calculate_profit_reability(num_urllc_1,num_urllc_2,num_urllc_3, urllc_1_accepted_reqs,urllc_2_accepted_reqs,urllc_3_accepted_reqs)
    step_profit = step_latency_profit + step_reability_profit

    step_urllc_1_profit = step_urllc_1_profit_reability + step_urllc_1_profit_latency
    step_urllc_2_profit = step_urllc_2_profit_reability + step_urllc_2_profit_latency
    step_urllc_3_profit = step_urllc_3_profit_reability + step_urllc_3_profit_latency




    c.total_profit += step_profit ## here we have the global profits for all steps not only one
    c.latency_profit += step_latency_profit
    c.reability_profit += step_reability_profit
    c.urllc_1_profit += step_urllc_1_profit
    c.urllc_2_profit += step_urllc_2_profit
    c.urllc_3_profit += step_urllc_3_profit
    """c.total_utl += step_total_utl
    c.node_utl += step_node_utl 
    c.central_utl += step_central_cpu_utl
    c.link_utl += step_links_bw_utl"""
    
    r = step_profit ### ATT this is the reward to pass to the agent
    next_state = get_state(c.substrate,c.simulation) #getting the next state    
    
    #s_ = translateStateToIndex(next_state) #getting index of the next state
    #a_ = agente.take_action(s_,False) #select action for the next state    
    #agente.updateQ(step_profit,s,a,s_,a_,evt.extra["end_state"]) #(reward,s,a,s_,a_end_sate)
    
    s_ = next_state
    a_ = agente.step(s_,r) ## we give the new reward and the current state in order to get the action to take
                           ## here we are getting the new action, no need to execute the step function above since its no longer the first state
    a = a_ ## set the next action to the current action
    s = s_  ## set the next state to the current state
    if counter_windows  == (sim.run_till/twindow_length) - 2: ## here twindow_length is set to 1 as global, need to figure out why we substrate the 2 to set the end_state to true
        end_state = True
        print("the end state is set to True for the twindow event")
    else:
        end_state = False
        
    ### ATTT!!! recursive CALL here  |
    
    evt = sim.create_event(type="twindow_end",start=sim.horario+twindow_length, extra={"first_state":False,"end_state":end_state,"current_state":s,"action":a}, f=func_twindow)  
    print("added a twindow_end event")
    sim.add_event(evt)
    sim.window_req_list = [[],[],[]] #
    #sim.window_req_list = []
    sim.granted_req_list = [] 
  
def prepare_sim(s):## prepares the simulation object for all services and sets the params for them
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_1_arrival_rate),extra={"service_type":"urllc_1","arrival_rate":urllc_1_arrival_rate},f=func_arrival) 
    s.add_event(evt)
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_2_arrival_rate),extra={"service_type":"urllc_2","arrival_rate":urllc_2_arrival_rate},f=func_arrival)    
    s.add_event(evt)
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_3_arrival_rate),extra={"service_type":"urllc_3","arrival_rate":urllc_3_arrival_rate},f=func_arrival)    
    s.add_event(evt)
    ## here maybe its the first state
    evt = s.create_event(type="twindow_end",start=s.horario+twindow_length,extra={"first_state":True,"end_state":False},f=func_twindow)## att here the function is different
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
    global urllc_2_arrival_rate
    global urllc_3_arrival_rate
    
    for m in arrival_rates:  ### the most global loop, arrival_rates = [100,80,60,40,30,25,20,15,10,7,5,3,1]
        urllc_1_arrival_rate = m/3 ##  calculate the rate arrival for each service, its logical we devide by 3 here
        urllc_2_arrival_rate = m/3
        urllc_3_arrival_rate = m/3        
        
        total_profit_rep = []
        reability_profit_rep = []
        latency_profit_rep = []
        central_profit_rep = []
        profit_urllc_1_rep = []
        profit_urllc_2_rep = []
        profit_urllc_3_rep = []
        
        acpt_rate_rep = []
        acpt_rate_urllc_1_rep = []
        acpt_rate_urllc_2_rep = []
        acpt_rate_urllc_3_rep = []

        total_utl_rep = []
        link_utl_rep = []
        node_utl_rep = []
        central_utl_rep = []
        urllc_1_utl_rep = []
        urllc_2_utl_rep = []
        urllc_3_utl_rep = []    
        
        for i in range(episodes): ## we loop the set of episodes which is 350 global var 
                                  ## here creation of empty lists
                                  ## 3
            total_profit_rep.append([])
            reability_profit_rep.append([])
            latency_profit_rep.append([])
            central_profit_rep.append([])
            profit_urllc_1_rep.append([])
            profit_urllc_2_rep.append([])
            profit_urllc_3_rep.append([])
            
            acpt_rate_rep.append([])
            acpt_rate_urllc_1_rep.append([])
            acpt_rate_urllc_2_rep.append([])
            acpt_rate_urllc_3_rep.append([])

            total_utl_rep.append([])
            link_utl_rep.append([])
            node_utl_rep.append([])
            central_utl_rep.append([])
            urllc_1_utl_rep.append([])
            urllc_2_utl_rep.append([])
            urllc_3_utl_rep.append([])
        
        for i in range(repetitions): ## repetitions=33 global 
                                     ## 3


            print("################ REPITITION LOOP #####################", i)                       
            #agente = ql.Qagent(0.9, 0.9, 0.9, episodes, n_states, n_actions) #(alpha, gamma, epsilon, episodes, n_states, n_actions)
            agente = dql.Agent(9,n_actions) ## here we pass the state size and the action size
                                            ## state is with size 9
            for j in range(episodes): ## 1
                agente.handle_episode_start() ## sets last_state and last_action to none


                print("\n","episode:",j,"\n")
                print("################ EPISODE LOOP #####################", j)
                controller = None
                controller = Controlador()                   
                controller.substrate = copy.deepcopy(substrate_graphs.get_graph("16node_BA")) #get substrate  with 16 nodes
                                                                                              ## maybe we dont need to pass the agent to the controller


                # controller.substrate = copy.deepcopy(substrate_graphs.get_graph("abilene")) #get substrate    
                centralized_initial = controller.substrate.graph["centralized_cpu"]
                bw_initial = controller.substrate.graph["bw"]
                controller.simulation.set_run_till(5)   ## set the run_till variable of SIm to 15, the end of the simulatin is after 15 time units
                                                        ## initially was 15
                prepare_sim(controller.simulation)   ## creates the arrival events and the twindow_end event to prepare the environment          
                controller.run()    ## runs all the events of the list one by one, here we execute the run of the class SIm, and a function for each event     
                
                total_profit_rep[j].append(controller.total_profit) ## update all params for the episode j
                latency_profit_rep[j].append(controller.latency_profit)        
                reability_profit_rep[j].append(controller.reability_profit)
                central_profit_rep[j].append(controller.central_profit)
                profit_urllc_1_rep[j].append(controller.urllc_1_profit)
                profit_urllc_2_rep[j].append(controller.urllc_2_profit)
                profit_urllc_3_rep[j].append(controller.urllc_3_profit)
                        
                acpt_rate_rep[j].append(controller.simulation.accepted_reqs/controller.simulation.total_reqs)
                acpt_rate_urllc_1_rep[j].append(controller.simulation.urllc_1_accepted_reqs/controller.simulation.total_urllc_1_reqs)
                acpt_rate_urllc_2_rep[j].append(controller.simulation.urllc_2_accepted_reqs/controller.simulation.total_urllc_2_reqs)
                acpt_rate_urllc_3_rep[j].append(controller.simulation.urllc_3_accepted_reqs/controller.simulation.total_urllc_3_reqs)
                
                """total_utl_rep[j].append(controller.total_utl)
                link_utl_rep[j].append(controller.link_utl)
                node_utl_rep[j].append(controller.node_utl)
                central_utl_rep[j].append(controller.central_utl) 
                urllc_1_utl_rep[j].append(controller.urllc_1_utl)
                urllc_2_utl_rep[j].append(controller.urllc_2_utl)
                urllc_3_utl_rep[j].append(controller.urllc_3_utl)"""

            #bot.sendMessage("Repetition " + str(i) + " finishes!")
            
            f = open("deepsara_"+str(m)+"_16BA_9de10sta_30actv22_wWWWW2_maxexpl05_btchsz15_rpsrtsz400_anrate1-400_1h150ns_350epi_prioritizerv6.txt","w+")

            f.write("Repetition: "+str(i)+"\n")
            f.write("**Reward:\n")
            f.write(str(total_profit_rep)+"\n\n")
            f.write("**latency_profit_rep:\n")
            f.write(str(latency_profit_rep)+"\n\n")
            f.write("**reability_profit_rep:\n")
            f.write(str(reability_profit_rep)+"\n\n")
            f.write("**central_profit_rep:\n")
            f.write(str(central_profit_rep)+"\n\n")
            f.write("**profit_urllc_1_rep:\n")
            f.write(str(profit_urllc_1_rep)+"\n\n")
            f.write("**profit_urllc_2_rep:\n")
            f.write(str(profit_urllc_2_rep)+"\n\n")
            f.write("**profit_urllc_3_rep:\n")
            f.write(str(profit_urllc_3_rep)+"\n\n")

            f.write("**Acceptance Rate:\n")
            f.write(str(acpt_rate_rep)+"\n\n")
            f.write("**acpt_rate_urllc_1_rep:\n")
            f.write(str(acpt_rate_urllc_1_rep)+"\n\n")
            f.write("**acpt_rate_urllc_2_rep:\n")
            f.write(str(acpt_rate_urllc_2_rep)+"\n\n")
            f.write("**acpt_rate_urllc_3_rep:\n")
            f.write(str(acpt_rate_urllc_3_rep)+"\n\n")

            """f.write("**total_utl_rep:\n")
            f.write(str(total_utl_rep)+"\n\n")
            f.write("**node_utl_rep:\n")
            f.write(str(node_utl_rep)+"\n\n")
            f.write("**link_utl_rep:\n")
            f.write(str(link_utl_rep)+"\n\n")
            f.write("**central_utl_rep:\n")
            f.write(str(central_utl_rep)+"\n\n")
            f.write("**urllc_1_utl_rep:\n")
            f.write(str(urllc_1_utl_rep)+"\n\n")
            f.write("**urllc_2_utl_rep:\n")
            f.write(str(urllc_2_utl_rep)+"\n\n")
            f.write("**urllc_3_utl_rep:\n")
            f.write(str(urllc_3_utl_rep)+"\n\n")        
            f.close()"""
            

if __name__ == '__main__':
    #bot.sendMessage("Simulation starts!")
    start = time.time()## in order to receive the current time
    print("start time: ",start)
    main()
    end = time.time()
    print("end time: ",end)
    #bot.sendMessage("Simulation finishes!")
    #bot.sendMessage("total time: " + str(end-start))
