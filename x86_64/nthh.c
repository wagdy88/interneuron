/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__hh2
#define _nrn_initial _nrn_initial__hh2
#define nrn_cur _nrn_cur__hh2
#define _nrn_current _nrn_current__hh2
#define nrn_jacob _nrn_jacob__hh2
#define nrn_state _nrn_state__hh2
#define _net_receive _net_receive__hh2 
#define evaluate_fct evaluate_fct__hh2 
#define states states__hh2 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gnabar _p[0]
#define gnabar_columnindex 0
#define gkbar _p[1]
#define gkbar_columnindex 1
#define vtraub _p[2]
#define vtraub_columnindex 2
#define inaf _p[3]
#define inaf_columnindex 3
#define ikf _p[4]
#define ikf_columnindex 4
#define m _p[5]
#define m_columnindex 5
#define h _p[6]
#define h_columnindex 6
#define n _p[7]
#define n_columnindex 7
#define ena _p[8]
#define ena_columnindex 8
#define ek _p[9]
#define ek_columnindex 9
#define Dm _p[10]
#define Dm_columnindex 10
#define Dh _p[11]
#define Dh_columnindex 11
#define Dn _p[12]
#define Dn_columnindex 12
#define ina _p[13]
#define ina_columnindex 13
#define ik _p[14]
#define ik_columnindex 14
#define il _p[15]
#define il_columnindex 15
#define tadj _p[16]
#define tadj_columnindex 16
#define _g _p[17]
#define _g_columnindex 17
#define _ion_ena	*_ppvar[0]._pval
#define _ion_ina	*_ppvar[1]._pval
#define _ion_dinadv	*_ppvar[2]._pval
#define _ion_ek	*_ppvar[3]._pval
#define _ion_ik	*_ppvar[4]._pval
#define _ion_dikdv	*_ppvar[5]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_evaluate_fct(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_hh2", _hoc_setdata,
 "evaluate_fct_hh2", _hoc_evaluate_fct,
 0, 0
};
 /* declare global and static user variables */
#define exptemp exptemp_hh2
 double exptemp = 36;
#define h_exp h_exp_hh2
 double h_exp = 0;
#define h_inf h_inf_hh2
 double h_inf = 0;
#define m_exp m_exp_hh2
 double m_exp = 0;
#define m_inf m_inf_hh2
 double m_inf = 0;
#define n_exp n_exp_hh2
 double n_exp = 0;
#define n_inf n_inf_hh2
 double n_inf = 0;
#define tau_n tau_n_hh2
 double tau_n = 0;
#define tau_h tau_h_hh2
 double tau_h = 0;
#define tau_m tau_m_hh2
 double tau_m = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gnabar_hh2", "mho/cm2",
 "gkbar_hh2", "mho/cm2",
 "vtraub_hh2", "mV",
 "inaf_hh2", "mA/cm2",
 "ikf_hh2", "mA/cm2",
 0,0
};
 static double delta_t = 1;
 static double h0 = 0;
 static double m0 = 0;
 static double n0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "exptemp_hh2", &exptemp_hh2,
 "m_inf_hh2", &m_inf_hh2,
 "h_inf_hh2", &h_inf_hh2,
 "n_inf_hh2", &n_inf_hh2,
 "tau_m_hh2", &tau_m_hh2,
 "tau_h_hh2", &tau_h_hh2,
 "tau_n_hh2", &tau_n_hh2,
 "m_exp_hh2", &m_exp_hh2,
 "h_exp_hh2", &h_exp_hh2,
 "n_exp_hh2", &n_exp_hh2,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(NrnThread*, _Memb_list*, int);
static void nrn_state(NrnThread*, _Memb_list*, int);
 static void nrn_cur(NrnThread*, _Memb_list*, int);
