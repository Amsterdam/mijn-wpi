from app.tests.wpi_test_app import WpiApiTestApp


class WPITestServer(WpiApiTestApp):
    def test_status_health(self):
        result = self.client.get("/status/health")

    def test_aanvragen(self):
        result = self.client.get("/wpi/aanvragen")

    def test_document(self):
        result = self.client.get("/wpi/document")

    def test_jaaropgaven(self):
        result = self.client.get("/wpi/jaaropgaven")

    def test_uitkeringspecificaties(self):
        result = self.client.get("/wpi/uitkeringsspecificaties")

    def test_stadspassen(self):
        result = self.client.get("/wpi/stadspas")

    def test_stadspastransactions(self):
        result = self.client.get(
            "/wpi/stadspas/transacties/<string:encrypted_admin_pasnummer>"
        )
