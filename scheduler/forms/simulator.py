from django.forms import CharField, FloatField, FileField, BooleanField, \
    IntegerField, ChoiceField
from form_utils.forms import BetterForm



# global settings
telescope = (
    'name',
    'observatory',
    'sefd',
    'output',
)

# set skymodel
sky = (
    'sky_type',
    'sky_model',
    'katalog_id',
    'radius',
    'fluxrange',
    'add_noise',
    'vis_noise_std',
)

# observation setup
observation = (
    'ms_synthesis',
    'ms_dtime',
    'ms_freq0',
    'ms_dfreq',
    'ms_nchan',
    'ms_dec',
    'ms_ra',
)

# imaging settings
imaging = (
    'use_default_im',
    'imager',
    'im_npix',
    'im_cellsize',
    'im_weight',
    'im_robust',
    'im_weight_fov',
    'im_wprojplanes',
    'im_mode',
    'channelise',
    'im_stokes',
)


lwimager = (
    'lwimager',
    'lwimager_niter',
    'lwimager_gain',
    'lwimager_threshold',
    'lwimager_sigmalevel',
    'lwimager_operation',
    'lwimager_nscales',
    'lwimager_uservector',
    'lwimager_cyclefactor',
    'lwimager_cyclespeedup',
    'lwimager_stoppointmode',
)

wsclean = (
    'wsclean',
    'wsclean_niter',
    'wsclean_gain',
    'wsclean_mgain',
    'wsclean_threshold',
    'wsclean_sigmalevel',
    'wsclean_joinpolarizations',
    'wsclean_joinchannels',
    'wsclean_multiscale',
    'wsclean_multiscale_dash_scale_dash_bias',
    'wsclean_multiscale_dash_threshold_dash_bias',
    'wsclean_cleanborder',
    'wsclean_smallpsf',
    'wsclean_nonegative',
    'wsclean_beamsize',
)

casa = (
    'casa',
    'casa_niter',
    'casa_gain',
    'casa_threshold',
    'casa_sigmalevel',
    'casa_psfmode',
    'casa_imagermode',
    'casa_gridmode',
    'casa_nterms',
    'casa_reffreq',
    'casa_multiscale',
    'casa_negcomponent',
    'casa_smallscalebias',
    'casa_restoringbeam',
    'casa_cyclefactor',
    'casa_cyclespeedup',
)

moresane = (
    'moresane',
    'moresane_scalecount',
    'moresane_startscale',
    'moresane_stopscale',
    'moresane_sigmalevel',
    'moresane_loopgain',
    'moresane_tolerance',
    'moresane_accuracy',
    'moresane_majorloopmiter',
    'moresane_minorloopmiter',
    'moresane_convmode',
    'moresane_enforcepositivity',
    'moresane_edgesupression',
    'moresane_edgeoffset',
    'moresane_mfs',
    'moresane_spi_dash_sigmalevel',
)


