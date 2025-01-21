 # ricky fan

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin
from optimization import func, costing_comparison
from pathlib import Path
import cleaning

# to run this app, open your cmd and make sure "streamlit is installed"
# then type "streamlit run {PATH TO streamlitapp.py}" into console

fonts = {
    "header1": '<p style="font-family:Amasis MT Std; color:white; font-size: 44px; text-align: center;">',
    "body": '<p style="font-family:Aptos Display; color:white; font-size: 25px;">',
    "numbers": '<p style="font-family:Aptos Display; color:white; font-size: 30px;">',
    "header2": '<p style="font-family:Aptos Display; color:white; font-size: 28px; text-align: center;">',
}

def md(font, text):
    st.markdown(fonts[font] + text + "</p>", unsafe_allow_html=True)

# initialization of streamlit app and text
st.set_page_config(layout="wide")

with open(str(Path(__file__).parents[0]) + "\\styles.css") as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

md("header1", "FoulX Predictor App")
md("header2", "Authors: Aliana Andres, Ricky Fan, Curtis Rhodes, Dorothy Wan")
md("body", "This is the web app tool developed by the CHE Capstone group 4. The intended use case is to determine the optimal cleaning schedule for a heat exchanger as it degrades in efficiency.")

# initial values, can be tweaked to match prophet predictions
# baseline operation days is 3650, q threshold 4350
t_initial =int(365 * 10) 
f_threshold_initial = 0.9
q_threshold_initial = 4350.0 #maximum is 9157 for daily operating cost of 16759.65 over 10 years
energy_rate_initial = 18.2
with st.sidebar:
    md("header2", "<strong>Parameter Inputs</strong>")
    # user input parameter values
    t =           st.number_input("Insert parameter 1, **t**, the number of days to be modeled.", value = t_initial, min_value=1)
    f_threshold = st.number_input("Insert parameter 2, **f threshold**, the correction factor.", value = f_threshold_initial, min_value=0.00, max_value=0.950)
    q_threshold = st.number_input("Insert parameter 3, **q threshold**, the higher bound for the heat duty in $kW$.", value = q_threshold_initial, min_value=2600.0)
    energy_rate = st.number_input("Insert parameter 4, **energy rate**, the cost of energy in $cents / kWh$.", value = energy_rate_initial, min_value=1.0, max_value=25.0)

    year_enable = st.checkbox("Years/Days", value=True)

optimal = fmin(func, [0.9, 3650], (t, energy_rate))

# creation of columns to split the page
cols = st.columns(2)

# from prophet prediction, m = -1.6522190073960615e-05, m=-8.897745181041325e-06
# heat duty, m = 1.0228404255319148

# mass flowrate = 30.945 kg/s
# heat capacity = 2.219 kJ / kg C
# 18.2 cents / kWh from 
# https://www.oeb.ca/consumer-information-and-protection/electricity-rates
m_dot = 30.945 
heat_capacity = 2.219

# plotting x vals
x_vals = np.linspace(0, t, 1000)

y_vals, q_vals, cleanings = cleaning.main(x_vals, f_threshold, q_threshold, energy_rate)
y_vals_baseline, q_vals_baseline, cleanings_baseline = cleaning.main(x_vals, 0.9, 4350, energy_rate)
y_vals_optimized, q_vals_optimized, cleanings_optimized = cleaning.main(x_vals, optimal[0], optimal[1], energy_rate)

fig, ax1 = plt.subplots(figsize=[10,7])

# plotting values
ax1.set_title("Performance vs Time")
ax1.set_xlabel("Time (Days)")
ax1.set_ylabel("Performance")
ax1.plot(x_vals, y_vals, color="#63221E")
ax1.hlines(f_threshold, xmin = 0, xmax = t, linestyles='dashed')
ax1.hlines(1.0, xmin = 0, xmax = t, linestyles='dashed')

# plot limits
ax1.set_ylim([f_threshold-0.05, 1.05])
ax1.set_xlim([0, t])

