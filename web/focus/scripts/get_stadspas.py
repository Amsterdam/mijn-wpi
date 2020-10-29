import sys

from ..focusconnect import FocusConnection

import focus.focusconnect
import focus.gpass_connect

from ..config import config, credentials, get_TMA_certificate
from ..focusserver import FocusServer

bsn = sys.argv[1]

focus.focusconnect.LOG_RAW = True
focus.gpass_connect.LOG_RAW = True

focus_connection = FocusConnection(config, credentials)
# Serve the FOCUS requests that are exposed by this server
focus_server = FocusServer(focus_connection, get_TMA_certificate())

stadspas = focus_server._collect_stadspas_data(bsn)
