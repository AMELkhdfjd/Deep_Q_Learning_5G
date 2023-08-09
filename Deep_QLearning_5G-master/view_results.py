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
y = []
topologies = ["16BA","abilene"]

########### arrivalRate20 ############
arrival_rate = "20"



lost_r= [0.9635943347955631, 0.9639364955522162, 0.9583541990839156, 0.9630484665073595, 0.9665691099986501, 0.9634258210432834, 0.962947138627546, 0.9605807795436274, 0.9611619145500798, 0.964606163801482, 0.9629174908484893, 0.9641324454441789, 0.9631590996190776, 0.9625207824675401, 0.9652480249351258, 0.9626642604372606, 0.963296352650276, 0.9599739008366549, 0.9633715084109875, 0.9646056163625255, 0.9597369555284312, 0.9615778940798636, 0.9647218154443615, 0.9586525477351066, 0.9623772224014493, 0.9604195392690866, 0.9626235636256154, 0.9615493793703629, 0.963236199590829, 0.9609612566337582, 0.9625144703607895, 0.9648661852759469, 0.9649295399058254, 0.9605831228793025, 0.9620333000375806, 0.9612109938301611, 0.961915958675205, 0.9638390378837647, 0.9615252628821289, 0.9613409480734132, 0.9635345085009537, 0.9648615987576117, 0.9669946759140423, 0.962361954030914, 0.9662416037199812, 0.9579446064646129, 0.9664775312237356, 0.9649288772555198, 0.9627855792030059, 0.9645618626041254, 0.9644776631532832, 0.9659792858920428, 0.9602225541512417, 0.9642586952595583, 0.9610125019911014, 0.961488361798634, 0.9651547060970243, 0.9642970634481541, 0.9612981547314182, 0.960908632550447, 0.96213809951236, 0.9631768952695328, 0.9632300195991146, 0.9655341620561962, 0.9603049575542754, 0.962540345208385, 0.9660251050722866, 0.9636586185527558, 0.961895351267172, 0.9610892424347108, 0.9589419859486678, 0.9604280565317032, 0.9591661029346101, 0.9627577617279908, 0.9606973187393466, 0.9658829749180513, 0.96417301874081, 0.9633281137899083, 0.9599504210476403, 0.9647126454884625, 0.9676721752174745, 0.9621040122937993, 0.9645328195142328, 0.9661679849626392, 0.9622282627372718, 0.9620496971061632, 0.9611037950519362, 0.9609483898432447, 0.9624289198330374, 0.9648374692613976, 0.9614502394243402, 0.9618316247821722, 0.961567582691738, 0.9617587988632799, 0.9600278890148578, 0.9648274492295241, 0.9623526644490573, 0.9672046711979926, 0.9607444750433966, 0.9671846727861759]


lost_r_old = [10, 8, 11, 9, 7, 6, 7, 5, 7, 9]




font = {'family' : 'sans-serif',
        'size'   : 16}
matplotlib.rc('font', **font)



for i in range(200):
    x.append(i+1)


for i in range(10):
    y.append(i+1)
# Profit


#plt.errorbar(x,lost_r,fmt="-", color="blue",ecolor="lightgray",capsize=2)
plt.errorbar(y,lost_r_old,fmt="-", color="gray",ecolor="lightgray",capsize=2)



#plt.axvline(x=12, color = "silver", linestyle='--')
#plt.errorbar(x,acceptance_ratio, fmt="-",label="SARA",ecolor="lightgray",capsize=2)
#plt.errorbar(x,profit_reability,fmt="-",label="NR", color="red", ecolor="lightgray",capsize=2)
#plt.errorbar(x,lost_r,fmt="-",label="AAR", color="gray",ecolor="lightgray",capsize=2)

#plt.errorbar(x,profit_r2c,fmt="-",label="AAR", color="blue",ecolor="lightgray",capsize=2)
plt.xlabel('Episodes')
plt.ylabel('Acceptance Ratio')
plt.title(' Acceptance Ratio vs Episodes')
#plt.legend()
plt.legend(fontsize = 14,loc='lower right', fancybox=True, shadow=True)
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1), fancybox=True, shadow=True, ncol=3)
#plt.show() 
plt.savefig("test.png",bbox_inches = 'tight') 
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
