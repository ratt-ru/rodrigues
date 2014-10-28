from form_utils.forms import BetterModelForm
from .models import Simulation


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

fields = global_ + observation + dish + corruptions + imaging + deconvolution


class SimulateForm(BetterModelForm):
    class Meta:
        model = Simulation
        fields = fields

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