static void  nrn_jacob(NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(NrnThread*, _Memb_list*, int);
static void _ode_matsol(NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[6]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"hh2",
 "gnabar_hh2",
 "gkbar_hh2",
 "vtraub_hh2",
 0,
 "inaf_hh2",
 "ikf_hh2",
 0,
 "m_hh2",
 "h_hh2",
 "n_hh2",
 0,
 0};
 static Symbol* _na_sym;
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 18, _prop);
 	/*initialize range parameters*/
 	gnabar = 0.135;
 	gkbar = 0.27;
 	vtraub = -63;
 	_prop->param = _p;
 	_prop->param_size = 18;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 7, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[4]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[5]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _nthh_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("na", -10000.);
 	ion_reg("k", -10000.);
 	_na_sym = hoc_lookup("na_ion");
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 18, 7);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 hh2 /home/mohamed/myprojects/interneuron/data/fullCurrents/nthh.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int evaluate_fct(double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[3], _dlist1[3];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   evaluate_fct ( _threadargscomma_ v ) ;
   Dm = ( m_inf - m ) / tau_m ;
   Dh = ( h_inf - h ) / tau_h ;
   Dn = ( n_inf - n ) / tau_n ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 evaluate_fct ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_m )) ;
 Dh = Dh  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_h )) ;
 Dn = Dn  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_n )) ;
  return 0;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   evaluate_fct ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_m)))*(- ( ( ( m_inf ) ) / tau_m ) / ( ( ( ( - 1.0 ) ) ) / tau_m ) - m) ;
    h = h + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_h)))*(- ( ( ( h_inf ) ) / tau_h ) / ( ( ( ( - 1.0 ) ) ) / tau_h ) - h) ;
    n = n + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_n)))*(- ( ( ( n_inf ) ) / tau_n ) / ( ( ( ( - 1.0 ) ) ) / tau_n ) - n) ;
   }
  return 0;
}
 
static int  evaluate_fct (  double _lv ) {
   double _la , _lb , _lv2 ;
 _lv2 = _lv - vtraub ;
   _la = 0.32 * ( 13.0 - _lv2 ) / ( exp ( ( 13.0 - _lv2 ) / 4.0 ) - 1.0 ) ;
   _lb = 0.28 * ( _lv2 - 40.0 ) / ( exp ( ( _lv2 - 40.0 ) / 5.0 ) - 1.0 ) ;
   tau_m = 1.0 / ( _la + _lb ) / tadj ;
   m_inf = _la / ( _la + _lb ) ;
   _la = 0.128 * exp ( ( 17.0 - _lv2 ) / 18.0 ) ;
   _lb = 4.0 / ( 1.0 + exp ( ( 40.0 - _lv2 ) / 5.0 ) ) ;
   tau_h = 1.0 / ( _la + _lb ) / tadj ;
   h_inf = _la / ( _la + _lb ) ;
   _la = 0.032 * ( 15.0 - _lv2 ) / ( exp ( ( 15.0 - _lv2 ) / 5.0 ) - 1.0 ) ;
   _lb = 0.5 * exp ( ( 10.0 - _lv2 ) / 40.0 ) ;
   tau_n = 1.0 / ( _la + _lb ) / tadj ;
   n_inf = _la / ( _la + _lb ) ;
   m_exp = 1.0 - exp ( - dt / tau_m ) ;
   h_exp = 1.0 - exp ( - dt / tau_h ) ;
   n_exp = 1.0 - exp ( - dt / tau_n ) ;
    return 0; }
 
static void _hoc_evaluate_fct(void) {
  double _r;
   _r = 1.;
 evaluate_fct (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 3;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ena = _ion_ena;
  ek = _ion_ek;
     _ode_spec1 ();
   }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 3; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 ();
 }
 
static void _ode_matsol(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ena = _ion_ena;
  ek = _ion_ek;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_na_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 2, 4);
   nrn_update_ion_pointer(_k_sym, _ppvar, 3, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 4, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 5, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
  n = n0;
 {
   
/*VERBATIM*/
	ena = _ion_ena;
	ek = _ion_ek;
 tadj = pow( 3.0 , ( ( celsius - exptemp ) / 10.0 ) ) ;
   evaluate_fct ( _threadargscomma_ v ) ;
   m = m_inf ;
   h = h_inf ;
   n = n_inf ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  ena = _ion_ena;
  ek = _ion_ek;
 initmodel();
  }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   inaf = gnabar * m * m * m * h * ( v - ena ) ;
   ikf = gkbar * n * n * n * n * ( v - ek ) ;
   ina = inaf ;
   ik = ikf ;
   }
 _current += ina;
 _current += ik;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  ena = _ion_ena;
  ek = _ion_ek;
 _g = _nrn_current(_v + .001);
 	{ double _dik;
 double _dina;
  _dina = ina;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ina += ina ;
  _ion_ik += ik ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  ena = _ion_ena;
  ek = _ion_ek;
 { error =  states();
 if(error){fprintf(stderr,"at line 79 in file nthh.mod:\n	SOLVE states METHOD cnexp\n"); nrn_complain(_p); abort_run(error);}
 }  }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = m_columnindex;  _dlist1[0] = Dm_columnindex;
 _slist1[1] = h_columnindex;  _dlist1[1] = Dh_columnindex;
 _slist1[2] = n_columnindex;  _dlist1[2] = Dn_columnindex;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/home/mohamed/myprojects/interneuron/data/fullCurrents/nthh.mod";
