
import cPickle
import numpy
import pyfits,pyrap.tables
import math

from scipy.ndimage.measurements import *
# important to import from Pyxis, as this takes care of missing displays etc.

DEG = 180/math.pi;
ARCMIN = DEG*60;
ARCSEC = ARCMIN*60;
FWHM = math.sqrt(math.log(256));  # which is 2.3548;
import Pyxis
import imager
import ms
import mqt
import std

from Pyxis.ModSupport import *

SIMSCRIPT = "turbo-sim.py"
SIMJOB = "_tdl_job_1_simulate_MS"

imager.npix = 512
imager.cellsize = ".5arcsec"
imager.mode = "channel"
imager.stokes = "I"
imager.wprojplanes = 0
imager.weight = "natural"
imager.cachesize = "32000"
imager.LWIMAGER_PATH = "lwimager" # 
imager.DIRTY_IMAGE_Template = "${OUTFILE}.dirty.fits"
imager.RESTORED_IMAGE_Template = "${OUTFILE}.restored.fits"

# destination directory: if MS is foo.MS, then directory is [OUTDIR]/plots-foo[-LABEL] 
DESTDIR_Template = '${OUTDIR>/}plots-${MS:BASE}'

# base output file: DESTDIR/foo
OUTFILE_Template = '${DESTDIR>/}${MS:BASE}${-<LABEL}'

# this means: if MS is unset, no logfile. If MS is foo.MS, logfile will be set to [DESTDIR/]log-foo.txt
LOG_Template = lambda: II("${DESTDIR>/}log-${MS:BASE}.txt") if MS else II("${OUTDIR>/}log-ska1sims.txt");

WEIGHTS = "uniform"


OBSDIR = 'observatories'
_OBS = {
      'meerkat':'MeerKAT64_ANTENNAS',
      'kat-7':'KAT7_ANTENNAS',
      'jvla-a':'VLAA_ANTENNAS',
      'wsrt':'WSRT_ANTENNAS'
}

KATDIR = 'katalog'
_KATALOG = {
         'nvss6deg':'nvss6deg.lsm.html',
         'scubed1deg':'scubed1deg.lsm.html',
         'rand_pnts':'random_pts.txt',
         'rand_mix':'random.txt',
         'rand_mix_fits':'random.fits',
         '3c147_no_core':'3c147_field_no_3c147.lsm.html',
         '3c147_field':'3c147.lsm.html',
}
_SKYTYPE = {'tigger-lsm':'.lsm.html','ascii':'.txt','fits':'.fits'}

MEASURE_PSF = False
MEASURE_SIDELOBES = False
MEASURE_NOISE = True
SIDELOBES_CELL_ARCSEC = 0.5
SIDELOBES_R0_ARCSEC = 900
SIDELOBES_R1_ARCSEC = 1800
RFI = False # do sims with RFI as well
# use first channel of MS by default
ms.CHANRANGE = 0

NPIX_PSF = 1024
CELLSIZE_PSF = ".05arcsec"

# these are used to compute per-visibility noise
#SEFD = 528 
SEFD = 831 #MeerKAT band1b
INTEGRATION = None # None means look in MS 
BANDWIDTH = None   # None means look in MS
WAVELENGTH = 0.21
BASEFREQ = 1.4e+9
STATSFILE_Template = "${OUTDIR>/}genstats.py"

STATQUALS = ()

TDLCONF = 'tdlconf.profiles'
CFG = 'meerkat_sims.cfg'
CHANNELIZE = 0
NCHAN = 1
def str2bool(val):
    if val.lower() in 'true yes 1'.split():
        return True
    else: 
        return False

STAND_ALONE_DECONV = ['moresane']

