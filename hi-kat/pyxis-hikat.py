import os,sys,time
LSMFITS = 'cube2_4axis.fits'
TDLSEC = 'turbo-sim:hi-only'
LSMCONT = None
RA,DEC = 0,-30
ADD_NOISE = True
NOISE = None
CLEAN = 'operation=hogbom,niter=100'

def get_fitsFiles(fits_prefix):
  ext = fits_prefix.split('.')[-1]
  fits_prefix = fits_prefix.split('.'+ext)[0]
  prefix,frange = fits_prefix.split('#')
  frange = range(*map(int,frange.split(':')))
  files = map(II,['${prefix}%d.$ext'%d for d in frange])
  info('Looking for fits files')
  for item in files:
    if not os.path.exists(item) : abort('FITS file [$item] not found.')
  return files

def simulate(conf='MeerKAT64',lsmfits='$LSMFITS',label=None,lsmcont='$LSMCONT',tdlconf='$TDLCONF',section='$TDLSEC',add_continuum=False,ddid=0,make_new_ms=True,sim_only=False,image_only=False,options={},**kw):
  """ MeqTrees Simulator.
  msname : MS name
  lsmfits : HI sky model (FITS cube)
  tdlconf : MeqTrees TDL configuration  file
  tdlsec : MeqTrees TDL section to execute
  add_continnum : Add continuum sources to the simulation
  lsmcont : Use own contiuum field. Specify name of lsm (txt or Tigger LSM)
  ddid : Data description ID, useful if you simulating chunks of frequency channels into various subbands
  options : Dictionary containing MeqTree pipeliner extra TDL options
  **kw : Extra keyword arguments for makems
  """
  mqt.MULTITHREAD = 8
  #Check if fits image id fit for the simulator
  lsmfits = II(lsmfits)
  swap_stokes_freq(lsmfits)
  (v.RA,v.DEC),freqInfo,naxis = fitsInfo(lsmfits)
  if freqInfo : freq0,dfreq,nchan = freqInfo
  else: abort('$lsmfits has no Frequency information')
  if label is None: label = ''
  if make_new_ms: 
    ms_opts = dict(hours=12,dtime=10,ra=deg2hms(RA),dec=DEC,label=label)
    ms_opts.update(kw)
    makems(conf=conf,freq0=freq0,dfreq=dfreq,nchan=nchan,**ms_opts)
  noise_vis,noise = 0,0
  if not image_only: 
    if ADD_NOISE: 
      noise_vis =  NOISE or compute_vis_noise(sefd=get_sefd(freq0))/10000000
      simcube(cube=lsmfits,noise=noise_vis,column='MODEL_DATA' if ADD_NOISE else 'CORRECTED_DATA')
    noise = noise or 1e-5
  if not sim_only:
    if CLEAN:
      restore = {}
      restore.update(kw)
      for opt in CLEAN.split(','):
        key,val = opt.split('=')
        if key == 'thresh' :
           try : restore['threshold'] = '%.5eJy'%(float(val)*noise)
           except ValueError : abort('Thresh has to be a number.')
        else:
          restore[key] = val
    else: restore = False
    ms.CHANRANGE = 0,nchan-1,1
    imager.IMAGE_CHANNELIZE = 1
    imager.npix = 2048
    imager.cellsize = '1arcsec'
    imager.weight = 'uniform'
    # options['weigh_fov'] = '
    imager.mode = 'channel'
    imager.make_image(dirty=True,restore=restore,column='CORRECTED_DATA',restore_lsm=False,**options)
    # Run source finder[SoFiA]

def reduce(pfct_cube=None,sim_cube=None,extract_srcs=True,flux=True,shape=True):
  """ Runs source finder and generates some plots comparing input and simulated cube"""
  

SOFIA_CFG_Template = '${OUTFILE}sofia_conf.txt'
SOFIA_PATH = '/home/makhathini/sofia/'

def sofia_search(fitsname='${imager.RESTORED_IMAGE}',sofia_conf=None,threshold=4,do_reliability=True,reliability=0.9,merge=3,options={}):
  """ Runs SoFiA source finding pipeline. Only a few options are provided here. 
      For more eleborate settings add options (as you would in a SoFiA configuarion file) 
      via the [options] dictionary or provide a SoFiA configuration file via [sofia_conf]
     -------
     fitsname : Name of fits map on which to run the source finder
     sofia_conf : SoFiA configuration file
     threshold : Peak threshold for source finder [in units of sigma above noise rms]
     do_reliability : Do reliability caltulations
     reliability : Reliability threshold. (0,1]
     merge : merge 
     options : extra options which will directly to sofia configuration file.
  """
  fitsname = interpolate_locals('fitsname')
  swap_stokes_freq(fitsname,freq2stokes=True)
  if not os.path.exists(II(DESTDIR)): x.sh('mkdir -p $DESTDIR')
  if not sofia_conf:
    sofia_conf = II(SOFIA_CFG)
    #abort('>>>> $sofia_conf')
    _SOFIA_DEFAULTS['import']['inFile'] = fitsname
    if os.path.exists(sofia_conf):
      x.sh(II('mv $sofia_conf ${sofia_conf}.old'))
    sofia_std = open(sofia_conf,'w')
    if threshold!=4 and isinstance(threshold,(int,float)):
      _SOFIA_DEFAULTS['threshold']['threshold'] = threshold
    if do_reliability!=True and isinstance(do_reliability,bool):
      _SOFIA_DEFAULTS['steps']['doReliability'] = 'false'
    elif reliability!=0.9 and isinstance(reliabilty,(int,float)):
      _SOFIA_DEFAULTS['reliability']['relThresh'] = reliability
    if merge!=3 and isinstance(merge,int):
      _SOFIA_DEFAULTS['merge']['mergeX'] = merge
      _SOFIA_DEFAULTS['merge']['mergeY'] = merge
      _SOFIA_DEFAULTS['merge']['mergeZ'] = merge
    # Update default SoFia configuration dictionary with user options
    for key,val in options.iteritems():
      a,b = key.split('.')
      if a not in _SOFIA_DEFAULTS.keys():
        abort('Option ${a}.${b} is not recognisable.')
      _SOFIA_DEFAULTS[a][b] = val
    # Generate sofia configuration file
    sofia_std.write('#Sofia autogen configuration file [ceiling-kat]')
    for a,b in  _SOFIA_DEFAULTS.iteritems():
      for key,val in b.iteritems():
         sofia_std.write('\n%s.%s = %s'%(a,key,val))
    sofia_std.close()
  x.sh('python ${SOFIA_PATH}sofia_pipeline.py $sofia_conf')
