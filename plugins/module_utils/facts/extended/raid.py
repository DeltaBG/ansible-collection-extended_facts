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
                if re.search('megaraid_sas\s+', line):
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
                elif re.search('3w-xxxx\s+', line):
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
                elif re.search('md\s+|raid0\s+|raid1\s+|raid5\s+|raid6\s+|raid10\s+', line):
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



        # # LSI Megaraid / DELL PERC
        # if os.path.exists('/proc/scsi/scsi'):
        #     raid_facts = {}

        #     raid_facts['megaraid_sas']['model'] = 'unknown'
        #     for line in get_file_lines('/proc/scsi/scsi'):
        #         raid_facts['megaraid_sas'] = {}

        #         if raid_facts['megaraid_sas']['model'] == 'unknown':
        #             model = re.match(r'Model:\s?(.*)\s\s', line)
        #             if model:
        #                 raid_facts['megaraid_sas']['model'] = model
        #             else:
        #                 raid_facts['megaraid_sas']['model'] = 'unknown'


        #             # if re.match(r'^VxID:\s+0', line):
        #             #     virtual_facts['virtualization_role'] = 'host'
        #             # else:
        #             #     virtual_facts['virtualization_role'] = 'guest'
        #             # return virtual_facts


        facts_dict['raid'] = raid_facts
        return facts_dict