def readCFG(cfg='$CFG'):
    cfg_std = open(II(cfg))
    params = {}
    for line in cfg_std.readlines():
        if not line.startswith('#'):
            line = line.strip()
            key = line.split('=')[0]
            key = key.replace('_dash_','-')
            val = line.split('=')[-1]
            if not line.endswith('='):
                val = val.split(' ')[0]
                if val.lower()!='none':
                    params[key] = val

    options = dict(ms_={},cr_={},im_={},lwimager_={},wsclean_={},casa_={},moresane_={})
    for key in params.keys():
        found = False
        for item in options.keys():
            if not found:
                if key.startswith(item):
                    found=True
                    options[item][key.split(item)[-1]] = params[key].lower()
                    del params[key]
    global OBSERVATORY,POSITIONS,MS_LABEL
    OBSERVATORY = params['observatory'].lower()
    POSITIONS = '%s/%s'%(OBSDIR,_OBS[OBSERVATORY])
    if OBSERVATORY.startswith('jvla'):
       MS_LABEL = OBSERVATORY
       OBSERVATORY = 'VLA'

    global FITS,TIGGER,TDLSEC,KATALOG,SELECT
    skytype = params['skytype'].lower()
    if skytype in ['tigger-lsm','ascii']:  
        TIGGER = True
        v.LSM = params['sky_model']+_SKYTYPE[skytype]
        x.sh('cp %s $LSM'%(params['sky_model']))
        TDLSEC = 'turbo-sim:custom'
    elif skytype =='fits':
        FITS = True
        v.LSM = params['skyname']+_SKYTYPE[skytype]
        x.sh('cp %s $LSM'%(params['sky_model']))
    elif skytype=='katalog':
        TDLSEC = 'turbo-sim:custom'
        v.LSM = '%s/%s'%(KATDIR,_KATALOG[params['katalog_id']])
        if LSM.endswith('.fits'):
            FITS = True
        else:
            TIGGER = True
    elif skytype in ['nvss6deg','scubed1deg']:
        TIGGER = True
        TDLSEC = 'turbo-sim:custom'
        v.LSM = 'katalog/%s.lsm.html'%skytype

    if str2bool(params['add_noise']):
        visnoise = float(params['vis_noise_std']) 
        v.NOISE = visnoise if visnoise else None;

    global OUTPUT_TYPE,COLUMN
    OUTPUT_TYPE = params['output']
    #COLUMN = params['column'].upper()
    _deconv = []
    for dcv in 'lwimager wsclean moresane casa'.split():
       if str2bool(params[dcv]):
          _deconv.append(dcv.lower())
    
#    own_tdl = str2bool(params['upload_tdl'])
#    if own_tdl:
#        v.TDLCONF = params['tdlconf']
#        v.TDLSEC = params['tdlsection']

    global RADIUS,FLUXRANGE
    RADIUS = float(params['radius'])
    FLUXRANGE = params['fluxrange'].split('-')
    if len(FLUXRANGE)>1:
        FLUXRANGE = map(float,FLUXRANGE)
    elif len(FLUXRANGE)==1:
        FLUXRANGE = [0,float(FLUXRANGE[0])]
    _imager = params['imager'].lower()

    global CHANNELIZE
    CHANNELIZE = int(params['channelise'])

    return options,_imager,_deconv


def d_or_h_ms2deg(coord,hms=True):
    tmp = ''
    if coord.startswith('-'):
       sign = -1
    else:
       sign = 1
    for i in coord:
        if i.isdigit():
            tmp += i
        else:
            tmp += ' '
    coord = map(float,tmp.split())
    deg = 0
    for i,val in enumerate(coord):
        deg += val*60**i
    return sign*deg*15 if hms else sign*deg

_SEFD = {}
_SEFD['MKT'] = {'1b':831,'2':551}

def get_sefd(freq=650e6):
    freq0 = freq*1e-6 # work in MHz
    if np.logical_and(freq0>=580,freq0<=1020): 
        band = '1b'
    elif np.logical_and(freq0>=900,freq0<=1670): 
        band = '2'
    else : 
        warn('$freq0 MHz is is not within MeerKAT frequency range. Using SEFD for band 1b')
        band = '1b'
    return _SEFD['MKT'][band]

def clearstats ():
    if exists(STATSFILE):
        info("removing $STATSFILE");
        x.sh("rm $STATSFILE");

import fcntl

def _statsfile ():
    """Initializes stats file (if not existing), returns open file""";
    ff = file(STATSFILE,"a");
    fcntl.flock(ff,fcntl.LOCK_EX);
    # seek to end of file, if empty, make header
    ff.seek(0,2);
    if not ff.tell():
        ff.write("""# auto-generated noise stats file\n""");
        ff.write("""settings = dict(%s)\n"""%",".join([ "%s=%s"%(key,repr(val)) for key,val in globals().iteritems()
                if not callable(val) and key.upper() == key ]));
        ff.write("noisestats = {}\n");
    return ff;

def _writestat (name,value,*qualifiers):
    ff = _statsfile();
    subsets = list(STATQUALS) + list(qualifiers);
    subsets = ','.join(map(repr,subsets));
    ff.write("noisestats.setdefault('%s',{})[%s] = %s\n"%(name,subsets,repr(value)));
    fcntl.flock(ff,fcntl.LOCK_UN);

