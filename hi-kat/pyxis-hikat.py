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
    imager.npix = 1024
    imager.cellsize = '10arcsec'
    imager.weight = 'natural'
    imager.mode = 'channel'
    imager.make_image(dirty=True,restore=restore,column='CORRECTED_DATA',restore_lsm=False,**options)
