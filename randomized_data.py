import numpy as np
import pandas as pd

utility_temp_mid = np.mean([390, 450])
process_temp_mid = np.mean([180, 200])
flow_mid = np.mean([130000, 245600])

util_temp = [390, 450]
process_temp = [180,200]
flow = [130000, 245600]

# datum = np.array([utility_temp_mid, process_temp_mid, flow_mid])

# print(utility_temp_mid, process_temp_mid, flow_mid)

frames = []

for i, a in enumerate(util_temp):
    for j, b in enumerate(process_temp):
        for k, c in enumerate(flow):
            for _ in range(3):
                datum = np.array([a,b,c])
                treatment = ''
                code = ''

                if i==0:
                    treatment+="low, "
                    code+="-1"
                
                else:
                    treatment+="high, "
                    code+="+1"
                
                if j==0:
                    treatment+="low, "
                    code+="-1"
                
                else:
                    treatment+="high, "
                    code+="+1"
                
                if k==0:
                    treatment+="low"
                    code+="-1"
                
                else:
                    treatment+="high"       
                    code+="+1"

                random_vals = np.random.randint(-5, 5, [1,3]) / 100

                d = (datum + datum*random_vals).flatten()

                d = {
                    "Treatment" : treatment,
                    "Utility Temperature" : d[0],
                    "Process Temperature" : d[1],
                    "Flowrate" : d[2],
                }

                frames.append(d)
        # print(datum + datum*random_vals)

col = pd.DataFrame(frames)
print(col)