def compute_vis_noise (noise=0,sefd=SEFD):
  """Computes nominal per-visibility noise"""
  tab = ms.ms();
  spwtab = ms.ms(subtable="SPECTRAL_WINDOW");
  global BASEFREQ
  BASEFREQ = freq0 = spwtab.getcol("CHAN_FREQ")[ms.SPWID,0];
  global WAVELENGTH
  WAVELENGTH = 300e+6/freq0
  bw = BANDWIDTH or spwtab.getcol("CHAN_WIDTH")[ms.SPWID,0];
  dt = INTEGRATION or tab.getcol("EXPOSURE",0,1)[0];
  dtf = (tab.getcol("TIME",tab.nrows()-1,1)-tab.getcol("TIME",0,1))[0]
  # close tables properly, else the calls below will hang waiting for a lock...
  tab.close();
  spwtab.close();
  info(">>> $MS freq %.2f MHz (lambda=%.2fm), bandwidth %.2g kHz, %.2fs integrations, %.2fh synthesis"%(freq0*1e-6,WAVELENGTH,bw*1e-3,dt,dtf/3600));
  _writestat("freq0",freq0);
  _writestat("wavelength",WAVELENGTH);
  _writestat("bw",bw);
  _writestat("synthesis_time",dtf);
  _writestat("integration",dt);
  if not noise:
    noise = sefd/math.sqrt(2*bw*dt);
    info(">>> SEFD of %.2f Jy gives per-visibility noise of %.2f mJy"%(sefd,noise*1000));
  else:
    info(">>> using per-visibility noise of %.2f mJy"%(noise*1000));
  _writestat("vis_noise",noise);
  return noise;

def get_weight_opts (weight):
  """Parses a weight specification such as "robust=0,fov=10,taper=1" into a dict 
  of lwimager options. Used by compute_psf_and_noise() below"""
  opts = dict(weight=weight)
  # weight could have additional options: robust=X, fov=X, taper=X
  ws = weight.split(",");
  wo = dict([ keyval.split("=") for keyval in ws if "=" in keyval ]);
  opts['weight'] = ws[0] if "=" not in ws[0] else ws[0].split("=")[0];
  robust = wo.get('robust',wo.get('briggs',None));
  if robust is not None:
    opts['robust'] = robust = float(robust);
  if 'fov' in wo:
    fov = float(wo['fov']);
    opts['weight_fov'] = "%farcmin"%fov;
  taper = float(wo.get('taper',0)) or TAPER;
  if taper:
    opts['filter'] = "%farcsec,%farcsec,0deg"%(taper,taper);
  weight_txt = opts['weight'];
  quals = [ weight_txt ];  # qualifiers for _writestat
  if opts['weight'] != "natural":
    #opts.setdefault('weight_fov',FOV);
    if 'robust' in opts:
      weight_txt += "%+.1f"%opts['robust'];
      quals = [ "robust=%.1f"%opts['robust'] ];
    if 'weight_fov' in opts:
      info('>>>> %s'%(opts['weight_fov']))
      weight_txt += " FoV %s"%opts['weight_fov'].replace("arcsec","\"").replace("arcmin","'");
      quals.append("fov=%s"%opts['weight_fov']);
  if taper:
    weight_txt += " taper %.1f\""%taper;
    quals.append("taper=%.1f"%taper);
  else:
    quals.append("taper=0");
  return opts,weight_txt,quals;

def measure_psf (psffile,arcsec_size=4,savefig=None,title=None):
  ff = pyfits.open(psffile);
  pp = ff[0].data.T[:,:,0,0]
  secpix = abs(ff[0].header['CDELT1']*3600)
  ## get midpoint and size of cross-sections
  xmid,ymid = maximum_position(pp)
  ## print xmid,ymid,pp[xmid,ymid]
  sz = int(arcsec_size/secpix);
  xsec = pp[xmid-sz:xmid+sz,ymid]
  ysec = pp[xmid,ymid-sz:ymid+sz]
  axis = numpy.arange(-sz,sz)*secpix
  def fwhm (tsec):
    from scipy.interpolate import interp1d 
    tmid = len(tsec)/2;
    # find first minima off the peak, and flatten cross-section outside them
