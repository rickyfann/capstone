import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

def findfont():
    for i in (fm.findSystemFonts(fontpaths=None, fontext='ttf')):
        if r"Amasis MT Std Black.otf" in i:
            return rf"{i}"
        
x_vals = np.arange(-25,25)

y = lambda x: x**2

y_vals = y(x_vals)

fig, ax = plt.subplots(1, 2, figsize=[10,7])

ax[0].plot(x_vals, y_vals)
ax[0].set_title("test title",)

# with ax[0]:
#     plt.plot(x_vals, y_vals)
#     plt.title("test", font="Handwriting")