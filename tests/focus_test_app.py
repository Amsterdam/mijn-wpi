from unittest.mock import patch

from tma_saml import FlaskServerTMATestCase

from app.server import application


def get_fake_tma_cert():
    return "fake cert"


class FocusApiTestApp(FlaskServerTMATestCase):
    def setUp(self):
        self.client = self.get_tma_test_app(application)
        self.maxDiff = None