#    print tsec,tmid
    xmin = minimum_position(tsec[:tmid])[0];
    tsec[:xmin] = tsec[xmin];
    xmin = minimum_position(tsec[tmid:])[0];
    tsec[tmid+xmin:] = tsec[tmid+xmin];
    if tsec[0] > .5 or tsec[-1] > .5:
      warn("PSF FWHM over %2.f arcsec"%(arcsec_size*2));
      return arcsec_size,arcsec_size;
    x1 = interp1d(tsec[:tmid],range(tmid))(0.5);
    x2 = interp1d(1-tsec[tmid:],range(tmid,len(tsec)))(0.5);
    return x1,x2;
  from matplotlib import pyplot
  pyplot.figure(figsize=(10,10))
  pyplot.plot(axis,xsec)
  pyplot.plot(axis,ysec)
  ix0,ix1 = fwhm(xsec)
  iy0,iy1 = fwhm(ysec)
  pyplot.plot((numpy.array([ix0,ix1])-sz)*secpix,[0.5,0.5])
  pyplot.plot((numpy.array([iy0,iy1])-sz)*secpix,[0.5,0.5])
  rx,ry = (ix1-ix0)*secpix,(iy1-iy0)*secpix
  r0 = (rx+ry)/2
  pyplot.text(axis[-1],1,'FWHM %.2f" by %.2f" (mean %.2f")'%(rx,ry,r0),ha='right',size=20)
  if title:
    pyplot.title(title);
  if savefig:
    pyplot.savefig(savefig,dpi=100)
  else:
    pyplot.show();
  return rx,ry
  #print "Nominal resolution is %.2f by %.2f\""%(rx,ry)
  #print "Corresponding to a max baseline of",0.21/(r0/3600*math.pi/180)

def measure_image_noise (noise=0,scale_noise=1.0,add_noise=False,rowchunk=1000000,use_old_noise_map=False,**kw):
    info(' >>> Making noise map')
    if add_noise:
        simnoise(rowchunk=rowchunk,scale_noise=scale_noise,noise=noise) 
    noiseimage = II('$OUTFILE-${im.weight}-noise.fits')
    make_noise_map = True
    if use_old_noise_map:
        if os.path.exists(noiseimage): 
            info('Using existing noise map: $noiseimage')
            make_noise_map = False
        else: make_noise_map = True
    if make_noise_map:
        imager.make_image(column='MODEL_DATA',dirty_image=noiseimage,**kw)
    noise = pyfits.open(noiseimage)[0].data.std();
    info(">>>   rms pixel noise is %g uJy"%(noise*1e+6))
    return noise

def measure_sdl(r0,r1,**kw):
    r0 = r0 or int(SIDELOBES_R0_ARCSEC/SIDELOBES_CELL_ARCSEC)
    r1 = r1 or int(SIDELOBES_R1_ARCSEC/SIDELOBES_CELL_ARCSEC)
    npix = r1*2
    bigpsf = II('$OUTFILE-${im.weight}-bigpsf.fits')

    imager.make_image(dirty_image=bigpsf,dirty=dict(data="psf",cellsize="%farcsec"%SIDELOBES_CELL_ARCSEC,npix=npix),**kw);
    data = pyfits.open(bigpsf)[0].data[0,0,...];
    radius = numpy.arange(npix)-r1
    radius = numpy.sqrt(radius[numpy.newaxis,:]**2+radius[:,numpy.newaxis]**2)
    mask = (radius<=r1)&(radius>=r0)
    rms = data[mask].std();
    data = None;
    r0,r1 = r0/3600.,r1/3600.;
    info(">>>   rms far sidelobes is %g (%.2f<=r<=%.2fdeg"%(rms,r0,r1));
    return rms,r0,r1

def simnoise (noise=0,rowchunk=100000,skipnoise=False,addToCol=None,scale_noise=1.0,column='MODEL_DATA'):
  conf = MS.split('_')[0]
  spwtab = ms.ms(subtable="SPECTRAL_WINDOW")
  freq0 = spwtab.getcol("CHAN_FREQ")[ms.SPWID,0]/1e6
  tab = ms.msw()
  dshape = list(tab.getcol('DATA').shape)
  nrows = dshape[0]
  noise = noise or compute_vis_noise()
  if addToCol: colData = tab.getcol(addToCol)
  for row0 in range(0,nrows,rowchunk):
    nr = min(rowchunk,nrows-row0)
    dshape[0] = nr
    data = noise*(numpy.random.randn(*dshape) + 1j*numpy.random.randn(*dshape)) * scale_noise
    if addToCol: 
       data+=colData[row0:(row0+nr)]
       info(" $addToCol + noise --> CORRECTED_DATA (rows $row0 to %d)"%(row0+nr-1))
       column = 'CORRECTED_DATA'
    else : info("Adding noise to $column (rows $row0 to %d)"%(row0+nr-1))
    tab.putcol(column,data,row0,nr);
  tab.close() 

SKIPNOISE = False

