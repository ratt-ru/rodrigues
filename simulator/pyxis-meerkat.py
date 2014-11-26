import ms
import mqt
import lsm
import im
from simms import simms

MAKE_PSF = False
mqt.MULTITHREAD = 8
FITS = False
TIGGER = False
KATALOG = False
CLEAN = False
LSM = None
SELECT = None
NOISE = None
USING_SIAMESE = False
COLUMN = 'CORRECTED_DATA'
TDLSEC = 'turbo-sim:default'
CHANNELIZE = 0
MS_LABEL = None
TOTAL_SYNTHESIS = None

OBSERVATORY = None
POSITIONS = None

#TODO: Ask Gijs to install moresane in container 
im.MORESANE_PATH = '/home/makhathini/PyMORESANE/pymoresane.py'

_KATALOG = {
         'rand_pnts':'random_pts.txt',
         'rand_mix':'random.txt',
         '3c147_no_core':'3c147_field_no_3c147.lsm.html',
         '3c147_field':'3c147.lsm.html',
}

def simulate(msname='$MS',lsmname='$LSM',column='$COLUMN',tdlconf='$TDLCONF',section='$TDLSEC',options={},**kw):
    """ Simulates visibilities into an MS """
    msname,lsmname,column,section,tdlconf = interpolate_locals('msname lsmname column section tdlconf')

    if TIGGER:
        options['tiggerlsm.filename'] = lsmname
        options['noise_stddev'] = NOISE
        options['ms_sel.output_column'] = column
        options['ms_sel.msname'] = msname
        mqt.run('turbo-sim.py',job='_tdl_job_1_simulate_MS',config=tdlconf,section=section,options=options)
    elif FITS:
       predict_from_fits(lsmname,wprojplanes=128,column=COLUMN)

def azishe(cfg='$CFG',make_image=True):
    """ The driver for simulator """

    cfg = interpolate_locals('cfg')
    _cfg,_imager,_deconv = readCFG(cfg)
    # get options for component parts
    ms_opts = _cfg['ms_']
    cr_opts = _cfg['cr_']
    im_opts = _cfg['im_']

    # convert frequencies to Hz. This assumes [freq0,dfreq] = MHz,kHz
    freq0 = float(ms_opts['freq0'])*1e6
    del ms_opts['freq0']
    dfreq = float(ms_opts['dfreq'])*1e3
    del ms_opts['dfreq']
    
    # convert strings to floats/ints before passing them to simms.
    for opt in 'scan_length synthesis start_time nchan dtime'.split():
        if opt=='nchan':
            ms_opts[opt] = int(ms_opts[opt])
        else:
            ms_opts[opt] = float(ms_opts[opt])
    synthesis = ms_opts['synthesis']
    if synthesis> 12:
        ms_opts['synthesis'] = 12.0
        scalenoise = math.sqrt(synthesis/12.0)
    else:
        scalenoise = 1
    if not os.path.exists(MAKEMS_OUT):
        x.mkdir(MAKEMS_OUT)
    msname = simms.simms(freq0=freq0,label=MS_LABEL or OBSERVATORY,dfreq=dfreq,pos=POSITIONS,pos_type='casa',
                         tel=OBSERVATORY,outdir=MAKEMS_OUT,**ms_opts)
    v.MS = msname
    

    #plot uv-coverage
    if not os.path.exists(DESTDIR): x.sh('mkdir -p $DESTDIR ')
    ms.plot_uvcov(ms=.1,width=10,height=10,dpi=150,save="$OUTFILE-uvcov.png")
    
    tmp_std = tempfile.NamedTemporaryFile(suffix='.fits' if FITS else '.lsm.html')
    tmp_std.flush()
    tmp_file = tmp_std.name

    # construct selection to give to tigger-convert
    select = ''
    if RADIUS or FLUXRANGE:
        if RADIUS: select += '--select="r<%fdeg" '%RADIUS
        if FLUXRANGE: 
            select += '--select="I<%f" '%FLUXRANGE[1]
            select += '--select="I>%f" '%FLUXRANGE[0]
            
    if TIGGER:
        x.sh('tigger-convert $select --recenter=J2000,%s,%s $LSM $tmp_file -f'%(ms_opts['ra'],ms_opts['dec']))
        v.LSM = tmp_file
   #    xo.sh('cp $tmp_file current.lsm.html')
   #TODO(sphe) Should we keep LSMs from nvss and scubeb cut outs?
    elif FITS:
        from pyrap.measures import measures
        dm = measures()
        direction = dm.direction('J2000',ms_opts[ra],ms_opts[dec])
	ra = np.rad2deg(direction['m0']['value'])
	dec = np.rad2deg(direction['m1']['value'])
        hdu = pyfits.open(LSM)[0]
        hdr = hdu.header
        data = hdu.data
        hdr['CRVAL1'] = ra
        hdr['CRVAL2'] = dec
        pyfits.writeto(tmp_file,data,hdr,clobber=True)
        v.LSM = tmp_file
    ms.set_default_spectral_info()

    global NOISE
    NOISE = compute_vis_noise(sefd=get_sefd(freq0)) * scalenoise
    simulate()
    tmp_std.close()

    im.IMAGE_CHANNELIZE = CHANNELIZE
    # Set these here to have a standard way of accepting them in the form
    for opt in 'npix cellsize weight robust wprojplanes stokes weight_fov mode'.split():
        if opt in im_opts.keys():
            if opt == 'stokes':
                setattr(im,opt,im_opts[opt].upper())
            elif opt in ['npix']:
                setattr(im,opt,int(im_opts[opt]))
            elif opt in ['robust']:
                setattr(im,opt,float(im_opts[opt]))
            elif opt == 'cellsize':
                setattr(im,opt,im_opts[opt]+'arcsec')
            elif opt == 'weight_fov':
                setattr(im,opt,im_opts[opt]+'arcmin')
            else: 
                setattr(im,opt,im_opts[opt])
            del im_opts[opt]

    # make noise map. noise map will be 512x512 pixels 
    noise = measure_image_noise(make_psf=False,noise=NOISE,add_noise=True,npix=512)

    if not _deconv:
        __import__('im.%s'%_imager)
        call_imager = eval('im.%s.make_image'%_imager)
        call_imager(dirty=True,restore=False,restore_lsm=False,psf=MAKE_PSF,**im_opts)

    for deconv in _deconv:
        restore = _cfg['%s_'%deconv]
        for key,val in restore.items():
            if val.lower() in 'true yes 1':
                restore[key] = True
            elif val.lower() in 'false no 0':
                del restore[key]

        if deconv in 'wsclean casa lwimager'.split():
            _imager = deconv
            try:
                im.threshold = '%.3gJy'%(float(restore['sigmalevel'])*noise)
                del restore['sigmalevel']
            # set niter vey high to ensure threshold is reached
                im.niter = 10000 
                del restore['niter']
            except KeyError:
                im.threshold = restore['threshold']+'Jy'
                del restore['threshold']

        if _imager=='casa':
            for key,val in restore.iteritems():
                if key in ['niter']:
                    restore[key] = int(val)
                else:
                   try: restore[key] = float(val)
                   except ValueError: "do nothing"
        if deconv in STAND_ALONE_DECONV :
            im_opts['algorithm'] = devonv

        __import__('im.%s'%_imager)
        call_imager = eval('im.%s.make_image'%_imager)
        call_imager(dirty=True,restore=restore,restore_lsm=False,psf=MAKE_PSF,**im_opts)
