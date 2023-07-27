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
#from SimGNN_DQL import SimGNNTrainer ## for the gcn
from param_parser import parameter_parser ## for the gcn


# import bisect
#simulation parameters
# seed = 0
repetitions = 1 #33
twindow_length = 1
# urllc_1_arrival_rate = 10 #5#1#2 #reqXsecond
# urllc_2_arrival_rate = 40 #5#2.5 #reqXsecond
# urllc_3_arrival_rate = 10 #5#1#2 #reqXsecond

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
        #self.total_urllc_1_reqs = 0
        #self.total_urllc_2_reqs = 0
        #self.total_urllc_3_reqs = 0
        self.attended_reqs = 0
    
        self.reject_r_issue = 0
        self.reject_nslr = 0
        self.accepted_reqs = 0
        self.cpt = 0
  
                   

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
            evt.extra["id"] = self.total_reqs
            
            service_type = evt.extra["service_type"]## maybe the extra means the additional parameters for the event here we are assigining the service_type
            #self.request_list.append(nsl_request.get_nslr(self.total_reqs,service_type,mean_operation_time))## here we are calling the fonction from the file imported ATT
           
              ## self.total_reqs: to define the id of the new nslr, 
              ## mean_operation_time = 15 as a global variable


            """if evt.extra["service_type"] == "urllc_1":
                self.total_urllc_1_reqs += 1
                self.window_req_list[0].append(copy.deepcopy(request))## add the request to the window list according to the type of the service
            elif evt.extra["service_type"] == "urllc_2":
                self.total_urllc_2_reqs += 1
                self.window_req_list[1].append(copy.deepcopy(request))#
            else: #evt.extra["service_type"] == "urllc_3":
                self.total_urllc_3_reqs += 1
                self.window_req_list[2].append(copy.deepcopy(request))#"""
            
        #print("print details events:  ")
        #self.print_eventos()




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



def resource_allocation(cn, index, already_backup, a): #cn=controller
   #makes allocation for the set of nslrs captured in a time window ##and returns the profits calculated for the global allocations
    # the metrics calculated here correspond to a step
     
    sim = cn.simulation ## define the object of class Sim which is part of the Controller class
    substrate = cn.substrate ## substrate of the controller class
    step_urllc_1_profit_latency = 0 
    step_urllc_2_profit_latency = 0
    step_urllc_3_profit_latency = 0
    step_latency_profit=0
    end_simulation_time = sim.run_till
    
    req = sim.request
    vnfs = sim.request.nsl_graph["vnfs"]
    vnf = vnfs[index]
    reliability = 0    

    rejected, reliability, already_backup = nsl_placement.nsl_placement(req, index, substrate, already_backup, a)#mapping  ## here try to allocate the nslr req in the substrate graph
        
    if not rejected: ## successfully mapped
         
        
            profit_reliability = reliability
            #step_latency_profit += profit_latency 
           

            if(len(vnfs) -1   == index ): ## check here if its index-1, which means its not rejected and its the last vnf, create a termination event
                sim.request.set_end_time(sim.horario+sim.request.operation_time)
               
                print("the accepted reqs: ", sim.accepted_reqs)
                print("END TIME:  ", sim.request.end_time)

                evt = sim.create_event(type="termination",start=sim.request.end_time, extra=sim.request, f=func_terminate) ## add the event to the list of events
                sim.add_event(evt)
                print("TERMINATTION:   " )
                print(str(evt), end=" > \n")


                ## add here the final reward to get
    else:
        profit_reliability = -1 ## the bad reward when we reject all the request due to non allocation of a vnf

                      
            
        
             
    return profit_reliability, already_backup



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

    labels_1 = [[node["p"], node["cpu"]] for node in substrate.graph["nodes"]]

# Extract links' "source" and "target" values into "graph_1"
    graph_1 = [[link["source"], link["target"]] for link in substrate.graph["links"]]

