""" This file is to plot each of the sheets in comparison to the 
fullCurrents.py file
"""

# Created by Mohamed ElSayed, and reviewed by Sam Neymotin, Bill Lytton


import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib import rc  # for font rendering (see below)
import pandas as pd
import os
import h5py
from mpi4py import MPI


def main():

    # MPI setup
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Define output directory
    output_dir_full_sim = "full_comparison_plots"
    output_dir_zoomed_in = "zoomed_in_plots"
    os.makedirs(output_dir_full_sim, exist_ok=True)  # Create the directory if it doesn't exist
    os.makedirs(output_dir_zoomed_in, exist_ok=True)


    # Load full currents data (only rank 0 initially)
    # if rank == 0:
    #     with h5py.File("simulation_results.h5", "r") as results_file:
    #         full_group = results_file["rank_0"]["combo_0"]  # Assuming full data is stored here
    #         time_full = full_group["time"][:]
    #         voltage_full = full_group["voltage"][:]
    # else:
    #     time_full = None
    #     voltage_full = None
    
    # # Broadcast full currents data to all ranks
    # time_full = comm.bcast(time_full, root=0)
    # voltage_full = comm.bcast(voltage_full, root=0)
   
   # Load full simulation data from HDF5
    # with h5py.File("simulation_results.h5", "r") as results_file:
    #     full_currents_group = results_file["rank_0"]["combo_0"]  # Assuming rank_0, combo_0 has full data
    #     time_full = full_currents_group["time"][:]
    #     voltage_full = full_currents_group["voltage"][:]

    # Load and distribute simulation results
    with h5py.File("simulation_results.h5", "r") as results_file:
        rank_keys = list(results_file.keys())
        local_keys = rank_keys[rank::size]  # Divide results among ranks

        for rank_key in local_keys:
            rank_group = results_file[rank_key]
            for combo_key in rank_group.keys():
                sim_group = rank_group[combo_key]
                time = sim_group["time"][:]
                voltage = sim_group["voltage"][:]

        # Load fullCurrents.py data
        full_currents_data = pd.read_csv("fullCurrents_AllComp_data.csv")
        time_fullCurrents = full_currents_data["Time (ms)"]
        voltage_fullCurrents = full_currents_data["Soma Voltage (mV)"]

    # # Open the grid search results file
    # with h5py.File("simulation_results.h5", "r") as results_file:
    #     rank_group = results_file.get(f"rank_{rank}")
    #     if rank_group:
    #         for combo in rank_group.keys():
    #             sim_group = rank_group[combo]
    #             time = sim_group["time"][:]
    #             voltage = sim_group["voltage"][:]


        # Plot comparison
        plt.figure(figsize=(10, 6))
        plt.plot(time_fullCurrents, voltage_fullCurrents, label="fullCurrents.py", color="red")
        plt.plot(time, voltage, label=f"{rank}_{combo}", color="blue")
        plt.xlabel("Time (ms)")
        plt.ylabel("Voltage (mV)")
        plt.title(f"Comparison of {rank}_{combo} with fullCurrents.py")
        plt.legend()
        plt.grid()
        # Save figure with unique name
        plt.savefig(os.path.join(output_dir_full_sim, "Comparison_{sheet}.png"))
        plt.close()

    # Plot zoomed in simulation comparison from each sheet
    with h5py.File("simulation_results.h5", "r") as results_file:
        for rank in results_file.keys():
            rank_group = results_file[rank]
            for combo in rank_group.keys():
                sim_group = rank_group[combo]
                # Load simulation data
                time_grid = sim_group["time"][:]
                voltage_grid = sim_group["voltage"][:]

        # Plot comparison
        plt.figure(figsize=(10, 6))
        plt.plot(time_fullCurrents, voltage_fullCurrents, label="fullCurrents.py", color="red")
        plt.plot(time_grid, voltage_grid, label=f"{rank}_{combo}", color="blue")
        plt.xlabel("Time (ms)")
        plt.ylabel("Voltage (mV)")
        # Zoom on vertical and horizontal axes
        plt.xlim(1500, 1750)
        plt.ylim(-80, 60)
        plt.title(f"Voltage Trace Zoomed 1500 - 1750 ms for {rank}_{combo}")
        plt.legend()
        plt.grid()
        # Save figure with unique name
        plt.savefig(os.path.join(output_dir_zoomed_in, f"Zoomed_Comparison_{rank}_{combo}.png"))
        plt.close()

    print("Comparison plots saved.")


# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()