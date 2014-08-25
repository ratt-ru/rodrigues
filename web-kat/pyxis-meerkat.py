CFG = 'meerkat_sims.cfg'
MAKE_PSF = False
TDLCONF = 'tdlconf.profiles'
SECTION = 'turbo-sim:default'
ADD_NOISE = True
NOISE = None
LSM = None
mqt.MULTITHREAD = 4
COLUMN = 'DATA'
FITS = False
CLEAN =True

def readCFG(cfg='$CFG'):
  cfg_std = open(II(cfg))
  params = {}
  for line in cfg_std.readlines():
    if line!='\n' or line.startswith('#')!=False:
       key = line.split('=')[0]
       val = line.split('=')[-1].split()[0]
       params[key] = val
  options = dict(ms_={},cr_={},im_={},dc_={})
  for key in params.keys():
   found = False
   for item in options.keys():
     if not found:
      if key.startswith(item):
        found=True
        options[item][key.split(item)[-1]] = params[key]
        del params[key]
  if params['skytype'] == 'tiggerlsm': v.LSM = params['skyname']
  elif params['skytype'] == 'FITS' : v.FITS = params['skyname']
  else : USING_SIAMESE = True
  if params['add_noise'] == 'True' : NOISE = eval(params['vis_noise_std'])
  v.MAKE_PSF = eval(params['make_psf_map'])
  v.OUTPUT_TYPE = params['output']
  v.COLUMN = params['column']
  v.CLEAN = eval(params['clean'])
  return options

def simulate(lsmname='$LSM',tdlconf='$TDLCONF',section='$SECTION',freq0=1400e6,options={},**kw):
  """ Simulates visibilities into an MS """
  if LSM: options['me.sky.tiggerskymodel'] = LSM
  options['noise_stddev'] = NOISE or compute_vis_noise(sefd=get_sefd(freq0))
  options['ms_sel.output_column'] = COLUMN
  mqt.msrun('turbo-sim.py',job='_tdl_job_1_simulate_MS',config=tdlconf,section=section,options=options)

def image(msname='$MS',lsmname='$LSM',use_imager='LWIMAGER',restore=False,options={},**kw):
  """ Images MS"""
  if restore : 
     ms.copycol() # Copy content of DATA to CORRECTED_DATA if making clean map
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
  ms_opts['nchan'] = eval(ms_opts['nchan']) + 1
  makems(shift=True,**ms_opts) # simulate empty MS
  ms.CHANRANGE = 0,5,1
  simulate(freq0=freq0)
  restore = CLEAN
  if restore : restore = clean_opts
  info(im_opts)
  if im_opts['img_chanstep'] == 'None' : im_opts['img_chanstep'] = ms_opts['nchan']
  if clean_opts['operation'] != 'multiscale' : 
    del clean_opts['nscales']
    del clean_opts['usevector']
  im_opts['chanstart'] = eval(im_opts['chanstart']) + 1
  im_opts['img_chanstart'] = eval(im_opts['img_chanstart']) + 1
  image(restore=restore,options=im_opts)
