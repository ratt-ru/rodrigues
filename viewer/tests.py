from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewTest(TestCase):
    def test_database_view(self):
        url = reverse('fits', kwargs={'path': 'results.dirty.fits'})
        for _ in range(20):
            response = self.client.get(url)
        #self.assertEqual(response.status_code, 200)