overall_eff = np.average(y_vals)

fig2, ax2 = plt.subplots(figsize=[10,7])
ax2.set_title("Heat Duty vs Time")
ax2.set_xlabel("Time (Days)")
ax2.set_ylabel("Heat Duty (kW)")
ax2.plot(x_vals, q_vals, color="#63221E")
ax2.set_xlim([0, t])

ax2.hlines(q_threshold, xmin = 0, xmax = t, linestyles='dashed')

x_tick_locations = [int(365 * i) for i in range(t//365)]
x_tick_labels = np.arange(0, t//365)

modified = costing_comparison(q_vals, cleanings, energy_rate)
baseline = costing_comparison(q_vals_baseline, cleanings_baseline, energy_rate)
optimized = costing_comparison(q_vals_optimized, cleanings_optimized, energy_rate)

for ax in [ax1, ax2]:
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(22)
        item.set_fontname("Times New Roman")

if year_enable:        
    for axis in (ax1, ax2):
        axis.set_xlabel("Time (Years)")
        axis.set_xticks(x_tick_locations)
        axis.set_xticklabels(x_tick_labels)

with cols[0]:
    st.pyplot(fig, use_container_width=True)
    
with cols[1]:
    st.pyplot(fig2, use_container_width=True)

percent_diff = (baseline - modified)/baseline * 100

cols2 = st.columns([0.5, 0.5])
with cols2[0]:

    md("header2", "<strong>RESULTS SUMMARY</strong>")

    div = st.columns([0.5, 0.5])

    with div[0]:
        with st.container():
            md("body", "💵 BASELINE")
            md("numbers", fr"<strong>${round(baseline, -5):,.0f}</strong>")

        st.divider()
        with st.container():
            md("body", "💵 MODIFIED")
            md("numbers", fr"<strong>${round(modified, -5):,.0f}</strong>")
     
    with div[1]:
        with st.container():
            md("body", "📅 DOWNTIME DAYS")
            md("numbers", fr"<strong>{5 * cleanings}</strong>")

        st.divider()
        with st.container():
            md("body", "PERCENT DIFFERENCE")
            md("numbers", fr"<strong>{percent_diff:.1f} %</strong>")
    
    with st.container():
        with st.expander("**Frequently Asked Questions**"):
            md("body", "Q: What is included in the costs?")
            md("body", "A: The costing function includes the loss as a result of the number of days required for the shutdown, the maintenance cost of $150000 for each cleaning, and the cost of operation for the total number of uptime days.")
            md("body", "Q: Why does the correction factor reset to 0.95 after a cleaning?")
            md("body", "A: A perfect 1.0 is based on a 1-shell pass 1-tube pass heat exchanger with no fouling concerns. The data indicates that 0.95 was approximately the best correction factor for our given exchanger running at the highest flowrates.")
            md("body", "Q: Who are we?")
            md("body", "A: We are four Chemical Engineering students in our final year at the University of Waterloo (but you already knew that).")
            st.image(rf"{str(Path(__file__).parents[0])}\team_photo.png")
            
with cols2[1]:
    md("header2", "<strong>OPTIMIZED PARAMETERS</strong>")

    div = st.columns([0.5, 0.5])

    with div[0]:
        with st.container():
            md("body", "f, CORRECTION FACTOR")
            md("numbers",  fr"<strong>{optimal[0]:.3f}</strong>")

    with div[1]:
        with st.container():
            md("body", "Q, MAXIMUM HEAT DUTY")
            md("numbers",  fr"<strong>{optimal[1]:.2f} kW</strong>")

    st.divider()
    with st.container():
        md("header2", "<strong>SUMMARY</strong>")
        md("body", "From the dataset provided by our industrial partner, Petro Canada, we have built a model to predict the degradation of heat exchanger efficiency.")
        md("body", "The model was built using Meta Prophet, a library for data analysis. From this, several figures can be calculated, such as the baseline costs that would be incurred if the process were to be run at its current state by Petro Canada, as well as the cost for the optimized process.")
