import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import csv
import math
import numpy as np


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
y = []
topologies = ["16BA","abilene"]

########### arrivalRate20 ############
arrival_rate = "20"



lost_r=  []


lost_r_old = [4, 2, 3, 5, 3, 2, 2, 6, 3, 3, 6, 3, 5, 4, 7, 2, 5, 4, 5, 8, 0, 5, 3, 3, 3, 5, 3, 4, 6, 7, 1, 3, 1, 4, 3, 6, 4, 4, 2, 2, 3, 1, 7, 2, 3, 1, 3, 0, 1, 6, 2, 4, 4, 4, 1, 4, 5, 3, 1, 2, 0, 2, 3, 2, 2]







font = {'family' : 'sans-serif',
        'size'   : 16}
matplotlib.rc('font', **font)



for i in range(65):
   x.append(i+1)


for i in range(355):
    y.append(i+1)
# Profit

## Old_code
margin_error1 =[]
lost_r_old_2 =[]




plt.errorbar(x,lost_r_old,fmt="-", color="red",ecolor="lightgray",capsize=2, label= "Old")
#plt.errorbar(y,lost_r,fmt="-", color="blue",ecolor="lightgray",capsize=2,label= "New")



#plt.axvline(x=12, color = "silver", linestyle='--')
#plt.errorbar(x,acceptance_ratio, fmt="-",label="SARA",ecolor="lightgray",capsize=2)
#plt.errorbar(x,profit_reability,fmt="-",label="NR", color="red", ecolor="lightgray",capsize=2)
#plt.errorbar(x,lost_r,fmt="-",label="AAR", color="gray",ecolor="lightgray",capsize=2)

#plt.errorbar(x,profit_r2c,fmt="-",label="AAR", color="blue",ecolor="lightgray",capsize=2)
plt.xlabel('Episodes')
plt.ylabel('Reward')
plt.title(' Reward vs Episodes')
#plt.legend()
plt.legend(fontsize = 14,loc='lower right', fancybox=True, shadow=True)
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1), fancybox=True, shadow=True, ncol=3)
#plt.show() 
plt.savefig("Big_profit_r2C.png",bbox_inches = 'tight') 
plt.close()




