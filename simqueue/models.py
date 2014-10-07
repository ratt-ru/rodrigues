from django.db.models import Model, CharField, FileField, BooleanField,\
    TextField, FloatField, IntegerField


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
    sky_type = CharField(choices=SKY_TYPES, max_length=1)
    sky_model = FileField()
    upload_tdl = BooleanField(default=False)
    tdl_conf_file = FileField(help_text='TDL Configuration File')
    tdl_section = TextField()
    make_psf = BooleanField(default=False)
    add_noise = BooleanField(default=False)
    noise_standard_dev = FloatField()
    output = CharField(choices=OUTPUT_TYPES, max_length=1)

    # observation setup
    synthesis_time = FloatField()
    integration_time = FloatField()
    start_frequency = FloatField()
    channel_width = FloatField()
    channels_per_band = IntegerField(help_text='Number of frequency channels per band')
    freq_bands = IntegerField(help_text='Number of frequency bands')
    correlate = BooleanField(help_text='Autocorrelation data', default=False)
    declination = FloatField()
    right_ascension = FloatField()

    BEAM_TYPES = (
        ('M', 'MeerKAT 1'),
        ('N', 'MeerKAT 2'),
        ('O', 'MeerKAT 3'),
        ('K', 'KAT-7'),
        ('W', 'WSRT'),
        ('J', 'JVLA'),
    )

    # dish settings
    am_phase_gains = FloatField('Amplitude Phase Gains')
    par_angle_rot = BooleanField(help_text='Parallactic Angle Rotation',
                                 default=False)
    primary_beam = CharField(choices=BEAM_TYPES, max_length=1)

    # corruptions
    corrup_am_phase_gains = FloatField('Amplitude Phase Gains')
    pointing_errors = FloatField()
    rfi = FloatField()

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
        ('A', 'Average all'),
        ('E', 'Image every channel'),
        ('C', 'Custom'),
    )

    # imaging settings
    pixels = IntegerField()
    pixel_width = FloatField(help_text='in arcseconds')
    uv_weighting = CharField(choices=WEIGHTING_TYPES, max_length=1)
    weight_fov = FloatField(help_text='in arcminutes')
    w_projection_planes = IntegerField()
    imaging_mode = CharField(choices=IMAGING_TYPES, max_length=1)
    spectral_window = FloatField()
    num_channels = IntegerField()
    image_channelise = CharField(choices=CHANNELISE_TYPES, max_length=1)
    stokes = TextField()

    DECONV_TYPES = (
        ('C', 'csclean'),
        ('H', 'hogbom'),
        ('D', 'clark'),
        ('M', 'multiscale'),
    )

    # deconvolution settings
    clean = BooleanField(default=False)
    Deconv_alg = CharField(choices=DECONV_TYPES, max_length=1)
    clean_scales = FloatField()
    num_scales = FloatField()
    num_clean_iter = IntegerField(help_text='number of clean iterations')
    clean_threshold = FloatField(help_text='in mJy')