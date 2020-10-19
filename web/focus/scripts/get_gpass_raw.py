import sys

from focus.config import get_gpass_api_location, get_gpass_bearer_token
from focus.gpass_connect import GpassConnection


admin_number = sys.argv[1]

con = GpassConnection(get_gpass_api_location(), get_gpass_bearer_token())

print(con.get_stadspassen(admin_number))