# Create the desired format in the "graph" variable
    graph_s = {
    "labels_1": labels_1,
    "graph_1": graph_1
    }
    labels_2 = [[node["cpu"]] for node in simulation.request["vnfs"]]

# Extract links' "source" and "target" values into "graph_1"
    graph_2 = [[link["source"], link["vnfs"]["target"]] for link in simulation.request["vnfs"]]

# Create the desired format in the "graph" variable
    graph_v = {
    "labels_2": labels_2,
    "graph_2": graph_2
    }


    trainer = SimGNNTrainer(args, graph_s, graph_v, index)
    state = trainer.fit()
   

    return state

def func_arrival(c,evt): #NSL arrival, we will treate the one URLLC request arrived


    global counter_windows
    sim = c.simulation 
    
    
    num_urllc_1 = 0
    num_urllc_2 = 0
    num_urllc_3 = 0
    step_urllc_1_profit_reability =0
    step_urllc_2_profit_reability =0
    step_urllc_3_profit_reability =0
    already_backup =[[], []]
    reliability_total = 1
    actions = c.substrate.graph["nodes"]  ### NEW: defenition of the new action here

    #sim.request = sim.request_list[sim.cpt]

    sim.request = nsl_request.get_nslr(evt.extra["id"],evt.extra["service_type"],mean_operation_time)
    print("toto: ", sim.request.nsl_graph, sim.request.id)
   
    vnfs = sim.request.nsl_graph["vnfs"]
    vlinks = sim.request.nsl_graph["vlinks"]
    sim.attended_reqs = sim.attended_reqs +1
    print("TYPE  : ", evt.extra["service_type"])
    ## here we should take the action and state from the last request placement:
    if(evt.extra["first_event"] == True):
            r = 0
            #a = agente.step(state,0) ## this returns the action taken, here we call the function step from the dql file, give state, reward, training=true, 
           
    else:
            r = evt.extra["current_reward"]
            print("the reward outside the loop is : ", r)


    for index, vnf in enumerate(vnfs):

        

         #state = get_state(c.substrate,c.simulation, index)
        state = [0.3703, 0.3540, 0.0000, 0.7822, 0.0000, 0.0000, 0.0000, 0.0000, 0.901,
         0.5891, 0.6244, 0.0000, 0.1250, 0.1847, 0.2786, 0.0000]

        a =   agente.step(state,r)  
        print("THE ACTION : ", a)

        profit_reliability, already_backup = resource_allocation(c, index, already_backup, a)
        r = profit_reliability
        reliability_total = reliability_total*r 
        print("THE REWARD : ", r)
        ## adding the reward of the entire nslr
        if (index == len(vnfs)-1): ## we are on the last vnf
            print("the total reliability:  ", reliability_total)
            if(reliability_total <= sim.request.nsl_graph["reliability"]):
                r = -1
                sim.reject_r_issue = sim.reject_r_issue+1
                print("REABIILTY ISSUE --------------------- ")

                break
            else: ## means we have instantiated one whole nslr
                sim.accepted_reqs = sim.accepted_reqs +1
                print("accepted requests: ", sim.accepted_reqs)
        else:
            if(r == -1):
                sim.reject_nslr = sim.reject_nslr +1
                print("RESSOURCES ISSUE ____________________ ")
                break
            

    ## the original func_arrival
   
    # print("**/",evt.extra["arrival_rate"])
    arrival_rate = evt.extra["arrival_rate"]
    service_type = evt.extra["service_type"]
    inter_arrival_time = get_interarrival_time(arrival_rate)
    print("treated arrival event ---> creration of another arrival event")
    sim.add_event(evt = sim.create_event(type="arrival",start=sim.horario+inter_arrival_time, extra={"service_type":service_type,"arrival_rate":arrival_rate, "current_reward":r, "first_event": False}, f=func_arrival))



    #print("EVENTSSSSSSSSSSSSSS ")
    #print(str(evt), end=" > \n")
    #sim.print_eventos()
    ## the request variable will be changed here, and storing the new urllc request for the arriving event





