from django.db.models import Model, CharField, FileField, BooleanField,\
    FloatField, IntegerField, DateTimeField, TextField
from celery.result import AsyncResult
import celery.states


class Simulation(Model):
    SKY_TYPES = (
        ('T', 'Tigger-LSM'),
        ('A', 'ASCII'),
        ('F', 'FITS'),
        ('S', 'KATALOG'), # this is a catalog of known skies
    )

    OUTPUT_TYPES = (
        ('I', 'Image'),
        ('V', 'Visibilities'),
    )
    
    OBSERVATORIES = (
        ('MK','MeerKAT'),
        ('K7','KAT-7'),
        ('JA','JVLA-A'),
    )

    KATALOG = (
        ('NV','nvss6deg'), 
        ('S3','scubed1deg'), 
#        ('K1','rand_pnts'), 
#        ('K2','rand_mix'),
        ('K3','3c147_field'),
        ('K4','3c147_field_no_core'),
    )

    # Telescope setup
    name = CharField(default='New simulation', max_length=200)
    observatory = CharField(default='MK', 
                           choices=OBSERVATORIES,
                           max_length=32)
    output = CharField('Output type', choices=OUTPUT_TYPES, max_length=1,
                       default='I')
    sefd = FloatField('SEFD', blank=True,null=True,
                      help_text='System defaults will be used if left blank')

    # sky setup
    sky_type = CharField(choices=SKY_TYPES, max_length=1, default='T')
    sky_model = FileField(blank=True, upload_to='sky')
#    tdl_conf = FileField('TDL Configuration File', blank=True, upload_to='tdl')
#    tdl_section = CharField(blank=True, max_length=200)
    katalog_id = CharField('KATALOG',blank=True,
                           default='NV',
                           choices=KATALOG,
                           max_length=64,
                           help_text='Choose from our sky catalogs')
    radius = FloatField('Radius',default=0.5,blank=True,
                  help_text='Radius of degrees')
    fluxrange = CharField('Flux range',default='0.001-1',
                  max_length=32,
                  help_text='Flux range in Jy')
    ms_dec = CharField('Declination', 
                       default='-30d0m0s',
                       help_text='in dms',
                       max_length=32)
    ms_ra = CharField('Right ascension', 
                       default='0h0m0s',
                       help_text='in hms',
                       max_length=32)
    add_noise = BooleanField(default=True, blank=True)
    vis_noise_std = FloatField("Visibility noise std", default=0,
                               help_text='Generates from SEFD if 0')

    # observation setup
    ms_synthesis = FloatField('Synthesis time', default=0.25, help_text='in hours')
    ms_scan_length = FloatField('Scan length',blank=True, default=0.25, help_text='in hours')
    ms_start_time = FloatField('Initial hour angle',blank=True, default=-0.125, help_text='in hours')
    ms_dtime = IntegerField('Integration time', default=10,
                            help_text='in seconds')
    ms_freq0 = FloatField('Start frequency', default=700, help_text='in MHz')
    ms_dfreq = FloatField('Channel width', default=50e3, help_text='in kHz')
    ms_nchan = IntegerField('Channels', default=1,
                            help_text='Number of frequency channels')
