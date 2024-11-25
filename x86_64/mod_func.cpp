#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _cp2_reg(void);
extern void _cp_reg(void);
extern void _Iahp_reg(void);
extern void _Ican_reg(void);
extern void _IL_reg(void);
extern void _kdr2_orig_reg(void);
extern void _naf2_reg(void);
extern void _nthh_reg(void);
extern void _ntIh_reg(void);
extern void _ntleak_reg(void);
extern void _ntt_int_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"cp2.mod\"");
    fprintf(stderr, " \"cp.mod\"");
    fprintf(stderr, " \"Iahp.mod\"");
    fprintf(stderr, " \"Ican.mod\"");
    fprintf(stderr, " \"IL.mod\"");
    fprintf(stderr, " \"kdr2_orig.mod\"");
    fprintf(stderr, " \"naf2.mod\"");
    fprintf(stderr, " \"nthh.mod\"");
    fprintf(stderr, " \"ntIh.mod\"");
    fprintf(stderr, " \"ntleak.mod\"");
    fprintf(stderr, " \"ntt_int.mod\"");
    fprintf(stderr, "\n");
  }
  _cp2_reg();
  _cp_reg();
  _Iahp_reg();
  _Ican_reg();
  _IL_reg();
  _kdr2_orig_reg();
  _naf2_reg();
  _nthh_reg();
  _ntIh_reg();
  _ntleak_reg();
  _ntt_int_reg();
}

#if defined(__cplusplus)
}
#endif
