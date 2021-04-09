# Collect facts related to Icinga2
#
# This file is part of Ansible Extended Facts
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible.module_utils.facts.collector import BaseFactCollector
from ansible.module_utils.facts.utils import get_file_content, get_file_lines

from ansible_collections.deltabg.extended_facts.plugins.module_utils.facts.extended.utils import FindService

class Icinga2FactCollector(BaseFactCollector):
    name = 'icinga2'
    _fact_ids = set()

    # Service vars
    bin_name = name
    service_names = ['icinga2']
    service_ver_regex = r'\(version:\ (.*?)\)'

    def collect(self, module=None, collected_facts=None):
        facts_dict = {}
        facts = [] # This is default

        svc_module = FindService()
        active_services = svc_module.gather_service(self.service_names, module)
        if active_services:
            for service in active_services:
                if service['source'] == 'docker':
                    docker_bin = module.get_bin_path('docker')
                    if docker_bin:
                        service_ver_command = '%s exec -i %s %s --version' % (docker_bin, service['name'], self.bin_name)

                else:
                    service_bin = module.get_bin_path(self.bin_name)
                    if service_bin:
                        service_ver_command = '%s --version' % service_bin

                rc, service_output, err = module.run_command('%s' % service_ver_command, use_unsafe_shell=True)
                if not rc:
                    service_regex = re.compile(self.service_ver_regex, re.MULTILINE)
                    service_version = service_regex.findall(service_output)
                    service['version'] = service_version[0]

                facts.append(service)

        facts_dict[self.name] = facts
        return facts_dict
