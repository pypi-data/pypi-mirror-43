import json
import requests
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue

DCMODEL = 'Dcstaticvm'
ARMMODELS = ['Checkpoint', 'CheckpointMgmt', 'Fortigate']
NIC_ROLES = ['FortiBranch', 'WANCPFW']
SB_SERVER_MODEL = 'Skybox-Server'
VSRX_Model = 'VSRx_NS'
AZURE_COMMANDS_SERVICE_ALIAS = 'Azuresupplementcommands'

class parse_commands():
    def __init__(self, session, res_id, logger=None):
        self.session = session
        self.res_id = res_id
        if logger:
            self.logger = logger
        else:
            self.logger = None

    def get_definitions(self, file_name, file_type):
        GITHUB_URL = r'https://raw.githubusercontent.com/QualiSystemsLab/SkyboxDataFiles/master/DevicePolicy/{0}.{1}'.format(
            file_name, file_type
        )
        github_raw = requests.get(GITHUB_URL).content
        if file_type == 'json':
            policy_object = json.loads(github_raw)
        else:
            policy_object = github_raw
        return policy_object

    def replace_placeholders(self, file_name, file_type, reservation_description):
        services = reservation_description.Services
        subnets = [service for service in services if service.ServiceName == 'Subnet']
        commands = self.get_definitions(file_name, file_type).split('\n')
        parsed_commands = []
        for command in commands:
            if ('<<__SN__') in command:
                # reference to subnet as cidr
                command = self._parse_subnet_to_cidr(command = command, subnets=subnets)

            if ('<<__NA__') in command:
                # reference to subnet as NA
                command = self._parse_subnet_to_cidr_NA(command=command, subnets=subnets)

            if ('<<__NX1__') in command:
                # reference to subnet as NX
                command = self._parse_subnet_to_cidr_NX(command=command, subnets=subnets)

            if ('<<__D__') in command:
                # reference to device with subnet
                command = self._parse_device_with_subnet(command=command,
                                                          reservation_description=reservation_description,
                                                          subnets=subnets)
            if ('<<__DS__') in command:
                # reference to device without subnet
                command = self._parse_device_short(command = command, reservation_description=reservation_description)

            parsed_commands.append(command)

        return parsed_commands

    def replace_placeholders_additional_nics(self, file_name, file_type, reservation_description):
        services = reservation_description.Services
        subnets = [service for service in services if service.ServiceName == 'Subnet']
        commands = self.get_definitions(file_name, file_type).split('\n')
        parsed_commands = []
        for command in commands:
            if ('<<__SN__') in command:
                # reference to subnet
                command = self._parse_subnet_to_alias(command=command, subnets=subnets)

            if ('<<__DS__') in command:
                # reference to device without subnet
                command = self._parse_device_short(command = command, reservation_description=reservation_description)

            parsed_commands.append(command)

        return parsed_commands

    def replace_place_holders_devices_name(self, file_name, file_type, reservation_description):
        services = reservation_description.Services
        subnets = [service for service in services if service.ServiceName == 'Subnet']
        commands = self.get_definitions(file_name, file_type).split('\n')
        parsed_commands = []
        for command in commands:
            if ('<<__DS__') in command:
                # reference to device without subnet
                command = self._parse_device_short(command = command, reservation_description=reservation_description)

            parsed_commands.append(command)

        return parsed_commands

    def _parse_device_with_subnet (self, command, reservation_description, subnets):
        device_reference = command.split('<<__D__')[1].split('__D__>>')[0]
        current_device_name = device_reference.split('__SN__')[0]
        current_device_subnet_name = device_reference.split('__SN__')[1]

        selected_subnet = self._get_subnet(current_device_subnet_name, subnets)
        subnet_name = '' if selected_subnet is None else selected_subnet.Alias

        device_full_name = self._find_gateway_entity(current_device_name, reservation_description)

        if device_full_name is not None:
            self.logger.info(
                'Located device full name {0} in command {1}'.format(device_full_name, command))
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_device_name, command))

        nic_ip = self._get_nic_connected_to_subnet(
            session=self.session,
            entity_name=device_full_name,
            subnet_name=subnet_name,
            reservation_description=reservation_description,
            subnets=subnets,
            res_id=self.res_id
        )
        device_name_with_placeholders = '<<__D__{0}__SN__{1}__D__>>'.format(current_device_name,
                                                                            current_device_subnet_name)
        command = command.replace(device_name_with_placeholders, nic_ip)

        return command

    def _parse_device_short (self, command, reservation_description):
        current_device_name = command.split('<<__DS__')[1].split('__DS__>>')[0]

        device_full_name = self._find_gateway_entity(current_device_name, reservation_description)

        self.logger.info('B3 Device full Name  is {0}'.format(device_full_name))
        if device_full_name is not None:
            self.logger.info(
                'Located device full name {0} in command {1}'.format(device_full_name, command))
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_device_name, command))

        device_name_with_placeholders = '<<__DS__{0}__DS__>>'.format(current_device_name)
        command = command.replace(device_name_with_placeholders, device_full_name)
        return command

    def _parse_subnet_to_alias(self, command, subnets):
        current_subnet_name = command.split('<<__SN__')[1].split('__SN__>>')[0]

        # current_subnet = [x for x in subnets if x.Alias.startswith(current_subnet_name)][0]
        current_subnet = self._get_subnet(current_subnet_name, subnets)

        if current_subnet is not None:
            self.logger.info('Located subnet full name {0} in command {1}'.format(current_subnet.Alias, command))
            subnet_name_with_placeholders = '<<__SN__{}__SN__>>'.format(current_subnet_name)
            command = command.replace(subnet_name_with_placeholders, current_subnet.Alias)
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_subnet_name, command))

        return command

    def _parse_subnet_to_cidr(self, command, subnets):
        current_subnet_name = command.split('<<__SN__')[1].split('__SN__>>')[0]

        # current_subnet = [x for x in subnets if x.Alias.startswith(current_subnet_name)][0]
        current_subnet = self._get_subnet(current_subnet_name, subnets)

        if current_subnet is not None:
            self.logger.info('Located subnet full name {0} in command {1}'.format(current_subnet.Alias, command))
            current_subnet_cidr = filter(lambda x: x.Name == 'Allocated CIDR', current_subnet.Attributes)[0].Value
            subnet_name_with_placeholders = '<<__SN__{}__SN__>>'.format(current_subnet_name)
            command = command.replace(subnet_name_with_placeholders, current_subnet_cidr)
        else:
            self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_subnet_name, command))

        return command

    def _parse_subnet_to_cidr_NA(self, command, subnets):
        current_subnet_name = command.split('<<__NA__')[1].split('__NA__>>')[0]

        if current_subnet_name == 'SandboxWide':
            sandbox_wide_subnet_cidr_raw = filter(lambda x: x.Name == 'Allocated CIDR',
                                                  subnets[0].Attributes)[0].Value
            current_subnet_cidr = '.'.join(sandbox_wide_subnet_cidr_raw.split('.')[:-1]) + '.0'
        else:
            current_subnet = self._get_subnet(current_subnet_name, subnets)
            if current_subnet is not None:
                current_subnet_cidr = filter(lambda x: x.Name == 'Allocated CIDR',
                                             current_subnet.Attributes)[0].Value.split('/')[0]
            else:
                self.logger.info('Failed to locate subnet {0} in command {1}'.format(current_subnet_name, command))

        subnet_name_with_placeholders = '<<__NA__{}__NA__>>'.format(current_subnet_name)
        self.logger.info(
            'replacing placeholder {0} with {1}'.format(subnet_name_with_placeholders, current_subnet_cidr))
        command = command.replace(subnet_name_with_placeholders, current_subnet_cidr)

        return command

    def _parse_subnet_to_cidr_NX(self, command, subnets):
        current_subnet_name = command.split('<<__NX1__')[1].split('__NX1__>>')[0]

        # current_subnet = [x for x in subnets if x.Alias.startswith(current_subnet_name)][0]
        current_subnet = self._get_subnet(current_subnet_name, subnets)

        if current_subnet is not None:
            self.logger.info(
                'Located subnet full name {0} in command {1}'.format(current_subnet.Alias, command))
            current_subnet_cidr_raw = \
            filter(lambda x: x.Name == 'Allocated CIDR', current_subnet.Attributes)[0].Value.split('/')[0]
            octat = str(int(current_subnet_cidr_raw.split('.')[-1]) + 1)
            current_subnet_cidr = '.'.join(current_subnet_cidr_raw.split('.')[:-1]) + '.' + octat
            subnet_name_with_placeholders = '<<__NX1__{}__NX1__>>'.format(current_subnet_name)
            self.logger.info(
                'replacing placeholder {0} with {1}'.format(subnet_name_with_placeholders, current_subnet_cidr))
            command = command.replace(subnet_name_with_placeholders, current_subnet_cidr)
        else:
            self.logger.info('failed to locate subnet {0} in command {1}'.format(current_subnet_name, command))

        return command

    def _get_subnet(self, subnet_partial_name, subnets):
        found_subnet = None

        for subnet_candidate in subnets:
            formatted_alias = '{}'.format('-'.join(subnet_candidate.Alias.split('-')[:-2]).strip())
            if formatted_alias == subnet_partial_name:
                found_subnet = subnet_candidate
        
        return found_subnet

    def _get_nic_connected_to_subnet(self, session, entity_name, subnet_name, reservation_description, subnets, res_id):
        connections = reservation_description.Connectors
        resources = reservation_description.Resources
        services = reservation_description.Services
        # subnets = [service for service in services if service.ServiceName == 'Subnet']
        subnet_connections = [c for c in connections if c.Source == subnet_name or c.Target == subnet_name]
        subnet_object = [sub for sub in subnets if sub.Alias == subnet_name][0]
        subnet_id = [attr.Value for attr in subnet_object.Attributes if attr.Name == 'Subnet Id'][0]
        requested_ip = None
        try:
            resource_details = session.GetResourceDetails(entity_name)
            subnet_net_id_adddata = [x for x in resource_details.VmDetails.NetworkData if x.NetworkId == subnet_id][0]
            requested_ip = [x.Value for x in subnet_net_id_adddata.AdditionalData if x.Name == 'ip'][0]
            pass
        except:
            # this is a service then
            try:
                service_nics_data_raw = session.ExecuteCommand(
                reservationId=res_id,
                targetType='Service',
                targetName=AZURE_COMMANDS_SERVICE_ALIAS,
                commandName='print_vm_nic_information',
                commandInputs=[InputNameValue(
                    Name='alias',
                    Value=entity_name
                )],
                printOutput=False
                ).Output
                service_nics_data = json.loads(service_nics_data_raw)
            except:
                pass
            try:
                requested_ip = [x['Private IP'] for x in service_nics_data if x['Subnet Name'] == subnet_id][0]
            except:
                requested_ip = 'Not Found'
        return requested_ip

    def _find_gateway_entity(self, gateway_name, reservation_description):
        '''
        :param CloudShellAPISession session:
        '''
        resources = reservation_description.Resources
        services = reservation_description.Services
        resources_from_apps = [res for res in resources if res.AppDetails]
        gateway = [x.Name for x in resources_from_apps if x.AppDetails.AppName.lower() == gateway_name.lower()]
        if gateway.__len__() > 0:
            return gateway[0]
        else:
            gateway = [x.Alias for x in services if x.Alias.lower() == gateway_name.lower()]
            if gateway.__len__() > 0:
                return gateway[0]
            else:
                gateway = None
                return gateway

