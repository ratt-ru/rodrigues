from form_utils.forms import BetterModelForm
from .models import Simulation


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
#    'tdl_conf',
#    'tdl_section',
    'katalog_id',
    'radius',
    'fluxrange',
    'add_noise',
    'vis_noise_std',
)

# observation setup
observation = (
    'ms_synthesis',
    'ms_scan_length',
    'ms_start_time',
    'ms_dtime',
    'ms_freq0',
    'ms_dfreq',
    'ms_nchan',
#    'ms_write_auito_corr',
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
    'imager',
    'im_npix',
    'im_cellsize',
    'im_weight',
    'im_robust',
    'im_weight_fov',
    'im_wprojplanes',
    'im_mode',
    'im_spwid',
    'channelise',
    'im_stokes',
    'make_psf',
)


lwimager = (
    'lwimager',
    'lwimager_niter',
    'lwimager_gain',
    'lwimager_threshold',
    'lwimager_operation',
    'lwimager_nscales',
    'lwimager_uservector',
    'lwimager_cyclefactor',
)

wsclean = (
    'wsclean',
    'wsclean_niter',
    'wsclean_gain',
    'wsclean_mgain',
    'wsclean_threshold',
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

fields = telescope + sky + observation + imaging + lwimager + wsclean + casa + moresane # + dish + curruptions

class SimulateForm(BetterModelForm):
    class Meta:
        model = Simulation
        fields = fields

        fieldsets = [('telescope', {'fields': telescope,
                                 'description': 'Observatory'}),
                     ('sky', {'fields': sky,
                                      'description': 'Sky Model'}),
                     ('observation', {'fields': observation,
                                      'description': 'Observation setup'}),
                     ('imaging', {'fields': imaging,
                                  'description': 'imaging settings'}),
#                     ('dish', {'fields': dish,
#                               'description': 'dish settings'}),
#                     ('corruptions', {'fields': corruptions,
#                                      'description': 'Corruptions'}),

                     ('lwimager', {'fields': lwimager,
                                        'description': 'LWIMAGER deconvolution settings'}),
                     ('wsclean', {'fields': wsclean,
                                        'description': 'WSCLEAN deconvolution settings'}),
                     ('casa', {'fields': casa,
                                        'description': 'CASA deconvolution settings'}),
                     ('moresane', {'fields': moresane,
                                        'description': 'MORESANE deconvolution settings'}),
                     ]
