import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# STEAM OUTLET TEMP APPROX 377.4 F

def grab_year_indices(year, stamps):
    start_index = 0
    final_index = 0
    for i,stamp in enumerate(stamps):
        if year in stamp:
            if final_index==0:
                start_index=i

            final_index = i
    
    return(start_index, final_index)

# data = pd.read_excel(r'C:\Users\SticksandStones\OneDrive\Documents\CAPSTONE\Raw Data.xlsx')
data = pd.read_excel(r'Raw Data.xlsx')

stamp_values = np.array(data.iloc[:,0], dtype=str)
time_values_all = np.array(data.iloc[:,1])
temp1_values_all = np.array(data.iloc[:,2])
temp2_values_all = np.array(data.iloc[:,3])
steam_values_all = np.array(data.iloc[:,6])
corr_values_all = np.array(data.iloc[:,15])

d = dict({
    'Stamp': stamp_values,
    'Time': time_values_all,
    'Temperature 1': temp1_values_all,
    'Temperature 2': temp2_values_all,
    'Delta': temp2_values_all-temp1_values_all,
    'Steam Values': steam_values_all,
    'Correction Factor': corr_values_all,
})

collection = pd.DataFrame(data=d)
# frame = pd.DataFrame(data=d)

frame = []

# df.where, df.drop, df.diff

for i, (val1, val2, val3) in enumerate(zip(collection['Temperature 1'], collection['Temperature 2'], collection['Delta'])):
    if 160<=val1<=215 and 270<=val2<=380 and 90<=val3<=160:
    # if True:
        frame.append(collection.iloc[i,:])

frame = pd.DataFrame(frame)

indices = [
    grab_year_indices('2018', frame['Stamp']),
    grab_year_indices('2019', frame['Stamp']),
    grab_year_indices('2020', frame['Stamp']),
    grab_year_indices('2021', frame['Stamp']),
    grab_year_indices('2022', frame['Stamp']),
    grab_year_indices('2023', frame['Stamp']),
]

years = [
    2018,
    2019,
    2020,
    2021,
    2022,
    2023
]

# fig, ax = plt.subplots(1, figsize=[10,7])

fig,ax = plt.subplots(2,1, figsize=[10,15])

time = np.array(frame['Time'])
T1 = np.array(frame['Temperature 1'])
T2 = np.array(frame['Temperature 2'])
de = np.array(frame['Delta'])
f = np.array(frame['Correction Factor'])

# # creating trendline and associated function
z1 = np.polyfit(time, T2, 1)
p1 = np.poly1d(z1)

z2 = np.polyfit(time, de, 1)
p2 = np.poly1d(z2)

# ax.plot(time, T1, '.', label="Temperature In")
# ax.plot(time, T2, '.', label="Temperature Out")
# ax.plot(time, p1(time), label="Trendline")
# ax.set_title("Temperature vs Time (2018-2023)")
# ax.set_ylabel("Temperature (deg C)")
# ax.set_xlabel("Time (h)")
# ax.legend()

ax[0].plot(time, T1, '.', label="Temperature In")
ax[0].plot(time, T2, '.', label="Temperature Out")
ax[0].plot(time, p1(time), label="Trendline")

# ax[1].plot(time, de, '.', label="Temperature Difference")
# ax[1].plot(time, p2(time), label="Trendline")
# ax[1].set_ylim([0,160])

ax[1].plot(time, f, '.', label="Correction Factor")

for axis in ax:
    axis.set_title("Temperature vs Time (2018-2023)")
    axis.set_ylabel("Temperature (deg C)")
    axis.set_xlabel("Time (h)")
    axis.legend()

# ax[1].set_title("Temperature Difference vs Time (2018-2023)")

ax[1].set_title("Correction Factor vs Time (2018-2023)")
ax[1].set_ylabel("Correction Factor")

# for (i, (ix,year)) in enumerate(zip(indices, years)):
#     fig,ax = plt.subplots(1,3, figsize=[30,7])

#     z1 = np.polyfit(time[ix[0]:ix[1]], T2[ix[0]:ix[1]], 1)
#     p1 = np.poly1d(z1)

#     z2 = np.polyfit(time[ix[0]:ix[1]], de[ix[0]:ix[1]], 1)
#     p2 = np.poly1d(z2)

#     ax[0].plot(time[ix[0]:ix[1]], T1[ix[0]:ix[1]], '.',label="T In")
#     ax[0].plot(time[ix[0]:ix[1]], T2[ix[0]:ix[1]], '.',label="T Out")
#     ax[1].plot(time[ix[0]:ix[1]], de[ix[0]:ix[1]], '.',label="T delta")
#     ax[2].plot(time[ix[0]:ix[1]], f[ix[0]:ix[1]], '.',label="Correction Factor")
#     ax[0].plot(time[ix[0]:ix[1]], p1(time[ix[0]:ix[1]]), label="Trendline")
#     ax[1].plot(time[ix[0]:ix[1]], p2(time[ix[0]:ix[1]]), label="Trendline")

#     ax[0].set_title(f"Temperature vs Time ({year})")
#     ax[0].set_xlabel("Time(h)")
#     ax[0].set_ylabel("Temperature (deg C)")
#     ax[0].legend()

#     ax[1].set_title(f"Temperature Difference vs Time ({year})")
#     ax[1].set_xlabel("Time(h)")
#     ax[1].set_ylabel("Temperature (deg C)")
#     ax[1].set_ylim([0,160])

#     ax[2].set_title(f"Correction Factor vs Time ({year})")
#     ax[2].set_xlabel("Time(h)")
#     ax[2].set_ylabel("Correction Factor")

# diffs = frame['Delta'].diff()
# diffs = diffs.where(diffs<20)
# diffs = diffs.where(diffs>-20)

# plt.figure()
# plt.plot(time, np.array(diffs))