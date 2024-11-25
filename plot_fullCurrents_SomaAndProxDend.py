from sTI_cell import sTI_cell
from neuron import h, gui
import matplotlib.pyplot as plt 
from matplotlib import rc  # for font rendering (see below)
from netpyne.support.scalebar import add_scalebar
from matplotlib.ticker import FormatStrFormatter # for adding units to y axis 
import numpy as np

### USE LATEX FOR FONT RENDERING ###
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

#############################################
############## ADD CELL CLASS ###############
#############################################


# class sTI_cell:
#     def __init__(self, x=0, y=0, z=0, ID=0, ty=0):
#         self.x = x
#         self.y = y
#         self.z = z
#         self.ID = ID
#         self.ty = ty
#         self.soma = soma = h.Section(name='soma', cell=self)
#         self.dend = dend = h.Section(name='dend', cell=self)
#         self.dend.connect(self.soma(0), 0)  # Connect dend(0) to soma(0)
#         for sec in [self.soma, self.dend]:
#             sec.Ra = 120
#         self.initsoma()
#         self.initdend()

#     def initsoma(self):
#         soma = self.soma
#         soma.nseg = 1
#         soma.diam = 10
#         soma.L = 16
#         soma.cm = 1
#         ## Insert mechanisms with parameters
#         soma.insert('Pass')
#         soma.g_Pass = 13e-06
#         soma.erev_Pass = -74
#         soma.insert('naf2')
#         soma.gmax_naf2 = 0.1
#         # Continue with other parameters...

#     def initdend(self):
#         dend = self.dend
#         dend.nseg = 1
#         dend.diam = 3.25
#         dend.L = 240
#         dend.cm = 1
#         dend.insert('Pass')
#         dend.g_Pass = 13e-06
#         dend.erev_Pass = -74


###############################
### ADDING GLOBAL PARAMETERS###
###############################
h.Cai0_Ca_ion = 5e-05
h.Cao0_Ca_ion = 2.0
h.beta_iahp = 0.02
h.beta_icanINT = 0.003
h.cac_iahp = 0.0008
h.cac_icanINT = 0.00011
h.kd2_Cad_int = 0.0009
h.kd2_cad_int = 0.0009
h.sh1_icalINT = -10.0
h.sh_it2INT = 4.6
h.shift2_it2INT = 0.0
h.sm_it2INT = 4.8
h.x_icanINT = 8.0





#############################################
############## CREATE SECTIONS ##############
#############################################

# Instantiate cell and replace previous soma/dend setup
cell = sTI_cell('TI_reduced_cellParams.json')

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


# ######## CREATE SOMA ######## 
# soma = h.Section(name='soma')
# soma.nseg = 1
# soma.diam = 10
# soma.L = 16
# soma.cm = 1


# ################## CREATE DENDRITES #################### 
# dend = [h.Section(name='dend[%d]' % i) for i in range(14)]

# ### PROXIMAL DENDRITES ### 
# prox_dends = dend[0:2]

# secLists = {
#     "all": [soma, dend[0], dend[1]],
#     "dend_all": [dend[0], dend[1]],
#     "proximal": [soma, dend[0], dend[1]]
# }


# dend[0].L = 240.0
# dend[0].Ra = 120.0
# dend[0].cm = 1.0
# dend[0].diam = 3.25
# dend[0].nseg = 1
# dend[0].insert('Pass')
# dend[0].g_Pass = 1.3e-05
# dend[0].erev_Pass = -74.0
# dend[0].connect(soma(0), 0)

# #### DISTAL DENDRITES ####
# dist_dends = dend[2:]

# for dist_dend in dist_dends: 
# 	dist_dend.nseg = 1
# 	dist_dend.diam = 1.75
# 	dist_dend.L = 180
# 	dist_dend.cm = 1