def func_terminate(c,evt):   ## terminates a request, updates the ressources and reduced the number of instantiated reqs list
    global counter_termination
    sim = c.simulation
    
    print("*******************  terminating")
    print("BEFORE \n", c.substrate.graph["nodes"], c.substrate.graph["links"],"\n\n")
    
    request = evt.extra
    print("the request terminated: \n ", request.nsl_graph)

    update_resources(c.substrate,request,True)
    print("AFTER ", c.substrate.graph["nodes"], c.substrate.graph["links"])

  


"""def func_twindow(c,evt):  ## recursive function need to understand it more
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
      
    sim.granted_req_list, remaining_req_list, num_urllc_1, num_urllc_2, num_urllc_3 = prioritizer(sim.window_req_list, a) #the list of reqs is filtered depending on the action
    #print("results of prioritizer: num_urllc1, num_urllc2, num_urllc3:  ", num_urllc_1, num_urllc_2, num_urllc_3)
    #the list is sent to the Resource Allocation module
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
        #print("the end state is set to True for the twindow event")
    else:
        end_state = False
        
    ### ATTT!!! recursive CALL here  |
    
    evt = sim.create_event(type="twindow_end",start=sim.horario+twindow_length, extra={"first_state":False,"end_state":end_state,"current_state":s,"action":a}, f=func_twindow)  
    #print("added a twindow_end event")
    sim.add_event(evt)
    sim.window_req_list = [[],[],[]] #
    #sim.window_req_list = []
    sim.granted_req_list = [] """
  
