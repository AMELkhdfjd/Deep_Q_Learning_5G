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



lost_r= [87.17948717948718, 86.8421052631579, 75.0, 89.74358974358975, 85.0, 92.10526315789474, 92.10526315789474, 79.48717948717949, 86.48648648648648, 89.47368421052632, 79.48717948717949, 75.0, 92.10526315789474, 82.5, 89.47368421052632, 89.74358974358975, 89.74358974358975, 86.48648648648648, 92.10526315789474, 82.05128205128204, 82.05128205128204, 88.88888888888889, 82.05128205128204, 89.1891891891892, 78.94736842105263, 76.92307692307693, 84.61538461538461, 92.10526315789474, 73.80952380952381, 65.9090909090909, 81.57894736842105, 89.74358974358975, 97.36842105263158, 81.57894736842105, 82.5, 84.21052631578947, 80.55555555555556, 78.57142857142857, 69.76744186046511, 64.1025641025641, 97.2972972972973, 82.05128205128204, 84.61538461538461, 86.8421052631579, 60.97560975609756, 80.48780487804879, 82.05128205128204, 87.5, 91.8918918918919, 73.17073170731707, 68.88888888888889, 71.42857142857143, 88.88888888888889, 78.04878048780488, 89.1891891891892, 82.92682926829268, 89.47368421052632, 77.5, 92.10526315789474, 86.8421052631579, 71.05263157894737, 81.08108108108108, 87.5, 86.48648648648648, 66.66666666666666, 77.5, 84.21052631578947, 66.66666666666666, 94.73684210526315, 100.0, 86.8421052631579, 82.05128205128204, 75.60975609756098, 74.35897435897436, 94.5945945945946, 67.44186046511628, 70.73170731707317, 76.19047619047619, 84.21052631578947, 86.48648648648648, 81.57894736842105, 89.1891891891892, 77.5, 86.11111111111111, 85.0, 87.17948717948718, 66.66666666666666, 84.21052631578947, 86.8421052631579, 94.73684210526315, 76.31578947368422, 97.36842105263158, 82.05128205128204, 78.94736842105263, 74.35897435897436, 76.31578947368422, 84.21052631578947, 79.48717948717949, 91.66666666666666, 66.66666666666666, 76.92307692307693, 82.05128205128204, 97.2972972972973, 72.5, 97.22222222222221, 79.48717948717949, 77.5, 86.8421052631579, 81.57894736842105, 87.17948717948718, 73.80952380952381, 82.05128205128204, 79.48717948717949, 86.8421052631579, 87.17948717948718, 89.1891891891892, 94.87179487179486, 81.08108108108108, 77.5, 87.5, 80.48780487804879, 84.61538461538461, 86.8421052631579, 82.5, 73.17073170731707, 80.0, 94.73684210526315, 84.61538461538461, 66.66666666666666, 73.80952380952381, 89.74358974358975, 94.73684210526315, 84.61538461538461, 82.05128205128204, 82.92682926829268, 89.47368421052632, 75.0, 70.73170731707317, 82.05128205128204, 97.36842105263158, 74.35897435897436, 84.21052631578947, 82.5, 82.05128205128204, 82.5, 85.36585365853658, 70.45454545454545, 76.92307692307693, 76.92307692307693, 75.60975609756098, 92.10526315789474, 86.8421052631579, 92.10526315789474, 73.17073170731707, 84.21052631578947, 82.05128205128204, 84.21052631578947, 80.0, 94.5945945945946, 87.17948717948718, 84.21052631578947, 82.05128205128204, 84.21052631578947, 94.87179487179486, 84.61538461538461, 86.8421052631579, 75.0, 84.61538461538461, 94.44444444444444, 86.48648648648648, 81.08108108108108, 79.48717948717949, 86.8421052631579, 76.92307692307693, 85.0, 83.78378378378379, 78.57142857142857, 68.18181818181817, 80.0, 78.94736842105263, 74.4186046511628, 83.78378378378379, 79.48717948717949, 78.04878048780488, 79.48717948717949, 80.0, 86.48648648648648, 82.5, 74.35897435897436, 85.0, 57.77777777777777, 78.94736842105263, 76.92307692307693, 62.5, 81.57894736842105, 76.92307692307693, 78.94736842105263, 91.8918918918919, 78.94736842105263, 85.0, 81.08108108108108, 71.7948717948718, 92.3076923076923, 84.21052631578947, 92.3076923076923, 85.0, 81.57894736842105, 94.87179487179486, 72.5, 71.7948717948718, 89.74358974358975, 89.74358974358975, 87.17948717948718, 82.05128205128204, 73.17073170731707, 71.7948717948718, 80.48780487804879, 75.0, 66.66666666666666, 89.47368421052632, 77.5, 76.92307692307693, 92.10526315789474, 81.08108108108108, 92.10526315789474, 70.73170731707317, 90.0, 89.47368421052632, 70.73170731707317, 97.36842105263158, 66.66666666666666, 85.0, 94.73684210526315, 83.78378378378379, 78.04878048780488, 92.10526315789474, 69.23076923076923, 80.48780487804879, 73.17073170731707, 92.10526315789474, 71.42857142857143, 71.42857142857143, 78.57142857142857, 92.3076923076923, 86.8421052631579, 83.33333333333334, 85.36585365853658, 77.5, 82.05128205128204, 84.21052631578947, 75.0, 85.0, 66.66666666666666, 70.45454545454545, 91.8918918918919, 68.29268292682927, 72.72727272727273, 82.92682926829268, 66.66666666666666, 82.5, 81.57894736842105, 80.48780487804879, 92.10526315789474, 64.28571428571429, 61.36363636363637, 71.42857142857143, 80.48780487804879, 94.73684210526315, 87.5, 76.19047619047619, 87.17948717948718, 82.5, 76.74418604651163, 86.11111111111111, 92.3076923076923, 75.0, 70.73170731707317, 81.08108108108108, 74.4186046511628, 73.17073170731707, 77.27272727272727, 84.21052631578947, 75.60975609756098, 72.09302325581395, 85.0, 85.36585365853658, 92.3076923076923, 85.71428571428571, 89.47368421052632, 82.92682926829268, 97.2972972972973, 87.17948717948718, 71.42857142857143, 78.04878048780488, 82.5, 82.05128205128204, 70.73170731707317, 87.17948717948718, 89.74358974358975, 78.57142857142857, 73.17073170731707, 75.60975609756098, 78.04878048780488, 80.48780487804879, 94.73684210526315, 70.73170731707317, 80.0, 81.3953488372093, 87.5, 82.05128205128204, 79.06976744186046, 76.74418604651163, 84.61538461538461, 71.05263157894737, 79.48717948717949, 82.05128205128204, 80.48780487804879, 84.21052631578947, 78.94736842105263, 77.5, 81.08108108108108, 80.0, 81.57894736842105, 79.48717948717949, 86.8421052631579, 90.0, 80.48780487804879, 92.10526315789474, 92.10526315789474, 68.29268292682927, 89.47368421052632, 97.36842105263158, 78.04878048780488, 87.17948717948718, 80.48780487804879, 79.48717948717949, 81.08108108108108, 84.61538461538461, 92.3076923076923, 68.29268292682927, 69.76744186046511, 68.29268292682927, 85.0, 73.80952380952381, 84.61538461538461, 71.42857142857143, 76.74418604651163, 89.1891891891892, 64.44444444444444, 78.57142857142857, 94.73684210526315, 76.92307692307693, 60.0, 74.4186046511628, 91.8918918918919, 87.5, 65.85365853658537, 69.76744186046511, 86.8421052631579, 70.45454545454545, 97.36842105263158, 94.73684210526315, 61.36363636363637, 59.183673469387756, 79.48717948717949, 80.95238095238095, 80.0, 69.76744186046511, 78.04878048780488, 82.5, 86.48648648648648, 74.35897435897436, 73.17073170731707, 84.61538461538461, 78.04878048780488, 75.0, 83.33333333333334, 86.8421052631579, 79.48717948717949, 81.57894736842105, 70.0, 70.73170731707317, 69.23076923076923, 86.8421052631579, 66.66666666666666, 82.5, 73.17073170731707, 74.4186046511628, 76.74418604651163, 87.5, 80.0, 74.4186046511628]





