import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot
import datetime

data = pd.read_excel(r'Raw Data.xlsx')

stamp_values = np.array(data.iloc[:,0])
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

for i, (val1, val2, val3) in enumerate(zip(collection['Temperature 1'], 
                                           collection['Temperature 2'], 
                                           collection['Delta'])):
    
    if 160<=val1<=215 and 270<=val2<=380 and 90<=val3<=160:
        frame.append(collection.iloc[i,:])

frame = pd.DataFrame(frame)

a = pd.DataFrame(
    {
    'ds': frame.iloc[:,0],
    'y': frame.iloc[:,6]
    }
    )

#m = Prophet()
m = Prophet(changepoint_prior_scale=0.005, changepoint_range = 1)
m.fit(a)

future = m.make_future_dataframe(periods=365)
future.tail()

forecast = m.predict(future)

fig1 = m.plot(forecast)
a = add_changepoints_to_plot(fig1.gca(), m, forecast)

for x in m.changepoints:
    print(x)
