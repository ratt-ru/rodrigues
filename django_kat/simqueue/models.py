from django.db.models import Model, CharField, FileField, BooleanField,\
    FloatField, IntegerField, DateTimeField, TextField
from celery.result import AsyncResult


class Simulation(Model):
    SKY_TYPES = (
        ('T', 'Tigger LSM'),
        ('F', 'FITS'),
        ('S', 'Siamese Model'),
    )

    OUTPUT_TYPES = (
        ('I', 'Image'),
        ('V', 'Visibilities'),
    )

    # global settings
    name = CharField(default='New simulation', max_length=200)
    sky_type = CharField(choices=SKY_TYPES, max_length=1, default='T')
    sky_model = FileField(blank=True, upload_to='sky')
    tdl_conf = FileField('TDL Configuration File', blank=True, upload_to='tdl')
    tdl_section = CharField(blank=True, max_length=200)
    make_psf = BooleanField(default=True, blank=True)
    add_noise = BooleanField(default=True, blank=True)
    vis_noise_std = FloatField("Noise Standard Deviation", default=0)
    output = CharField('Output type', choices=OUTPUT_TYPES, max_length=1,
                       default='I')

    # observation setup
    ms_hours = FloatField('Synthesis time', default=0.25, help_text='in hours')
    ms_dtime = IntegerField('Integration time', default=10, help_text='in seconds')
    ms_freq0 = FloatField('Start frequency', default=1400e6, help_text='in Hz')
    ms_dfreq = FloatField('Channel width', default=50e6, help_text='in Hz')
    ms_nchan = IntegerField('Channels per band', default=1,
                            help_text='Number of frequency channels per band')
    ms_nband = IntegerField('Frequency bands', default=1,
                            help_text='Number of frequency bands')
    ms_write_auto_corr = BooleanField('Autocorrelations',
                                      help_text='Include autocorrelation in data',
                                      default=True)
    ms_dec = FloatField('Declinations', default=-30)
    ms_ra = FloatField('Right ascension', default=0)

    BEAM_TYPES = (
        ('M', 'MeerKAT 1'),
        ('N', 'MeerKAT 2'),
        ('O', 'MeerKAT 3'),
        ('K', 'KAT-7'),
        ('W', 'WSRT'),
        ('J', 'JVLA'),
    )

    # dish settings
    ds_amp_phase_gains = FloatField('Amplitude Phase Gains', default=1)
    ds_parallactic_angle_rotation = BooleanField('Parallactic Angle Rotation',
                                                 default=True)
    ds_primary_beam = CharField(choices=BEAM_TYPES, max_length=1, default='M')
    ds_feed_angle = FloatField("Feed angle", default=0)

    # corruptions
    cr_amp_phase_gains = FloatField("Amplitude Phase Gains", default=1)
    cr_pointing_error = FloatField(default=0)
    cr_rfi = FloatField(default=0)

    WEIGHTING_TYPES = (
        ('N', 'Natural'),
        ('U', 'Uniform'),
        ('B', 'Briggs'),
    )

    IMAGING_TYPES = (
        ('C', 'Channel'),
        ('M', 'MFS'),
    )

    CHANNELISE_TYPES = (
        ('NCHAN', 'Average all'),
        ('1', 'Image every channel'),
        ('custom', 'Custom'),
    )

    # imaging settings
    im_npix = IntegerField('Image size', default=512, help_text='in pixels')
    im_cellsize = FloatField('Pixel size', help_text='in arcseconds',
                             default=1)
    im_weight = CharField('uv-Weighting', choices=WEIGHTING_TYPES, max_length=1,
                          default='N')
    im_weight_fov = FloatField('Weight FoV', help_text='in arcminutes',
                               default=1)
    im_wprojplanes = IntegerField('w-Projection planes', default=0)
    im_mode = CharField('Imaging mode', choices=IMAGING_TYPES, max_length=1,
                        default='C')
    im_spwid = CharField('Spectral window', default=0, max_length=32)
    channelise = CharField('Image channelise', choices=CHANNELISE_TYPES,
                           max_length=10, default='A')
    im_stokes = CharField('Stokes', default='I', max_length=4)

    DECONV_TYPES = (
        ('C', 'csclean'),
        ('H', 'hogbom'),
        ('D', 'clark'),
        ('M', 'multiscale'),
        ('S', 'MORESANE'),
    )

    # deconvolution settings
    deconvolve = BooleanField('Deconvolve', default=True)
    dc_operation = CharField('Deconvolution Algorithm', choices=DECONV_TYPES,
                             max_length=1, default='C')
    dc_uservector = CharField('Clean scales',
                              default='0 1 4 8 16 64 128',
                              help_text='List of scales to clean',
                              max_length=64)
    dc_nscales = FloatField('Scales to clean', default=4)
    dc_niter = IntegerField('Clean Iterations',
                            help_text='number of clean iterations',
                            default=1000)
    dc_threshold = FloatField('Clean threshold', help_text='in mJy',
                              default=0)

    # status of the task
    SCHEDULED = 'S'
    RUNNING = 'R'
    STOPPED = 'T'
    ABORTED = 'A'
    CRASHED = 'C'
    FINISHED = 'F'

    STATE_TYPES = (
        (SCHEDULED, 'scheduled'),
        (RUNNING, 'running'),
        (STOPPED, 'stopped'),
        (ABORTED, 'aborted'),
        (CRASHED, 'crashed'),
        (FINISHED, 'finished'),
    )
    state = CharField(choices=STATE_TYPES, max_length=1, default=SCHEDULED)
    started = DateTimeField(blank=True, null=True)
    finished = DateTimeField(blank=True, null=True)
    log = TextField(blank=True, null=True)
    task_id = CharField(max_length=36, null=True, blank=True)

    # results
    result_dir = CharField(blank=True, null=True, max_length=11)
    results_uvcov = FileField(blank=True, upload_to='uvcov', null=True)
    results_dirty = FileField(blank=True, upload_to='dirty', null=True)
    results_model = FileField(blank=True, upload_to='model', null=True)
    results_residual = FileField(blank=True, upload_to='residual', null=True)
    results_restored = FileField(blank=True, upload_to='restored', null=True)

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

    def get_task_status(self):
        if self.task_id:
            try:
                return AsyncResult(self.task_id).status
            except OSError as e:
                return "can't connect to broker: " + str(e)
        else:
            return 'NO TASK ID'

    def duration(self):
        if self.finished and self.started:
            return str(self.finished - self.started)