lost_r_old = [84.21052631578947, 76.31578947368422, 78.94736842105263, 84.61538461538461, 75.67567567567568, 72.97297297297297, 81.08108108108108, 58.97435897435898, 78.94736842105263, 68.42105263157895, 68.42105263157895, 86.48648648648648, 89.47368421052632, 71.7948717948718, 84.21052631578947, 83.78378378378379, 91.8918918918919, 84.21052631578947, 76.31578947368422, 84.21052631578947, 80.0, 89.47368421052632, 84.21052631578947, 89.47368421052632, 77.5, 75.60975609756098, 89.1891891891892, 82.05128205128204, 75.60975609756098, 86.8421052631579, 83.33333333333334, 72.97297297297297, 76.31578947368422, 60.97560975609756, 69.23076923076923, 73.68421052631578, 77.5, 75.0, 72.97297297297297, 94.73684210526315, 81.08108108108108, 84.21052631578947, 69.23076923076923, 81.57894736842105, 78.94736842105263, 84.21052631578947, 76.31578947368422, 92.3076923076923, 81.57894736842105, 81.08108108108108, 75.67567567567568, 87.17948717948718, 97.36842105263158, 78.37837837837837, 80.0, 70.0, 84.61538461538461, 74.35897435897436, 81.08108108108108, 91.8918918918919, 79.48717948717949, 86.48648648648648, 73.17073170731707, 77.5, 83.78378378378379, 65.85365853658537, 78.94736842105263, 86.48648648648648, 73.80952380952381, 73.68421052631578, 94.73684210526315, 76.92307692307693, 79.48717948717949, 84.21052631578947, 84.21052631578947, 80.0, 76.92307692307693, 81.57894736842105, 78.37837837837837, 68.42105263157895, 84.21052631578947, 86.8421052631579, 63.04347826086957, 82.05128205128204, 86.8421052631579, 70.27027027027027, 84.61538461538461, 84.61538461538461, 84.21052631578947, 86.48648648648648, 89.47368421052632, 78.94736842105263, 73.17073170731707, 72.5, 83.33333333333334, 81.57894736842105, 81.57894736842105, 89.47368421052632, 84.61538461538461, 94.73684210526315, 76.74418604651163, 79.48717948717949, 87.5, 97.43589743589743, 85.0, 86.8421052631579, 71.7948717948718, 71.42857142857143, 89.47368421052632, 94.73684210526315, 97.36842105263158, 86.8421052631579, 75.67567567567568, 70.73170731707317, 74.4186046511628, 89.47368421052632, 86.8421052631579, 72.5, 79.48717948717949, 92.3076923076923, 73.17073170731707, 81.57894736842105, 91.8918918918919, 92.10526315789474, 82.05128205128204, 84.61538461538461, 89.47368421052632, 94.44444444444444, 92.10526315789474, 75.60975609756098, 86.8421052631579, 72.5, 94.5945945945946, 80.0, 82.92682926829268, 70.0, 78.94736842105263, 87.5, 92.10526315789474, 81.08108108108108, 84.21052631578947, 73.17073170731707, 86.48648648648648, 84.61538461538461, 73.68421052631578, 81.57894736842105, 80.0, 84.61538461538461, 81.57894736842105, 86.8421052631579, 84.21052631578947, 78.04878048780488, 89.1891891891892, 75.60975609756098, 89.47368421052632, 70.73170731707317, 89.1891891891892, 78.94736842105263, 78.94736842105263, 84.61538461538461, 86.8421052631579, 80.0, 77.5, 72.5, 84.21052631578947, 76.31578947368422, 92.10526315789474, 81.08108108108108, 75.0, 78.37837837837837, 73.68421052631578, 86.8421052631579, 73.68421052631578, 75.0, 92.10526315789474, 94.5945945945946, 89.47368421052632, 72.5, 89.74358974358975, 84.21052631578947, 83.78378378378379, 76.92307692307693, 83.78378378378379, 91.8918918918919, 89.47368421052632, 89.1891891891892, 86.48648648648648, 90.0, 73.17073170731707, 67.5, 84.21052631578947, 92.10526315789474, 82.5, 84.61538461538461, 87.5, 84.21052631578947, 65.11627906976744, 81.57894736842105, 86.8421052631579, 84.21052631578947, 86.48648648648648, 80.0, 86.48648648648648, 86.11111111111111, 86.48648648648648, 97.43589743589743, 81.57894736842105, 86.8421052631579, 75.0, 81.08108108108108, 86.8421052631579, 69.04761904761905, 94.73684210526315, 73.17073170731707, 80.0, 86.48648648648648, 82.05128205128204, 82.05128205128204, 71.7948717948718, 78.94736842105263, 86.8421052631579, 91.8918918918919, 78.37837837837837, 89.1891891891892, 89.74358974358975, 87.17948717948718, 81.57894736842105, 83.78378378378379, 86.8421052631579, 69.76744186046511, 82.05128205128204, 97.36842105263158, 82.92682926829268, 84.61538461538461, 94.73684210526315, 92.3076923076923, 89.47368421052632, 87.17948717948718, 83.78378378378379, 84.21052631578947, 86.11111111111111, 79.48717948717949, 84.21052631578947, 76.19047619047619, 76.31578947368422, 77.5, 80.0, 89.74358974358975, 94.73684210526315, 94.5945945945946, 87.17948717948718, 82.05128205128204, 79.48717948717949, 94.73684210526315, 79.48717948717949, 78.37837837837837, 84.21052631578947, 94.87179487179486, 86.48648648648648, 79.48717948717949, 86.8421052631579, 74.35897435897436, 82.05128205128204, 74.35897435897436, 87.17948717948718, 79.48717948717949, 87.17948717948718, 86.8421052631579, 72.97297297297297, 75.67567567567568, 87.5, 84.61538461538461, 84.21052631578947, 89.47368421052632, 73.17073170731707, 76.31578947368422, 74.35897435897436, 84.21052631578947, 70.73170731707317, 97.36842105263158, 89.74358974358975, 65.9090909090909, 89.47368421052632, 86.8421052631579, 89.47368421052632, 78.94736842105263, 72.5, 86.8421052631579, 72.09302325581395, 77.5, 78.04878048780488, 94.5945945945946, 81.3953488372093, 86.48648648648648, 73.17073170731707, 84.61538461538461, 76.92307692307693, 76.92307692307693, 80.95238095238095, 75.0, 97.2972972972973, 68.29268292682927, 68.42105263157895, 86.8421052631579, 89.47368421052632, 76.92307692307693, 61.904761904761905, 87.17948717948718, 84.61538461538461, 89.74358974358975, 84.21052631578947, 75.0, 84.61538461538461, 87.5, 87.5, 94.73684210526315, 87.17948717948718, 78.37837837837837, 75.60975609756098, 92.10526315789474, 87.17948717948718, 92.3076923076923, 80.95238095238095, 71.7948717948718, 65.9090909090909, 89.1891891891892, 89.47368421052632, 80.48780487804879, 78.04878048780488, 89.1891891891892, 74.35897435897436, 75.0, 89.47368421052632, 89.47368421052632, 57.77777777777777, 70.73170731707317, 86.48648648648648, 92.10526315789474, 86.48648648648648, 80.0, 92.10526315789474, 86.48648648648648, 80.0, 78.04878048780488, 89.47368421052632, 82.05128205128204, 82.5, 81.57894736842105, 86.8421052631579, 71.42857142857143, 82.05128205128204, 81.08108108108108, 76.74418604651163, 94.5945945945946, 76.19047619047619]


font = {'family' : 'sans-serif',
        'size'   : 16}
matplotlib.rc('font', **font)



for i in range(355):
   x.append(i+1)


for i in range(392):
    y.append(i+1)
# Profit

## Old_code
margin_error1 =[]
lost_r_old_2 =[]




#plt.bar(range(len(lost_r_old)), lost_r_old)


plt.errorbar(x,lost_r_old,fmt="-", color="grey",ecolor="lightgray",capsize=2, label= "Old")
plt.errorbar(y,lost_r,fmt="-", color="red",ecolor="lightgray",capsize=2,label= "New")



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




