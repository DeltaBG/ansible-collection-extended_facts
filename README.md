# Ansible Collection - Extended facts

This is a collection with a module for extended Ansible facts. Currently, the module returns information about RAID controllers and `smartctl --scan-open`.

## Getting Started

This collection contains the following ressources.

| Ressources                                          | Comment                                                   |
| :-------------------------------------------------- | :-------------------------------------------------------- |
| **plugins/modules/extended_facts.py**               | Main script of module.                                    |
| **plugins/module_utils/facts/extended/raid.py**     | Script for checking about RAID.                           |
| **plugins/module_utils/facts/extended/smartctl.py** | Script for checking about block devices using smartctl.   |
| **plugins/module_utils/facts/extended/mysql.py**    | Script for checking about MySQL.                          |

### Prerequisites

The only prerequisite is to have an [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/index.html) >= 2.9

#### Smartmontools
If you want the module to return information from `smartctl`, you need to have a `smartmontools` package installed on each node.

### Installing
From Galaxy:
```sh
ansible-galaxy collection install mlg1.extended_facts
```

From GitHub:
```sh
ansible-galaxy collection install git+https://github.com/mlg1/ansible-collection-extended_facts.git,master
```

To install via the `requirements.yml` file:
```yaml
collections:
  - name: mlg1.extended_facts
    version: 1.0.2
    source: https://galaxy.ansible.com
```
or
```yaml
collections:
  - name: https://github.com/mlg1/ansible-collection-extended_facts.git
    type: git
    version: master
```

## Example usage in playbook

```yaml
---
- name: Get extended facts
  hosts: all
  gather_facts: no
  tasks:

    - name: Install smartmontools to receive data from smartctl
      package:
        name: smartmontools

    - name: Gather extended facts
      mlg1.extended_facts.extended_facts:

    # Print extended facts
    - name: Debug
      debug:
        var: ansible_facts
```
