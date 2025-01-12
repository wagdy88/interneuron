## Made by Erica Griffith -- 2 compartment thalamic nucleus interneuron w/ oscillatory bursting 
from neuron import h
import json


class sTI_cell:
    def __init__(self, x=0, y=0, z=0, ID=0, ty=0, param_file=None,
                 useJson=False):
        self.x = x
        self.y = y
        self.z = z
        self.ID = ID
        self.ty = ty
        self.useJson = useJson
        self.param_file = param_file

        self.soma = h.Section(name='soma', cell=self)
        self.dend = h.Section(name='dend', cell=self)
        self.dend.connect(self.soma, 0, 0)  # connect dend(0), soma(0)
        for sec in [self.soma, self.dend]:
            sec.Ra = 120

        if self.useJson and param_file:
            # Load parameters from JSON file
            with open(param_file, 'r') as f:
                self.params = json.load(f)
                # Apply JSON parameters to the mechanisms
                for mech, props in self.params['secs']['soma']['mechs'].items():
                    self.soma.insert(mech)  # Insert the mechanism (e.g., 'naf2')
                    for key, value in props.items():
                        setattr(self.soma, f"{key}_{mech}", value)  # Assign parameters
        else:
            # Use default parameters from fullCurrents.py
            self.params = self.default_params()

        self.initsoma()
        self.initdend()

    def default_params(self):
        """ Defines default parameters for the sTI template adapted from fullCurrents.py
        if json is FALSE"""
        #############################################
        ############# INSERT MECHANISMS #############
        #############################################

        # LEAK CURRENT ##
        g_Pass = 2.5e-05 
        # SOMA
        self.soma.insert('Pass')
        self.soma.g_Pass = g_Pass 
        self.soma.erev_Pass = -72 

        # PROXIMAL DENDRITES
        self.dend.insert('Pass')
        self.dend.g_Pass = g_Pass
        self.dend.erev_Pass = -72

        ##FAST SODIUM 
        self.soma.insert('naf2')
        self.soma.gmax_naf2     = 0.042
        self.soma.mvhalf_naf2   = -40
        self.soma.mvalence_naf2 =  5
        self.soma.hvhalf_naf2   = -43
        self.soma.hvalence_naf2 = -6


        # POTASSIUM DELAYED RECTIFIER -- ORIGINAL
        self.soma.insert('kdr2orig')
        self.soma.ek = -95
        self.soma.gmax_kdr2orig     	= 0.1
        self.soma.mvhalf_kdr2orig  	= -31
        self.soma.mvalence_kdr2orig 	=  3.8

        # IH current
        self.soma.insert('iar')
        self.soma.ghbar_iar = 1.3e-4		# 0.13 mS/cm2; correct re: jun.pdf
        self.soma.shift_iar = -0.0

        # ICAN current
        self.soma.insert('icanINT')
        self.soma.gbar_icanINT = 0.0003
        h.beta_icanINT = 0.003							# correct re: jun.pdf
        h.cac_icanINT = 1.1e-04
        self.soma.ratc_icanINT = 1	 						# low-thresh pool (IT)
        self.soma.ratC_icanINT = 0.2							# high-thresh pool (IL)
        h.x_icanINT = 8									# correct re: jun.pdf, if x_ican == "n"

        # IAHP current
        self.soma.insert('iahp')
        self.soma.gkbar_iahp = 0.3
        h.beta_iahp = 0.02								# correct re: jun.pdf
        h.cac_iahp = 8e-04
        self.soma.ratc_iahp = 0.2 							# low-thresh pool (IT)
        self.soma.ratC_iahp = 0.8 							# high-thresh pool (IL)

        # IT current
        self.soma.insert('it2INT')
        self.soma.gcabar_it2INT = 1.0e-4
        self.soma.shift1_it2INT = 7
        h.shift2_it2INT = 0
        h.mx_it2INT = 3.0
        h.hx_it2INT = 1.5
        h.sm_it2INT = 4.8
        h.sh_it2INT = 4.6

        # CALCIUM PUMP FOR "ca" ION POOL - associated with IT
        self.soma.insert('cad_int')
        self.soma.taur_cad_int  = 150
        self.soma.taur2_cad_int  = 80
        self.soma.cainf_cad_int = 1e-8
        self.soma.cainf2_cad_int  = 5.2e-5
        self.soma.kt_cad_int = 0
        self.soma.kt2_cad_int = 0
        self.soma.k_cad_int  = 5e-3
        self.soma.kd_cad_int = 9e-4
        h.kd2_cad_int = 9e-4

        # IL current 
        self.soma.insert('icalINT')
        self.soma.pcabar_icalINT = 0.0006
        h.sh1_icalINT = -10
        h.sh2_icalINT = 0

        # CALCIUM PUMP FOR "Ca" ION POOL -- associated with IL 
        self.soma.insert('Cad_int')
        self.soma.taur_Cad_int  = 150
        self.soma.taur2_Cad_int = 80
        self.soma.Cainf_Cad_int  = 1e-8
        self.soma.Cainf2_Cad_int  = 5.2e-5
        self.soma.kt_Cad_int = 0
        self.soma.kt2_Cad_int = 0
        self.soma.k_Cad_int  = 5e-3
        self.soma.kd_Cad_int = 9e-4
        h.kd2_Cad_int = 9e-4


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

        ####### NEED TO DO THIS ONE WHEN ADDING CALCIUM PUMPS ####### 
        ## RESET INTERNAL AND EXTERNAL CONCENTRATIONS OF "Ca" ION IN h _ion STRUCT
        h.Cai0_Ca_ion = 5e-5
        h.Cao0_Ca_ion = 2


        ## RESET INTERNAL AND EXTERNAL CONCENTRATIONS OF "k2" ION IN h _ion STRUCT
        h.k2i0_k2_ion = 54.5
        h.k2o0_k2_ion = 2.5 

        h.ki0_k_ion = 54.5
        h.ko0_k_ion = 2.5 

    def initsoma(self):
        soma = self.soma
        soma.nseg = 1
        soma.diam = 10
        soma.L = 16
        soma.cm = 1

        ## Inserting mechanisms
        # ## Passive current
        soma.insert('Pass') #ntleak.mod
        # ## Fast sodium 
        soma.insert('naf2')
        # ## DELAYED RECTIFIER POTASSIUM 
        soma.insert('kdr2orig')
        # ## H CURRENT 
        soma.insert('iar')
        # ## ICAN current 
        soma.insert('icanINT')
        # ## IAHP current 
        soma.insert('iahp')
        # ## IT current (low-thresh calcium pool)
        soma.insert('it2INT')
        # # low-thresh calcium pool pump 
        soma.insert('cad_int')
        # ## IL current (high-thresh calcium pool)
        soma.insert('icalINT')
        # ## High-thresh calcium pool pump 
        soma.insert('Cad_int')

    def initdend(self):
        dend = self.dend
        dend.nseg = 1
        dend.diam = 3.25
        dend.L = 240
        dend.cm = 1
        # ## Passive current
        dend.insert('Pass')









