"""This file is to plot two compartments vs. all compartments
of the interneuron model.
"""

# Created by Mohamed ElSayed, and reviewed by Sam Neymotin, Bill Lytton

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from matplotlib import rc  # for font rendering (see below)
import matplotlib.pyplot as plt
import csv

# Load data from fullCurrents
time_full = []
voltage_soma_full = []

with open("fullCurrents_AllComp_data.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        time_full.append(float(row[0]))
        voltage_soma_full.append(float(row[1]))

# Load data from fullCurrents_SomaAndProxDend
time_dend = []
voltage_soma_dend = []
# voltage_dend = []

with open("fullCurrents_TwoComp_Json_data.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        time_dend.append(float(row[0]))
        voltage_soma_dend.append(float(row[1]))
#        voltage_dend.append(float(row[2]))

# Plotting
fig, axes = plt.subplots(1, 1, figsize=(14, 6), sharey=False)

# Subplot: Voltages from both simulations
axes.plot(time_full, voltage_soma_full, label="FullCurrents Soma Voltage",
             color='r')
axes.plot(time_dend, voltage_soma_dend, label="ProxDend Soma Voltage",
             color='g')
# axes.plot(time_dend, voltage_dend, label="ProxDend Dend Voltage", color='r',
#             linestyle="--")
axes.set_title("Voltages from Both Simulations")
axes.set_xlabel("Time (ms)")
axes.set_ylabel("Voltage (mV)")
axes.legend()

# Zoom on vertical and horizontal axes
axes.set_xlim(1500, 1750)
axes.set_ylim(-80, 60)

plt.tight_layout()
plt.show()
