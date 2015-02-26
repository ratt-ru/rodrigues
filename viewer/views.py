import logging
import os

from django.views.generic import TemplateView
from django.http import Http404
from django.http import HttpResponse
from django.conf import settings

import matplotlib
import aplpy


logger = logging.getLogger(__name__)


class FitsView(TemplateView):
    """
    Returns an rendered image. uses path keyword argument. Only
    allowes files which are in te settings.RESULTS_DIR folder somewhere.
    """
    def render_to_response(self, context, **kwargs):
        path = self.kwargs['path']
        fullpath = os.path.realpath(os.path.join(settings.MEDIA_ROOT, path))
        if not fullpath.startswith(settings.MEDIA_ROOT):
            raise Http404
        if not os.access(fullpath, os.R_OK):
            raise Http404
        response = HttpResponse(content_type='image/png')
        fig = matplotlib.pyplot.figure()

        try:
            plot = aplpy.FITSFigure(fullpath, figure=fig,
                                    auto_refresh=False)
        except IOError as e:
            matplotlib.pyplot.text(0.1, 0.8, str(e))
        else:
            plot.show_colorscale()
        fig.canvas.print_figure(response, format='png')
        return response

