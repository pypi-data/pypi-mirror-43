from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as sh
import cloudshell.api.cloudshell_api as api
from sandbox_extractor import sandbox_extractor

res_id = '9d6fd7bc-4989-43e3-b394-f12283d5e93d'

attach_to_cloudshell_as(
    user='yoav.e',
    password='1234',
    domain='Global',
    reservation_id=res_id,
    server_address='40.91.201.107'
)
session = sh.get_api_session()
sb_ext = sandbox_extractor(session, res_id)
extracted_data = sb_ext.get_sandbox_data()
pass

