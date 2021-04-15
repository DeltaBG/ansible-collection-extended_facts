# Collect facts related to IPMI
#
# This file is part of Ansible Extended Facts
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import re

from ansible.module_utils.facts.collector import BaseFactCollector
from ansible.module_utils.facts.utils import get_file_content, get_file_lines

class IpmiFactCollector(BaseFactCollector):
    name = 'ipmi'
    _fact_ids = set()

    def collect(self, module=None, collected_facts=None):
        facts_dict = {}
        facts = False # This is default

        # Find loaded kernel modules for IPMI Adapter
        if os.path.exists('/proc/modules'):
            for line in get_file_lines('/proc/modules'):

                # If have module ipmi_si or ipmi_ssif return true
                if re.search('^ipmi_si\s+|^ipmi_ssif\s+', line):
                    facts = True

        facts_dict[self.name] = facts
        return facts_dict
