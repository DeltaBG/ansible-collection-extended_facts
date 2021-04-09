# This file is part of Ansible Extended Facts
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

# class ServiceFindService():

#     def gather_services(self):
#         services = {}
#         service_path = self.module.get_bin_path("service")
#         if service_path is None:
#             return None
#         initctl_path = self.module.get_bin_path("initctl")
#         chkconfig_path = self.module.get_bin_path("chkconfig")


class FindService():

    def gather_service(self, find=[], module=None):
        services = []

        service_bin = module.get_bin_path('service')
        systemctl_bin = module.get_bin_path('systemctl')
        docker_bin = module.get_bin_path('docker')

        if systemctl_bin:
            systemctl_command = [systemctl_bin, 'list-units', '--no-pager', '--type', 'service']
            for service_name in find:
                systemctl_command.append(service_name + '.service')
            rc, systemctl_output, err = module.run_command(systemctl_command)
            systemctl_regex = re.compile(r'^\s+((.*?).service)\s+(.*?)\s+(.*?)\s+(.*?)\s+(.+)$', re.MULTILINE)
            for service in systemctl_regex.findall(systemctl_output):
                services.append({
                    'name'        : service[1],
                    'state'       : service[4].strip(),
                    'source'      : 'systemd'
                })

        if service_bin and systemctl_bin is None:
            for service_name in find:
                rc, service_output, err = module.run_command('%s %s status' % (service_bin, service_name), use_unsafe_shell=True)
                if rc != 1:
                    service_regex = re.compile(r'^(.*?)[: ].*(is not running|is running|is stopped)')
                    service = service_regex.findall(service_output)
                    services.append({
                        'name'   : service[0][0],
                        'state'  : 'stopped' if service[0][1] == 'is not running' or service[0][1] == 'is stopped' else 'running',
                        'source' : 'init'
                    })

        if docker_bin:
            service_name = "|".join(map(str, find))
            rc, docker_output, err = module.run_command('%s ps -a --format "{{.ID}}:::{{.Names}}:::{{.Status}}:::{{.Image}}" | grep -iE "%s"' % (docker_bin, service_name), use_unsafe_shell=True)
            if rc != 1:
                docker_regex = re.compile(r'^(.*):::(.*):::(Up|Exited).*:::(.*)$', re.MULTILINE)
                for service in docker_regex.findall(docker_output):
                    services.append({
                        'docker_id'    : service[0],
                        'name'         : service[1],
                        'state'        : 'stopped' if service[2] == 'Exited' else 'running',
                        'docker_image' : service[3],
                        'source'       : 'docker'
                    })

        return services
