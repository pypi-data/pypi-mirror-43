import json
import requests
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue

DCMODEL = 'Dcstaticvm'
ARMMODELS = ['Checkpoint', 'CheckpointMgmt', 'Fortigate']
NIC_ROLES = ['FortiBranch', 'WANCPFW']
SB_SERVER_MODEL = 'Skybox-Server'
VSRX_Model = 'VSRx_NS'
AZURE_COMMANDS_SERVICE_ALIAS = 'Azuresupplementcommands'

class virtualMachine():
    def __init__(self):
        self.name = ''
        self.username = ''
        self.password = ''
        self.publicIP = ''
        self.nics = []

class virtualNic():
    def __init__(self):
        self.name = ''
        self.privateIP = ''
        self.mac_address = ''
        self.subnet_CIDR = ''
        self.subnet_name = ''

class subnet():
    def __init__(self):
        self.name = ''
        self.CIDR = ''
        self.short_name = ''
        self.attributes = []

class extracted_sandbox_data():
    def __init__(self):
        self.subnets = []
        self.resources = []
        self.nics = []

class sandbox_extractor():
    def __init__(self, session, res_id, logger=None):
        '''
        :param CloudShellAPISession session: 
        :param res_id: 
        :param logger: 
        '''
        self.session = session
        self.res_id = res_id
        if logger:
            self.logger = logger
        else:
            self.logger = None

    def get_sandbox_data(self):
        sandbox_extraction_data = extracted_sandbox_data()
        reservation_details = self.session.GetReservationDetails(self.res_id).ReservationDescription
        self.subnets = [subnet for subnet in reservation_details.Services if subnet.ServiceName == 'Subnet']
        self.resources = reservation_details.Resources
        # find resources
        for resource in self.resources:
            resource_info_object = self.handle_resource(resource)
            if resource_info_object:
                sandbox_extraction_data.resources.append(resource_info_object)
        # find subnets
        for service in self.subnets:
            subnet_object = self.handle_subnets(service)
            sandbox_extraction_data.subnets.append(subnet_object)
        # find all nics:
        for current_resource in sandbox_extraction_data.resources:
            for nic in current_resource.nics:
                sandbox_extraction_data.nics.append(self.populate_nics(sandbox_extraction_data.subnets, current_resource, nic))

        return sandbox_extraction_data

    def populate_nics(self, subnets, resource, nic):
        '''
        :param virtualMachine resource:
        :param virtualNic nic:
        :return:
        '''
        current_nic = self.find_subnet_name_by_cidr(subnets, resource, nic)
        return current_nic


    def find_subnet_name_by_cidr(self, subnets, resource, nic):
        '''
        :param virtualNic nic:
        :param list(subnet) subnets:
        :return:
        '''
        for current_subnet in subnets:
            if nic.subnet_CIDR == current_subnet.CIDR:
                nic.subnet_name = current_subnet.name.split('-')[:-2][0].strip()
                short_resource_name = resource.name.split('-')[:-1][0].strip()
                nic.name = '{0}_in_{1}'.format(short_resource_name, nic.subnet_name)
                return nic
        return None

    def handle_resource(self, resource):
        '''
        :param resource:
        :return:
        '''
        if resource.VmDetails:
            current_virtual_asset = virtualMachine()
            current_virtual_asset.name = resource.Name
            res_details = self.session.GetResourceDetails(resource.Name)
            username = filter(lambda x: x.Name == 'User' or x.Name == '{}.User'.format(resource.ResourceModelName),
                              res_details.ResourceAttributes)[0].Value
            current_virtual_asset.username = username
            Pass_enc = \
            filter(lambda x: x.Name == 'Password' or x.Name == '{}.Password'.format(resource.ResourceModelName),
                   res_details.ResourceAttributes)[0].Value
            pass_dec = self.session.DecryptPassword(Pass_enc).Value
            current_virtual_asset.password = pass_dec
            resource_details = self.session.GetResourceDetails(resource.Name)
            current_virtual_asset.publicIP = [attr.Value for attr in resource_details.ResourceAttributes if
                                              attr.Name == 'Public IP' or attr.Name == '{}.Public IP'.format(
                                                  resource.ResourceModelName)][0]
            for nic in resource.VmDetails.NetworkData:
                current_nic = virtualNic()
                current_nic.subnet_CIDR = nic.NetworkId.split('_')[1].replace('-', '/')
                for add_data in nic.AdditionalData:
                    if add_data.Name == 'ip':
                        current_nic.privateIP = add_data.Value
                    if add_data.Name == 'mac address':
                        current_nic.mac_address = add_data.Value
                current_virtual_asset.nics.append(current_nic)
            return current_virtual_asset
        else:
            return None

    def handle_subnets(self, service):
        '''
        :param service:
        :return:
        '''
        current_subnet = subnet()
        current_subnet.name = service.Alias
        current_subnet.attributes = service.Attributes
        current_subnet.short_name = service.Alias.split('-')[:-2][0].strip()
        for attr in service.Attributes:
            if attr.Name == 'Allocated CIDR':
                current_subnet.CIDR = attr.Value
        return current_subnet