static const char* nmodl_file_text = 
  ":TITLE Hippocampal HH channels\n"
  ":\n"
  ": Fast Na+ and K+ currents responsible for action potentials\n"
  ": Iterative equations.  final check on save\n"
  ":\n"
  ": Equations modified by Traub, for Hippocampal Pyramidal cells, in:\n"
  ": Traub & Miles, Neuronal Networks of the Hippocampus, Cambridge, 1991\n"
  ":\n"
  ": range variable vtraub adjust threshold\n"
  ":\n"
  ": Written by Alain Destexhe, Salk Institute, Aug 1992\n"
  ":\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX hh2\n"
  "	USEION na READ ena WRITE ina\n"
  "	USEION k READ ek WRITE ik\n"
  "	RANGE gnabar, gkbar, vtraub, inaf, ikf\n"
  "	GLOBAL m_inf, h_inf, n_inf\n"
  "	GLOBAL tau_m, tau_h, tau_n\n"
  "	GLOBAL m_exp, h_exp, n_exp, exptemp\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	gnabar	= .135 	(mho/cm2)\n"
  "	gkbar	= .270 	(mho/cm2)\n"
  "\n"
  "	ena	= 50	(mV)\n"
  "	ek	= -95	(mV)\n"
  "	celsius = 36    (degC)\n"
  "        exptemp = 36\n"
  "	dt              (ms)\n"
  "	v               (mV)\n"
  "	vtraub	= -63	(mV)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	m h n\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	VERBATIM\n"
  "	ena = _ion_ena;\n"
  "	ek = _ion_ek;\n"
  "	ENDVERBATIM\n"
  "	tadj = 3.0 ^ ((celsius-exptemp)/ 10 )\n"
  "	evaluate_fct(v)\n"
  "	m = m_inf\n"
  "        h = h_inf\n"
  "	n = n_inf\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ina	(mA/cm2)\n"
  "	ik	(mA/cm2)\n"
  "	inaf	(mA/cm2)\n"
  "	ikf	(mA/cm2)\n"
  "        il	(mA/cm2)\n"
  "	m_inf\n"
  "	h_inf\n"
  "	n_inf\n"
  "	tau_m\n"
  "	tau_h\n"
  "	tau_n\n"
  "	m_exp\n"
  "	h_exp\n"
  "	n_exp\n"
  "	tadj\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states METHOD cnexp\n"
  "	inaf = gnabar * m*m*m*h * (v - ena)\n"
  "	ikf  = gkbar * n*n*n*n * (v - ek)\n"
  "        ina = inaf\n"
  "        ik  = ikf\n"
  "}\n"
  "\n"
  "DERIVATIVE states {   : exact Hodgkin-Huxley equations\n"
  "	evaluate_fct(v)\n"
  "	m' = (m_inf - m) / tau_m\n"
  "	h' = (h_inf - h) / tau_h\n"
  "	n' = (n_inf - n) / tau_n\n"
  "}\n"
  "\n"
  ":   PROCEDURE states() {	: exact when v held constant\n"
  ":           evaluate_fct(v)\n"
  ":           m = m + m_exp * (m_inf - m)\n"
  ":           h = h + h_exp * (h_inf - h)\n"
  ":           n = n + n_exp * (n_inf - n)\n"
  ":           VERBATIM\n"
  ":           return 0;\n"
  ":           ENDVERBATIM\n"
  ":   }\n"
  "\n"
  "UNITSOFF\n"
  "\n"
  "PROCEDURE evaluate_fct(v(mV)) { LOCAL a,b,v2\n"
  "\n"
  "\n"
  "	v2 = v - vtraub : convert to traub convention\n"
  "\n"
  "	a = 0.32 * (13-v2) / ( exp((13-v2)/4) - 1)\n"
  "	b = 0.28 * (v2-40) / ( exp((v2-40)/5) - 1)\n"
  "	tau_m = 1 / (a + b) / tadj\n"
  "	m_inf = a / (a + b)\n"
  "\n"
  "	a = 0.128 * exp((17-v2)/18)\n"
  "	b = 4 / ( 1 + exp((40-v2)/5) )\n"
  "	tau_h = 1 / (a + b) / tadj\n"
  "	h_inf = a / (a + b)\n"
  "\n"
  "	a = 0.032 * (15-v2) / ( exp((15-v2)/5) - 1)\n"
  "	b = 0.5 * exp((10-v2)/40)\n"
  "	tau_n = 1 / (a + b) / tadj\n"
  "	n_inf = a / (a + b)\n"
  "\n"
  "	m_exp = 1 - exp(-dt/tau_m)\n"
  "	h_exp = 1 - exp(-dt/tau_h)\n"
  "	n_exp = 1 - exp(-dt/tau_n)\n"
  "}\n"
  "\n"
  "UNITSON\n"
  ;
#endif
