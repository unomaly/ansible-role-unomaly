Unomaly Ansible Role
=========

Ansible role for installing and configuring [Unomaly](https://unomaly.com/).

Requirements
------------

Debian 8 (jessie).

Role Variables
--------------

```yaml
unomaly_version: 2.30.4
unomaly_license_string: ABCDEF
```

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- hosts: unomaly-instances
  roles:
    - { role: ansible-role-unomaly, unomaly_version: 2.30.4 }
```

License
-------

MIT
