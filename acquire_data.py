#allow output from every line
#from IPython.core.interactiveshell import InteractiveShell
#InteractiveShell.ast_node_interactivity = "all"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from urllib.request import urlopen
import time
from scipy.stats import skellam
from scipy.stats import poisson
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl() #default settings for Matplotlib

session = fastf1.get_session(2018, 'Austin', 'Q') #2018 Grand Prix

session.load()
fast_hamlerc = session.laps.pick_driver('HAM').pick_fastest() #Hamilton
fast_hamlerc.get_telemetry().to_csv("data/ham_telemetry.csv")
ham_car_data = fast_hamlerc.get_car_data() #Hamilton Car Data

t = ham_car_data['Time'] #time
vCar = ham_car_data['Speed'] *0.6214 #speed


# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(t, vCar)
ax.set_xlabel('Time')
ax.set_ylabel('Speed (mph)')
ax.set_title('2018 US Grand Prix Lewis Hamilton Pole Lap')
ax.legend()
#plt.show()
plt.savefig('visuals/hamilton_speed.pdf')
ham_car_data.to_csv("data/ham_car_data.csv")



