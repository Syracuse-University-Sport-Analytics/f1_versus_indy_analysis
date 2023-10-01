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
import fastf1 as ff1
from pygam import LinearGAM, s, f
fastf1.plotting.setup_mpl() #default settings for Matplotlib


#ham_car_data = pd.read_csv("data/ham_car_data.csv")
ham_car_data = pd.read_csv("data/ham_telemetry.csv")


ham_car_indy = pd.read_csv("data/Indy v. F1 Table.csv")

#convert the ham_car_indy['Time'] from min:sec to seconds
def convert_time(time):
    time = str(time).split(':')
    if len(time) == 2:
        return float(time[0])*60 + float(time[1])
    return float(time[0])

ham_car_indy['Time'] = ham_car_indy['Time'].apply(convert_time)


ham_car_data['Time'] = pd.to_timedelta(ham_car_data['Time']).dt.total_seconds()



#remove any rows with NA values
ham_car_indy = ham_car_indy.dropna()

#create a gam model that predicts Delta based upon Time for the ham_car_indy data
#https://www.statsmodels.org/stable/gam.html
#fit the model
import statsmodels.api as sm
import statsmodels.formula.api as smf



NUMBER_SPLINES = 135
#predict the delta for the ham_car_data data
gam = LinearGAM(s(0), n_splines=NUMBER_SPLINES).fit(ham_car_indy['Time'].to_numpy(), ham_car_indy['Delta'].to_numpy())

#compare the predicted delta to the actual delta
#plot the predicted delta vs. the actual delta
fig = plt.figure(figsize = (8,8))
plt.scatter(ham_car_indy['Time'].to_numpy(), ham_car_indy['Delta'].to_numpy())
            
XX = gam.generate_X_grid(term=0)
pdep, confi = gam.partial_dependence(term=0, X=XX, width=0.95)
            
#plt.plot(XX[:, 0], pdep)
#plt.plot(XX[:, 0], confi, c='r', ls='--')

plt.plot(XX, gam.predict(XX), 'r')
plt.plot(XX, gam.prediction_intervals(XX, width=.95), color='b', ls='--')
plt.title("Delta Prediction vs. Actual")

#plt.show()
plt.savefig('visuals/delta_prediction.pdf')

ham_car_data['Delta'] = gam.predict(ham_car_data['Time'].to_numpy())


#join the two dataframes using a fuzzy match on time


session = ff1.get_session(2021, 'Austin', 'Q') #2018 Grand Prix
weekend = session.event
session.load()
lap = session.laps.pick_driver("HAM").pick_fastest()
#ham_car_data = lap.get_telemetry()
#lap.get_telemetry().to_csv("data/2018_ham_telemetry.csv")

ham_2019_tel = lap.get_telemetry()
ham_2019_tel['Time'] = pd.to_timedelta(ham_2019_tel['Time']).dt.total_seconds()
ham_2019_tel['Time0'] = ham_2019_tel['Time'].shift(1)
ham_2019_tel['TimeDelta'] = ham_2019_tel['Time'] - ham_2019_tel['Time0']
ham_2019_tel['TimeDelta'] = ham_2019_tel['TimeDelta'].fillna(0)
ham_2019_tel['Distance'] = ham_2019_tel['TimeDelta'] * ham_2019_tel['Speed']/60/60
ham_2019_tel['Distance'] = ham_2019_tel['Distance'].cumsum()

ham_car_data['Time0'] = ham_car_data['Time'].shift(1)
ham_car_data['TimeDelta'] = ham_car_data['Time'] - ham_car_data['Time0']
ham_car_data['TimeDelta'] = ham_car_data['TimeDelta'].fillna(0)
ham_car_data['Distance'] = ham_car_data['TimeDelta'] * ham_car_data['Speed']/60/60
ham_car_data['Distance'] = ham_car_data['Distance'].cumsum()



#the 2018 X and Y values have a gap, so using the 2019 distance on track to predict the X and Y values. Everything else is coming directly from the 2018 data
NUMBER_SPLINES = 250
#predict the delta for the ham_car_data data
gam_x = LinearGAM(s(0), n_splines=NUMBER_SPLINES).fit(ham_2019_tel['Distance'].to_numpy(), ham_2019_tel['X'].to_numpy())
ham_car_data['X'] = gam_x.predict(ham_car_data['Distance'].to_numpy())

gam_y = LinearGAM(s(0), n_splines=NUMBER_SPLINES).fit(ham_2019_tel['Distance'].to_numpy(), ham_2019_tel['Y'].to_numpy())
ham_car_data['Y'] = gam_y.predict(ham_car_data['Distance'].to_numpy())

ham_car_data['TimeIndy'] = ham_car_data['Time'] + ham_car_data['Delta']
ham_car_data['TimeIndy0'] = ham_car_data['TimeIndy'].shift(1)
ham_car_data['TimeIndyDelta'] = ham_car_data['TimeIndy'] - ham_car_data['TimeIndy0']
ham_car_data['TimeIndyDelta'] = ham_car_data['TimeIndyDelta'].fillna(0)

ham_car_data['Distance0'] = ham_car_data['Distance'].shift(1)
ham_car_data['DistanceDelta'] = ham_car_data['Distance'] - ham_car_data['Distance0']
ham_car_data['DistanceDelta'] = ham_car_data['DistanceDelta'].fillna(0)

ham_car_data['IndySpeed'] = ham_car_data['DistanceDelta'] / (ham_car_data['TimeIndyDelta'] / 60 / 60)
ham_car_data['SpeedDelta'] = ham_car_data['Speed'] - ham_car_data['IndySpeed']

ham_car_data.to_csv("data/ham_car_data_delta.csv")