# #### CONNECT SECTIONS #####
# ## PROXIMAL DENDRITES ## 
# dend[0].connect(soma(0),0) 		# '0' end of dend[0] connects to '0' end of soma
# dend[1].connect(soma(1),0)		# '0' end of dend[1] connects to '1' end of soma

# ## DISTAL DENDRITES PART 1 (dend[2] thru dend[7]) ## 
# for ndend in dist_dends[0:6]:
# 	ndend.connect(dend[0](1), 0)

# ## DISTAL DENDRITES PART 2 (dend[8] thru dend[13]) ## 
# for ndend in dist_dends[6:]:
# 	ndend.connect(dend[1](1), 0)

## SET Ra FOR ALL SECTIONS (SOMA & ALL DENDRITES) ## 
# for sec in h.allsec():
# 	sec.Ra = 120 




#############################################
############# INSERT MECHANISMS #############
#############################################

# LEAK CURRENT ##
g_Pass = 2.5e-05 
# SOMA
cell.soma.insert('Pass')
cell.soma.g_Pass = g_Pass 
cell.soma.erev_Pass = -72 

# PROXIMAL DENDRITES
cell.dend.insert('Pass')
cell.dend.g_Pass = g_Pass
cell.dend.erev_Pass = -7


# # DISTAL DENDRITES 
# for dist_dend in dist_dends: 
# 	dist_dend.insert('Pass')
# 	dist_dend.g_Pass = g_Pass
# 	dist_dend.erev_Pass = -72

## Adding soma parameters from mechanisms in Erica's Github ##
cell.soma.insert('Cad_int')
cell.soma.Cainf_Cad_int = 1e-8
cell.soma.k_Cad_int = 0.005
cell.soma.taur_Cad_int = 150.0


##FAST SODIUM 
cell.soma.insert('naf2')
cell.soma.gmax_naf2     = 0.1 #0.042
cell.soma.mvhalf_naf2   = -40
cell.soma.mvalence_naf2 =  5
cell.soma.hvhalf_naf2   = -43
cell.soma.hvalence_naf2 = -6



# POTASSIUM DELAYED RECTIFIER -- ORIGINAL
cell.soma.insert('kdr2orig')
cell.soma.ek = -95
cell.soma.gmax_kdr2orig     	= 0.1
cell.soma.mvhalf_kdr2orig  	= -31
cell.soma.mvalence_kdr2orig 	=  3.8

# IH current
cell.soma.insert('iar')
cell.soma.ghbar_iar =  0.7e-04   # 1.3e-4		# 0.13 mS/cm2; correct re: jun.pdf
cell.soma.shift_iar = -0.0
#h.erev_iar = -44 	# ALREADY THE DEFAULT VALUE IN .mod 
#h.stp_iar = 7.4 	# ALREADY THE DEFAULT VALUE IN .mod 


# ICAN current
cell.soma.insert('icanINT')
cell.soma.gbar_icanINT = 0.0001 #0.0003
h.beta_icanINT = 0.003							# correct re: jun.pdf
h.cac_icanINT = 1.1e-04
cell.soma.ratc_icanINT = 0.8 #1	 						# low-thresh pool (IT)
cell.soma.ratC_icanINT = 0.1 #0.2							# high-thresh pool (IL)
h.x_icanINT = 8									# correct re: jun.pdf, if x_ican == "n"


# IAHP current
cell.soma.insert('iahp')
cell.soma.gkbar_iahp = 0.45 #0.3
h.beta_iahp = 0.02								# correct re: jun.pdf
h.cac_iahp = 8e-04
cell.soma.ratc_iahp = 0.2 							# low-thresh pool (IT)
cell.soma.ratC_iahp = 1 #0.8 							# high-thresh pool (IL)
# soma.ek2_iahp = -95 # added from Erica's Github

# IT current
cell.soma.insert('it2INT')
cell.soma.gcabar_it2INT = 0.4e-04  #1.0e-4
cell.soma.shift1_it2INT = 7
h.shift2_it2INT = 0
h.mx_it2INT = 3.0
h.hx_it2INT = 1.5
h.sm_it2INT = 4.8
h.sh_it2INT = 4.6


