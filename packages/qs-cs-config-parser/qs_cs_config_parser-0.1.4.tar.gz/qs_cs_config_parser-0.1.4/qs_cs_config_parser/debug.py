from parse_config import parse_commands
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as sh
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
res_id = 'f6dea0aa-4fb8-424e-b69d-8e5e2f14358b'

attach_to_cloudshell_as(
    user='yoav.e',
    password='1234',
    domain='Global',
    reservation_id=res_id,
    server_address='40.91.201.107'
)
session = sh.get_api_session()

command_parser = parse_commands(session=session, res_id=res_id)

command = 'blah blah <<__DX__wancpfw__SN__Internet_Transit__PV__2__DX__>> and something else'
reservation_description = session.GetReservationDetails(res_id).ReservationDescription
result_ip = command_parser._parse_device_with_addl_ips(command=command, reservation_description=reservation_description)
pass