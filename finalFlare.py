import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats

############## IMPORT DATA FROM GOES-15 SATELITTE ###########################

solar_data = pd.read_csv('2012,07,05.csv') # Import data using pandas library

plt.plot(solar_data.iloc[:,0], solar_data.iloc[:,1]) # Plot the solar data
plt.title("Solar Flare")
plt.ylabel("Power (W/m^2)")
plt.xlabel("Time (s)")
plt.show()

############### CALCULATE ENERGY PER SECOND ################################

# Calculate power in ergs/s
w2erg = 10**7 # Conversion factors from watts to ergs per second
int_m2 = 4*np.pi*(1.496*10**11)**2 # area to integrate over
solar_data['longwave (W/m^2)'] = solar_data['longwave (W/m^2)']*w2erg*int_m2
# Rename dataframe
solar_data = solar_data.rename(columns={'longwave (W/m^2)': 'longwave (ergs/s)'})
# Convert miliseconds to seconds
solar_data["time (milliseconds since 1970-01-01)"] = solar_data["time (milliseconds since 1970-01-01)"]/1000
# Rename dataframe
solar_data = solar_data.rename(columns={'time (milliseconds since 1970-01-01)': "time (s)"})
# Calculate elasped time from first data point
solar_data.iloc[:,0] = solar_data.iloc[:,0]-solar_data.iloc[0,0]

################## ENERGY PER SECOND FLARE GRAPH ############################

plt.plot(solar_data.iloc[:,0], solar_data.iloc[:,1]) # Plot the solar data
plt.title("Solar Flare")
plt.ylabel("Power (ergs/s)")
plt.xlabel("Time (s)")
plt.show()


########################### BASELINE CORRECTION ##############################
import scipy.integrate as integrate

plt.plot(solar_data.iloc[:,1]) #Plot the flare with an indexed time
plt.title("Solar Flare Index") #instead of seconds
plt.ylabel("Power")
plt.xlabel("Time Index")
plt.show()

plt.plot(solar_data.iloc[20:75,1]) #Zoom in on an area used to determine
plt.title("Pre Flare") #the average baseline
plt.ylabel("Power")
plt.xlabel("Time Index")

avg_baseline = solar_data.iloc[20:75,1].mean() #calculuate the avg. baseline
x_coordinates = [20, 75] #adding the average baseline to the graph
y_coordinates = [avg_baseline, avg_baseline]

plt.plot(x_coordinates, y_coordinates, 'r--')
plt.show()

plt.plot(solar_data.iloc[0:300,1]) #overlaying the baseline on top of the
plt.title("Solar Flare Index with Avg. Baseline") #graph of the whole flare
plt.ylabel("Power (ergs/s)")
plt.xlabel("Time Index")
x_coordinates = [0, 300]
y_coordinates = [avg_baseline, avg_baseline]
plt.plot(x_coordinates, y_coordinates, 'r--')
plt.show()

#removing the average baseline from the solar data aka, baseline correction
solar_data_blremov = solar_data['longwave (ergs/s)'].subtract(avg_baseline)
plt.plot(solar_data_blremov[100:175]) #graphing corrected solar flare data
plt.title("Dynamit Flare with Baseline Removed")
plt.ylabel("Power (ergs/s)")
plt.xlabel("Time Indexed")
plt.show()

print("Average baseline is",avg_baseline, ".") #numerical value for baseline


############## COMPUTE TOTAL ENERGY ########################################

#integrating the flare with the baseline correction, using trapezoidal method to find
#total power
A_wblc = integrate.trapz(solar_data_blremov.iloc[124:145], solar_data.iloc[124:145,0])
print('\n Total area under the curve with baseline correction: ', A_wblc, ' ergs')

#integrating the flare without the baseline correction, using trapezoidal method to find
#total power
A_woblc = integrate.trapz(solar_data.iloc[124:145,1], solar_data.iloc[124:145,0])
print('\n Total area under the curve without baseline correction: ', A_woblc, ' ergs')

#finding the percent difference between the area with and without baseline correction
pd1 = ((A_woblc - A_wblc)/A_woblc)*100
print('\n The percent difference in energy calculated \n when doing a baseline correctionusing the \n "subtract the average" method comparing do not doing a \n baseline correction at all: ', pd1, '%')