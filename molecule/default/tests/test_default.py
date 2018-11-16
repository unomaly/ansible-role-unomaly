import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    dirs = [
        '/DATA',
        '/DATA/docker',
        '/DATA/fluentd',
        '/DATA/grafana',
        '/DATA/metrics',
        '/DATA/migrations',
        '/DATA/mongodb',
        '/DATA/plugins',
        '/DATA/postgresql',
        '/DATA/prometheus',
        '/DATA/tokeraggregated',
        '/DATA/unomaly_actions',
        '/DATA/unomaly_celery',
        '/DATA/unomaly_logs',
        '/DATA/unomaly_transports',
        '/opt/unomaly',
        '/opt/unomaly/conf',
        '/opt/unomaly/bin',
        '/opt/unomaly/fluentd',
        '/opt/unomaly/install',
        '/opt/unomaly/install/logs',
        '/opt/unomaly/license',
        '/opt/unomaly/mayday',
        '/opt/unomaly/mayday/scripts',
        '/opt/unomaly/role',
        '/opt/unomaly/www',
    ]
    for d in dirs:
        dir = host.file(d)
        assert dir.is_directory


def test_unomaly_files_exist(host):
    in_file = host.file('/DATA/unomaly_instance')
    assert in_file.is_file
    version_file = host.file('/opt/unomaly/VERSION')
    assert version_file.contains('2.3')
    assert version_file.is_file


def test_apache(host):
    pkg = host.package("apache2")
    assert pkg.is_installed
    assert pkg.version.startswith("2.4")
    service = host.service('apache2')
    assert service.is_running
    assert service.is_enabled



def test_unomaly_command(host):
    with host.sudo():
        comm = host.command('unomaly')
    assert comm.rc == 0
    output = comm.stdout
    services = [
        'fluentd',
        'grafana',
        'nats',
        'cupid',
        'postgres',
        'celery-beat',
        'celery-deletion',
        'celery',
        'check-standalone',
        'config-wizard',
        'connect',
        'dashboard',
        'horizon',
        'ingestion',
        'licensed',
        'api',
        'forager',
        'tad',
        'pluginjs',
        'sid',
        'systemstated',
        'transportd',
        'unomalyweb',
        'prometheus-core',
        'prometheus-cadvisor',
        'prometheus-mongo',
        'prometheus-node',
        'prometheus-postgres',
        'syslogng',
    ]
    for srv in services:
        assert srv in output

    assert 'inactive'   not in output
    assert 'dead'       not in output
    assert 'activating' not in output