#    ms_write_auto_corr = BooleanField('Include Autocorrelations',
#                                      help_text='Include autocorrelation in data',
#                                      default=True)

    BEAM_TYPES = (
        ('M', 'MeerKAT-1'),
        ('N', 'MeerKAT-2'),
        ('O', 'MeerKAT-3'),
        ('K', 'KAT-7'),
        ('W', 'WSRT'),
        ('J', 'JVLA'),
    )

    # dish settings
    ds_parallactic_angle_rotation = BooleanField('Parallactic Angle Rotation',
                                                 default=True,help_text='Can not be applied to FITS skymodels at the moment.')
    ds_primary_beam = CharField('Primary Beam',choices=BEAM_TYPES, max_length=1, default='M')
    ds_feed_angle = FloatField("Feed angle", default=0)

    # corruptions
    cr_amp_phase_gains = FloatField("Amplitude Phase Gains", default=1)
    cr_pointing_error = FloatField(default=0)
    cr_rfi = FloatField(default=0)

    IMAGERS = (
        ('LW', 'LWIMAGER'),
        ('WS', 'WSCLEAN'),
        ('CA', 'CASA'),
    )



    WEIGHTING_TYPES = (
        ('N', 'Natural'),
        ('U', 'Uniform'),
        ('B', 'Briggs'),
    )

    IMAGING_TYPES = (
        ('C', 'channel'),
        ('M', 'mfs'),
        ('V', 'velocity'),
        ('F', 'frequency'),
    )

    # imaging settings
    imager = CharField('Imager',default='LW',
                       choices=IMAGERS,
                       max_length=32)
    im_npix = IntegerField('Image size', default=512, help_text='in pixels')
    im_cellsize = FloatField('Pixel size', help_text='in arcseconds',
                             default=1)
    im_weight = CharField('uv-Weighting', choices=WEIGHTING_TYPES, max_length=1,
                          default='N')
    im_robust = FloatField('Robust',
                           default=0,
                           help_text='Briggs robust parameter')
    im_weight_fov = FloatField('Weight FoV', help_text='in arcminutes',
                               blank=True,null=True)
    im_wprojplanes = IntegerField('w-Projection planes', default=0)
    im_mode = CharField('Imaging mode', choices=IMAGING_TYPES, max_length=1,
                        default='C')
#    im_spwid = CharField('Spectral window', default=0, max_length=32)
    channelise = IntegerField('Image channelise',
                           default=0,
                           help_text='0 means average all, 1 per channel, etc.')
    im_stokes = CharField('Stokes', default='I', max_length=4)
