import logging
import os

from django.views.generic import TemplateView
from django.http import Http404
from django.http import HttpResponse
from django.conf import settings

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot
import aplpy
import astropy


astropy.log.setLevel('ERROR')
logger = logging.getLogger(__name__)


class FitsView(TemplateView):
    """
    Returns an rendered image. uses path keyword argument. Only
    allowes files which are in te settings.RESULTS_DIR folder somewhere.
    """
    def render_to_response(self, context, **kwargs):

        size = int(self.request.GET.get('size', 5))
        vmin = float(self.request.GET.get('vmin', 0))
        vmax = float(self.request.GET.get('vmax', 0.1))
        colorbar = (self.request.GET.get('colorbar', 'True').lower() != 'false')

        path = self.kwargs['path']
        fullpath = os.path.realpath(os.path.join(settings.MEDIA_ROOT, path))

        if not fullpath.startswith(os.path.realpath(settings.MEDIA_ROOT)):
            raise Http404
        if not os.access(fullpath, os.R_OK):
            raise Http404

        response = HttpResponse(content_type='image/png')
        figure = matplotlib.pyplot.figure(figsize=(size, size))

        if colorbar:
            subplot = [0.0, 0.0, 0.9, 1]
        else:
            subplot = [0.0, 0.0, 1, 1]

        try:
            fig = aplpy.FITSFigure(fullpath,
                                   figure=figure,
                                   subplot=subplot,
                                   figsize=(size, size))
        except IOError as e:
            matplotlib.pyplot.text(0.1, 0.8, str(e))
        else:
            fig.show_colorscale(vmin=vmin, vmax=vmax)
            if colorbar:
                fig.add_colorbar()
                fig.colorbar.set_font(size='xx-small')
            fig.axis_labels.hide()
            fig.tick_labels.hide()
            fig.ticks.hide()
        figure.canvas.print_figure(response, format='png')
        return response


