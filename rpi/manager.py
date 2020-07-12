#!/usr/bin/python3

import logging
import re
import os
import socket
import struct
import subprocess
import sys
import time

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

# Log to a file
logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(BASE_PATH, 'logfile'),
     filemode="a+",
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)

# Also log to stdout
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
sys_status = ''
enabled = False

# Say hello
logging.info('Hello World! Stream-manager is now running')

def get_connected_macs():
    cmd = [b'hcitool', b'con']
    out = subprocess.check_output(cmd)
    split = out.split(b'\n')

    found = []

    for line in split:
        p = re.compile(b'(?:[0-9a-fA-F]:?){12}')
        macs = re.findall(p, line)
        found.extend(macs)

    return found

def get_name(mac):
    cmd = [b'hcitool', b'name', mac]
    out = subprocess.check_output(cmd)
    split = out.split(b'\n')

    for line in split:
        return line.decode('utf-8')

    return ''

def get_status():
    global sys_status
    global enabled

    if sys_status:
        return sys_status

    if not enabled:
        return 'System Disabled'

    status = 'Not Connected'
    cons = get_connected_macs()
    for con in cons:
        # just return the first
        name = get_name(con)
        status = 'Connected to: {}'.format(name)

    return status

def disconnect():
    cons = get_connected_macs()
    for con in cons:
        cmd = [b'hcitool', b'dc', con]
        subprocess.check_output(cmd)

def reboot():
    logging.info('Reboot')
    try:
        subprocess.check_output(['reboot'])
    except Exception as e:
        print(e)

def stop_all(force=False):
    global sys_status
    global enabled

    if not enabled and force == False:
        return

    enabled = False

    sys_status = 'Disabling All Services'
    subprocess.check_output(['systemctl', 'stop', 'bluetooth'])
    subprocess.check_output(['systemctl', 'stop', 'a2dp-agent'])
    subprocess.check_output(['systemctl', 'stop', 'bluealsa-aplay'])
    subprocess.check_output(['systemctl', 'stop', 'aes67'])
    subprocess.check_output(['systemctl', 'stop', 'alsaloop'])
    sys_status = ''

def start_all():
    global sys_status
    global enabled

    if enabled:
        return

    sys_status = 'Starting aes67 Service'
    subprocess.check_output(['systemctl', 'start', 'aes67'])
    time.sleep(2)

    sys_status = 'Starting alsaloop Service'
    subprocess.check_output(['systemctl', 'start', 'alsaloop'])
    time.sleep(2)

    sys_status = 'Starting Bluetooth Service'
    subprocess.check_output(['systemctl', 'start', 'bluetooth'])
    time.sleep(1)

    sys_status = 'Starting a2dp-agent Service'
    subprocess.check_output(['systemctl', 'start', 'a2dp-agent'])
    time.sleep(1)

    sys_status = 'Starting bluealsa-aplay Service'
    subprocess.check_output(['systemctl', 'start', 'bluealsa-aplay'])
    time.sleep(1)

    sys_status = ''

    enabled = True

def restart():
    global sys_status

    logging.info('Restart services')
    try:
        stop_all(force=True)
        time.sleep(1)
        start_all()

        sys_status = ''
    except Exception as e:
        sys_status = 'Error restarting'
        print(e)

def run():
    logging.info('Starting Manager')
    global enabled

    # Start all services
    subprocess.check_output(['systemctl', 'daemon-reload'])
    stop_all(force=True)
    time.sleep(5)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # https://stackoverflow.com/a/27360648
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    sock.bind(('0.0.0.0', 10000))

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        logging.info('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            logging.info('connection from {}'.format(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                if not data:
                    break

                if data == b'disconnect':
                    disconnect()
                elif data == b'reboot':
                    connection.sendall('Rebooting...'.encode('utf-8'))
                    reboot()
                    continue
                elif data == b'restart':
                    connection.sendall('Restarting...'.encode('utf-8'))
                    restart()
                elif data == b'status:enable':
                    if not enabled:
                        connection.sendall('Enabling...'.encode('utf-8'))
                        start_all()
                elif data == b'status:disable':
                    if enabled:
                        connection.sendall('Disabling...'.encode('utf-8'))
                        stop_all()

                status = get_status()
                connection.sendall(status.encode('utf-8'))

        finally:
            # Clean up the connection
            connection.close()

run()
