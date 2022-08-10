import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

############ IMPORT DATA ########################

class_data = pd.read_csv('Class_Data.csv') # Import data using pandas library


############ CLEAN DATA PLOTTING #####################

plt.plot(class_data["Peak Irr"], class_data["Tot Eng"], '.')
#plotting the data set, peak irradiance vs total energy
plt.xlabel("Peak Irr") #Labeling and scaling the axes (on a log scale)
plt.ylabel("Tot Eng")
plt.xscale("log")
plt.yscale("log")
plt.title("Class Data on Log Scale")
plt.show()

############# DEFINE VARIABLES #######################

## The slope of the expression from last week relating the Peak Irradiance to
## the flare frequency
PI2F_slope = -2.2602908249559817
## The intercept of the expression from last week relating the Peak Irradiance
## to the flare frequency
PI2F_intercept = -9.027271325132089

## Calculate the flare frequency using the expression from last week
freq = np.exp(PI2F_slope*np.log(class_data.iloc[:,0]) + PI2F_intercept)

## Flare Frequency 
IEslope = 0.87425779
IEintercept = -68.43255879
derivs = ((np.exp(IEintercept)*IEslope)*class_data.iloc[:,1]**(IEslope-1))
#Apply the conversion
freq = freq*derivs

################ PLOTTING KEY GRAPHS ###############

plt.plot(class_data["Tot Eng"], freq, '.') #plotting total energy against frequency
# data plotted linearly
plt.xlabel("Total Energy") #frequency determined above with last week's data
plt.ylabel("Frequency")
plt.title("Flare Frequency and Total Energy on Linear Scale")
plt.show()

#plotting total energy against frequency
plt.plot(class_data["Tot Eng"], freq, '.')
plt.xlabel("Total Energy")
plt.ylabel("Frequency")
plt.xscale("log") #plotted on a log scale
plt.yscale("log")
plt.title("Flare Frequency and Total Energy on Log Scale")
plt.show()

################ FINDING VALUES BASED OF GRAPHS ##################
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(class_data.iloc[:,1]), np.log(freq))
# Calculate the best fit line based on the output of the linregress function
best_fit_line = np.exp((slope*np.log(class_data.iloc[:,1]))+intercept)

plt.plot(class_data["Tot Eng"], freq, '.') #plotting total energy against frequence
plt.xlabel("Total Energy")
plt.ylabel("Frequency")
plt.xscale("log") #plotting on a log scale
plt.yscale("log")
plt.title("Flare Frequency and Total Energy on Log Scale")
plt.plot(class_data["Tot Eng"], best_fit_line) #plottng best fit line

plt.legend(['Class data', 'alpha =-1.766600591755681']) #create legend for plot
plt.show()