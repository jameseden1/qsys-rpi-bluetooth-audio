import json
import os
import subprocess

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DAEMON_CONF_PATH = os.path.join(BASE_PATH, 'daemon.conf')
STATUS_PATH = os.path.join(BASE_PATH, 'status.json')
INSTALL_PACKAGES_PATH = os.path.join(BASE_PATH, 'install_packages.sh')
SET_HOSTNAME_PATH = os.path.join(BASE_PATH, 'set_hostname.sh')

# First, check the script is running with the right permissions
if os.geteuid() != 0:
    raise Exception('You must use sudo to do this')

# Get the ID
print('Please choose an ID for this Bluetooth Receiver: ')
device_id = input()
device_id = int(device_id)
if device_id <= 0 or device_id > 255:
    raise Exception('Out of range')

# Get the Bluetooth name (pretty hostname)
print('Please enter the Bluetooth name: ')
pretty_hostname = input()
pretty_hostname = pretty_hostname.strip()
pretty_hostname = pretty_hostname.replace(' ', '')
if len(pretty_hostname) == 0:
    raise Exception('Hostname is invalid') 

mcast_base = '239.69.0.{}'.format(device_id)
hostname = 'AV-Bluetooth{}'.format(device_id)

if os.path.exists(DAEMON_CONF_PATH):
    print('Deleting {}'.format(DAEMON_CONF_PATH))
    os.remove(DAEMON_CONF_PATH)

print('Creating {}'.format(DAEMON_CONF_PATH))
daemon_conf = {
    'http_port': 8080,
    'rtsp_port': 8854,
    'http_base_dir': os.path.join(BASE_PATH, 'aes67-linux-daemon', 'webui', 'build'),
    'log_severity': 3,
    'playout_delay': 0,
    'tic_frame_size_at_1fs': 48,
    'max_tic_frame_size': 1024,
    'sample_rate': 48000,
    'rtp_mcast_base': mcast_base,
    'rtp_port': 5004,
    'ptp_domain': 0,
    'ptp_dscp': 48,
    'sap_mcast_addr': '239.255.255.255',
    'sap_interval': 30,
    'syslog_proto': 'none',
    'syslog_server': '255.255.255.254:1234',
    'status_file': STATUS_PATH,
    'interface_name': 'eth0',
    'mdns_enabled': False,
    'node_id': hostname,
}

with open(DAEMON_CONF_PATH, 'w', encoding='utf-8') as f:
    json.dump(daemon_conf, f, indent=4)

if os.path.exists(STATUS_PATH):
    print('Deleting {}'.format(STATUS_PATH))
    os.remove(STATUS_PATH)

print('Creating {}'.format(STATUS_PATH))
status_conf = {
    'sources': [
        {
            'id': 0,
            'enabled': True,
            'name': hostname,
            'io': 'Audio Device',
            'max_samples_per_packet': 48,
            'codec': 'L24',
            'ttl': 15,
            'payload_type': 98,
            'dscp': 34,
            'refclk_ptp_traceable': False,
            'map': [ 0, 1 ],
        },
    ],
  'sinks': [],
}

with open(STATUS_PATH, 'w', encoding='utf-8') as f:
    json.dump(status_conf, f, indent=4)

print('Installing packages. This could take a while...')
subprocess.run(['sudo', 'bash', INSTALL_PACKAGES_PATH])

print('Setting hostname')
subprocess.run(['sudo', 'bash', SET_HOSTNAME_PATH, hostname, pretty_hostname])

print('Reboot now (Y?)')
yes = input()
if yes == 'Y':
    subprocess.run(['sudo', 'reboot'])
else:
    print('Reboot aborted')