# CALCIUM PUMP FOR "ca" ION POOL - associated with IT
cell.soma.insert('cad_int')
cell.soma.taur_cad_int  = 150
cell.soma.taur2_cad_int  = 80
cell.soma.cainf_cad_int = 1e-8
cell.soma.cainf2_cad_int  = 5.3e-5 #5.2e-5
cell.soma.kt_cad_int = 0
cell.soma.kt2_cad_int = 0
cell.soma.k_cad_int  = 7.5e-3 #5e-3
cell.soma.kd_cad_int = 9e-4
h.kd2_cad_int = 9e-4


# IL current 
cell.soma.insert('icalINT')
cell.soma.pcabar_icalINT = 0.00009 #0.0006
h.sh1_icalINT = -10
h.sh2_icalINT = 0


# CALCIUM PUMP FOR "Ca" ION POOL -- associated with IL 
cell.soma.insert('Cad_int')
cell.soma.taur_Cad_int  = 150
cell.soma.taur2_Cad_int = 80
cell.soma.Cainf_Cad_int  = 1e-8
cell.soma.Cainf2_Cad_int  = 5.2e-5
cell.soma.kt_Cad_int = 0
cell.soma.kt2_Cad_int = 0
cell.soma.k_Cad_int  = 5e-3
cell.soma.kd_Cad_int = 9e-4
h.kd2_Cad_int = 9e-4
h.Cai0_Ca_ion = 5e-5 # added from Erica's Github
h.Cao0_Ca_ion = 2 # added from Erica's Github


### INPUT RESISTANCE VALUES: 
# soma.gbar_icanINT = 0.001
# soma.ghbar_iar = 2e-3 
# soma.gkbar_iahp = 1.4 




# #############################################
# ########### CHANGE ION PARAMETERS ###########
# #############################################

## ion style 
print("h.ion_style('ca_ion')",h.ion_style('ca_ion'))
print("h.ion_style('Ca_ion')",h.ion_style('Ca_ion'))
h.ion_style('ca_ion',3,2,1,1,0)
h.ion_style('Ca_ion',3,2,1,1,0)
print("h.ion_style('ca_ion')",h.ion_style('ca_ion'))
print("h.ion_style('Ca_ion')",h.ion_style('Ca_ion'))

# print("h.ion_style('k_ion')",h.ion_style('k_ion'))
# print("h.ion_style('k2_ion')",h.ion_style('k2_ion'))
# h.ion_style('k_ion',1,3,1,1,1)
# h.ion_style('k2_ion',1,3,1,1,1)
# print("h.ion_style('k_ion')",h.ion_style('k_ion'))
# print("h.ion_style('k2_ion')",h.ion_style('k2_ion'))

# ###### NEED TO DO THIS ONE WHEN ADDING CALCIUM PUMPS ####### 
## RESET INTERNAL AND EXTERNAL CONCENTRATIONS OF "Ca" ION IN h _ion STRUCT
h.Cai0_Ca_ion = 5e-5
h.Cao0_Ca_ion = 2


## RESET INTERNAL AND EXTERNAL CONCENTRATIONS OF "k2" ION IN h _ion STRUCT
h.k2i0_k2_ion = 54.5
h.k2o0_k2_ion = 2.5 

h.ki0_k_ion = 54.5
h.ko0_k_ion = 2.5 

## INITIALIZE CHANGES
h.v_init = -66
h.finitialize(-66)


###################################
######### STIM OBJECT #########
##################################

# stim = h.IClamp(soma(0.5))
# stim.delay = 1000
# stim.dur = 750 
# stim.amp = 0.11


###################################
######### RECORDING #########
###################################

### TIME
# t_vec = h.Vector()
# t_vec.record(h._ref_t)

