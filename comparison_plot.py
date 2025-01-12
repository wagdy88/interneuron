""" This file is to plot each of the sheets in comparison to the 
fullCurrents.py file
"""

# Created by Mohamed ElSayed, and reviewed by Sam Neymotin, Bill Lytton


import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib import rc  # for font rendering (see below)
import pandas as pd
import os

# Define output directory
output_dir_full_sim = "full_comparison_plots"
output_dir_zoomed_in = "zoomed_in_plots"
os.makedirs(output_dir_full_sim, exist_ok=True)  # Create the directory if it doesn't exist
os.makedirs(output_dir_zoomed_in, exist_ok=True)

# Load fullCurrents.py data
full_currents_data = pd.read_csv("fullCurrents_AllComp_data.csv")
time_full = full_currents_data["Time (ms)"]
voltage_full = full_currents_data["Soma Voltage (mV)"]

# Read the Excel file
excel_file = "grid_search_results.xlsx"
sheets = pd.ExcelFile(excel_file).sheet_names

# Plot full simulation comparison data from each sheet
for sheet in sheets:
    data = pd.read_excel(excel_file, sheet_name=sheet)
    time_grid = data["Time (ms)"]
    voltage_grid = data["Voltage (mV)"]

    # Plot comparison
    plt.figure(figsize=(10, 6))
    plt.plot(time_full, voltage_full, label="fullCurrents.py", color="red")
    plt.plot(time_grid, voltage_grid, label=sheet, color="blue")
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (mV)")
    plt.title(f"Comparison of {sheet} with fullCurrents.py")
    plt.legend()
    plt.grid()
    # Save figure with unique name
    plt.savefig(os.path.join(output_dir_full_sim, "Comparison_{sheet}.png"))
    plt.close()

# Plot zoomed in simulation comparison from each sheet
for sheet in sheets:
    data = pd.read_excel(excel_file, sheet_name=sheet)
    time_grid = data["Time (ms)"]
    voltage_grid = data["Voltage (mV)"]

    # Plot comparison
    plt.figure(figsize=(10, 6))
    plt.plot(time_full, voltage_full, label="fullCurrents.py", color="red")
    plt.plot(time_grid, voltage_grid, label=sheet, color="blue")
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (mV)")
    # Zoom on vertical and horizontal axes
    plt.xlim(1500, 1750)
    plt.ylim(-80, 60)
    plt.title("Voltage Trace Zoomed 1500 - 1750 ms)")
    plt.legend()
    plt.grid()
    # Save figure with unique name
    plt.savefig(os.path.join(output_dir_zoomed_in, "Zoomed_Comparison_{sheet}.png"))
    plt.close()


print("Comparison plots saved.")