#    make_psf = BooleanField('Make PSF',default=False, blank=True)

    CLEAN_TYPES = (
        ('C', 'csclean'),
        ('H', 'hogbom'),
        ('D', 'clark'),
        ('M', 'multiscale'),
    )


    # lwimager
    lwimager = BooleanField('Deconvolve with me!',default=False)
    lwimager_niter = IntegerField('NITER',default=1000)
    lwimager_gain = FloatField('Loop gain',default=0.1)
    lwimager_threshold = FloatField('Clean Threshold',default=0,
                               help_text='In Jy')
    
    lwimager_operation = CharField('Clean algorithm',
                              choices=CLEAN_TYPES,
                              default='C',
                              max_length=1)
    lwimager_cyclefactor = FloatField('Cycle factor',default=1.5)
    lwimager_cyclespeedup = FloatField('Cycle speed up',default=-1)
    lwimager_stoppointmode = FloatField('Stop point mode,',default=-1)
    lwimager_nscales = IntegerField('Scales for MS clean',default=4)
    # Multi scale clean : No need to have a seperate block for MS clean. 
    lwimager_uservector = CharField('Clean scales',
                              blank=True,null=True,
                              help_text='Comma seperated scales in pixels',
                              max_length=64)

    # wsclean
    wsclean = BooleanField('Deconvolve with me!',default=False)
    wsclean_niter = IntegerField('NITER',default=1000)
    wsclean_gain = FloatField('Minor loop gain',default=0.1)
    wsclean_mgain = FloatField('Major loop gain',default=0.1)
    wsclean_threshold = FloatField('Clean Threshold',default=0,
                               help_text='In Jy')
    wsclean_joinpolarizations = BooleanField('Join polarizations',default=False)
    wsclean_joinchannels = BooleanField('Join channels',default=False)
    wsclean_multiscale = BooleanField('Multiscale clean',default=False)
    wsclean_multiscale_dash_threshold_dash_bias = FloatField('Multi scale threshold bias',default=0.7)
    wsclean_multiscale_dash_scale_dash_bias = FloatField('Multi scale bias',default=0.6)
    wsclean_cleanborder = FloatField('Clean border',
                                default=5,
                                help_text='In percentage of image width/height')
    wsclean_smallpsf = BooleanField('Small PSF',
                               default=False,
                               help_text='Resize the psf to speed up minor clean iterations')
    wsclean_nonegative = BooleanField('No negative',
                            default=False,
                            help_text='Do not allow negative components during cleaning')
    wsclean_stopnegative = BooleanField('Stop on negative',default=False)
    wsclean_beamsize = CharField('Restoring beam size',
                            blank=True,null=True,
                            help_text='In arcseconds',
                            max_length=32)


    PSF_MODE = (
        ('CL','clark'),
        ('CS','clarkstokes'),
        ('H','hogbom'),
    )

    IMAGER_MODE = (
        ('C','csclean'),
        ('M','mosiac'),
    )

    GRID_MODE = (
        ('W','widefield'),
        ('A','aprojection'),
    )

    #casa
    casa = BooleanField('Deconvolve with me!',default=False)
    casa_niter = IntegerField('NITER',default=1000)
    casa_threshold = FloatField('Threshold',default=0)
    casa_gain = FloatField('Loop Gain',
                           default='0.1',
                           help_text='Clean Loop gain')
    casa_psfmode = CharField('PSF mode',
                             default='CL',
                             choices=PSF_MODE,
                             max_length=32)
    casa_imagermode = CharField('Imager mode',
                             blank=True,
                             choices=IMAGER_MODE,
                             default='csclean',
                             max_length=32)
    casa_gridmode = CharField('Grid mode',
                              blank=True,
                              choices=GRID_MODE,
                              default='W',
                              max_length=32,
                              help_text='A-projection only works JVLA')
    casa_nterms = IntegerField('NTERMS',
                             default=1,
                             help_text='See CASA clean task')
    casa_reffreq = FloatField('MFS ref Frequency',blank=True,null=True,
                             help_text='in MHz')
    casa_multiscale = CharField('Multiscale',
                                blank=True,null=True,
                                help_text='Deconvolution scales in pixels',
                                max_length=200)
    casa_negcomponent = FloatField('Negative Components',
                                  default=-1,
                                  help_text='See CASA clean task')
    casa_smallscalebias = FloatField('Small scale bias',
                                     default=0.6,
                                     help_text='See CASA clean task')
    casa_restoringbeam = CharField('Restoring beam',
                                   blank=True,null=True,
                                   max_length=32)
    casa_cyclefactor = FloatField('Cycle factor',default=1.5)
    casa_cyclespeedup = FloatField('Cycle speed up',default=-1)
   
    
    #moresane
    CONV_TYPES=(
        ('C','circular'),
        ('L','linear'),
    )

    moresane = BooleanField('Deconvolve with me!',default=False)
    moresane_scalecount = IntegerField('Scale count',
                          blank=True,null=True,
                          help_text='See MORESANE help')
    moresane_subregion = IntegerField('Sub region',
                          blank=True,null=True,
                          help_text='Inner region to deconvolve in pixels')
    moresane_startscale = IntegerField('Start scale',default=1)
    moresane_stopscale = IntegerField('Stop scale',default=20)
    moresane_sigmalevel = FloatField('Threshold level',
                          default=3,
                          help_text='in sigma above noise')
    moresane_loopgain = FloatField('Loop gain',default='0.1')
    moresane_tolerance = FloatField('Tolerance',default=.75)
    moresane_accuracy = FloatField('Accuracy',default=1e-6)
    moresane_majorloopmiter = IntegerField('Major loop iterations',default=100)
    moresane_minorloopmiter = IntegerField('Minor loop iterations',default=50)
    moresane_convmode = CharField('Convolution mode',
                          default='C',
                          choices=CONV_TYPES,
                          max_length=32)
    moresane_enforcepositivity = BooleanField('Enforce Positivity',default=False)
    moresane_edgesupression = BooleanField('Edge Suppression',default=False)
    moresane_edgeoffset = IntegerField('Edge offset',default=0)
    moresane_mfs = BooleanField('MFS map',
                          default=False,
                          help_text='Comes with an spi map') 
    # I use a double underscore to a represent hyphen (for simulator)
    moresane_spi_dash_sigmalevel = FloatField('spi threshold level',
                               default=10,
                               help_text='In sigma above noise')

    # status of the task
    SCHEDULED = 'S'
    RUNNING = 'R'
    CRASHED = 'C'
    FINISHED = 'F'

    STATE_TYPES = (
        (SCHEDULED, 'scheduled'),
        (RUNNING, 'running'),
        (CRASHED, 'crashed'),
        (FINISHED, 'finished'),
    )
    state = CharField(choices=STATE_TYPES, max_length=1, default=SCHEDULED)
    started = DateTimeField(blank=True, null=True)
    finished = DateTimeField(blank=True, null=True)
    log = FileField(blank=True, null=True)
    console = TextField(blank=True, null=True)
    task_id = CharField(max_length=36, null=True, blank=True)

    # results
    results_uvcov = FileField(blank=True, upload_to='uvcov', null=True)
    results_dirty = FileField(blank=True, upload_to='dirty', null=True)
    results_psf = FileField(blank=True, upload_to='psf', null=True)
