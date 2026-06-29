from django.conf import settings
from django.test import SimpleTestCase


class StaticFilesSettingsTests(SimpleTestCase):
    def test_staticfiles_use_whitenoise_storage(self):
        self.assertEqual(
            settings.STORAGES["staticfiles"]["BACKEND"],
            "whitenoise.storage.CompressedManifestStaticFilesStorage",
        )
