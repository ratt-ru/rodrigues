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
NOISE = None
USING_SIAMESE = False
COLUMN = 'CORRECTED_DATA'
TDLSEC = 'turbo-sim:default'
CHANNELIZE = 0
MS_LABEL = None

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

def simulate(msname='$MS',lsmname='$LSM',column='$COLUMN',tdlconf='$TDLCONF',section='$TDLSEC',freq0=1400e6,options={},**kw):
    """ Simulates visibilities into an MS """
    msname,lsmname,column,section,tdlconf = interpolate_locals('msname lsmname column section tdlconf')

    noise = NOISE or compute_vis_noise(sefd=get_sefd(freq0))
    if TIGGER:
        options['tiggerlsm.filename'] = lsmname
        options['noise_stddev'] = noise
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


    freq0 = float(ms_opts['freq0'])*1e6
    del ms_opts['freq0']
    dfreq = float(ms_opts['dfreq'])*1e3
    del ms_opts['dfreq']
    
    for opt in 'hours start_time nchan dtime'.split():
        if opt=='nchan':
            ms_opts[opt] = int(ms_opts[opt])
        else:
            ms_opts[opt] = float(ms_opts[opt])
            
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
    nchan =  int(ms_opts['nchan'])
    if TIGGER:
        x.sh('tigger-convert --recenter=J2000,%s,%s $LSM $tmp_file -f'%(ms_opts['ra'],ms_opts['dec']))
        v.LSM = tmp_file
    elif FITS:
	ra = d_or_h_ms2deg(ms_opts['ra'])
        dec = d_or_h_ms2deg(ms_opts['dec'])
        hdu = pyfits.open(LSM)[0]
        hdr = hdu.header
        data = hdu.data
        hdr['CRVAL1'] = ra
        hdr['CRVAL2'] = dec
        pyfits.writeto(tmp_file,data,hdr,clobber=True)
        v.LSM = tmp_file
    ms.set_default_spectral_info()
    simulate(freq0=freq0)
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
   
    # Cater for csclean,clark and such
    if _deconv not in STAND_ALONE_DECONV :
        _deconv = _imager
    restore = _cfg['%s_'%_deconv] if DECONV else False
    if _deconv in 'wsclean casa lwimager'.split():
        im.threshold = restore['threshold']+'Jy'
        del restore['threshold']
    for key,val in restore.iteritems():
        if val.lower() in 'true yes 1':
            restore[key] = True
        elif val.lower() in 'false no 0':
            del restore[key]

    if _imager=='casa':
        for key,val in restore.iteritems():
            if key in ['niter']:
               restore[key] = int(val)
            else:
               try: restore[key] = float(val)
               except ValueError: "do nothing"
    __import__('im.%s'%_imager)
    call_imager = eval('im.%s.make_image'%_imager)
    call_imager(dirty=False,restore=restore,algorithm=_deconv,restore_lsm=False,psf=MAKE_PSF,**im_opts)
