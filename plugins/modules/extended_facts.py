#!/usr/bin/python

# Copyright: (c) 2020, Nedelin Petkov <mlg@abv.bg>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: extended_facts

short_description: Module for extended Ansible facts.

version_added: "1.0.0"

description: Collecting information about the system in favor.

author:
    - Nedelin Petkov (https://github.com/mlg1/)
'''

EXAMPLES = r'''
- name: Gathering extended facts
  extended_facts:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
'''

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.facts.namespace import PrefixFactNamespace
from ansible.module_utils.facts import ansible_collector

from ansible_collections.mlg1.extended_facts.plugins.module_utils.facts.extended.raid import RaidFactCollector
from ansible_collections.mlg1.extended_facts.plugins.module_utils.facts.extended.smartctl import SmartctlFactCollector

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
    minimal_gather_subset = frozenset(['raid','smartctl'])

    all_collector_classes = [
        RaidFactCollector,
        SmartctlFactCollector
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