def apply_rfi_flagging (rfihist='RFIdata/rfipc.cp'):
  """Applies random flagging based on baseline length. Flagging percentages are taken
  from the rfihist file"""
  info("applying mock RFI flagging to $MS");
  # import table of flagging percentages
  (baselines,pc) = cPickle.load(file(rfihist));
  info("max fraction is %.2f, min is %.2f"%(pc.max(),pc.min()));
  # binsize is in km
  binsize = baselines[0]*1000;
  info("baseline binsize is %.2fm"%binsize);
  # open MS, get the per-row baseline length, 
  tab = ms.msw();
  uvw = tab.getcol('UVW')
  uvw = numpy.sqrt((uvw**2).sum(1))
  info("max baseline is %f"%uvw.max())
  # convert it to uvbin 
  uvbin = numpy.int64(uvw/binsize)
  info("max uv-bin is %d, we have %d bins tabulated"%(uvbin.max(),len(pc)));
  uvbin[uvbin>=len(pc)] = len(pc)-1
  # uvbin gives the number of the baseline bin in the 'pc' table above
  # now pull out a random number [0,1} for each row
  rr = numpy.random.random_sample(len(uvw))
  ## compute per-row threshold by looking up 'pc' array using the uvbin
  thr = pc[uvbin]
  ## kill the unlucky rows
  unlucky = rr<thr
  info(">>> mock RFI applied, flagged fraction is %.2f"%(float(unlucky.sum())/len(thr)));
  tab.putcol("FLAG_ROW",unlucky);
  
def clear_flags ():
  tab = ms.msw();
  tab.putcol("FLAG_ROW",numpy.zeros(tab.nrows(),bool));
  info("cleared all flags in $MS");
  
import numpy.random  
  
def addnoise (noise=0,rowchunk=100000):
  """adds noise to MODEL_DATA, writes to CORRECTED_DATA""";
  # compute expected noise
  noise = compute_vis_noise(noise);
  # fill MS with noise
  tab = ms.msw()
  nrows = tab.nrows();
  for row0 in range(0,nrows,rowchunk):
    nr = min(rowchunk,nrows-row0);
    info("Copying MODEL_DATA+noise to CORRECTED_DATA (rows $row0 to %d)"%(row0+nr-1));
    data = tab.getcol("MODEL_DATA",row0,nr);
    data += noise*(numpy.random.randn(*data.shape) + 1j*numpy.random.randn(*data.shape));
    tab.putcol("CORRECTED_DATA",data,row0,nr)
  tab.close()

CUBE_IMAGE_Template = "${MS:BASE}.1chan.fits";

def decompose_cube (image,freq0=1000,delta=1000):
  cube = pyfits.open(image)[0].data
  ff = pyfits.open(CUBE_IMAGE);
  ff[0].header['CRVAL4'] = freq0*1e+6;
  ff[0].header['CDELT4'] = delta*1e+6;
  nchan = cube.shape[0];
  info("decomposing $image into $nchan per-channel images, faking $delta MHz-wide image at $freq0 MHz");
  for i in range(nchan):
    ff[0].data[0,...] = cube[i,...];
    out = os.path.splitext(image)[0]+II("$i.fits");
    info("writing $out");
    ff.writeto(out,clobber=True);
  
MSLIST_Template = '${OUTDIR>/}mslist.txt'
DOALL = False
def _addms(msname = "$MS"):
  """ Keeps track of MSs when making MSs using multiple threds.
    The MS names are stored into a file which can be specified 
    via MSLIST on the command line. The list of MSs can then be 
    returned as python list using the function get_mslist().
    "DOALL" must be set to True for this feature to be enabled"""
  try :
    ms_std = open(MSLIST,"r")
    line = ms_std.readline().split("\n")[0]
    ms_std.close()
  except IOError: line = ''
  ms_std = open(MSLIST,"w")
  line+= ",%s"%msname if len(line.split()) > 0 else msname
  ms_std.write(line)
  ms_std.close()
  info("New MS list : $line")
document_globals(_addms,"DOALL");

def get_mslist(filename):
  """ See help for _addms"""
  ms_std = open(filename)
  mslist = ms_std.readline().split('\n')[0].split(',')
  info('>>>>>>>>>>>>> $mslist')
  return mslist

define("MAKEMS_REDO",False,"if False, makems will omit existing MSs");
define("MAKEMS_OUT","MS","place MSs in this subdirectory");

