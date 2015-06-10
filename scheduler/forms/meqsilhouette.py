from django.forms import CharField, FloatField, FileField, BooleanField, \
    IntegerField, ChoiceField
from form_utils.forms import BetterForm


# global settings
telescope = (
	'name',
        'sim_SMT',
        'sim_CARMA',
        'sim_LMT',
        'sim_ALMA',
        'sim_PV',
        'sim_PdBI',
        'sim_Hawaii',
	'sim_GLT',
        'addant',
        'addantpos',


)

# set skymodel
sky = (
    'fitsname',


)
#data output
outputvisibility = (
	'exportms',
	'exportuvfits',
	)

# observation setup
observation = (
    'ms_obslength',
    'ms_tint',
    'ms_nu',
    'ms_dnu',
    'ms_nchan',
    'ms_elevation_flag',
    'ms_StartTime',
)

#Noise
noise = (
    'add_noise',
    'sefd_SMT',
    'sefd_CARMA',
    'sefd_LMT',
    'sefd_ALMA',
    'sefd_PV',
    'sefd_PdBI',
    'sefd_Hawaii',
    'sefd_GLT',
    'addantsefd',

    )

#G-Jones
gjones = (
'gjones_me_g_enable',
'gjones_gain_error_model',
'gjones_phase_error_model',
'gjones_gain_minval',
'gjones_gain_maxval',
'gjones_gain_min_period',
'gjones_gain_max_period',
'gjones_phase_maxerr',
'gjones_phase_min_period',
'gjones_phase_max_period',
'gjones_gain_min0',
'gjones_gain_max0',
'gjones_gain_max1',
'gjones_gain_max2',
'gjones_gain_max3',
'gjones_gain_scale',
'gjones_gain_offset',
'gjones_phase_min0',
'gjones_phase_max0',
'gjones_phase_max1',
'gjones_phase_max2',
'gjones_phase_max3',
'gjones_phase_scale',
'gjones_phase_offset',
'gjones_gain_offset',
'gjones_phase_offset',
)

##E-jones
ejones=(
'ejones_me_e_enable',
'ejones_me_epe_enable',
'ejones_pe_l_error_model',
'ejones_pe_m_error_model',
'ejones_pe_l_maxerr',
'ejones_pe_l_min_period',
'ejones_pe_l_max_period',
'ejones_pe_m_maxerr',
'ejones_pe_m_min_period',
'ejones_pe_m_max_period',
'ejones_pe_l_min0',
'ejones_pe_l_max0',
'ejones_pe_l_max1',
'ejones_pe_l_max2',
'ejones_pe_l_max3',
'ejones_pe_l_offset',
'ejones_pe_l_scale',
'ejones_pe_m_min0',
'ejones_pe_m_max0',
'ejones_pe_m_max1',
'ejones_pe_m_max2',
'ejones_pe_m_max3',
'ejones_pe_m_offset',
'ejones_pe_m_scale',
'ejones_pe_l_offset',
'ejones_pe_m_offset',
 )

#ISM scattering
ism = (
    'ismscatter',
    'ism_major_axis',
    'ism_minor_axis',
    'ism_rotation_angle',
    )
    

# imaging settings
imaging = (
    'im_npix',
    'im_cellsize',
'im_uvweight',
'im_robust',
'im_operation',
'im_niter',
'im_gain',
'im_threshold',
'im_stokes',
)