# ### VOLTAGE
# v_vec = h.Vector()
# v_vec.record(soma(0.5)._ref_v)


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

# ### SODIUM IONS
# ena_soma = h.Vector()
# ena_soma.record(soma(0.5)._ref_ena)
# nai_soma = h.Vector()
# nai_soma.record(soma(0.5)._ref_nai)
# nao_soma = h.Vector()
# nao_soma.record(soma(0.5)._ref_nao)

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

# ### CALCIUM EQUILIBRIUM POTENTIALS
# eca_soma = h.Vector()
# eca_soma.record(soma(0.5)._ref_eca)
# eCa_soma = h.Vector()
# eCa_soma.record(soma(0.5)._ref_eCa)


### CALCIUM INTERNAL CONCENTRATIONS
cai_soma = h.Vector()
cai_soma.record(cell.soma(0.5)._ref_cai)
Cai_soma = h.Vector() 
Cai_soma.record(cell.soma(0.5)._ref_Cai)


# ### CALCIUM EXTERNAL CONCENTRATIONS
# cao_soma = h.Vector()
# cao_soma.record(soma(0.5)._ref_cao)
# Cao_soma = h.Vector() 
# Cao_soma.record(soma(0.5)._ref_Cao)



# ## ion style 
# print("h.ion_style('ca_ion')",h.ion_style('ca_ion'))
# print("h.ion_style('Ca_ion')",h.ion_style('Ca_ion'))
# h.ion_style('ca_ion',3,2,1,1,0)
# h.ion_style('Ca_ion',3,2,1,1,0)
# print("h.ion_style('ca_ion')",h.ion_style('ca_ion'))
# print("h.ion_style('Ca_ion')",h.ion_style('Ca_ion'))


#####################
######## RUN ########
#####################
h.finitialize()

h.celsius = 36
h.tstop = 2500
h.run()

########### INPUT RESISTANCE 
print('soma input resistance')
print(cell.soma(0.5).ri())




##############################
######### PLOTTING #########
##############################

### PLOLTTING FOR INTERACTION OF CURRENTS FIGURE! 

fancyVoltage = 0
plainVoltage = 0
allCurrents  = 1