def makems (conf="MeerKAT64",writeAutoCorr=True,hours=8,dtime=60,dec=-40,ra='0:0:0',freq0=1400e6,nchan=1,dfreq=3.9e3,nband=1,label='',start_time=None,shift=False,start_freq=1.5):
  """Makes a MS given a Casa Table of itrf antenna positions 
  conf is e.g. SKA1REF or MeerKAT64 (antenna table $conf_ANTENNAS must exist)
  hours is total synthesis time, in hours
  integration is integration time, in seconds 
  dec is declination
  freq0 is base freq in MHz
  nchan is number of channels
  channels is channel width, in kHz
  nband is how many spws to split the channels into
  """
  # make sure that floats are floats and ints are ints
  dec,hours,dtime,freq0,dfreq = map(float,[dec,hours,dtime,freq0,dfreq])
  nchan,nband = map(int,[nchan,nband])
  if label =='None': label=''
  for anttab in conf,"$conf","${conf}_ANTENNAS","Layouts/${conf}_ANTENNAS":#,"SimsCont_Cosm/${conf}_ANTENNAS":
    if exists(anttab):
      anttab = II(anttab);
      break;
  else:
    abort("configuration $conf not found");
  conf = os.path.basename(anttab);
  if conf.endswith("_ANTENNAS"):
    conf = conf.rsplit("_",1)[0];
  if MAKEMS_OUT:
    makedir("$MAKEMS_OUT");
  msname = II("${MAKEMS_OUT>/}%s_%dh%ds_dec%+d_%dMHz_%dch${_<label}.MS"%(conf,hours,dtime,dec,freq0/1e6,nchan-1 if shift else nchan));
  info("ms $msname, configuration $conf, antenna table $anttab");
  if exists(msname):
    if not MAKEMS_REDO:
      info("$msname already exists and MAKEMS_REDO=False, skipping");
      v.MS = msname
      if DOALL: _addms(msname)
      return;
    x.sh("rm -fr $msname");
  conffile = II("makems.${msname:BASE}.cfg");
  if start_time == None:
   if msname.startswith(II('${MAKEMS_OUT>/}SKASUR')): # If SKASUR MS
    # work out start time: 12:50:0 is middle of observation, so subtract half
    date = '2000/1/5'
    m0 = (8.83*60) - (hours*60)//2
    h0 = m0//60;
    m0 = m0%60;
   else : # Assume SKA-Mid MS
    # work out start time: 19:45 is middle of observation, so subtract half
    date = "2011/11/16"
    m0 = (19.75*60)-(hours*60.)//2;
    h0 = m0//60;
    m0 = m0%60;
  start_time = start_time or '%s/%d/%d/00'%(date,h0,m0)
  MSName = "%s"%(msname.split(MAKEMS_OUT+"/")[-1])
  file(conffile,"w").write(II("""WriteAutoCorr=$writeAutoCorr
StartFreq=%g
StepFreq=%g
NFrequencies=$nchan
WriteImagerColumns=True
StepTime=$dtime
#TileSizeRest=10
NParts=1
MSDesPath=.
AntennaTableName=$anttab
Declination=${dec}.0.0
NBands=$nband
RightAscension=$ra
StartTime=%s  # 19:00 is center
MSName=$MSName
NTimes=%d
#TileSizeFreq=16"""%(freq0-(dfreq)*start_freq,dfreq,start_time,(hours*3600)//dtime)));
  info("creating $msname: ${hours}h synthesis, ${dtime}s integration, Dec=$dec, $nchan channels of %.4g kHz starting at %.4g MHz"%(dfreq/1e3,freq0/1e6));
  # run makems
  x.sh("/usr/bin/makems $conffile");
  if exists(MSName+"_p0") and not exists(msname):
    x.mv("${MSName}_p0 $msname");
    for item in '.gds _p0.vds'.split():
      if os.path.exists('%s%s'%(MSName,item)) : xo.rm('%s%s -f'%(MSName,item))
#  pyrap.tables.addImagingColumns(msname)
  v.MS = msname;
  if DOALL: _addms(msname)
  # plot uv-coverage
  if not os.path.exists(DESTDIR): x.sh('mkdir -p $DESTDIR ')
  ms.plot_uvcov(ms=.1,width=10,height=10,dpi=150,save="$OUTFILE-uvcov.png")

document_globals(makems,"MAKEMS_*");

define("SCWEIGHT","uniform","weight for simcube");
define("SCWEIGHTFOV","512arcsec","weight_fov for simcube");
define("SCROBUST","","robustness parameter for simcube");
define("SCTAPER",1,"taper for simcube, in arcsec. 0 for none");

def predict_from_fits (cube,padding=1.5,noise=0,column='DATA',wprojplanes=0):
    ms.set_default_spectral_info()
    import im.lwimager
    im.lwimager.predict_vis(image=cube,padding=padding,copy=False,column=column,wprojplanes=wprojplanes);
    if noise > 0:
        simnoise(addToCol=column,noise=noise)
#document_globals(simcube,"SC*");

def flag_stepped_timeslot (step=3):
  """Flags every Nth timeslot"""
  nant = ms.ms(subtable="ANTENNA").nrows();
  tab = ms.msw();
  nb = nant*(nant+1)/2
  frow = tab.getcol("FLAG_ROW");
  nr = len(frow);
  nt = len(frow)/nb;
  info("$MS has $nr rows, $nant antennas, $nb baselines and $nt timeslots, flagging every $step timeslots");
  frow = frow.reshape([nt,nb]);
  frow[::step,:] = True;
  tab.putcol("FLAG_ROW",frow.reshape((nr,)));

def fitsInfo(fits):
  hdr = pyfits.open(fits)[0].header
  ra = hdr['CRVAL1'] 
  dec = hdr['CRVAL2']
  naxis = hdr['NAXIS']
  if naxis>3: freq_ind = 3 if hdr['CTYPE3'].startswith('FREQ') else 4
  else: 
    freq_ind = 3
    if hdr['CRTYPE3'].startswith('FREQ') is False: 
       freq_axis = False
       return (ra,dec),freq_axis,naxis
  nchan = hdr['NAXIS%d'%freq_ind]
  dfreq = hdr['CDELT%d'%freq_ind]
  freq0 = hdr['CRVAL%d'%freq_ind] + hdr['CRPIX%d'%freq_ind]*dfreq
  return (ra,dec),(freq0,dfreq,nchan),naxis

def swap_stokes_freq(fitsname,freq2stokes=False):
  info('Checking STOKES and FREQ in FITS file, might need to swap these around.')
  hdu = pyfits.open(fitsname)[0]
  hdr = hdu.header
  data = hdu.data
  if hdr['NAXIS']<4: 
    warn('Editing fits file [$fitsname] to make it usable by the pipeline.')
    isfreq = hdr['CTYPE3'].startswith('FREQ')
    if not isfreq : abort('Fits header has frequency information')
    hdr.update('CTYPE4','STOKES')
    hdr.update('CDELT4',1)
    hdr.update('CRVAL4',1)
    hdr.update('CUNIT4','Jy/Pixel')
    data.resize(1,*data.shape)
  if freq2stokes:
    if hdr["CTYPE3"].startswith("FREQ") : return 0;
    else:
      hdr0 = hdr.copy()
      hdr.update("CTYPE4",hdr0["CTYPE3"])
      hdr.update("CRVAL4",hdr0["CRVAL3"])
      hdr.update("CDELT4",hdr0["CDELT3"])
      try :hdr.update("CUNIT4",hdr0["CUNIT3"])
      except KeyError: hdr.update('CUNIT3','Hz    ')
   #--------------------------
      hdr.update("CTYPE3",hdr0["CTYPE4"])
      hdr.update("CRVAL3",hdr0["CRVAL4"])
      hdr.update("CDELT3",hdr0["CDELT4"])
      try :hdr.update("CUNIT3",hdr0["CUNIT4"])
      except KeyError: hdr.update('CUNIT4','Jy/Pixel    ')
      warn('Swapping FREQ and STOKES axes in the fits header [$fitsname]. This is a SoFiA work arround.')
      pyfits.writeto(fitsname,np.rollaxis(data,1),hdr,clobber=True)
  elif hdr["CTYPE3"].startswith("FREQ"):
    hdr0 = hdr.copy()
    hdr.update("CTYPE3",hdr0["CTYPE4"])
    hdr.update("CRVAL3",hdr0["CRVAL4"])
    hdr.update("CDELT3",hdr0["CDELT4"])
    try :hdr.update("CUNIT3",hdr0["CUNIT4"])
    except KeyError: hdr.update('CUNIT3','Jy/Pixel    ')
   #--------------------------
    hdr.update("CTYPE4",hdr0["CTYPE3"])
    hdr.update("CRVAL4",hdr0["CRVAL3"])
    hdr.update("CDELT4",hdr0["CDELT3"])
    try :hdr.update("CUNIT4",hdr0["CUNIT3"])
    except KeyError: hdr.update('CUNIT4','Hz    ')
    warn('Swapping FREQ and STOKES axes in the fits header [$fitsname]. This is a  MeqTrees work arround.')
    pyfits.writeto(fitsname,np.rollaxis(data,1),hdr,clobber=True)
  return 0;


def deg2hms(deg):
  deg = deg * 24/360.
  hrs = deg - deg%1
  mins_tmp  = (deg - hrs)%1 * 60
  mins = mins_tmp - mins_tmp%1
  secs = (mins_tmp - mins)*60
  return '%d:%d:%.2f'%(hrs,mins,secs)

_SOFIA_DEFAULTS = {'steps': {'doFlag' : 'false',\
'doSmooth' : 'flase',\
'doScaleNoise' : 'false',\
'doSCfind' : 'true',\
'doThreshold' : 'false',\
'doWavelet' : 'false',\
'doCNHI' : 'false',\
'doMerge' : 'true',\
'doReliability' : 'true',\
'doParameterise' : 'true',\
'doWriteMask' : 'true',\
'doWriteCat' : 'true',\
'doMom0' : 'false',\
'doMom1' : 'false',\
'doCubelets' : 'false',\
'doDebug' : 'false'},\
'import': {'inFile' : '',\
'weightsFile' : '',\
'maskFile' : '',\
'weightsFunction' : '',\
'subcube' : [],\
'subcubeMode' : 'wcs'},\
'flag': {'regions' : []},\
'smooth': {'kernel' : 'gaussian',\
'edgeMode' : 'constant',\
'kernelX' : 3.0,\
'kernelY' : 3.0,\
'kernelZ' : 3.0},\
'scaleNoise': {'statistic' : 'mad',\
'edgeX' : 0,\
'edgeY' : 0,\
'edgeZ' : 0},\
'SCfind': {'threshold' : 4.0,\
'sizeFilter' : 0.0,\
'maskScaleXY' : 2.0,\
'maskScaleZ' : 2.0,\
'edgeMode' : 'constant',\
'rmsMode' : 'negative',\
'kernels' : [[ 0, 0, 0,'b'],[ 0, 0, 2,'b'],[ 0, 0, 4,'b'],[ 0, 0, 8,'b'],[ 0, 0,16,'b'],[ 3, 3, 0,'b'],[ 3, 3, 2,'b'],[ 3, 3, 4,'b'],[ 3, 3, 8,'b'],[ 3, 3,16,'b'],[ 6, 6, 0,'b'],[ 6, 6, 2,'b'],[ 6, 6, 4,'b'],[ 6, 6, 8,'b'],[ 6, 6,16,'b'],[ 9, 9, 0,'b'],[ 9, 9, 2,'b'],[ 9, 9, 4,'b'],[ 9, 9, 8,'b'],[ 9, 9,16,'b']],\
'kernelUnit' : 'pixel',\
'verbose':'true'},\
'threshold': {'threshold' : 4.0,\
'clipMethod' : 'relative',\
'rmsMode' : 'std',\
'verbose' : 'false'}, \
'merge': {'mergeX' : 3,\
'mergeY' : 3,\
'mergeZ': 3,\
'minSizeX' : 3,\
'minSizeY' : 3,\
'minSizeZ' : 2}, \
'reliability': {'parSpace' : ['ftot','fmax','nrvox'],\
'kernel' : [0.15,0.05,0.1],\
'fMin' : 0.0,\
'relThresh' : 0.9},\
'parameters': {'fitBusyFunction': 'false', 'optimiseMask':'false'}, \
'writeCat': {'basename' : '',\
'writeASCII' : 'true',\
'writeXML' : 'false',\
'writeSQL' : 'false',\
'parameters' : ['*']}}

# wsclean work around
def add_weight_spectrum(msname='$MS'):
 msname = interpolate_locals('msname')
 tab = pyrap.tables.table(msname,readonly=False)
 try: tab.getcol('WEIGHT_SPECTRUM')
 except RuntimeError:
  warn('Did not find WEIGHT_SPECTRUM column in $msname')
  from pyrap.tables import maketabdesc
  from pyrap.tables import makearrcoldesc
  coldmi = tab.getdminfo('DATA')
  dshape = tab.getcol('DATA').shape
  coldmi['NAME'] = 'weight_spec'
  info('adding WEIGHT_SPECTRUM column to $msname')
  shape = tab.getcol('DATA')[0].shape
  tab.addcols(maketabdesc(makearrcoldesc('WEIGHT_SPECTRUM',0,shape=shape,valuetype='float')),coldmi)
  ones = np.ndarray(dshape)
  info('Filling WEIGHT_SPECTRUM with unity')
  ones[...] = 1
  tab.putcol('WEIGHT_SPECTRUM',ones)
 tab.close()