#    results_lwimager_dirty = FileField(blank=True, upload_to='lwimager_dirty', null=True)
    results_lwimager_model = FileField(blank=True, upload_to='lwimager_model', null=True)
    results_lwimager_residual = FileField(blank=True, upload_to='lwimager_residual', null=True)
    results_lwimager_restored = FileField(blank=True, upload_to='lwimager_restored', null=True)
#    results_casa_dirty = FileField(blank=True, upload_to='casa_dirty', null=True)
    results_casa_model = FileField(blank=True, upload_to='casa_model', null=True)
    results_casa_residual = FileField(blank=True, upload_to='casa_residual', null=True)
    results_casa_restored = FileField(blank=True, upload_to='casa_restored', null=True)
#    results_wsclean_dirty = FileField(blank=True, upload_to='wsclean_dirty', null=True)
    results_wsclean_model = FileField(blank=True, upload_to='wsclean_model', null=True)
    results_wsclean_residual = FileField(blank=True, upload_to='wsclean_residual', null=True)
    results_wsclean_restored = FileField(blank=True, upload_to='wsclean_restored', null=True)
#    results_moresane_dirty = FileField(blank=True, upload_to='moresane_dirty', null=True)
    results_moresane_model = FileField(blank=True, upload_to='moresane_model', null=True)
    results_moresane_residual = FileField(blank=True, upload_to='moresane_residual', null=True)
    results_moresane_restored = FileField(blank=True, upload_to='moresane_restored', null=True)

    def __str__(self):
        return "<simulation name='%s' id=%s>" % (self.name, self.id)

    def set_crashed(self, error):
        self.state = self.CRASHED
        self.log = error
        self.started = None
        self.finished = None
        self.save(update_fields=["state", "log", "started", "finished"])

    def set_scheduled(self):
        self.state = self.SCHEDULED
        self.started = None
        self.finished = None
        self.log = ""
        self.save(update_fields=["state", "started", "finished"])

    def clear(self):
        self.results_uvcov = None
        self.results_psf = None
        self.results_dirty = None
#        self.results_lwimager_dirty = None
        self.results_lwimager_model = None
        self.results_lwimager_residual = None
        self.results_lwimager_restored = None
#        self.results_casa_dirty = None
        self.results_casa_model = None
        self.results_casa_residual = None
        self.results_casa_restored = None
#        self.results_wsclean_dirty = None
        self.results_wsclean_model = None
        self.results_wsclean_residual = None
        self.results_wsclean_restored = None
#        self.results_moresane_dirty = None
        self.results_moresane_model = None
        self.results_moresane_residual = None
        self.results_moresane_restored = None


        self.log = None
        self.console = ""
        self.save(update_fields=["results_uvcov","results_dirty","results_psf",
        "results_lwimager_model", "results_lwimager_residual", "results_lwimager_restored", 
        "results_casa_model", "results_casa_residual", "results_casa_restored", 
        "results_wsclean_model", "results_wsclean_residual", "results_wsclean_restored", 
        "results_moresane_model", "results_moresane_residual", "results_moresane_restored", 
        "log", "console"])

    def get_task_status(self):
        if not self.task_id:
            return 'NO TASK ID'
        try:
            broker_status = AsyncResult(self.task_id).status
            # somehow the job is running but status is PENDING
            if broker_status == celery.states.PENDING and \
                            self.state == self.RUNNING:
                return celery.states.STARTED
            elif broker_status == celery.states.SUCCESS and \
                self.state == self.CRASHED:
                return celery.states.FAILURE
            return broker_status
        except OSError as e:
            return "can't connect to broker: " + str(e)

    def can_reschedule(self):
        """
        We want only to be able reschedule jobs that are finished
        """
        return self.get_task_status() in (celery.states.SUCCESS,
                                          celery.states.FAILURE,
                                          celery.states.REVOKED)

    def duration(self):
        if self.finished and self.started:
            return str(self.finished - self.started)