class Form(BetterForm):
    docker_image = 'tariqblecher/meqsilhouette'

    class Meta:
        fieldsets = [('telescope', {'fields': telescope,
                                    'description': 'Observatory'}),
                     ('sky', {'fields': sky,
                              'description': 'Sky Model'}),
                     ('outputvisibility', {'fields': outputvisibility,
                              'description': 'Visibility outputs'}),

                     ('observation', {'fields': observation,
                                      'description': 'Observation setup'}),
                     ('noise',{'fields':noise,
                               'description':'Noise'}),
                     ('gjones',{'fields':gjones,
                               'description':'Direction independent complex gains'}),
                     ('ejones',{'fields':ejones,
                               'description':'Direction dependent complex gains'}),
                     ('ism',{'fields':ism,
                             'description':'ISM scattering gaussian'}),
                     ('imaging', {'fields': imaging,
                                  'description': 'imaging settings'}),
                    
                     ]



    # Telescope setup
    name = CharField(initial='New simulation', max_length=200)
    sim_SMT = BooleanField(label='SMT', required=False,initial=True)
    sim_CARMA = BooleanField(label='CARMA', required=False,initial=True)
    sim_LMT = BooleanField(label='LMT', required=False,initial=True)
    sim_ALMA = BooleanField(label='ALMA', required=False,initial=True)
    sim_PV = BooleanField(label='PV', required=False,initial=True)
    sim_PdBI = BooleanField(label='PdBI', required=False,initial=True)
    sim_Hawaii = BooleanField(label='Hawaii', required=False,initial=True)
    sim_GLT= BooleanField(label='GLT', required=False,initial=True,
				help_text='Choose antennae set for observation')
    addant= BooleanField(label='Additional Antenna', required=False,initial=False,
                                help_text='Add an additional Antenna to the array')
    addantpos=CharField(label='Add. antenna position',initial='1.0 2.0 3.0 ',max_length=300,
			help_text='x y z coordinates in units of metres?? Separated by a whitespace') 
    


    # sky setup
    fitsname=FileField(label='input sky fits',initial='test.fits',required=False,
				help_text='if blank a default image will be chosen. Pixelsizes need to be in units of arcsec.')
    # Output visibilities
    exportms = BooleanField(label='Export Measurement Set', required=False,initial=True)
    exportuvfits = BooleanField(label='Export UV FITS', required=False,initial=False)


    # observation setup
    ms_obslength = FloatField(label='observation length', initial=0.25,
                              help_text='in hours')
    ms_tint = IntegerField(label='Integration time', initial=10,
                            help_text='in seconds')
    ms_nu = FloatField(label='Start frequency', initial=230, help_text='in GHz')
    ms_dnu = FloatField(label='Channel width', initial=4, help_text='in GHz')
    ms_nchan = IntegerField(label='Channels', initial=1,
                            help_text='Number of frequency channels')
    ms_elevation_flag = IntegerField(label='lower elevation flag', initial=10,
                            help_text='degrees')
    ms_StartTime=CharField(label='Start Time',required=False,initial='2009/04/06/12:20:00.00')

   
    #Noise

    add_noise = BooleanField(initial=True, required=False,help_text='defaults taken from Lu. et al 201?') 
    sefd_SMT = FloatField(label='SMT', required=False,initial=11900)
    sefd_CARMA = FloatField(label='CARMA', required=False,initial=3500)
    sefd_LMT = FloatField(label='LMT', required=False,initial=560)
    sefd_ALMA = FloatField(label='ALMA', required=False,initial=110)
    sefd_PV = FloatField(label='PV', required=False,initial=2900)
    sefd_PdBI = FloatField(label='PdBI', required=False,initial=1600)
    sefd_Hawaii = FloatField(label='Hawaii', required=False,initial=4900)
    sefd_GLT= FloatField(label='GLT', required=False,initial=7300)
    addantsefd= FloatField(label='Additional Antenna', required=False,initial=7300)
    ERROR_MODELS =(
		( 'SineError','SineError'),
		('RandomPolc','RandomPolc'),
		('FixedOFFset','FixedOFFset'),
		)
    UV_WEIGHT=(
	   ('uniform','uniform'),
		('briggs','briggs'),
		('natural','natural'),
		)
    OPERATION=(
		('csclean','csclean'),
		('clark','clark'),
		('hogbom','hogbom'),
		('multiscale','multiscale')
		)
   


    gjones_me_g_enable = BooleanField(label='enable per antennae gain and phase corruptions',required=False,initial=True)
    gjones_gain_error_model = ChoiceField(label='gain error model',required=False,choices=ERROR_MODELS,initial='SineError')
    gjones_phase_error_model = ChoiceField(label='phase error model',required=False,choices=ERROR_MODELS,initial='SineError',help_text='Phase units are in degrees')
    gjones_gain_minval = FloatField(label='gain minval',required=False,initial=0.1)
    gjones_gain_maxval = FloatField(label='gain maxval',required=False,initial=4)
    gjones_gain_min_period = FloatField(label='gain min period (hours)',required=False,initial=0.01)
    gjones_gain_max_period = FloatField(label='gain max period(hours)',required=False,initial=0.5)
    gjones_phase_maxerr = FloatField(label='phase maxerr',required=False,initial=10)
    gjones_phase_min_period = FloatField(label='phase min period',required=False,initial=0.01)
    gjones_phase_max_period = FloatField(label='phase max period',required=False,initial=0.5)
    gjones_gain_min0 = FloatField(label='gain min0',required=False,initial=-1)
    gjones_gain_max0 = FloatField(label='gain max0',required=False,initial=1)
    gjones_gain_max1 = FloatField(label='gain max1',required=False,initial=2)
    gjones_gain_max2 = FloatField(label='gain max2',required=False,initial=1)
    gjones_gain_max3 = FloatField(label='gain max3',required=False,initial=1)
    gjones_gain_scale = FloatField(label='gain time scale variability (hours)',required=False,initial=0.1)
    gjones_gain_offset = FloatField(label='gain offset',required=False,initial=0)
    gjones_phase_min0 = FloatField(label='phase min0',required=False,initial=-10)
    gjones_phase_max0 = FloatField(label='phase max0',required=False,initial=10)
    gjones_phase_max1 = FloatField(label='phase max1',required=False,initial=20)
    gjones_phase_max2 = FloatField(label='phase max2',required=False,initial=10)
    gjones_phase_max3 = FloatField(label='phase max3',required=False,initial=10)
    gjones_phase_scale = FloatField(label='phase time scale variability (hours)',required=False,initial=0.1)
    gjones_phase_offset = FloatField(label='phase offset',required=False,initial=0)
    gjones_gain_offset = FloatField(label='gain offset',required=False,initial=5)
    gjones_phase_offset = FloatField(label='phase offset',required=False,initial=10)
 
    ejones_me_e_enable =  BooleanField(initial=True,label='enable',required=False)
    ejones_me_epe_enable =  BooleanField(initial=True,label='enable pointing errors',required=False,)

    ejones_pe_l_error_model = ChoiceField(label='pe l error model',required=False,choices=ERROR_MODELS,initial='SineError')
    ejones_pe_m_error_model = ChoiceField(label='pe m error model',required=False,choices=ERROR_MODELS,initial='SineError',help_text='Pointing errors are in units of arcseconds')


    ejones_pe_l_maxerr = FloatField(label='pe l maxerr',required=False,initial=2)
    ejones_pe_l_min_period = FloatField(label='pe l min period',required=False,initial=0.5)
    ejones_pe_l_max_period = FloatField(label='pe l max period',required=False,initial=3)
    ejones_pe_m_maxerr = FloatField(label='pe m maxerr',required=False,initial=2)
    ejones_pe_m_min_period = FloatField(label='pe m min period',required=False,initial=0.5)
    ejones_pe_m_max_period = FloatField(label='pe m max period',required=False,initial=3)

    ejones_pe_l_min0 = FloatField(label='pe l min0',required=False,initial=-0.5)
    ejones_pe_l_max0 = FloatField(label='pe l max0',required=False,initial=0.5)
    ejones_pe_l_max1 = FloatField(label='pe l max1',required=False,initial=0.5)
    ejones_pe_l_max2 = FloatField(label='pe l max2',required=False,initial=0.5)
    ejones_pe_l_max3 = FloatField(label='pe l max3',required=False,initial=0)
    ejones_pe_l_offset = FloatField(label='pe l offset',required=False,initial=0.1)
    ejones_pe_l_scale = FloatField(label='pe l time scale variability(hours)',required=False,initial=2)
    ejones_pe_m_min0 = FloatField(label='pe m min0',required=False,initial=-0.5)
    ejones_pe_m_max0 = FloatField(label='pe m max0',required=False,initial=0.5)
    ejones_pe_m_max1 = FloatField(label='pe m max1',required=False,initial=0.5)
    ejones_pe_m_max2 = FloatField(label='pe m max2',required=False,initial=0.5)
    ejones_pe_m_max3 = FloatField(label='pe m max3',required=False,initial=0)
    ejones_pe_m_offset = FloatField(label='pe m offset',required=False,initial=0.1)
    ejones_pe_m_scale = FloatField(label='pe m time scale variability',required=False,initial=2)
    ejones_pe_l_offset = FloatField(label='pe l offset',required=False,initial=0.1)
    ejones_pe_m_offset = FloatField(label='pe m offset',required=False,initial=0.1)

