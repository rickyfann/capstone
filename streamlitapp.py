import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

# to run this app, open your cmd and make sure "streamlit is installed"
# then type "streamlit run {PATH TO streamlitapp.py}" into console

# initialization of streamlit app and text
st.set_page_config(layout="wide")
st.title("FoulX Predictor App")
st.write(r"This is the web app tool developed by the CHE Capstone group INSERT NUMBER. The intended use case is to determine the optimal cleaning schedule a for heat exchanger as it degrades in efficiency.")
st.write(r'"a" represents the exponent, or degredation rate of the heat exchanger correction factor.')
st.write(r'"t0" represents the expected time between cleanings.')

# creation of columns to split the page
cols = st.columns([0.2, 0.7])

# initial values, can be tweaked to match prophet predictions
a_initial = 1.5
t0_initial = 200
threshold_initial = 0.65

# user input paramater values
a = cols[0].number_input("Insert parameter 1, a", value = a_initial)
t0 = cols[0].number_input("Insert parameter 2, t0", value = t0_initial)
threshold = cols[0].number_input("Insert parameter 3, threshold", value = threshold_initial, min_value=0.0, max_value=1.0)

# mathematical function, to be changed
f = lambda t0, t, a: 1 - (t / t0) ** a

# plotting x vals
x_vals = np.linspace(0, t0_initial*3, 100)

# plotting y vals
y_vals = f(t0 = t0, t = x_vals, a = a)

# cleaning modification
def check(y_vals):
    if True in list(y_vals<threshold):
        ind = list(y_vals<threshold).index(True)
        y_vals[ind:] = f(t0, x_vals[:len(y_vals[ind:])], a)

        check(y_vals)
    
    else:
        pass

# running function
check(y_vals)

fig, ax = plt.subplots(figsize=[10,7])

# plotting values
ax.set_title("Correction Factor vs Time")
ax.set_xlabel("Time")
ax.set_ylabel("Correction Factor")
ax.plot(x_vals, y_vals, color="#aa0000")
ax.hlines(threshold, xmin = 0, xmax = t0*3, linestyles='dashed')

# plot limits, should be tweaked
ax.set_ylim([0, 1])
ax.set_xlim([0, t0*3])

# pasting image
cols[1].pyplot(fig, use_container_width=True)
