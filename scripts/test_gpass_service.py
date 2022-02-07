from app.focus_service_stadspas_admin import get_stadspas_admin_number
from app.gpass_service import get_stadspassen


bsn = ""

admin = get_stadspas_admin_number(bsn)
stadspas = get_stadspassen(admin["admin_number"])

print(stadspas)
