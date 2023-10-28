import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel(r'Raw Data.xlsx')

t_values = np.array(data.iloc[:,1])
temp1_values = np.array(data.iloc[:,2])
temp2_values = np.array(data.iloc[:,3])

delta = temp2_values-temp1_values

fig,ax = plt.subplots(1,2, figsize=[20,7])

ax[0].plot(t_values, temp1_values, label="Temperature In")
ax[0].plot(t_values, temp1_values, label="Temperature Out")

ax[1].plot(t_values, delta, label="Temperature Difference")

for axis in ax:
    axis.set_title("Temperature vs Time")
    axis.set_ylabel("Temperature (deg C)")
    axis.set_xlabel("Time (h)")
    axis.legend()

ax[1].set_title("Temperature Difference vs Time")

