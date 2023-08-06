# Copyright 2018 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.common import compute
from tempest.common import utils
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from neutron_tempest_plugin.common import ssh
from neutron_tempest_plugin import config
from neutron_tempest_plugin.scenario import base

CONF = config.CONF


class NetworkConnectivityTest(base.BaseTempestTestCase):
    credentials = ['primary', 'admin']

    @classmethod
    @utils.requires_ext(extension="router", service="network")
    def resource_setup(cls):
        super(NetworkConnectivityTest, cls).resource_setup()
        # Create keypair with admin privileges
        cls.keypair = cls.create_keypair()
        # Create security group with admin privileges
        cls.secgroup = cls.create_security_group(
            name=data_utils.rand_name('secgroup'))
        # Execute funcs to achieve ssh and ICMP capabilities
        cls.create_loginable_secgroup_rule(secgroup_id=cls.secgroup['id'])
        cls.create_pingable_secgroup_rule(secgroup_id=cls.secgroup['id'])

    def _create_servers(self, port_1, port_2):
        params = {
            'flavor_ref': CONF.compute.flavor_ref,
            'image_ref': CONF.compute.image_ref,
            'key_name': self.keypair['name']
        }
        vm1 = self.create_server(networks=[{'port': port_1['id']}], **params)

        if (CONF.compute.min_compute_nodes > 1 and
                compute.is_scheduler_filter_enabled("DifferentHostFilter")):
            params['scheduler_hints'] = {
                'different_host': [vm1['server']['id']]}

        self.create_server(networks=[{'port': port_2['id']}], **params)

    @decorators.idempotent_id('8944b90d-1766-4669-bd8a-672b5d106bb7')
    def test_connectivity_through_2_routers(self):
        ap1_net = self.create_network()
        ap2_net = self.create_network()
        wan_net = self.create_network()
        ap1_subnet = self.create_subnet(
            ap1_net, cidr="10.10.210.0/24", gateway="10.10.210.254")
        ap2_subnet = self.create_subnet(
            ap2_net, cidr="10.10.220.0/24", gateway="10.10.220.254")
        self.create_subnet(
            wan_net, cidr="10.10.200.0/24", gateway="10.10.200.254")

        ap1_rt = self.create_router(
            router_name=data_utils.rand_name("ap1_rt"),
            admin_state_up=True,
            external_network_id=CONF.network.public_network_id)
        ap2_rt = self.create_router(
            router_name=data_utils.rand_name("ap2_rt"),
            admin_state_up=True)

        ap1_internal_port = self.create_port(
            ap1_net, security_groups=[self.secgroup['id']])
        ap2_internal_port = self.create_port(
            ap2_net, security_groups=[self.secgroup['id']])
        ap1_wan_port = self.create_port(wan_net)
        ap2_wan_port = self.create_port(wan_net)

        self._create_servers(ap1_internal_port, ap2_internal_port)

        self.client.add_router_interface_with_port_id(
            ap1_rt['id'], ap1_wan_port['id'])
        self.client.add_router_interface_with_port_id(
            ap2_rt['id'], ap2_wan_port['id'])
        self.create_router_interface(ap1_rt['id'], ap1_subnet['id'])
        self.create_router_interface(ap2_rt['id'], ap2_subnet['id'])

        self.client.update_router(
            ap1_rt['id'],
            routes=[{"destination": ap2_subnet['cidr'],
                     "nexthop": ap2_wan_port['fixed_ips'][0]['ip_address']}])
        self.client.update_router(
            ap2_rt['id'],
            routes=[{"destination": ap1_subnet['cidr'],
                     "nexthop": ap1_wan_port['fixed_ips'][0]['ip_address']}])

        ap1_fip = self.create_and_associate_floatingip(
            ap1_internal_port['id'])
        ap1_sshclient = ssh.Client(
            ap1_fip['floating_ip_address'], CONF.validation.image_ssh_user,
            pkey=self.keypair['private_key'])

        self.check_remote_connectivity(
            ap1_sshclient, ap2_internal_port['fixed_ips'][0]['ip_address'])
