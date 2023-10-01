import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
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
from pygam import LinearGAM, s, f
import fastf1 as ff1
from pygam import LinearGAM, s, f
#fastf1.Cache.clear_cache()
fastf1.plotting.setup_mpl() #default settings for Matplotlib
colormap = mpl.cm.plasma

ham_car_data = pd.read_csv("data/ham_car_data_delta.csv")



# Get telemetry data
x = ham_car_data['X']          # values for x-axis
y = ham_car_data['Y']            # values for y-axis
color = ham_car_data['Delta']      # value to base color gradient on

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# We create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle("2018 US Grand Prix Lewis Hamilton Pole Lap\nIndyCar Time Difference (sec)", size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')


# After this, we plot the data itself.
# Create background track line
ax.plot(ham_car_data['X'], ham_car_data['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

# Create a continuous norm to map from data points to colors
norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

# Set the values used for colormapping
lc.set_array(color)

# Merge all line segments together
line = ax.add_collection(lc)


# Finally, we create a color bar as a legend.
cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")


# Show the plot
#plt.show()
plt.savefig('visuals/delta_time.pdf')

# Get telemetry data
x = ham_car_data['X']          # values for x-axis
y = ham_car_data['Y']            # values for y-axis
color = ham_car_data['SpeedDelta'] *0.6214     # value to base color gradient on. convert to mph

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# We create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle("2018 US Grand Prix Hamilton (F1) Pole Lap\nRosenqvist (IndyCar) 2019 Speed Difference (mph)", size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')


# After this, we plot the data itself.
# Create background track line
ax.plot(ham_car_data['X'], ham_car_data['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

# Create a continuous norm to map from data points to colors
norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

# Set the values used for colormapping
lc.set_array(color)

# Merge all line segments together
line = ax.add_collection(lc)


# Finally, we create a color bar as a legend.
cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")


# Show the plot
#plt.show()
plt.savefig('visuals/delta_speed.pdf')


# Get telemetry data
x = ham_car_data['X']          # values for x-axis
y = ham_car_data['Y']            # values for y-axis
color = (ham_car_data['SpeedDelta']/ham_car_data['IndySpeed'])*100

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# We create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle("2018 US Grand Prix Hamilton (F1) Pole Lap \n Speed Difference Percentage over Rosenqvist (IndyCar) 2019 Speed", size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')


# After this, we plot the data itself.
# Create background track line
ax.plot(ham_car_data['X'], ham_car_data['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

# Create a continuous norm to map from data points to colors
norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

# Set the values used for colormapping
lc.set_array(color)

# Merge all line segments together
line = ax.add_collection(lc)


# Finally, we create a color bar as a legend.
cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")
legend.set_label('Speed Difference Percentage')

# Show the plot
#plt.show()
plt.savefig('visuals/delta_speed_diff_percentage.pdf')


# Get telemetry data
x = ham_car_data['X']          # values for x-axis
y = ham_car_data['Y']            # values for y-axis
color = (ham_car_data['Speed']/ham_car_data['IndySpeed'])*100

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# We create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle("2018 US Grand Prix Hamilton (F1) Pole Lap \n Speed Percentage over Rosenqvist (IndyCar) 2019 Speed", size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')


# After this, we plot the data itself.
# Create background track line
ax.plot(ham_car_data['X'], ham_car_data['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

# Create a continuous norm to map from data points to colors
norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

# Set the values used for colormapping
lc.set_array(color)

# Merge all line segments together
line = ax.add_collection(lc)


# Finally, we create a color bar as a legend.
cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")
legend.set_label('Percentage of Speed')

# Show the plot
#plt.show()
plt.savefig('visuals/delta_speed_percentage.pdf')