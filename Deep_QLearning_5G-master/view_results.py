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


profit_r2c = [0.9670545777874494, 0.9656693015542346, 0.9652767646075043, 0.9643337584382928, 0.9655000752889347, 0.9651069760855349, 0.9679990484233417, 0.9650431775900629, 0.962547786823705, 0.9649256964728553, 0.9664619225897014, 0.9614448409422837, 0.9647054637503623, 0.9614643942658727, 0.9652493585004701, 0.9663322549923798, 0.9645009669603161, 0.9652554675609535, 0.9690562654459377, 0.9666478327530589, 0.9660274258699586, 0.9636480415068867, 0.9629264520509467, 0.9685691178508175, 0.9672473825486486, 0.9663834969559881, 0.9655800908553981, 0.9649585435498176, 0.9642644181441529, 0.9648599792093011, 0.9616887703591996, 0.9642483085735399, 0.962684090190126, 0.9642386173076529, 0.9635474866462019, 0.9655852779308933, 0.9632989780258756, 0.9639658449047689, 0.967184927270077, 0.9653224209725869, 0.9643919801391042, 0.968084968055228, 0.9669831632899517, 0.9663645933762177, 0.964140110071542, 0.9673158556842637, 0.9681537676235463, 0.967050698877076, 0.9670614112758364, 0.9681987688839852, 0.9659663596428519, 0.9655369491031222, 0.9650115614809973, 0.9636645914171276, 0.9670387357933199, 0.96583474953784, 0.9646528719547952, 0.9683176470236078, 0.9664579867541611, 0.9645376183962149]
               


acceptance_ratio = [81.2603648424544, 82.27272727272728, 84.56591639871382, 84.02777777777779, 81.71521035598705, 87.2852233676976, 84.87394957983193, 88.50174216027874, 84.7972972972973, 84.06040268456377, 88.63636363636364, 84.58781362007169, 83.96825396825398, 82.2866344605475, 83.86581469648561, 86.15384615384616, 87.39352640545145, 82.4476650563607, 85.88850174216029, 84.60207612456747, 83.5820895522388, 79.45859872611464, 82.62987012987013, 81.77257525083613, 86.67820069204151, 80.78817733990148, 82.84734133790738, 83.38815789473685, 79.90580847723704, 82.5, 84.7246891651865, 86.08247422680412, 85.431654676259, 84.27152317880795, 82.8150572831424, 79.76391231028668, 77.74030354131534, 81.76197836166924, 79.93254637436762, 79.64458804523424, 79.93630573248409, 75.67567567567568, 80.95238095238095, 81.46788990825688, 78.13021702838063, 79.53795379537954, 79.734219269103, 80.33898305084746, 75.49342105263158, 79.75352112676056, 74.87603305785125, 71.58385093167702, 79.04085257548846, 76.8, 75.76271186440678, 78.34179357021996, 74.63651050080774, 77.00348432055749, 70.78464106844741, 74.39862542955326]




profit_reability =  [0.9316673570238565, 0.9358105871106246, 0.9358304659548281, 0.9366693167455651, 0.937489736626795, 0.9359199250907858, 0.9368926795749647, 0.9367259126775553, 0.9386664409671805, 0.938301768195108, 0.9385009999140049, 0.9387932067037097, 0.9377554855840975, 0.9390038225038894, 0.9383381076176776, 0.9374696564874314, 0.9371669432345308, 0.9377503230110419, 0.9363902284116898, 0.937656591868814, 0.9381974835242428, 0.9368041260045104, 0.9377727461003099, 0.9379559869793199, 0.9378497450596468, 0.9382545738166035, 0.9374457159328108, 0.9383952602458094, 0.938538682574968, 0.9381705699173669, 0.9398623736278658, 0.9391664648639745, 0.9369851414241955, 0.9391718194895086, 0.9374385029592194, 0.9403555143899691, 0.9372673274742116, 0.9379312399647436, 0.9379024450295528, 0.9392890912257349, 0.9391330942392695, 0.9395347380569524, 0.9382908378835544, 0.9373867572888475, 0.9375734507306837, 0.9393125399043518, 0.9363531585029103, 0.9376268249034522, 0.9379396371697658, 0.9371673975264875, 0.9374116205031033, 0.937071226315196, 0.9390582623037612, 0.9386450312007919, 0.9360844198612844, 0.93848027180193, 0.9365011949731457, 0.9385270765677017, 0.9365914725537882, 0.9382053782804453]
                              
lost_r=   [109, 80, 49, 64, 58, 46, 60, 45, 61, 61, 39, 50, 51, 53, 57, 40, 38, 52, 47, 45, 64, 53, 50, 47, 37, 61, 72, 51, 50, 47, 38, 47, 44, 46, 55, 38, 71, 49, 46, 53, 53, 42, 49, 52, 60, 39, 74, 46, 64, 67, 47, 68, 49, 41, 70, 44, 62, 51, 73, 71]
                 
                  


font = {'family' : 'sans-serif',
        'size'   : 16}
matplotlib.rc('font', **font)



for i in range(60):
    x.append(i+1)

# Profit
#plt.axvline(x=12, color = "silver", linestyle='--')
#plt.errorbar(x,acceptance_ratio, fmt="-",label="SARA",ecolor="lightgray",capsize=2)
#plt.errorbar(x,profit_reability,fmt="-",label="NR", color="red", ecolor="lightgray",capsize=2)
#plt.errorbar(x,lost_r,fmt="-",label="AAR", color="gray",ecolor="lightgray",capsize=2)

plt.errorbar(x,profit_r2c,fmt="-",label="AAR", color="blue",ecolor="lightgray",capsize=2)
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
