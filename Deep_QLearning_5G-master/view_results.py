import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import csv
import math



def average(lista): # function to return the average of a list of data


    sum=0.0
    for l in range(0,len(lista)):
        sum=sum+lista[l] 
    return sum/len(lista)

def standardDev(lista): # function to calculate standard deviation
    sum = 0.0
    size = len(lista)
    avrg = average(lista)
    #print "average: ",avrg
    for l in range(0,len(lista)):
        sum = sum + math.pow((lista[l] - avrg), 2.0)    
    return math.sqrt(sum/(size));


x = []
topologies = ["16BA","abilene"]

########### arrivalRate20 ############
arrival_rate = "20"
profit_nr = [0.4694444444444444, 0.46034722222222224, 0.48458333333333325, 0.4847222222222223, 0.4030555555555555, 0.3065277777777778, 
              0.4633333333333334, 0.39743055555555556, 0.47069444444444436, 0.522986111111111, 0.5178472222222223, 0.4193055555555556, 
              0.46965277777777775, 0.33833333333333326, 0.4179861111111111, 0.54875, 0.3986111111111111]



font = {'family' : 'sans-serif',
        'size'   : 16}
matplotlib.rc('font', **font)



for i in range(17):
    x.append(i+1)

# Profit
#plt.axvline(x=12, color = "silver", linestyle='--')
plt.errorbar(x,profit_nr, fmt="-",label="SARA",ecolor="lightgray",capsize=2)
#plt.errorbar(x,profit_nr_aux,yerr = margin_error2,fmt="-",label="NR", color="red", ecolor="lightgray",capsize=2)
#plt.errorbar(x,profit_aar_aux,yerr = margin_error3,fmt="-",label="AAR", color="gray",ecolor="lightgray",capsize=2)
plt.xlabel('Episodes')
plt.ylabel('Profit')
plt.title('Time Step Profit')
#plt.legend()
plt.legend(fontsize = 14,loc='lower right', fancybox=True, shadow=True)
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1), fancybox=True, shadow=True, ncol=3)
#plt.show() 
plt.savefig("profit_"+arrival_rate+"_"+topologies[0]+".png",bbox_inches = 'tight') 
plt.close()

# # Aceptance rate
# plt.errorbar(x,acpt_rate_rl_aux,yerr = margin_error4,fmt="-",label="SARA",ecolor="lightgray",capsize=2)
# plt.errorbar(x,acpt_rate_nr_aux,yerr = margin_error5,fmt="-",label="NR", color="red", ecolor="lightgray",capsize=2)
# plt.errorbar(x,acpt_rate_aar_aux,yerr = margin_error6,fmt="-",label="AAR ", color="gray",ecolor="lightgray",capsize=2)
# plt.xlabel('Episodes')
# plt.ylabel('Acceptance Rate')
# # plt.title('Time Step Acceptance Rate')
# plt.legend(fontsize = 14,fancybox=True,shadow=True,bbox_to_anchor=(1, 0.61))
# # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1), fancybox=True, shadow=True, ncol=3)
# # #plt.show()
# plt.savefig("acptrate_"+arrival_rate+"_"+topologies[0]+".eps",bbox_inches = 'tight')  
# plt.close()

# # # Resource Utilization
# plt.axvline(x=12, color = "silver", linestyle='--')
# plt.errorbar(x,res_utl_rl_aux,yerr = me_utl_rl,fmt="-",label="SARA",ecolor="lightgray",capsize=2)
# plt.errorbar(x,res_utl_nr_aux,yerr = me_utl_nr,fmt="-",label="NR", color="red", ecolor="lightgray",capsize=2)
# plt.errorbar(x,res_utl_aar_aux,yerr = me_utl_aar,fmt="-",label="AAR", color="gray",ecolor="lightgray",capsize=2)
# plt.xlabel('Episodes')
# plt.ylabel('Resource Utilization')
# # plt.title('Time Step Resource Utilization')
# plt.legend(fontsize = 14,loc='lower right', fancybox=True, shadow=True)
# # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1), fancybox=True, shadow=True, ncol=3)
# #plt.show()
# # plt.ylim(0.48,0.61)
# plt.savefig("resutl_"+arrival_rate+"_"+topologies[0]+".eps",bbox_inches = 'tight')  
# plt.close()

#
