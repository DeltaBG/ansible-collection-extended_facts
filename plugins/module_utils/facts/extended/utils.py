# This file is part of Ansible Extended Facts
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

def get_active_services(find=[], module=None):
    services = []
    systemctl_bin = module.get_bin_path('systemctl')

    if systemctl_bin:
        systemctl_command = [systemctl_bin, 'list-units', '--no-pager', '--type', 'service']
        for service in find:
            systemctl_command.append(service + '.service')
        rc, systemctl_output, err = module.run_command(systemctl_command)
        systemctl_regex = re.compile(r'^((.*?).service)\s+(.*?)\s+(.*?)\s+(.*?)\s+(.+)', re.MULTILINE)
        for service in systemctl_regex.findall(systemctl_output):
            services.append({
                'name'        : service[0],
                'service'     : service[1],
                # 'load'        : service[2],
                # 'active'      : service[3],
                'status'      : service[4],
                'description' : service[5].strip(),
                'source'      : 'systemd'
            })

    return services
