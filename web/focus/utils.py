def volledig_administratienummer(admin_number) -> str:
    """
    Return the complete admin number used in gpass

    Pad to 10 chars and add a static "gemeente code"
    """
    stadspas_admin_number = str(admin_number).zfill(10)
    stadspas_admin_number = f'0363{stadspas_admin_number}'
    return stadspas_admin_number
