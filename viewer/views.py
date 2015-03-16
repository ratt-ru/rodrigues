import logging
import os
from collections import namedtuple
import time
import magic

from django.views.generic import DetailView
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot
import aplpy
import astropy

from scheduler.models import Job


astropy.log.setLevel('ERROR')
logger = logging.getLogger(__name__)
filemagic = magic.Magic()  # flags=magic.MAGIC_MIME_TYPE)


class FitsView(DetailView):
    """
    Returns an rendered image. uses path keyword argument. Only
    allowes files which are in te settings.RESULTS_DIR folder somewhere.
    """
    model = Job

    def render_to_response(self, context, **kwargs):

        size = int(self.request.GET.get('size', 5))
        vmin = float(self.request.GET.get('vmin', 0))
        vmax = float(self.request.GET.get('vmax', 0.1))
        colorbar = (self.request.GET.get('colorbar', 'True').lower() != 'false')

        path = self.kwargs['path']
        prefix = os.path.realpath(os.path.join(settings.MEDIA_ROOT))
        fullpath = os.path.realpath(os.path.join(settings.MEDIA_ROOT,
                                                 self.object.results_dir,
                                                 path))

        if not fullpath.startswith(prefix):
            raise Http404("something weird with that filename")
        if not os.access(fullpath, os.R_OK):
            raise Http404("can't open filename")

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


DirItem = namedtuple('DirItem', ['fullpath', 'name', 'type', 'size',
                                 'modified', 'is_image'])


class OverView(DetailView):
    model = Job
    template_name = 'viewer/job_overview.html'

    def get_context_data(self, **kwargs):
        context = super(OverView, self).get_context_data(**kwargs)
        prefix = os.path.realpath(settings.MEDIA_ROOT)

        if not self.object.results_dir:
            messages.error(self.request, 'result_dir DB field empty')
            return context

        path = os.path.realpath(os.path.join(prefix,
                                             self.object.results_dir))

        if not os.access(path, os.R_OK):
            messages.error(self.request, 'Directory doesn\'t exists')
            return context
        if not path.startswith(prefix):
            raise Http404('something weird with that path')

        all_files = []
        for root, _, files in os.walk(path):
            all_files += [os.path.join(root, f) for f in files]

        images = []
        dirlist = []
        for fullpath in all_files:
            name = fullpath[len(path)+1:]
            type_ = filemagic.id_filename(fullpath)
            size = os.path.getsize(fullpath)
            modified = time.ctime(os.path.getmtime(fullpath))
            is_image = type_.startswith('FITS image data')
            if is_image:
                images.append(name)
            dirlist += [DirItem(fullpath, name, type_, size, modified,
                                is_image)]

        context['dirlist'] = dirlist
        context['images'] = images
        return context


class SomethingView(DetailView):
    """
    Will redirect to correct view according to file type.

    Will render error page if file type is not understood.
    """
    model = Job
    template_name = 'viewer/job_unknowntype.html'

    def get_context_data(self, **kwargs):
        context = super(SomethingView, self).get_context_data(**kwargs)
        prefix = os.path.realpath(settings.MEDIA_ROOT)
        fullpath = os.path.realpath(os.path.join(prefix,
                                                 self.object.results_dir,
                                                 self.kwargs['path']))

        # make sure we are not reading stuff outside of the media folder
        if not fullpath.startswith(prefix):
            raise Http404('something weird with that path')

        if not os.access(fullpath, os.R_OK):
            raise Http404('Directory doesn\'t exists')

        context['type'] = filemagic.id_filename(fullpath)
        context['path'] = self.kwargs['path']
        return context

    def render_to_response(self, context, **response_kwargs):
        if context['type'].startswith("FITS image data"):
            return HttpResponseRedirect(reverse('fits',
                                                kwargs={'pk': self.object.id,
                                                        'path': self.kwargs['path']}))
        if context['type'].startswith("ASCII text"):
            return HttpResponseRedirect(reverse('text',
                                                kwargs={'pk': self.object.id,
                                                        'path': self.kwargs['path']}))

        return super(SomethingView, self).render_to_response(context)


class TextView(DetailView):
    model = Job
    template_name = 'viewer/job_textfile.html'

    def get_context_data(self, **kwargs):
        context = super(TextView, self).get_context_data(**kwargs)
        path = self.kwargs['path']
        prefix = os.path.realpath(os.path.join(settings.MEDIA_ROOT))
        fullpath = os.path.realpath(os.path.join(settings.MEDIA_ROOT,
                                                 self.object.results_dir,
                                                 path))

        if not fullpath.startswith(prefix):
            raise Http404("something weird with that filename")
        if not os.access(fullpath, os.R_OK):
            raise Http404("can't open filename")

        with open(fullpath, 'r') as f:
            context['path'] = path
            context['content'] = ''.join(f.readlines())
        return context
