import ms,mqt,lsm,imager
MAKE_PSF = False
mqt.MULTITHREAD = 8
COLUMN = 'DATA'
FITS = False
CLEAN = False
LSM = None
NOISE = None

def simulate(msname='$MS',lsmname='$LSM',tdlconf='$TDLCONF',section='$TDLSEC',freq0=1400e6,options={},**kw):
  """ Simulates visibilities into an MS """
  v.MS,v.LSM = interpolate_locals('msname lsmname')
  if LSM: 
    options['tiggerlsm.filename'] = LSM
  options['noise_stddev'] = NOISE or compute_vis_noise(sefd=get_sefd(freq0))
  options['ms_sel.output_column'] = COLUMN
  options['ms_sel.msname'] = msname
  if USING_SIAMESE : section = 'turbo-sim:default'
  options['ms_sel.select_channels'] = 0
  mqt.run('turbo-sim.py',job='_tdl_job_1_simulate_MS',config=tdlconf,section=section,options=options)

def image(msname='$MS',lsmname='$LSM',use_imager='LWIMAGER',restore=False,options={},**kw):
  """ Images MS"""
  imager.cellsize = '1arcsec' 
  if restore : 
     if COLUMN!='CORRECTED_DATA' :ms.copycol(fromcol=COLUMN) # Copy content of DATA to CORRECTED_DATA if making clean map
     v.COLUMN = 'CORRECTED_DATA' # make sure to image corrected data
  if NCHAN>1 : 
    start = 1
    step = CHANNELIZE or NCHAN
    temp = dict(nchan=NCHAN,img_nchan=(NCHAN-1)/step,chanstart=0,img_chanstart=1,chanstep=1,img_chanstep=step)
    options.update(temp)
  imager.make_image(restore=restore,column=COLUMN,restore_lsm=False,**options)

def make_psf(options={}):
  """ make PSF map"""
  compute_psf_and_noise(noise_map=False)

def azishe(cfg='$CFG',make_image=True,psf='$MAKE_PSF'):
  if CLEAN : v.COLUMN = 'CORRECTED_DATA'
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
  freq0 = float(ms_opts['freq0'])
  nchan =  int(ms_opts['nchan'])
  if nchan>1 : 
   ms_opts['nchan'],shift = int(ms_opts['nchan']) + 1,True
   nchan +=1
  else: shift = False
  v.NCHAN = nchan
  makems(shift=shift,**ms_opts) # simulate empty MS
  ms.CHANRANGE = 0,nchan-1,1
  simulate(freq0=freq0)
  #imager.CHANNELIZE = 1
  restore = CLEAN
  if restore : 
    restore = clean_opts
    if clean_opts['operation'] != 'multiscale' : 
      if 'nscales' in clean_opts.keys(): del clean_opts['nscales']
      if 'uservector' in clean_opts.keys(): del clean_opts['uservector']
  try : imager.weight = im_opts['weight']
  except KeyError : imager.weight= 'uniform'
  imager.wprojplanes = 128
  imager.cellsize = '%sarcsec'%(im_opts['cellsize'])
  imager.stokes = im_opts['stokes'].upper()
  del im_opts['cellsize'],im_opts['stokes']
  image(restore=restore,options=im_opts)
