# Ansible Collection - Extended facts

This is a collection with a module for extended Ansible facts. Currently, the module returns information about RAID controllers and `smartctl --scan-open`.

## Getting Started

This collection contains the following ressources.

| Ressources                                          | Comment                                                   |
| :-------------------------------------------------- | :-------------------------------------------------------: |
| **plugins/modules/extended_facts.py**               | Main script of module.                                    |
| **plugins/module_utils/facts/extended/raid.py**     | Script for checking about RAID.                           |
| **plugins/module_utils/facts/extended/smartctl.py** | Script for checking about block devices using smartctl.   |                                                            |

### Prerequisites

The only prerequisite is to have an [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/index.html) >= 2.9

### Installing

```sh
ansible-galaxy collection install git+https://github.com/mlg1/ansible-collection-extended_facts.git,master
```

To install via the requirements.yml file:
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

    - name: Gathering extended facts
      extended_facts:

    # Print extended facts
    - name: Debug
      debug:
        var: ansible_facts
```
