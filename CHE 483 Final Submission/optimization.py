import numpy as np
from scipy.optimize import fmin

m_dot = 30.945 
heat_capacity = 2.219

f = lambda t,: 0.95 - (1.6522190073960615e-05 * t)
q = lambda t: 1.0228404255319148 * t + 2500

def costing_comparison(q_array, cleanings, energy_rate):
    # total operation days * cost of operation per day + downtime days * loss per downtime day
    return (3650 - 5 * cleanings) * (np.average(q_array) * 24 * energy_rate / 100) + 5 * cleanings * 200000 + 900000/6 *cleanings
    # return (3650 - 5 * cleanings) * cost(np.average(q_array)) + 5 * cleanings * 200000 + 900000 * cleanings

def func(par, days=3650, energy_rate=18.2):
    f_threshold, q_threshold = par
    x_vals = np.linspace(0, days, 1000)
    y_vals = f(t = x_vals)
    q_vals = q(t = x_vals)
    check_index = []

    # cleaning modification
    def check(y_values):
        if True in list(y_values < f_threshold):
            ind = list(y_values < f_threshold).index(True)
            check_index.append(ind)
            y_vals[ind:] = f(x_vals[:len(y_vals[ind:])])

            check(y_vals)

        else:
            pass

    check_index2 = []

    def check2(q_values):
        if True in list(q_values > q_threshold):
            ind = list(q_values > q_threshold).index(True)
            check_index2.append(ind)
            q_vals[ind:] = q(x_vals[:len(y_vals[ind:])])

            check2(q_vals)

        else:
            pass

    # running function
    check(y_vals)

    for ind in check_index:
        q_vals[ind:] = q(x_vals[:len(y_vals[ind:])])

    check2(q_vals)

    for ind in check_index2:
        y_vals[ind:] = f(x_vals[:len(y_vals[ind:])])

    return costing_comparison(q_vals, max(len(check_index), len(check_index2)), energy_rate)

print(fmin(func, [0.9, 3650]))