from django.forms import CharField, FileField, BooleanField, FloatField, IntegerField, ChoiceField
from form_utils.forms import BetterForm



# global settings
global_ = (
    'name',
    'sky_type',
    'sky_model',
    'tdl_conf',
    'tdl_section',
    'make_psf',
    'add_noise',
    'vis_noise_std',
    'output',
)

# observation setup
observation = (
    'ms_hours',
    'ms_dtime',
    'ms_freq0',
    'ms_dfreq',
    'ms_nchan',
    'ms_nband',
    'ms_write_auto_corr',
    'ms_dec',
    'ms_ra',
)

# dish settings
dish = (
    'ds_amp_phase_gains',
    'ds_parallactic_angle_rotation',
    'ds_primary_beam',
    'ds_feed_angle',
)

# corruptions
corruptions = (
    'cr_amp_phase_gains',
    'cr_pointing_error',
    'cr_rfi',
)

# imaging settings
imaging = (
    'im_npix',
    'im_cellsize',
    'im_weight',
    'im_weight_fov',
    'im_wprojplanes',
    'im_mode',
    'im_spwid',
    'channelise',
    'im_stokes',
)

# deconvolution settings
deconvolution = (
    'deconvolve',
    'dc_operation',
    'dc_uservector',
    'dc_nscales',
    'dc_niter',
    'dc_threshold',
)


class Form(BetterForm):
    docker_image = 'radioastro/simulator'

    class Meta:
        fieldsets = [('global', {'fields': global_,
                                 'description': 'Global settings'}),
                     ('observation', {'fields': observation,
                                      'description': 'Observation setup'}),
                     ('imaging', {'fields': imaging,
                                  'description': 'imaging settings'}),
                     ('dish', {'fields': dish,
                               'description': 'dish settings'}),
                     ('corruptions', {'fields': corruptions,
                                      'description': 'Corruptions'}),

                     ('deconvolution', {'fields': deconvolution,
                                        'description': 'deconvolution settings'}),
                     ]

    SKY_TYPES = (
        ('Tigger LSM', 'Tigger LSM'),
        ('FITS', 'FITS'),
        ('Siamese Model', 'Siamese Model'),
    )

    OUTPUT_TYPES = (
        ('Image', 'Image'),
        ('Visibilities', 'Visibilities'),
    )

    # global settings
    name = CharField(initial='New simulation', max_length=200)
    sky_type = ChoiceField(choices=SKY_TYPES, initial='T')
    sky_model = FileField(required=False)
    tdl_conf = FileField(label='TDL Configuration File', required=False)
    tdl_section = CharField(required=False, max_length=200,
                            initial='turbo-sim:initial')
    make_psf = BooleanField(initial=True, required=False)
    add_noise = BooleanField(initial=True, required=False)
    vis_noise_std = FloatField(label="Noise Standard Deviation", initial=0)
    output = ChoiceField(label='Output type', choices=OUTPUT_TYPES, initial='I')

    # observation setup
    ms_hours = FloatField(label='Synthesis time', initial=0.25, help_text='in hours')
    ms_dtime = IntegerField(label='Integration time', initial=10,
                            help_text='in seconds')
    ms_freq0 = FloatField(label='Start frequency', initial=1400e6, help_text='in Hz')
    ms_dfreq = FloatField(label='Channel width', initial=50e6, help_text='in Hz')
    ms_nchan = IntegerField(label='Channels per band', initial=1,
                            help_text='Number of frequency channels per band')
    ms_nband = IntegerField(label='Frequency bands', initial=1,
                            help_text='Number of frequency bands')
    ms_write_auto_corr = BooleanField(label='Autocorrelations',
                                      help_text='Include autocorrelation in data',
                                      initial=True)
    ms_dec = FloatField(label='Declinations', initial=-30)
    ms_ra = FloatField(label='Right ascension', initial=0)

    BEAM_TYPES = (
        ('MeerKAT 1', 'MeerKAT 1'),
        ('MeerKAT 2', 'MeerKAT 2'),
        ('MeerKAT 3', 'MeerKAT 3'),
        ('KAT-7', 'KAT-7'),
        ('WSRT', 'WSRT'),
        ('JVLA', 'JVLA'),
    )

    # dish settings
    ds_amp_phase_gains = FloatField(label='Amplitude Phase Gains', initial=1)
    ds_parallactic_angle_rotation = BooleanField(label='Parallactic Angle Rotation',
                                                 initial=True)
    ds_primary_beam = ChoiceField(choices=BEAM_TYPES, initial='M')
    ds_feed_angle = FloatField(label="Feed angle", initial=0)

    # corruptions
    cr_amp_phase_gains = FloatField(label="Amplitude Phase Gains", initial=1)
    cr_pointing_error = FloatField(initial=0)
    cr_rfi = FloatField(initial=0)

    WEIGHTING_TYPES = (
        ('Natural', 'Natural'),
        ('Uniform', 'Uniform'),
        ('Briggs', 'Briggs'),
    )

    IMAGING_TYPES = (
        ('Channel', 'Channel'),
        ('MFS', 'MFS'),
    )

    CHANNELISE_TYPES = (
        ('NCHAN', 'Average all'),
        ('1', 'Image every channel'),
        ('custom', 'Custom'),
    )

    # imaging settings
    im_npix = IntegerField(label='Image size', initial=512, help_text='in pixels')
    im_cellsize = FloatField(label='Pixel size', help_text='in arcseconds',
                             initial=1)
    im_weight = ChoiceField(label='uv-Weighting', choices=WEIGHTING_TYPES, initial='N')
    im_weight_fov = FloatField(label='Weight FoV', help_text='in arcminutes',
                               initial=1)
    im_wprojplanes = IntegerField(label='w-Projection planes', initial=0)
    im_mode = ChoiceField(label='Imaging mode', choices=IMAGING_TYPES, initial='C')
    im_spwid = CharField(label='Spectral window', initial=0, max_length=32)
    channelise = ChoiceField(label='Image channelise', choices=CHANNELISE_TYPES, initial='A')
    im_stokes = CharField(label='Stokes', initial='I', max_length=4)

    DECONV_TYPES = (
        ('csclean', 'csclean'),
        ('hogbom', 'hogbom'),
        ('clark', 'clark'),
        ('multiscale', 'multiscale'),
        ('MORESANE', 'MORESANE'),
    )

    # deconvolution settings
    deconvolve = BooleanField(label='Deconvolve', initial=True)
    dc_operation = ChoiceField(label='Deconvolution Algorithm', choices=DECONV_TYPES,
                               initial='C')
    dc_uservector = CharField(label='Clean scales',
                              initial='0 1 4 8 16 64 128',
                              help_text='List of scales to clean',
                              max_length=64)
    dc_nscales = FloatField(label='Scales to clean', initial=4)
    dc_niter = IntegerField(label='Clean Iterations',
                            help_text='number of clean iterations',
                            initial=1000)
    dc_threshold = FloatField(label='Clean threshold', help_text='in mJy',
                              initial=0)