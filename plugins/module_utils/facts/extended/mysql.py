# Collect facts related to MySQL
#
# This file is part of Ansible Extended Facts
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible.module_utils.facts.collector import BaseFactCollector
from ansible.module_utils.facts.utils import get_file_content, get_file_lines

from ansible_collections.mlg1.extended_facts.plugins.module_utils.facts.extended.utils import get_active_services

class MysqlFactCollector(BaseFactCollector):
    name = 'mysql'
    _fact_ids = set()

    def collect(self, module=None, collected_facts=None):
        facts_dict = {}
        mysql_facts = {} # This is default

        # Check if there is MYSQL
        active_services = get_active_services(['mysql', 'mysqld', 'mariadb'], module)
        if active_services:
            mysql_facts['service'] = active_services[0]

            # If have MySQL, check version and other
            mysql_bin = module.get_bin_path('mysql')
            if mysql_bin:
                rc, mysql_output, err = module.run_command([mysql_bin, '--version'])
                mysql_regex = re.compile(r'.*?\s+[V-v]er\s(.*?)\s+[D-d]istrib\s+(.*?)\s+for.*')
                mysql_version = mysql_regex.findall(mysql_output)
                mysql_facts['version'] = {
                    'client' : mysql_version[0][0],
                    'server' : mysql_version[0][1].replace(',', '')
                }

        facts_dict['mysql'] = mysql_facts
        return facts_dict
