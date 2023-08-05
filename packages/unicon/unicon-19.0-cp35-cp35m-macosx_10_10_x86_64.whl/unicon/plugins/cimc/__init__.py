__copyright__ = "# Copyright (c) 2017 by cisco Systems, Inc. All rights reserved."
__author__ = "Dave Wapstra <dwapstra@cisco.com>"

from unicon.plugins.generic import GenericSingleRpConnection, ServiceList, service_implementation as svc
from unicon.plugins.generic.connection_provider import GenericSingleRpConnectionProvider

from .statemachine import CimcStateMachine
from .settings import CimcSettings


class CimcConnectionProvider(GenericSingleRpConnectionProvider):
    """
        Connection provider class for cimc connections.
    """
    def init_handle(self):
        con = self.connection
        con._is_connected = True
        self.execute_init_commands()


class CimcServiceList(ServiceList):
    """ cimc services. """

    def __init__(self):
        self.send = svc.Send
        self.sendline = svc.Sendline
        self.expect = svc.Expect
        self.expect_log = svc.ExpectLogging
        self.log_user = svc.LogUser
        self.execute = svc.Execute


class CimcConnection(GenericSingleRpConnection):
    """
        Connection class for cimc connections.
    """
    os = 'cimc'
    series = None
    chassis_type = 'single_rp'
    state_machine_class = CimcStateMachine
    connection_provider_class = CimcConnectionProvider
    subcommand_list = CimcServiceList
    settings = CimcSettings()
