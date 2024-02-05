import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot

# reads file
data = pd.read_excel(r'Raw Data.xlsx')

# reads individual columns
stamp_values = np.array(data.iloc[:,0])
time_values_all = np.array(data.iloc[:,1])
temp1_values_all = np.array(data.iloc[:,2])
temp2_values_all = np.array(data.iloc[:,3])
steam_values_all = np.array(data.iloc[:,6])
corr_values_all = np.array(data.iloc[:,15])
heat_duty = np.array(data.iloc[:,17])

# creates dictionary
d = dict({
    'Stamp': stamp_values,
    'Time': time_values_all,
    'Temperature 1': temp1_values_all,
    'Temperature 2': temp2_values_all,
    'Delta': temp2_values_all-temp1_values_all,
    'Steam Values': steam_values_all,
    'Correction Factor': corr_values_all,
    'Heat Duty': heat_duty,
})

# converts to dataframe
collection = pd.DataFrame(data=d)

frame = []

# filters dataframe for invalid data points
for i, (val1, val2, val3, val4, val5) in enumerate(zip(collection['Temperature 1'], 
                                           collection['Temperature 2'], 
                                           collection['Delta'],
                                           collection['Correction Factor'],
                                           collection['Heat Duty']
                                           )
                                           ):
    
    if 160<=val1<=215 and 270<=val2<=380 and 90<=val3<=160 and val4<=1 and val5>0:
        frame.append(collection.iloc[i,:])

# reconverts to dataframe
frame = pd.DataFrame(frame)

# grabs datetime values and 
a = pd.DataFrame(
    {
    'ds': frame.iloc[:,0],
    'y': frame.iloc[:,6]
    }
    )

# creates prophet object with specified changepoint scale and saturation point
# scale manipulates the sparsity of changepoints
# range manipulates the totality of the data being analyzed
# changepoints = [
#     "2022-04-12",
#     "2022-04-22",
#     "2022-05-04",
#     "2022-05-05",
#     "2022-05-20",
#     "2022-06-06",
#     "2022-06-28",
#     "2022-07-29",
#     "2022-08-18",
#     "2022-09-29",
#     "2022-10-14",
#     "2022-12-13",
#     "2023-01-17",
#     "2023-01-24",
#     "2023-01-30",
#     "2023-02-21",
#     "2023-03-14",
#     "2023-03-21",
#     "2023-03-30",
# ]

changepoint_scale = 0.005

m = Prophet(changepoint_prior_scale=changepoint_scale, changepoint_range = 1)
m.fit(a)

# makes prediction into future based on period (days)
future = m.make_future_dataframe(periods=365)

# set cap on prediction value (e.g. 1 for correction factor)
future['cap'] = 1

# grabs the predicted values
forecast = m.predict(future)

# plots the prediction alongside original data points
fig1 = m.plot(forecast, xlabel="Time", ylabel="Correction Factor", include_legend=True, figsize=(10,6))

# plots change points as vertical red lines
b = add_changepoints_to_plot(fig1.gca(), m, forecast)

# graph formatting
plt.title(f"Prophet Prediction - Scale:{changepoint_scale}")
plt.legend()

# plots heat duty on twin axis
fig2, ax = plt.subplots(figsize = [10,6])
ax.plot(frame["Stamp"], frame["Heat Duty"], color='green', label="Heat Duty")
ax.set_title("Heat Duty vs Time")
ax.set_ylabel("Heat Duty (kW)")
ax.set_xlabel("Time")
ax.legend()

# ax2 = plt.twinx()
# ax2.plot(frame["Stamp"], frame["Heat Duty"], color='green', label="Heat Duty")
# ax2.set_ylabel("Heat Duty (kW)")