if allCurrents:
	# DICT WITH INFO ABOUT EACH RECORDED CURRENT  (AND FIRST IN THE DICT IS VOLTAGE TRACE)
	vecInfo = {'voltage': {'label': r'$\mathbf{V_m}$', 'vec': v_vec, 'color': 'k', 'sizey': 25}, # 'Voltage'
	'leak':{'label': r'$\mathbf{I_{leak}}$', 'vec': iPass_vec, 'color':'darkblue', 'ytickmin': 0, 'ytickmax': 2},
	'IKdr': {'label': r'$\mathbf{I_{Kdr}}$', 'vec': ik_vec, 'color':'c'},
	'IH': {'label': r'$\mathbf{I_H}$', 'vec': ih_vec, 'color':'m', 'ytickmin': -0.2, 'ytickmax': 0.2}, # 'IH current'

	'INaf': {'label': r'$\mathbf{I_{Naf}}$', 'vec': ina_vec, 'color':'darkblue', 'sizey': 500, 'ytickmin': -1000, 'ytickmax': 0},

	'IL': {'label': r'$\mathbf{I_L}$', 'vec': iCa_vec_IL, 'color':'orangered', 'sizey': 25, 'ytickmin': -50, 'ytickmax': 0},
	'Ca': {'label': 'High-thresh ' r'$\mathbf{[Ca^{2+}]_{i}}$', 'vec': Cai_soma, 'color': 'coral','sizey': 100, 'ytickmin': 50, 'ytickmax':250}, # 'ytickmax':200 # r'$\mathbf{[Ca^{2+}]_i}$

	'IT': {'label': r'$\mathbf{I_T}$', 'vec': ica_vec_IT, 'color':'darkviolet', 'sizey': 2.5, 'ytickmin': -1, 'ytickmax': 0}, # 'IT current' # 'ytickmin': -2
	'ca': {'label': 'Low-thresh ' r'$\mathbf{[ca^{2+}]_{i}}$', 'vec': cai_soma, 'color': 'mediumorchid', 'sizey': 100,
			'ytickmin': 60, 'ytickmax':125}, # 'ytickmax':130 # r'$\mathbf{[ca^{2+}]_i}$

	'IAHP': {'label': r'$\mathbf{I_{AHP}}$', 'vec': iahp_vec, 'color':'seagreen', 'sizey': 25, 'ytickmin': 0, 'ytickmax': 50}, 
	'ICAN': {'label': r'$\mathbf{I_{CAN}}$', 'vec': ican_vec, 'color':'lightseagreen', 'sizey': 10, 'ytickmin': -10, 'ytickmax': 0} # 'ytickmin': -10 # 'ytickmin': -20
	}


	# ENTER WHICH CURRENTS TO PLOT 
	### vecsToPlot = ['voltage', 'IAHP', 'ICAN', 'IH', 'leak', 'INaf', 'IL', 'Ca', 'IT', 'ca']
	vecsToPlot = ['voltage', 'IT', 'ca', 'ICAN', 'INaf', 'IL', 'Ca', 'IAHP']


	# SLICE TIME VEC IF NECESSARY
	t_vec = list(t_vec)
	t_vec_allCurrents = t_vec[25000:] # USE SAME IN LOOP BELOW 

	time_points = [500, 1000]

	# CREATE SUBPLOTS 
	fig,ax = plt.subplots(nrows = len(vecsToPlot), ncols = 1, sharex=True)

	### WITH SCALEBAR
	scalebar = 0 

	if scalebar:
		for i,vec in enumerate(vecsToPlot):
			vecToPlot = vecInfo[vec]['vec']
			vecToPlot = list(vecToPlot)
			vecToPlot = vecToPlot[25000:]
			if vec == 'voltage':
				add_scalebar(ax[i],hidey=False,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='mV',barcolor=vecInfo[vec]['color'],loc=4) 

			elif vec in ['leak', 'INaf', 'IKdr', 'IH', 'IT', 'IL', 'IAHP', 'ICAN']:
				vecToPlotScaled = [i * 1000 for i in vecToPlot] 
				vecToPlot = vecToPlotScaled
				if vec == 'IAHP':
					add_scalebar(ax[i],hidey=True,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='pA',barcolor=vecInfo[vec]['color'],loc=4) 
				else:
					add_scalebar(ax[i],hidey=True,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='pA',barcolor=vecInfo[vec]['color'],loc=1)

			elif vec in ['ca', 'Ca']:
				vecToPlotScaled = [i * 1000000 for i in vecToPlot]
				vecToPlot = vecToPlotScaled
				add_scalebar(ax[i],hidey=True,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='nM',barcolor=vecInfo[vec]['color'],loc=4)


			ax[i].plot(t_vec_allCurrents,vecToPlot, color=vecInfo[vec]['color'],label=vecInfo[vec]['label'])
			ax[i].set_title(vecInfo[vec]['label'], x=0.1,y=0.25, color=vecInfo[vec]['color']) 


	### WITH AXES & SCALEBAR FOR VOLTAGE <-- USE THIS AS DEFAULT OPTION!! 
	else:
		for i,vec in enumerate(vecsToPlot):
			vecToPlot = vecInfo[vec]['vec']
			vecToPlot = list(vecToPlot)
			vecToPlot = vecToPlot[25000:]


			if vec == 'voltage':
				formatter = FormatStrFormatter('%d mV')
				add_scalebar(ax[i],hidey=True,hidex=True,matchx=False,matchy=False,sizey=vecInfo[vec]['sizey'], sizex=0, labelx=None, unitsy='mV',barcolor=vecInfo[vec]['color'],loc=4) 


			elif vec in ['leak', 'INaf', 'IKdr', 'IH', 'IT', 'IL', 'IAHP', 'ICAN']:
				vecToPlotScaled = [i * 1000 for i in vecToPlot] 
				vecToPlot = vecToPlotScaled
				formatter = FormatStrFormatter('%d pA')
				ytickmin = vecInfo[vec]['ytickmin']
				ytickmax = vecInfo[vec]['ytickmax']
				ax[i].spines['right'].set_bounds(ytickmin, ytickmax) # set y axis label bounds 
				yticks = np.linspace(ytickmin, ytickmax, 2)
				ax[i].set_yticks(yticks)

			elif vec in ['ca', 'Ca']:
				vecToPlotScaled = [i * 1000000 for i in vecToPlot]
				vecToPlot = vecToPlotScaled
				formatter = FormatStrFormatter('%d nM')
				ytickmin = vecInfo[vec]['ytickmin']
				ytickmax = vecInfo[vec]['ytickmax']
				ax[i].spines['right'].set_bounds(ytickmin, ytickmax) # set y axis label bounds 
				yticks = np.linspace(ytickmin, ytickmax, 2)
				ax[i].set_yticks(yticks)

			# set units next to y axis ticks
			ax[i].yaxis.set_major_formatter(formatter)

			# set all spines invisible except the right 
			ax[i].spines['bottom'].set_visible(False)
			ax[i].spines['top'].set_visible(False)
			ax[i].spines['left'].set_visible(False)
			ax[i].spines['right'].set_visible(True)

			# set color of right spine
			ax[i].spines['right'].set_color(vecInfo[vec]['color'])

			# remove ticks on x axis 
			for tic in ax[i].xaxis.get_major_ticks():
				tic.tick1On = tic.tick2On = False
				tic.label1On = tic.label2On = False

			# only label the tickmarks on the right spine 
			ax[i].yaxis.set_ticks_position('right')

			# set color of y ticks 
			ax[i].tick_params(axis='y',colors=vecInfo[vec]['color'])


			# PLOT 
			ax[i].plot(t_vec_allCurrents,vecToPlot, color=vecInfo[vec]['color'],label=vecInfo[vec]['label'])

			ax[i].set_ylabel(vecInfo[vec]['label'])

			ax[i].set_title(vecInfo[vec]['label'], x=0.1,y=0.25, color=vecInfo[vec]['color']) 

			# ADDING VERTICAL TIME BARS
			for time_point in time_points:
				ax[i].axvline(x=time_point, color='gray', linestyle='--', linewidth=1)

			# ADDING LABEL FOR X-AXIS ON LAST PLOT
			ax[-1].set_xlabel('Time (ms)')

	plt.show()


if fancyVoltage:
	### FANCIER VOLTAGE PLOTTING 
	t_vec = list(t_vec)
	v_vec = list(v_vec)

	plt.figure(figsize=(6,3))
	ax = plt.gca()
	ax.yaxis.set_label_coords(-0.07, 0.5)
	plt.ylim(-137,10)

	plt.ylabel('Voltage (mV)')
	plt.xlabel('Time (ms)')
	plt.plot(t_vec[37000:80000],v_vec[37000:80000],'k', label='voltage', linewidth=0.8)


	x = [t_vec[37000], stim.delay, stim.delay + stim.dur, t_vec[80000]]
	y = [-83,-83,-83 + 5,-83] 
	plt.step(x,y,'k', linewidth=1)

	add_scalebar(ax,hidey=True,hidex=True,matchx=True,matchy=False,sizey=10,unitsx='ms', unitsy='mV', 
				labely='10 mV\n220pA',loc=3,pad=-2.4)


	plt.show()


if plainVoltage:
	plt.figure()
	plt.plot(t_vec,v_vec,label='voltage')
	plt.title('somatic voltage trace')
	plt.xlabel('time (ms)')
	plt.ylabel('voltage (mV)')
	plt.show()
	plt.close()


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