class Form(BetterForm):
    docker_image = 'skasa/simulator'

    class Meta:
        fieldsets = [('telescope', {'fields': telescope,
                                    'description': 'Observatory'}),
                     ('sky', {'fields': sky,
                              'description': 'Sky Model'}),
                     ('observation', {'fields': observation,
                                      'description': 'Observation setup'}),
                     ('imaging', {'fields': imaging,
                                  'description': 'imaging settings'}),
                     ('lwimager', {'fields': lwimager,
                                   'description':
                                       'LWIMAGER deconvolution settings'}),
                     ('wsclean', {'fields': wsclean,
                                  'description':
                                      'WSCLEAN deconvolution settings'}),
                     ('casa', {'fields': casa,
                               'description': 'CASA deconvolution settings'}),
                     ('moresane', {'fields': moresane,
                                   'description':
                                       'MORESANE deconvolution settings'}),
                     ]

    SKY_TYPES = (
        ('Tigger-LSM', 'Tigger-LSM'),
        ('ASCII', 'ASCII'),
        ('FITS', 'FITS'),
        ('KATALOG', 'KATALOG'),  # this is a catalog of known skies
    )

    OUTPUT_TYPES = (
        ('Image', 'Image'),
        ('Visibilities', 'Visibilities'),
    )

    OBSERVATORIES = (
        ('MeerKAT', 'MeerKAT'),
        ('KAT-7', 'KAT-7'),
        ('JVLA-A', 'JVLA-A'),
    )

    KATALOG = (
        ('nvss6deg', 'nvss6deg'),
        ('scubed1deg', 'scubed1deg'),
        ('3c147_field', '3c147_field'),
        ('3c147_field_no_core', '3c147_field_no_core'),
    )

    # Telescope setup
    name = CharField(initial='New simulation', max_length=200)
    observatory = ChoiceField(initial='MK', choices=OBSERVATORIES)
    output = ChoiceField(label='Output type', choices=OUTPUT_TYPES, initial='Image')
    sefd = FloatField(label='SEFD', required=False,
                      help_text='System defaults will be used if left blank')

    # sky setup
    sky_type = ChoiceField(choices=SKY_TYPES, initial='Tigger-LSM')
    sky_model = FileField(required=False)
    katalog_id = ChoiceField(label='KATALOG', required=False, initial='nvss6deg', choices=KATALOG,
                             help_text='Choose from our sky catalogs')
    radius = FloatField(label='Radius', initial=0.5, required=False,
                        help_text='Radius of degrees')
    fluxrange = CharField(label='Flux range', initial='0.001-1',
                          max_length=32,
                          help_text='Flux range in Jy')
    ms_dec = CharField(label='Declination',
                       initial='-30d0m0s',
                       help_text='in dms',
                       max_length=32)
    ms_ra = CharField(label='Right ascension',
                      initial='0h0m0s',
                      help_text='in hms',
                      max_length=32)
    add_noise = BooleanField(initial=True, required=False)
    vis_noise_std = FloatField(label='Visibility noise std', initial=0,
                               help_text='Generates from SEFD if 0')

    # observation setup
    ms_synthesis = FloatField(label='Synthesis time', initial=0.25,
                              help_text='in hours')
    ms_dtime = IntegerField(label='Integration time', initial=10,
                            help_text='in seconds')
    ms_freq0 = FloatField(label='Start frequency', initial=700, help_text='in MHz')
    ms_dfreq = FloatField(label='Channel width', initial=50e3, help_text='in kHz')
    ms_nchan = IntegerField(label='Channels', initial=1,
                            help_text='Number of frequency channels')

    IMAGERS = (
        ('LWIMAGER', 'LWIMAGER'),
        ('WSCLEAN', 'WSCLEAN'),
        ('CASA', 'CASA'),
    )

    WEIGHTING_TYPES = (
        ('Natural', 'Natural'),
        ('Uniform', 'Uniform'),
        ('Briggs', 'Briggs'),
    )

    IMAGING_TYPES = (
        ('channel', 'channel'),
        ('mfs', 'mfs'),
        ('velocity', 'velocity'),
        ('frequency', 'frequency'),
    )

    # imaging settings
    use_default_im = BooleanField(label='Use default imaging settings',
                                  initial=True, required=False)
    imager = ChoiceField(label='Imager', initial='LW', choices=IMAGERS)
    im_npix = IntegerField(label='Image size', initial=512, help_text='in pixels')
    im_cellsize = FloatField(label='Pixel size', help_text='in arcseconds',
                             initial=1)
    im_weight = ChoiceField(label='uv-Weighting', choices=WEIGHTING_TYPES,
                            initial='N')
    im_robust = FloatField(label='Robust',
                           initial=0,
                           help_text='Briggs robust parameter')
    im_weight_fov = FloatField(label='Weight FoV', help_text='in arcminutes',
                               required=False)
    im_wprojplanes = IntegerField(label='w-Projection planes', initial=0)
    im_mode = ChoiceField(label='Imaging mode', choices=IMAGING_TYPES,
                          initial='C')
    channelise = IntegerField(label='Image channelise',
                              initial=0,
                              help_text='0 means average all, 1 per channel, etc.')
    im_stokes = CharField(label='Stokes', initial='I', max_length=4)

    CLEAN_TYPES = (
        ('csclean', 'csclean'),
        ('hogbom', 'hogbom'),
        ('clark', 'clark'),
        ('multiscale', 'multiscale'),
    )


    # lwimager
    lwimager = BooleanField(label='Deconvolve with me!', required=False)
    lwimager_niter = IntegerField(label='NITER', initial=1000)
    lwimager_gain = FloatField(label='Loop gain', initial=0.1)
    lwimager_threshold = FloatField(label='Clean Threshold', initial=0,
                                    help_text='In Jy')

    lwimager_sigmalevel = FloatField(label='Clean sigma level', initial=0,
                                     help_text='In sigma above noise')
    lwimager_operation = ChoiceField(label='Clean algorithm',
                                     choices=CLEAN_TYPES, initial='C')
    lwimager_cyclefactor = FloatField(label='Cycle factor', initial=1.5)
    lwimager_cyclespeedup = FloatField(label='Cycle speed up', initial=-1)
    lwimager_stoppointmode = FloatField(label='Stop point mode,', initial=-1)
    lwimager_nscales = IntegerField(label='Scales for MS clean', initial=4)
    # Multi scale clean : No need to have a seperate block for MS clean.
    lwimager_uservector = CharField(label='Clean scales', required=False,
                                    help_text='Comma seperated scales in pixels',
                                    max_length=64)

    # wsclean
    wsclean = BooleanField(label='Deconvolve with me!', required=False)
    wsclean_niter = IntegerField(label='NITER', initial=1000)
    wsclean_gain = FloatField(label='Minor loop gain', initial=0.1)
    wsclean_mgain = FloatField(label='Major loop gain', initial=0.9)
    wsclean_threshold = FloatField(label='Clean Threshold', initial=0,
                                   help_text='In Jy')
    wsclean_sigmalevel = FloatField(label='Clean sigma level', initial=0,
                                    help_text='In sigma above noise')
    wsclean_joinpolarizations = BooleanField(label='Join polarizations',
                                             required=False)
    wsclean_joinchannels = BooleanField(label='Join channels', required=False)
    wsclean_multiscale = BooleanField(label='Multiscale clean', required=False)
    wsclean_multiscale_dash_threshold_dash_bias = FloatField(label='Multi scale threshold bias', initial=0.7)
    wsclean_multiscale_dash_scale_dash_bias = FloatField(label='Multi scale bias',
                                                         initial=0.6)
    wsclean_cleanborder = FloatField(label='Clean border', initial=5,
                                     help_text='In percentage of image '
                                               'width/height')
    wsclean_smallpsf = BooleanField(label='Small PSF', required=False,
                                    help_text='Resize the psf to speed up '
                                              'minor clean iterations')
    wsclean_nonegative = BooleanField(label='No negative', required=False,
                                      help_text='Do not allow negative '
                                                'components during cleaning')
    wsclean_stopnegative = BooleanField(label='Stop on negative', required=False)
    wsclean_beamsize = CharField(label='Restoring beam size', required=False,
                                 help_text='In arcseconds',
                                 max_length=32)

    PSF_MODE = (
        ('clark', 'clark'),
        ('clarkstokes', 'clarkstokes'),
        ('hogbom', 'hogbom'),
    )

    IMAGER_MODE = (
        ('csclean', 'csclean'),
        ('mosiac', 'mosiac'),
    )

    GRID_MODE = (
        ('widefield', 'widefield'),
        ('aprojection', 'aprojection'),
    )

    #casa
    casa = BooleanField(label='Deconvolve with me!', required=False)
    casa_niter = IntegerField(label='NITER', initial=1000)
    casa_threshold = FloatField(label='Threshold', initial=0)
    casa_sigmalevel = FloatField(label='Clean sigma level', initial=0,
                                 help_text='In sigma above noise')
    casa_gain = FloatField(label='Loop Gain',
                           initial=0.1,
                           help_text='Clean Loop gain')
    casa_psfmode = ChoiceField(label='PSF mode',
                               initial='clark',
                               choices=PSF_MODE)
    casa_imagermode = ChoiceField(label='Imager mode',
                                  required=False,
                                  choices=IMAGER_MODE,
                                  initial='csclean')
    casa_gridmode = ChoiceField(label='Grid mode',
                                required=False,
                                choices=GRID_MODE,
                                initial='widefield',
                                help_text='A-projection only works JVLA')
    casa_nterms = IntegerField(label='NTERMS',
                               initial=1,
                               help_text='See CASA clean task')
    casa_reffreq = FloatField(label='MFS ref Frequency', required=False,
                              help_text='in MHz')
    casa_multiscale = CharField(label='Multiscale',
                                required=False,
                                help_text='Deconvolution scales in pixels',
                                max_length=200)
    casa_negcomponent = FloatField(label='Negative Components',
                                   initial=-1,
                                   help_text='See CASA clean task')
    casa_smallscalebias = FloatField(label='Small scale bias',
                                     initial=0.6,
                                     help_text='See CASA clean task')
    casa_restoringbeam = CharField(label='Restoring beam',
                                   required=False,
                                   max_length=32)
    casa_cyclefactor = FloatField(label='Cycle factor', initial=1.5)
    casa_cyclespeedup = IntegerField(label='Cycle speed up', initial=-1)


    #moresane
    CONV_TYPES = (
        ('circular', 'circular'),
        ('linear', 'linear'),
    )

    moresane = BooleanField(label='Deconvolve with me!', required=False)
    moresane_scalecount = IntegerField(label='Scale count',
                                       required=False,
                                       help_text='See MORESANE help')
    moresane_subregion = IntegerField(label='Sub region',
                                      required=False,
                                      help_text='Inner region to deconvolve in pixels')
    moresane_startscale = IntegerField(label='Start scale', initial=1)
    moresane_stopscale = IntegerField(label='Stop scale', initial=20)
    moresane_sigmalevel = FloatField(label='Threshold level',
                                     initial=3,
                                     help_text='in sigma above noise')
    moresane_loopgain = FloatField(label='Loop gain', initial='0.1')
    moresane_tolerance = FloatField(label='Tolerance', initial=.75)
    moresane_accuracy = FloatField(label='Accuracy', initial=1e-6)
    moresane_majorloopmiter = IntegerField(label='Major loop iterations',
                                           initial=100)
    moresane_minorloopmiter = IntegerField(label='Minor loop iterations',
                                           initial=50)
    moresane_convmode = ChoiceField(label='Convolution mode',
                                    initial='circular',
                                    choices=CONV_TYPES)
    moresane_enforcepositivity = BooleanField(label='Enforce Positivity',
                                              required=False)
    moresane_edgesupression = BooleanField(label='Edge Suppression',
                                           required=False)
    moresane_edgeoffset = IntegerField(label='Edge offset', initial=0)
    moresane_mfs = BooleanField(label='MFS map', required=False,
                                help_text='Comes with an spi map')

    # I use a double underscore to a represent hyphen (for simulator)
    moresane_spi_dash_sigmalevel = FloatField(label='spi threshold level',
                                              initial=10,
                                              help_text='In sigma above noise')
