from unittest.mock import patch

from tma_saml import FlaskServerTMATestCase

from app.server import application


class FocusApiTestApp(FlaskServerTMATestCase):
    def setUp(self):
        self.client = self.get_tma_test_app(application)
        self.maxDiff = None
