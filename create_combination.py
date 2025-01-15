from sTI import sTI_cell
from neuron import h, gui
import matplotlib.pyplot as plt 
from matplotlib import rc  # for font rendering (see below)
from netpyne.support.scalebar import add_scalebar
from matplotlib.ticker import FormatStrFormatter  # for adding units to y axis 
import numpy as np
import pandas as pd
import h5py
#from mpi4py import MPI
import os 


def main():
	# First codes to run before using ipython
	# module avail mpi
	# module load mpi/mpich-x86_64

	### USE LATEX FOR FONT RENDERING ###
	rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
	rc('text', usetex=True)

	# MPI setup
	# comm = MPI.COMM_WORLD
	# rank = comm.Get_rank()
	# size = comm.Get_size()

	# Create a results folder
	# os.makedirs("simulation_results", exist_ok=True)

	# if rank == 0:  # Single-core operation for generating HDF5
	#     print("Running grid search on one core...")

	#############################################
	############## CREATE SECTIONS ##############
	#############################################

	# Instantiate cell and replace previous soma/dend setup
	cell = sTI_cell(param_file='TI_reduced_cellParams.json', useJson=True)

	# cell = sTI_cell(param_file=None, useJson=False)


	# Modify the script to use cell.soma and cell.dend
	stim = h.IClamp(cell.soma(0.5))
	stim.delay = 1000
	stim.dur = 750
	stim.amp = 0.11

	# Adjust recording vectors
	t_vec = h.Vector()
	t_vec.record(h._ref_t)

	v_vec = h.Vector()
	v_vec.record(cell.soma(0.5)._ref_v)

	# Setting parameter grid search
	g_Pass_values = np.linspace((1.3e-05)/10, (1.3e-05)*10, 3)  # Range for g_Pass
	gmax_naf2_values = np.linspace(0.1/10, 0.1*10, 3)  # Range for gmax_naf2 
	gmax_kdr2orig_values = np.linspace(0.1/10, 0.1*10, 3)
	ghbar_iar_values = np.linspace((7e-05)/10, (7e-05)*10, 3)
	gbar_icanINT_values = np.linspace((9e-05)/10, (9e-05)*10, 2)
	gkbar_iahp_values = np.linspace(0.45/10, 0.45*10, 2)
	gcabar_it2INT_values = np.linspace((4e-05)/10, (4e-05)*10, 2)
	pcabar_icalINT_values = np.linspace((9e-05)/10, (9e-05)*10, 2)

	# Save the combination of parameters in an HDF5 file
	# with h5py.File("grid_search_results.h5", "w", driver="mpio", comm=MPI.COMM_WORLD) as h5file:
	with h5py.File("grid_search_results.h5", "w") as h5file:
		parameter_group = h5file.create_group("parameters")
		index = 0
		for g_Pass in g_Pass_values:
			for gmax_naf2 in gmax_naf2_values:
				for gmax_kdr2orig in gmax_kdr2orig_values:
					for ghbar_iar in ghbar_iar_values:
						for gbar_icanINT in gbar_icanINT_values:
							for gkbar_iahp in gkbar_iahp_values:
								for gcabar_it2INT in gcabar_it2INT_values:
									for pcabar_icalINT in pcabar_icalINT_values:
										param_subgroups = parameter_group.create_group(f"combo_{index:05d}")
										param_subgroups.attrs["g_Pass"] = g_Pass
										param_subgroups.attrs["gmax_naf2"] = gmax_naf2
										param_subgroups.attrs["gmax_kdr2orig"] = gmax_kdr2orig
										param_subgroups.attrs["ghbar_iar"] = ghbar_iar
										param_subgroups.attrs["gbar_icanINT"] = gbar_icanINT
										param_subgroups.attrs["gkbar_iahp"] = gkbar_iahp
										param_subgroups.attrs["gcabar_it2INT"] = gcabar_it2INT
										param_subgroups.attrs["pcabar_icalINT"] = pcabar_icalINT
										index += 1
	print(f"Created {index} parameter combinations.")


if __name__ == "__main__":
	main()
