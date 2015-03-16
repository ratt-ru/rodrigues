from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewTest(TestCase):
    def test_fits_view(self):
        url = reverse('fits', kwargs={'path': 'results.dirty.fits'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)