def prepare_sim(s):## prepares the simulation object for all services and sets the params for them
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_1_arrival_rate),extra={"service_type":"urllc_1","arrival_rate":urllc_1_arrival_rate, "first_event": True},f=func_arrival) 
    s.add_event(evt)
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_1_arrival_rate),extra={"service_type":"urllc_2","arrival_rate":urllc_1_arrival_rate, "first_event": True},f=func_arrival)    
    s.add_event(evt)
    evt = s.create_event(type="arrival",start=s.horario+get_interarrival_time(urllc_1_arrival_rate),extra={"service_type":"urllc_3","arrival_rate":urllc_1_arrival_rate, "first_event": True},f=func_arrival)    
    s.add_event(evt)
    ## here maybe its the first state
    #evt = s.create_event(type="twindow_end",start=s.horario+twindow_length,extra={"first_state":True,"end_state":False},f=func_twindow)## att here the function is different
    #s.add_event(evt)


                                
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
    #global urllc_2_arrival_rate
    #global urllc_3_arrival_rate
    
    for m in arrival_rates:  ### the most global loop, arrival_rates = [100,80,60,40,30,25,20,15,10,7,5,3,1]
        #urllc_1_arrival_rate = m/3 ##  calculate the rate arrival for each service, its logical we devide by 3 here
        urllc_1_arrival_rate = m   ## we have only one service type, logically take the arival rate as it is
               
        
        total_profit_rep = []
     
        profit_urllc_1_rep = []
       
        
        acpt_rate_rep = []
        acpt_rate_urllc_1_rep = []
      
        total_utl_rep = []
        link_utl_rep = []
        node_utl_rep = []
      
        urllc_1_utl_rep = []
          
        
        for i in range(episodes): ## we loop the set of episodes which is 350 global var 
                                  ## here creation of empty lists
                                  ## 1
            total_profit_rep.append([])
            #reability_profit_rep.append([])
            #latency_profit_rep.append([])
            #central_profit_rep.append([])
            profit_urllc_1_rep.append([])
            #profit_urllc_2_rep.append([])
            #profit_urllc_3_rep.append([])
            
            acpt_rate_rep.append([])
            acpt_rate_urllc_1_rep.append([])
            #acpt_rate_urllc_2_rep.append([])
            #acpt_rate_urllc_3_rep.append([])

            total_utl_rep.append([])
            link_utl_rep.append([])
            node_utl_rep.append([])
            #central_utl_rep.append([])
            urllc_1_utl_rep.append([])
            #urllc_2_utl_rep.append([])
            #urllc_3_utl_rep.append([])


        
        for i in range(repetitions): ## repetitions=33 global 
                                     ## 1


            print("################ REPITITION LOOP #####################", i)                       
            #agente = ql.Qagent(0.9, 0.9, 0.9, episodes, n_states, n_actions) #(alpha, gamma, epsilon, episodes, n_states, n_actions)
            agente = dql.Agent(12,10) ## here we pass the state size and the action size
                                            ## 
                                            ## the action size is the number of nodes in the phisical graph, we take it 10
            for j in range(episodes): ## 1
                agente.handle_episode_start() ## sets last_state and last_action to none


                print("\n","episode:",j,"\n")
                print("################ EPISODE LOOP #####################", j)
                controller = None
                controller = Controlador()                   
                controller.substrate = copy.deepcopy(substrate_graphs.get_graph(10)) #get substrate  with 16 nodes
                                                                                              ## maybe we dont need to pass the agent to the controller


                # controller.substrate = copy.deepcopy(substrate_graphs.get_graph("abilene")) #get substrate    
                centralized_initial = controller.substrate.graph["centralized_cpu"]
                bw_initial = controller.substrate.graph["bw"]
                controller.simulation.set_run_till(1)   ## set the run_till variable of SIm to 15, the end of the simulatin is after 15 time units
                                                        ## initially was 15
                prepare_sim(controller.simulation)   ## creates the arrival events and the twindow_end event to prepare the environment          
                controller.run()    ## runs all the events of the list one by one, here we execute the run of the class SIm, and a function for each event     
                print("the lost requests: ", controller.simulation.reject_r_issue)
                print("the lost requests: ", controller.simulation.reject_nslr)
                print("the attended requests: ", controller.simulation.attended_reqs)
                print("the accepted requests: ", controller.simulation.accepted_reqs)

                print("the acceptence ratio: ", (controller.simulation.accepted_reqs/ controller.simulation.attended_reqs)*100 )



                total_profit_rep[j].append(controller.total_profit) ## update all params for the episode j
                """latency_profit_rep[j].append(controller.latency_profit)        
                reability_profit_rep[j].append(controller.reability_profit)
                central_profit_rep[j].append(controller.central_profit)
                profit_urllc_1_rep[j].append(controller.urllc_1_profit)
                profit_urllc_2_rep[j].append(controller.urllc_2_profit)
                profit_urllc_3_rep[j].append(controller.urllc_3_profit)
                        
                acpt_rate_rep[j].append(controller.simulation.accepted_reqs/controller.simulation.total_reqs)
                acpt_rate_urllc_1_rep[j].append(controller.simulation.urllc_1_accepted_reqs/controller.simulation.total_urllc_1_reqs)
                acpt_rate_urllc_2_rep[j].append(controller.simulation.urllc_2_accepted_reqs/controller.simulation.total_urllc_2_reqs)
                acpt_rate_urllc_3_rep[j].append(controller.simulation.urllc_3_accepted_reqs/controller.simulation.total_urllc_3_reqs)"""
                
                """total_utl_rep[j].append(controller.total_utl)
                link_utl_rep[j].append(controller.link_utl)
                node_utl_rep[j].append(controller.node_utl)
                central_utl_rep[j].append(controller.central_utl) 
                urllc_1_utl_rep[j].append(controller.urllc_1_utl)
                urllc_2_utl_rep[j].append(controller.urllc_2_utl)
                urllc_3_utl_rep[j].append(controller.urllc_3_utl)"""

            #bot.sendMessage("Repetition " + str(i) + " finishes!")
            
            f = open("deepsara_"+str(m)+"_16BA_9de10sta_30actv22_wWWWW2_maxexpl05_btchsz15_rpsrtsz400_anrate1-400_1h150ns_350epi_prioritizerv6.txt","w+")
"""
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
            f.write(str(acpt_rate_urllc_3_rep)+"\n\n")"""

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
