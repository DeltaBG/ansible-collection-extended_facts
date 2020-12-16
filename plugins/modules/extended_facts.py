#!/usr/bin/python
#
# MIT License
#
# Copyright (c) 2020 Nedelin Petkov <mlg@abv.bg>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: mlg1.extended_facts.extended_facts
short_description: Module for extended Ansible facts
version_added: "1.0.2"
description:
  - Collecting information about the system in favor
author:
  - Nedelin Petkov (https://github.com/mlg1/)
'''

EXAMPLES = r'''
- name: Gathering extended facts
  mlg1.extended_facts.extended_facts:

# These are examples of possible return values.
ansible_facts:
  raid:
    megaraid:
      cli: 'perccli'
      host: 'scsi0'
      model: 'PERC H740P Mini'
      rev: '5.05'
      type: 'Direct-Access'
      vendor: 'DELL'
  smartctl:
    devices:
    - check_smart.pl: 'check_smart.pl -d /dev/bus/0 -i sat+megaraid,0'
      comment: '/dev/bus/0 [megaraid_disk_00] [SAT], ATA device'
      device: '/dev/bus/0'
      name: 'megaraid_disk_00'
      type: 'sat+megaraid,0'
    - check_smart.pl: 'check_smart.pl -d /dev/bus/0 -i sat+megaraid,1'
      comment: '/dev/bus/0 [megaraid_disk_01] [SAT], ATA device'
      device: '/dev/bus/0'
      name: 'megaraid_disk_01'
      type: 'sat+megaraid,1'
  mysql:
    service:
      description: 'MariaDB 10.3.14 database server'
      name: 'mariadb.service'
      service: 'mariadb'
      source: 'systemd'
      status: 'running'
    version:
      client: '15.1'
      server: '10.3.14-MariaDB'
'''

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.facts.namespace import PrefixFactNamespace
from ansible.module_utils.facts import ansible_collector

from ansible_collections.mlg1.extended_facts.plugins.module_utils.facts.extended.raid import RaidFactCollector
from ansible_collections.mlg1.extended_facts.plugins.module_utils.facts.extended.smartctl import SmartctlFactCollector
from ansible_collections.mlg1.extended_facts.plugins.module_utils.facts.extended.mysql import MysqlFactCollector

def main():
    module = AnsibleModule(
        argument_spec=dict(
            gather_subset=dict(default=["all"], required=False, type='list'),
            gather_timeout=dict(default=10, required=False, type='int'),
            filter=dict(default="*", required=False),
            fact_path=dict(default='/etc/ansible/facts.d', required=False, type='path'),
        ),
        supports_check_mode=True,
    )

    gather_subset = module.params['gather_subset']
    gather_timeout = module.params['gather_timeout']
    filter_spec = module.params['filter']
    minimal_gather_subset = frozenset(['raid','smartctl', 'mysql'])

    all_collector_classes = [
        RaidFactCollector,
        SmartctlFactCollector,
        MysqlFactCollector
    ]

    # rename namespace_name to root_key?
    namespace = PrefixFactNamespace(namespace_name='ansible',
                                    prefix='ansible_')

    fact_collector = \
        ansible_collector.get_ansible_collector(all_collector_classes=all_collector_classes,
                                                namespace=namespace,
                                                filter_spec=filter_spec,
                                                gather_subset=gather_subset,
                                                gather_timeout=gather_timeout,
                                                minimal_gather_subset=minimal_gather_subset)

    facts_dict = fact_collector.collect(module=module)

    module.exit_json(ansible_facts=facts_dict)


if __name__ == '__main__':
    main()
