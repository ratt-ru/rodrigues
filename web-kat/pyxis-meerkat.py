MAKE_PSF = False
mqt.MULTITHREAD = 8
COLUMN = 'DATA'
FITS = False
CLEAN =True

def simulate(lsmname='$LSM',tdlconf='$TDLCONF',section='$TDLSEC',freq0=1400e6,options={},**kw):
  """ Simulates visibilities into an MS """
  if LSM: 
    options['tiggerlsm.filename'] = LSM
  options['noise_stddev'] = NOISE or compute_vis_noise(sefd=get_sefd(freq0))
  #options['ms_sel.output_column'] = COLUMN
  mqt.msrun('turbo-sim.py',job='_tdl_job_1_simulate_MS',config=tdlconf,section=section,options=options)

def image(msname='$MS',lsmname='$LSM',use_imager='LWIMAGER',restore=False,options={},**kw):
  """ Images MS"""
  if restore : 
     #ms.copycol() # Copy content of DATA to CORRECTED_DATA if making clean map
     options['data'] = 'CORRECTED_DATA' # make sure to image corrected data
  imager.make_image(restore=restore,restore_lsm=False,**options)

def make_psf(options={}):
  """ make PSF map"""
  compute_psf_and_noise(noise_map=False)

def azishe(cfg='$CFG',make_image=True,psf='$MAKE_PSF'):
  _cfg = readCFG(cfg)
  ms_opts = _cfg['ms_']
  cr_opts = _cfg['cr_']
  im_opts = _cfg['im_']
  clean_opts = _cfg['dc_']
  # ------------convret ra from degrees to hms for MAKEMS------------
  ra = float(ms_opts['ra'])
  ra = ra * 24/360.
  hrs = ra - ra%1
  mins_tmp  = (ra - hrs)%1 * 60
  mins = mins_tmp - mins_tmp%1
  secs = (mins_tmp - mins)*60
  ra_str = '%d:%d:%.2f'%(hrs,mins,secs)
  ms_opts['ra'] = ra_str
  #--------------------------------------------------------
  freq0 = eval(ms_opts['freq0'])
  nchan =  eval(ms_opts['nchan'])
  if nchan>1 : ms_opts['nchan'] = eval(ms_opts['nchan']) + 1
  makems(shift=nchan>1,**ms_opts) # simulate empty MS
  ms.CHANRANGE = 0,nchan,1
  simulate(freq0=freq0)
  restore = CLEAN
  if restore : restore = clean_opts
  if im_opts['img_chanstep'] == 'None' : im_opts['img_chanstep'] = ms_opts['nchan']
  if clean_opts['operation'] != 'multiscale' : 
    del clean_opts['nscales']
    del clean_opts['usevector']
  if nchan>1 : 
    im_opts['chanstart'] = eval(im_opts['chanstart']) + 1
    im_opts['img_chanstart'] = eval(im_opts['img_chanstart']) + 1
  imager.weight = im_opts['weight']
  image(restore=restore,options=im_opts)
