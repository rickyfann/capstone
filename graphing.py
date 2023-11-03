import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# STEAM OUTLET TEMP APPROX 377.4 F

def grab_year_data(year, raw_data):
    return [raw_data[i] for (i,stamp) in enumerate(stamp_values) if year in stamp]

data = pd.read_excel(r'C:\Users\SticksandStones\OneDrive\Documents\CAPSTONE\Raw Data.xlsx')

# for i, val in enumerate(data.iloc[:,2]):
#     if val>225 or val<150:
#         data.drop(data.index[[i]])

stamp_values = np.array(data.iloc[:,0], dtype=str)
t_values_all = np.array(data.iloc[:,1])
temp1_values_all = np.array(data.iloc[:,2])
temp2_values_all = np.array(data.iloc[:,3])
steam_values_all = np.array(data.iloc[:,6])
corr_values_all = np.array(data.iloc[:,15])

# temp1_values_all = np.array([i for i in temp1_values_all if i<=225 and i>150]).flatten()
# temp2_values_all = np.array([i for i in temp2_values_all if i<=390 and i >=250]).flatten()
# corr_values_all = np.array([i for i in corr_values_all if i<=1 and i>=0.89]).flatten()

delta = temp2_values_all-temp1_values_all

temp1_vals_2018 = grab_year_data('2018', temp1_values_all)
temp1_vals_2019 = grab_year_data('2019', temp1_values_all)
temp1_vals_2020 = grab_year_data('2020', temp1_values_all)
temp1_vals_2021 = grab_year_data('2021', temp1_values_all)
temp1_vals_2022 = grab_year_data('2022', temp1_values_all)
temp1_vals_2023 = grab_year_data('2023', temp1_values_all)

index1 = len(temp1_vals_2018)
index2 = len(temp1_vals_2019)+index1
index3 = len(temp1_vals_2020)+index2
index4 = len(temp1_vals_2021)+index3
index5 = len(temp1_vals_2022)+index4
index6 = len(temp1_vals_2023)+index5

indices = [
    [0,index1],
    [index1,index2],
    [index2,index3],
    [index3,index4],
    [index4,index5],
    [index5,index6],
]

years = [
    2018,
    2019,
    2020,
    2021,
    2022,
    2023
]

fig,ax = plt.subplots(1,3, figsize=[30,7])

ax[0].plot(t_values_all, temp1_values_all, label="Temperature In")
ax[0].plot(t_values_all, temp2_values_all, label="Temperature Out")

ax[1].plot(t_values_all, delta, label="Temperature Difference")

ax[2].plot(t_values_all, corr_values_all, label="Correction Factor")

for axis in ax:
    axis.set_title("Temperature vs Time (2018-2023)")
    axis.set_ylabel("Temperature (deg C)")
    axis.set_xlabel("Time (h)")
    axis.legend()

ax[1].set_title("Temperature Difference vs Time (2018-2023)")

ax[2].set_title("Correction Factor vs Time (2018-2023)")
ax[2].set_ylabel("Correction Factor")

for (i, (ix,year)) in enumerate(zip(indices, years)):
    fig,ax = plt.subplots(1,3, figsize=[30,7])

    ax[0].plot(t_values_all[ix[0]:ix[1]], temp1_values_all[ix[0]:ix[1]], label="T In")
    ax[0].plot(t_values_all[ix[0]:ix[1]], temp2_values_all[ix[0]:ix[1]], label="T Out")
    ax[1].plot(t_values_all[ix[0]:ix[1]], delta[ix[0]:ix[1]], label="T delta")
    ax[2].plot(t_values_all[ix[0]:ix[1]], corr_values_all[ix[0]:ix[1]], label="Correction Factor")

    ax[0].set_title(f"Temperature vs Time ({year})")
    ax[0].set_xlabel("Time(h)")
    ax[0].set_ylabel("Temperature (deg C)")
    ax[0].legend()

    ax[1].set_title(f"Temperature Difference vs Time ({year})")
    ax[1].set_xlabel("Time(h)")
    ax[1].set_ylabel("Temperature (deg C)")

    ax[2].set_title(f"Correction Factor vs Time ({year})")
    ax[2].set_xlabel("Time(h)")
    ax[2].set_ylabel("Correction Factor")