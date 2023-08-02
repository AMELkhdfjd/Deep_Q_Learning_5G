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
profit_nr =   [109, 80, 49, 64, 58, 46, 60, 45, 61, 61, 39, 50, 51, 53, 57, 40, 38, 52, 47, 45, 64, 53, 50, 47, 37, 61, 72, 51, 50, 47, 38, 47, 44, 46, 55, 38, 71, 49, 46, 53, 53, 42, 49, 52, 60, 39, 74, 46, 64, 67, 47, 68, 49, 41, 70, 44, 62, 51, 73, 71, 36, 53, 76, 60, 65, 53, 63, 74, 70, 84, 84, 83, 71, 53, 67, 95, 49, 79, 73, 105, 91, 91, 61, 84, 48, 76, 94, 44, 88, 98, 103, 123, 94, 110, 55, 70, 65, 74, 88, 127, 67, 83, 93, 61, 56, 143, 76, 134, 91, 76, 93, 104, 68, 77, 95, 154, 70, 112, 108, 121, 118, 107, 123, 103, 84, 85, 42, 73, 83, 86, 168, 96, 109, 155, 168, 67, 62, 115, 54, 114, 66, 72, 122, 82, 98, 66, 86, 50, 68, 111, 90, 142, 171, 129, 85, 146, 90, 75, 80, 77, 46, 140, 82, 91, 92, 92, 101, 111, 86, 91, 87, 117, 119, 49, 203, 122, 93, 92, 94, 129, 74, 193, 73, 103, 137, 62, 84, 76, 45, 48, 70, 109, 116, 89, 37, 183, 82, 92, 54, 55]


font = {'family' : 'sans-serif',
        'size'   : 16}
matplotlib.rc('font', **font)



for i in range(200):
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