#ISM scattering gaussian
    ismscatter=BooleanField(initial=True, required=False,help_text='Ensure the pixelsize in fits header is correct')

    ism_major_axis=FloatField(label='major axis', initial=1.309,
			  help_text='mas/cm^2') 
    ism_minor_axis=FloatField(label='minor axis', initial=0.64,
			  help_text='mas/cm^2')
    ism_rotation_angle=FloatField(label='rotation angle', initial=78,
			      help_text='degrees East of North')
    


    
    # imaging settings
   
    im_npix = IntegerField(label='Image size', required=True,initial=128,help_text='in pixels ')
    im_cellsize = FloatField(label='Pixel size', required=True,initial=1,help_text='in micro arcseconds ')
    
   
    im_uvweight=ChoiceField(choices=UV_WEIGHT,initial=uniform,label='Pixel size')
    im_robust= FloatField(label='Robust',initial=0)
    im_operation=ChoiceField(label='Clean operation',choices=OPERATION,initial=clark)
    im_niter=FloatField(label='Number of iterations', help_text='for a dirty image set this to zero')
    im_gain=FloatField(label='Loop Gain',initial=0.1)
    im_threshold=FloatField(label='Clean Threshold', initial=0)
    im_stokes=CharField(label='STOKES',initial='I')
    


  
    

    
