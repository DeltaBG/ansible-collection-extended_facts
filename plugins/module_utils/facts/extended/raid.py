# Collect facts related to RAID
#
# This file is part of Ansible Extended Facts
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import re

from ansible.module_utils.facts.collector import BaseFactCollector
from ansible.module_utils.facts.utils import get_file_content, get_file_lines

class RaidFactCollector(BaseFactCollector):
    name = 'raid'
    _fact_ids = set()

    def collect(self, module=None, collected_facts=None):
        facts_dict = {}
        raid_facts = {} # This is default

        # Find loaded kernel modules for RAID controllers
        if os.path.exists('/proc/modules'):
            for line in get_file_lines('/proc/modules'):

                # If have LSI Megaraid / DELL PERC
                if re.search('^megaraid_sas\s+', line):
                    raid_facts['megaraid'] = {}

                    if os.path.exists('/proc/scsi/scsi'):
                        scsi_content = get_file_content('/proc/scsi/scsi')
                        scsi_regex = re.compile(r'Host:\s+(.*?)\s+.*\n\s+[V-v]endor:\s+(.*?)\s+[M-m]odel:\s+(.*?)\s+[R-r]ev:\s+(.*?)\n\s+[T-t]ype:\s+(.*?)\s+.*')
                        for controller in scsi_regex.findall(scsi_content):
                            raid_facts['megaraid'] = {
                                'host'   : controller[0],
                                'vendor' : controller[1],
                                'model'  : controller[2],
                                'rev'    : controller[3],
                                'type'   : controller[4]
                            }
                            # Else another method
                            # raid_facts['megaraid'][controller[0]] = {
                            #     'vendor' : controller[1],
                            #     'model'  : controller[2],
                            #     'rev'    : controller[3],
                            #     'type'   : controller[4]
                            # }
                            if re.search('[D-d][E-e][L-l][L-l]', raid_facts['megaraid']['vendor']):
                                raid_facts['megaraid']['cli'] = 'perccli'
                            else:
                                raid_facts['megaraid']['cli'] = 'megacli'

                # If have 3ware
                elif re.search('^3w-xxxx\s+', line):
                    # TODO: This part of the module is to be developed. Must return the following information:
                    raid_facts['3ware'] = {
                        'cli'    : 'tw_cli',
                        'host'   : 'example',
                        'model'  : 'example',
                        'rev'    : 'example',
                        'type'   : 'example',
                        'vendor' : '3ware'
                    }

                # If have mdadm
                elif re.search('^md\s+|^raid0\s+|^raid1\s+|^raid5\s+|^raid6\s+|^raid10\s+', line):
                    mdadm_bin = module.get_bin_path('mdadm')
                    if mdadm_bin:
                        rc, mdadm_output, mdadm_error = module.run_command([mdadm_bin, '-V'])
                        mdadm_regex = re.compile(r'mdadm\s+-\s+v(.*?)\s+-\s+(.*)')
                        mdadm_version = mdadm_regex.findall(mdadm_error)
                        raid_facts['mdadm'] = {
                            'cli'     : 'mdadm',
                            'model'   : 'mdadm',
                            'version' : '{} {}'.format(mdadm_version[0][0], mdadm_version[0][1]),
                            'type'    : 'software',
                            'vendor'  : 'Linux'
                        }
                    else:
                        # If mdadm binary is missing
                        raid_facts['mdadm'] = {
                            'cli'     : 'unknown',
                            'model'   : 'unknown',
                            'version' : 'unknown',
                            'type'    : 'software',
                            'vendor'  : 'Linux'
                        }

        facts_dict['raid'] = raid_facts
        return facts_dict
