import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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

for (i, (ix,year)) in enumerate(zip(indices, years)):

    z1 = np.polyfit(time[ix[0]:ix[1]], T2[ix[0]:ix[1]], 1)
    p1 = np.poly1d(z1)

    z2 = np.polyfit(time[ix[0]:ix[1]], de[ix[0]:ix[1]], 1)
    p2 = np.poly1d(z2)

    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=(f"Temperature vs Time ({year})", f"Temperature Difference vs Time ({year})", f"Correction Factor vs Time ({year})"))
    fig.add_trace(
        go.Scatter(
            x = time[ix[0]:ix[1]],
            y = T1[ix[0]:ix[1]],
            mode = "markers",
            name = "Temperature In",
            ),
        row=1, col=1,
        )
    
    fig.add_trace(
        go.Scatter(
            x = time[ix[0]:ix[1]],
            y = T2[ix[0]:ix[1]],
            mode="markers",
            name = "Temperature Out",
            ),
        row=1, col=1,
        )
    
    fig.add_trace(
        go.Scatter(
            x = time[ix[0]:ix[1]],
            y = p1(time[ix[0]:ix[1]]),
            name = "Trendline",
            ),
        row=1, col=1,
        )
    
    fig.add_trace(
        go.Scatter(
            x = time[ix[0]:ix[1]],
            y = de[ix[0]:ix[1]],
            mode = "markers",
            name = "Temperature Delta",
            ),
        row=1, col=2,
        )
    
    fig.add_trace(
        go.Scatter(
            x = time[ix[0]:ix[1]],
            y = p2(time[ix[0]:ix[1]]),
            name = "Trendline",
            ),
        row=1, col=2,
        )
    
    fig.add_trace(
        go.Scatter(
            x = time[ix[0]:ix[1]],
            y = f[ix[0]:ix[1]],
            mode = "markers",
            name = "Correction Factor",
            ),
        row=1, col=3,
        )
    
    fig['layout']['xaxis']['title'] = "Time (h)"
    fig['layout']['xaxis2']['title'] = "Time (h)"
    fig['layout']['xaxis3']['title'] = "Time (h)"
    fig['layout']['yaxis']['title'] = "Temperature (C)"
    fig['layout']['yaxis2']['title'] = "Temperature (C)"
    fig['layout']['yaxis3']['title'] = "Correction Factor"
    fig['layout']['yaxis']['range'] = (0, 350)
    fig['layout']['yaxis2']['range'] = (0, 350)

    fig.show()
