import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import prophet
# from prophet import Prophet

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

for i, (val1, val2, val3) in enumerate(zip(collection['Temperature 1'], collection['Temperature 2'], collection['Delta'])):
    if 160<=val1<=215 and 270<=val2<=380 and 90<=val3<=160:
        frame.append(collection.iloc[i,:])

frame = pd.DataFrame(frame)

a = pd.DataFrame(
    {
    'ds': frame.iloc[:,0],
    'y': frame.iloc[:,1]
    }
    )

# m = prophet.
# m.fit(a)

# future = m.make_future_dataframe(periods=365)
# future.tail()

print ("Hi")
