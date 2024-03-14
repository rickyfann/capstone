import numpy as np

def main(x_vals, f_threshold, q_threshold, energy_rate):

    # mathematical functions
    f = lambda t,: 0.95 - (1.6522190073960615e-05 * t)
    q = lambda t: 1.0228404255319148 * t + 2500
    cost = lambda Q: Q * 24 * energy_rate / 100

    # plotting y vals
    y_vals = f(t = x_vals)
    q_vals = q(t = x_vals)

    check_index = []

    # cleaning for resetting values
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
    
    return (y_vals, q_vals, max(len(check_index), len(check_index2)))