from sTI import sTI_cell
from neuron import h, gui
import matplotlib.pyplot as plt 
from matplotlib import rc  # for font rendering (see below)
from netpyne.support.scalebar import add_scalebar
from matplotlib.ticker import FormatStrFormatter  # for adding units to y axis 
import numpy as np
import pandas as pd
import h5py
from mpi4py import MPI
import os 


def main():
	# First codes to run before using ipython
	# module avail mpi
	# module load mpi/mpich-x86_64

	### USE LATEX FOR FONT RENDERING ###
	rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
	rc('text', usetex=True)

	# MPI setup
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()

	# Create a results folder
	os.makedirs("simulation_results", exist_ok=True)

	if rank == 0:  # Single-core operation for generating HDF5
		print("Running grid search on one core...")

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
	g_Pass_values = np.linspace((1.3e-05)/10, (1.3e-05)*10, 10)  # Range for g_Pass
	gmax_naf2_values = np.linspace(0.1/10, 0.1*10, 10)  # Range for gmax_naf2 
	gmax_kdr2orig_values = np.linspace(0.1/10, 0.1*10, 10)
	ghbar_iar_values = np.linspace((7e-05)/10, (7e-05)*10, 10)
	gbar_icanINT_values = np.linspace((9e-05)/10, (9e-05)*10, 10)
	gkbar_iahp_values = np.linspace(0.45/10, 0.45*10, 10)
	gcabar_it2INT_values = np.linspace((4e-05)/10, (4e-05)*10, 10)
	pcabar_icalINT_values = np.linspace((9e-05)/10, (9e-05)*10, 10)

	# Save the combination of parameters in an HDF5 file
	with h5py.File("grid_search_results.h5", "h5") as h5file:
		group = h5file.create_group("parameters")
		index = 0
		for g_Pass in g_Pass_values:
			for gmax_naf2 in gmax_naf2_values:
				for gmax_kdr2orig in gmax_kdr2orig_values:
					for ghbar_iar in ghbar_iar_values:
						for gbar_icanINT in gbar_icanINT_values:
							for gkbar_iahp in gkbar_iahp_values:
								for gcabar_it2INT in gcabar_it2INT_values:
									for pcabar_icalINT in pcabar_icalINT_values:
										param_set = {
											cell.soma.g_Pass: g_Pass,
											cell.soma.gmax_naf2: gmax_naf2,
											cell.soma.gmax_kdr2orig: gmax_kdr2orig,
											cell.soma.ghbar_iar: ghbar_iar,
											cell.soma.gbar_icanINT: gbar_icanINT,
											cell.soma.gkbar_iahp: gkbar_iahp,
											cell.soma.gcabar_it2INT: gcabar_it2INT,
											cell.soma.pcabar_icalINT: pcabar_icalINT,
											}
										param_group = group.create_group(f"combo_{index}")
										for key, value in param_set.items():
											param_group.attrs[key] = value
										index += 1

	comm.Barrier()  # Synchronize all cores before proceeding

	# Run simulations simulataneosly on 10 cores
	with h5py.File("grid_search_parameters.h5", "r") as h5file:
		param_keys = list(h5file["parameters"].keys())
		total_params = len(param_keys)
		chunk_size = total_params // size
		start_idx = rank * chunk_size
		end_idx = (rank + 1) * chunk_size if rank != size - 1 else total_params
		local_keys = param_keys[start_idx:end_idx]

		print(f"Rank {rank} processing {len(local_keys)} parameter sets...")

	# Open an HDF5 file for saving results
		with h5py.File("simulation_results.h5", "w") as h5file:
			results_group = h5file.create_group(f"rank_{rank}")

			for key in local_keys:
				param_group = h5file["parameters"][key].attrs
				g_Pass = param_group["g_Pass"]
				gmax_naf2 = param_group["gmax_naf2"]
				gmax_kdr2orig = param_group["gmax_kdr2orig"]
				ghbar_iar = param_group["ghbar_iar"]
				gbar_icanINT = param_group["gbar_icanINT"]
				gkbar_iahp = param_group["gkbar_iahp"]
				gcabar_it2INT = param_group["gcabar_it2INT"]
				pcabar_icalINT = param_group["pcabar_icalINT"]

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
				time_vector = list(h.Vector().record(h._ref_t))
				voltage_vector = list(h.Vector().record(cell.soma(0.5)._ref_v))

				# Save data in HDF5
				sim_group = results_group.create_group(key)
				sim_group.create_dataset("time", data=time_vector)
				sim_group.create_dataset("voltage", data=voltage_vector)


	comm.Barrier()

	if rank == 0:
		print("All simulations completed.")

	########### INPUT RESISTANCE 
	print('soma input resistance')
	print(cell.soma(0.5).ri())


	##############################
	######### PLOTTING #########
	##############################

	### PLOLTTING FOR INTERACTION OF CURRENTS FIGURE! 

	# fancyVoltage = 0
	# plainVoltage = 0
	# allCurrents  = 1


	# if allCurrents:
	# 	# DICT WITH INFO ABOUT EACH RECORDED CURRENT  (AND FIRST IN THE DICT IS VOLTAGE TRACE)
	# 	vecInfo = {'voltage': {'label': r'$\mathbf{V_m}$', 'vec': v_vec, 'color': 'k', 'sizey': 25}, # 'Voltage'
	# 	'leak':{'label': r'$\mathbf{I_{leak}}$', 'vec': iPass_vec, 'color':'darkblue', 'ytickmin': 0, 'ytickmax': 2},
	# 	'IKdr': {'label': r'$\mathbf{I_{Kdr}}$', 'vec': ik_vec, 'color':'c'},
	# 	'IH': {'label': r'$\mathbf{I_H}$', 'vec': ih_vec, 'color':'m', 'ytickmin': -0.2, 'ytickmax': 0.2}, # 'IH current'

	# 	'INaf': {'label': r'$\mathbf{I_{Naf}}$', 'vec': ina_vec, 'color':'darkblue', 'sizey': 500, 'ytickmin': -1000, 'ytickmax': 0},

	# 	'IL': {'label': r'$\mathbf{I_L}$', 'vec': iCa_vec_IL, 'color':'orangered', 'sizey': 25, 'ytickmin': -50, 'ytickmax': 0},
	# 	'Ca': {'label': 'High-thresh ' r'$\mathbf{[Ca^{2+}]_{i}}$', 'vec': Cai_soma, 'color': 'coral','sizey': 100, 'ytickmin': 50, 'ytickmax':250}, # 'ytickmax':200 # r'$\mathbf{[Ca^{2+}]_i}$

	# 	'IT': {'label': r'$\mathbf{I_T}$', 'vec': ica_vec_IT, 'color':'darkviolet', 'sizey': 2.5, 'ytickmin': -1, 'ytickmax': 0}, # 'IT current' # 'ytickmin': -2
	# 	'ca': {'label': 'Low-thresh ' r'$\mathbf{[ca^{2+}]_{i}}$', 'vec': cai_soma, 'color': 'mediumorchid', 'sizey': 100,
	# 			'ytickmin': 60, 'ytickmax':125}, # 'ytickmax':130 # r'$\mathbf{[ca^{2+}]_i}$

	# 	'IAHP': {'label': r'$\mathbf{I_{AHP}}$', 'vec': iahp_vec, 'color':'seagreen', 'sizey': 25, 'ytickmin': 0, 'ytickmax': 50}, 
	# 	'ICAN': {'label': r'$\mathbf{I_{CAN}}$', 'vec': ican_vec, 'color':'lightseagreen', 'sizey': 10, 'ytickmin': -10, 'ytickmax': 0} # 'ytickmin': -10 # 'ytickmin': -20
	# 	}


	# 	# ENTER WHICH CURRENTS TO PLOT 
	# 	## vecsToPlot = ['voltage', 'IAHP', 'ICAN', 'IH', 'leak', 'INaf', 'IL', 'Ca', 'IT', 'ca']
	# 	vecsToPlot = ['voltage', 'IT', 'ca', 'ICAN', 'INaf', 'IL', 'Ca', 'IAHP']


	# # 	# SLICE TIME VEC IF NECESSARY
	# 	t_vec = list(t_vec)
	# 	t_vec_allCurrents = t_vec[25000:] # USE SAME IN LOOP BELOW 

	# 	time_points = [500, 1000]

	# # 	# CREATE SUBPLOTS 
	# 	fig,ax = plt.subplots(nrows = len(vecsToPlot), ncols = 1, sharex=True)

	# # 	### WITH SCALEBAR
	# 	scalebar = 0 

	# 	if scalebar:
	# 		for i,vec in enumerate(vecsToPlot):
	# 			vecToPlot = vecInfo[vec]['vec']
	# 			vecToPlot = list(vecToPlot)
	# 			vecToPlot = vecToPlot[25000:]
	# 			if vec == 'voltage':
	# 				add_scalebar(ax[i],hidey=False,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='mV',barcolor=vecInfo[vec]['color'],loc=4) 

	# 			elif vec in ['leak', 'INaf', 'IKdr', 'IH', 'IT', 'IL', 'IAHP', 'ICAN']:
	# 				vecToPlotScaled = [i * 1000 for i in vecToPlot] 
	# 				vecToPlot = vecToPlotScaled
	# 				if vec == 'IAHP':
	# 					add_scalebar(ax[i],hidey=True,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='pA',barcolor=vecInfo[vec]['color'],loc=4) 
	# 				else:
	# 					add_scalebar(ax[i],hidey=True,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='pA',barcolor=vecInfo[vec]['color'],loc=1)

	# 			elif vec in ['ca', 'Ca']:
	# 				vecToPlotScaled = [i * 1000000 for i in vecToPlot]
	# 				vecToPlot = vecToPlotScaled
	# 				add_scalebar(ax[i],hidey=True,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='nM',barcolor=vecInfo[vec]['color'],loc=4)


	# 			ax[i].plot(t_vec_allCurrents,vecToPlot, color=vecInfo[vec]['color'],label=vecInfo[vec]['label'])
	# 			ax[i].set_title(vecInfo[vec]['label'], x=0.1,y=0.25, color=vecInfo[vec]['color']) 


	# # 	### WITH AXES & SCALEBAR FOR VOLTAGE <-- USE THIS AS DEFAULT OPTION!! 
	# 	else:
	# 		for i,vec in enumerate(vecsToPlot):
	# 			vecToPlot = vecInfo[vec]['vec']
	# 			vecToPlot = list(vecToPlot)
	# 			vecToPlot = vecToPlot[25000:]


	# 			if vec == 'voltage':
	# 				formatter = FormatStrFormatter('%d mV')
	# 				add_scalebar(ax[i],hidey=True,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='mV',barcolor=vecInfo[vec]['color'],loc=4) 


	# 			elif vec in ['leak', 'INaf', 'IKdr', 'IH', 'IT', 'IL', 'IAHP', 'ICAN']:
	# 				vecToPlotScaled = [i * 1000 for i in vecToPlot] 
	# 				vecToPlot = vecToPlotScaled
	# 				formatter = FormatStrFormatter('%d pA')
	# 				ytickmin = vecInfo[vec]['ytickmin']
	# 				ytickmax = vecInfo[vec]['ytickmax']
	# 				ax[i].spines['right'].set_bounds(ytickmin, ytickmax) # set y axis label bounds 
	# 				yticks = np.linspace(ytickmin, ytickmax, 2)
	# 				ax[i].set_yticks(yticks)

	# 			elif vec in ['ca', 'Ca']:
	# 				vecToPlotScaled = [i * 1000000 for i in vecToPlot]
	# 				vecToPlot = vecToPlotScaled
	# 				formatter = FormatStrFormatter('%d nM')
	# 				ytickmin = vecInfo[vec]['ytickmin']
	# 				ytickmax = vecInfo[vec]['ytickmax']
	# 				ax[i].spines['right'].set_bounds(ytickmin, ytickmax) # set y axis label bounds 
	# 				yticks = np.linspace(ytickmin, ytickmax, 2)
	# 				ax[i].set_yticks(yticks)

	# # 			# set units next to y axis ticks
	# 			ax[i].yaxis.set_major_formatter(formatter)

	# # 			# set all spines invisible except the right 
	# 			ax[i].spines['bottom'].set_visible(False)
	# 			ax[i].spines['top'].set_visible(False)
	# 			ax[i].spines['left'].set_visible(False)
	# 			ax[i].spines['right'].set_visible(True)

	# # 			# set color of right spine
	# 			ax[i].spines['right'].set_color(vecInfo[vec]['color'])

	# # 			# remove ticks on x axis 
	# 			for tic in ax[i].xaxis.get_major_ticks():
	# 				tic.tick1On = tic.tick2On = False
	# 				tic.label1On = tic.label2On = False

	# # 			# only label the tickmarks on the right spine 
	# 			ax[i].yaxis.set_ticks_position('right')

	# # 			# set color of y ticks 
	# 			ax[i].tick_params(axis='y',colors=vecInfo[vec]['color'])


	# # 			# PLOT 
	# 			ax[i].plot(t_vec_allCurrents,vecToPlot, color=vecInfo[vec]['color'],label=vecInfo[vec]['label'])

	# 			ax[i].set_ylabel(vecInfo[vec]['label'])

	# 			ax[i].set_title(vecInfo[vec]['label'], x=0.1,y=0.25, color=vecInfo[vec]['color']) 

	# # ADDING VERTICAL TIME BARS
	# 			for time_point in time_points:
	#  				ax[i].axvline(x=time_point, color='gray', linestyle='--', linewidth=1)
	# # ADDING LABEL FOR X-AXIS ON LAST PLOT 
	# #				ax[-1].set_xlabel('Time (ms)')

	# plt.show()


	# if fancyVoltage:
	# # 	### FANCIER VOLTAGE PLOTTING 
	#  	t_vec = list(t_vec)
	#  	v_vec = list(v_vec)

	# 	plt.figure(figsize=(6,3))
	# 	ax = plt.gca()
	# 	ax.yaxis.set_label_coords(-0.07, 0.5)
	# 	plt.ylim(-137,10)

	# 	plt.ylabel('Voltage (mV)')
	# 	plt.xlabel('Time (ms)')
	# 	plt.plot(t_vec[37000:80000],v_vec[37000:80000],'k', label='voltage', linewidth=0.8)


	# 	x = [t_vec[37000], stim.delay, stim.delay + stim.dur, t_vec[80000]]
	# 	y = [-83,-83,-83 + 5,-83] 
	# 	plt.step(x,y,'k', linewidth=1)

	# 	add_scalebar(ax,hidey=True,hidex=True,matchx=True,matchy=False,sizey=10,unitsx='ms', unitsy='mV', 
	# 				labely='10 mV\n220pA',loc=3,pad=-2.4)


	# 	plt.show()


	# if plainVoltage:
	# 	plt.figure()
	# 	plt.plot(t_vec,v_vec,label='voltage')
	# 	plt.title('somatic voltage trace')
	# 	plt.xlabel('time (ms)')
	# 	plt.ylabel('voltage (mV)')
	# 	plt.show()
	# 	plt.close()


	###############
	### VOLTAGE ###
	###############
	# plt.figure()
	# plt.plot(t_vec,v_vec,label='voltage')
	# plt.title('somatic voltage trace')
	# plt.xlabel('time (ms)')
	# plt.ylabel('voltage (mV)')
	# plt.show()
	# plt.close()

	#### FANCIER VOLTAGE PLOTTING 
	# t_vec = list(t_vec)	# time_slice = t_vec[35000:85000]
	# v_vec = list(v_vec) # volt_slice = v_vec[35000:85000]

	# plt.figure(figsize=(5,3))
	# ax = plt.gca()
	# ax.yaxis.set_label_coords(-0.07, 0.5)
	# #plt.ylim(-90,30)
	# plt.ylim(-137,10)

	# plt.ylabel('Voltage (mV)')
	# plt.xlabel('Time (ms)')
	# #plt.title('')
	# plt.plot(t_vec[37000:73000],v_vec[37000:73000],'k', label='voltage', linewidth=0.8)  #[35000:65000] # [37000:63000] (for 500ms stim dur) #t_vec[35000:85000]
	# #plt.plot(t_vec,v_vec,'k', label='voltage') 



	# x = [t_vec[37000], stim.delay, stim.delay + stim.dur, t_vec[73000]]
	# y = [-83,-83,-83 + 5,-83] 
	# #y = [-130, -130, -130-5, -130]
	# plt.step(x,y,'k', linewidth=1)

	# add_scalebar(ax,hidey=True,hidex=True,matchx=True,matchy=False,sizey=10,unitsx='ms', unitsy='mV', labely='10 mV\n300pA',loc=3,pad=-2.4) #,barwidth=2)


	# plt.show()


	################
	### CURRENTS ###
	################


	## LEAK CURRENT
	# plt.figure()
	# plt.plot(t_vec,iPass_vec,label='leak current')
	# plt.title('leak current')
	# plt.xlabel('time (ms)')
	# plt.ylabel('mA/cm2')
	# plt.show()
	# plt.close()

	# ## FAST SODIUM CURRENT
	# plt.figure()
	# plt.plot(t_vec,ina_vec,label='fast sodium current')
	#plt.title('fast sodium current')
	#plt.xlabel('time (ms)')
	#plt.show()
	#plt.close()

	## POTASSIUM CURRENT
	# plt.figure()
	# plt.plot(t_vec,ik_vec,label = 'kdr current')
	# plt.title('kdr current')
	# plt.title('CURRENTS')
	# plt.legend(loc='upper right')
	# plt.show()
	# plt.close()

	# ## IH CURRENT
	# plt.figure()
	# plt.plot(t_vec,ih_vec,label = 'IH current')
	# plt.legend(loc='upper right')
	# plt.title('CURRENTS')
	# # plt.title('H current')
	# plt.show()
	# plt.close()

	# ## IT CURRENT
	# plt.figure()
	# plt.plot(t_vec,ica_vec_IT,label='IT current')
	# plt.legend(loc='upper right')
	# plt.title('CURRENTS')
	# plt.title('ca current (IT)')
	# plt.show()
	# plt.close()


	# ## IL CURRENT
	# plt.figure()
	# plt.plot(t_vec,iCa_vec_IL,label='IL current')
	# plt.legend(loc='upper right')
	# plt.title('CURRENTS')
	# plt.title('Ca current (IL)')
	# plt.show()
	# plt.close()

	# ## ICAN CURRENT
	# plt.figure()
	# plt.plot(t_vec,ican_vec,label='ICAN current')
	# plt.title('ICAN current')
	# plt.legend(loc='upper right')
	# plt.title('CURRENTS')
	# plt.show()
	# plt.close()

	# ## IAHP CURRENT
	# plt.figure()
	# plt.plot(t_vec,iahp_vec,'--',label='IAHP current')
	# # plt.title('IAHP current')
	# plt.title('CURRENTS')
	# plt.legend(loc='upper right')
	# plt.show()
	# plt.close()




	##############################
	### EQUILIBRIUM POTENTIALS ###
	##############################

	# ### ena
	# plt.figure()
	# plt.plot(t_vec,ena_soma,label='ena')
	# plt.title('sodium reversal potential')
	# plt.show()
	# plt.close()

	# ### ek 
	# plt.figure()
	# plt.plot(t_vec,ek_soma,label='ek')
	# plt.title('K+ reversal potential')
	# plt.show()
	# plt.close()

	# ### 'ca ion' EQUILIBRIUM POTENTIAL
	# plt.figure()
	# plt.plot(t_vec,eca_soma,label='eca')
	# plt.legend(loc='upper right')
	# plt.show()
	# plt.close()


	# ### 'Ca ion' EQUILIBRIUM POTENTIAL
	# plt.figure()
	# plt.plot(t_vec,eCa_soma,label='eCa')
	# plt.title('EQUILIBRIUM POTENTIALS')
	# plt.legend(loc='upper right')
	# plt.show()
	# plt.close()



	###############################
	### INTERNAL CONCENTRATIONS ###
	###############################

	# ## nai 
	# plt.figure()
	# plt.plot(t_vec,nai_soma,label='nai')
	# plt.title('internal sodium concentration')
	# plt.show()
	# plt.close() 

	## ki 
	# plt.figure()
	# #plt.plot(t_vec,ki_soma,label='ki')
	# plt.plot(t_vec,ko_soma,label='ko')
	# plt.title('internal K+ concentration')
	# plt.legend(loc='best')
	# plt.show()
	# plt.close()

	# ## k2i 
	# plt.figure()
	# plt.plot(t_vec,k2i_soma,label='k2i')
	# plt.plot(t_vec,k2o_soma,label='k2o')
	# plt.title("internal 'K2 ion' concentration")
	# plt.legend(loc='best')
	# plt.show()
	# plt.close()

	## 'ca ion' [internal concentration]
	# plt.figure()
	# plt.plot(t_vec,cai_soma,label='cai')
	# # plt.legend(loc='upper right')
	# # plt.show()
	# # plt.close()

	# # ## 'Ca ion' [internal concentration]
	# # plt.figure()
	# plt.plot(t_vec,Cai_soma,label='Cai')
	# plt.legend(loc='upper right')
	# plt.show()
	# plt.close()

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()
