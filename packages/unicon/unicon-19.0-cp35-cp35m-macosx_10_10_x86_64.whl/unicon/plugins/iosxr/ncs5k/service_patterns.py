__copyright__ = "# Copyright (c) 2018 by cisco Systems, Inc. All rights reserved."
__author__ = "dwapstra"

from unicon.plugins.generic.service_patterns import ReloadPatterns

class Ncs5kReloadPatterns(ReloadPatterns):
    def __init__(self):
        super().__init__()
        self.system_config_completed = r"^(.*?)SYSTEM CONFIGURATION COMPLETED"
        self.reloading_node = r"^(.*?)Reloading node .*"
