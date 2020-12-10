# Collect facts related to selinux
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import re

from ansible.module_utils.facts.collector import BaseFactCollector
from ansible.module_utils.facts.utils import get_file_content, get_file_lines

class SmartctlFactCollector(BaseFactCollector):
    name = 'smartctl'
    _fact_ids = set()

    def collect(self, module=None, collected_facts=None):
        facts_dict = {}
        smartctl_facts = {} # This is default

        smartctl_bin = module.get_bin_path('smartctl')
        if smartctl_bin:
            rc, smartctl_output, err = module.run_command([smartctl_bin, '--scan-open'])
            #smartctl_facts['raw_output'] = smartctl_output # Uncomment for debug
            smartctl_facts['devices'] = []
            #smartctl_regex = re.compile(r'\n(/.*?)\s+-d\s+(.*?)\s+#\s+(.*)')
            smartctl_regex = re.compile(r'\n(/.*?)\s+-d\s+(.*?)\s+#\s+(.*?\[(.*?)\].*)')
            for device in smartctl_regex.findall(smartctl_output):
                smartctl_facts['devices'].append({
                    'device'         : device[0],
                    'type'           : device[1],
                    'comment'        : device[2],
                    'name'           : device[3],
                    'check_smart.pl' : 'check_smart.pl -d {} -i {}'.format(device[0], device[1])
                })
            # If have no devices
            if not smartctl_facts['devices']:
                smartctl_facts = {}

        facts_dict['smartctl'] = smartctl_facts
        return facts_dict
