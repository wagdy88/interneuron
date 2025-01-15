from sTI import sTI_cell
from neuron import h, gui
import matplotlib.pyplot as plt 
from matplotlib import rc  # for font rendering (see below)
from netpyne.support.scalebar import add_scalebar
from matplotlib.ticker import FormatStrFormatter  # for adding units to y axis 
import numpy as np
import pandas as pd
import h5py
import os 


def main():
    ### USE LATEX FOR FONT RENDERING ###
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)

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
# Open the HDF5 file containing parameter combinations

    with h5py.File("grid_search_results.h5", "r") as h5file:
        param_keys = list(h5file["parameters"].keys())
        print(f"Processing {len(param_keys)} parameter sets...")

        # Extract all parameter combinations
        for key in param_keys:
            param_group = h5file["parameters"][key].attrs
            # Extract parameters
            g_Pass = param_group["g_Pass"]
            gmax_naf2 = param_group["gmax_naf2"]
            gmax_kdr2orig = param_group["gmax_kdr2orig"]
            ghbar_iar = param_group["ghbar_iar"]
            gbar_icanINT = param_group["gbar_icanINT"]
            gkbar_iahp = param_group["gkbar_iahp"]
            gcabar_it2INT = param_group["gcabar_it2INT"]
            pcabar_icalINT = param_group["pcabar_icalINT"]

            print(f"Loaded parameters for {key}: g_Pass={g_Pass}, gmax_naf2={gmax_naf2}, ...")


# Open an HDF5 file to save simulation results
    with h5py.File("simulation_results.h5", "w") as h5file:
        results_group = h5file.create_group("simulations")

        for key in param_keys:
            
            with h5py.File("grid_search_results.h5", "r") as read_file:
                param_group = read_file["parameters"][key].attrs
                g_Pass = param_group["g_Pass"]
                gmax_naf2 = param_group["gmax_naf2"]
                gmax_kdr2orig = param_group["gmax_kdr2orig"]
                ghbar_iar = param_group["ghbar_iar"]
                gbar_icanINT = param_group["gbar_icanINT"]
                gkbar_iahp = param_group["gkbar_iahp"]
                gcabar_it2INT = param_group["gcabar_it2INT"]
                pcabar_icalINT = param_group["pcabar_icalINT"]

            # # Save the results in the new HDF5 file
            # sim_group = results_group.create_group(key)
            # sim_group.create_dataset("time", data=time_vector)
            # sim_group.create_dataset("voltage", data=voltage_vector)
        # Configure NEURON model
            cell.soma.g_Pass = g_Pass
            cell.soma.gmax_naf2 = gmax_naf2
            cell.soma.gmax_kdr2orig = gmax_kdr2orig
            cell.soma.ghbar_iar = ghbar_iar
            cell.soma.gbar_icanINT = gbar_icanINT
            cell.soma.gkbar_iahp = gkbar_iahp
            cell.soma.gcabar_it2INT = gcabar_it2INT
            cell.soma.pcabar_icalINT = pcabar_icalINT

            h.finitialize(-66)
            h.celsius = 36
            h.tstop = 2500
            h.run()

            ##################
            ### CURRENTS ###
            ##################

            ### LEAK CURRENT
            iPass_vec = h.Vector()
            iPass_vec.record(cell.soma(0.5)._ref_i_Pass)

            ### FAST SODIUM CURRENT
            ina_vec = h.Vector()
            ina_vec.record(cell.soma(0.5)._ref_ina)


            ### K+ DELAYED RECTIFIER CURRENT
            ik_vec = h.Vector()
            ik_vec.record(cell.soma(0.5)._ref_ik)

            ### IH CURRENT
            ih_vec = h.Vector()
            ih_vec.record(cell.soma(0.5)._ref_iother)

            # IT CURRENT -- technically "ca" current
            ica_vec_IT = h.Vector()
            ica_vec_IT.record(cell.soma(0.5)._ref_ica)

            # IL CURRENT -- technically "Ca" current
            iCa_vec_IL = h.Vector()
            iCa_vec_IL.record(cell.soma(0.5)._ref_iCa)

            # ICAN CURRENT
            ican_vec = h.Vector()
            ican_vec.record(cell.soma(0.5)._ref_iother2)

            # IAHP CURRENT
            iahp_vec = h.Vector()
            iahp_vec.record(cell.soma(0.5)._ref_ik2)


            ################
            ##### IONS #####
            ################

            ## POTASSIUM IONS FROM KDR2 ('K ion')
            ek_soma = h.Vector()
            ek_soma.record(cell.soma(0.5)._ref_ek)
            ki_soma = h.Vector()
            ki_soma.record(cell.soma(0.5)._ref_ki)
            ko_soma = h.Vector()
            ko_soma.record(cell.soma(0.5)._ref_ko)

            ### K2 POTASSIUM IONS FROM IAHP ('K2 ion')
            ek2_soma = h.Vector()
            ek2_soma.record(cell.soma(0.5)._ref_ek2)
            k2i_soma = h.Vector()
            k2i_soma.record(cell.soma(0.5)._ref_k2i)
            k2o_soma = h.Vector()
            k2o_soma.record(cell.soma(0.5)._ref_k2o)


            ### CALCIUM INTERNAL CONCENTRATIONS
            cai_soma = h.Vector()
            cai_soma.record(cell.soma(0.5)._ref_cai)
            Cai_soma = h.Vector() 
            Cai_soma.record(cell.soma(0.5)._ref_Cai)


            #####################
            ######## RUN ########
            #####################
            h.finitialize()
            h.celsius = 36
            h.tstop = 2500
            h.run()

            # Save results for this parameter combination
            # time_vector = list(h.Vector().record(h._ref_t))
            # voltage_vector = list(h.Vector().record(cell.soma(0.5)._ref_v))

            # Save data in HDF5
            sim_group = results_group.create_group(key)
            sim_group.create_dataset("time", data=list(t_vec), chunks=True, compression="gzip")
            sim_group.create_dataset("voltage", data=list(v_vec), chunks=True, compression="gzip")

        print("Simulations completed and results saved.")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()
