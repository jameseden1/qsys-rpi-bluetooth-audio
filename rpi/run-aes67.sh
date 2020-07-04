#!/bin/bash
#
# Tested on Ubuntu 18.04
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

function cleanup {
#kill and wait for previous daemon instances to exit
  sudo killall -q ptp4l
  killall -q aes67-daemon
  while killall -0 aes67-daemon 2>/dev/null ; do
    sleep 1
  done
}

if ! [ -x "$(command -v aes67-linux-daemon/daemon/aes67-daemon)" ]; then
  echo 'Error: aes67-daemon is not compiled.' >&2
  exit 1
fi

if ! [ -r "aes67-linux-daemon/3rdparty/ravenna-alsa-lkm/driver/MergingRavennaALSA.ko" ]; then
  echo 'Error: MergingRavennaALSA.ko module is not compiled.' >&2
  exit 1
fi

trap cleanup EXIT

#configure system parms
sudo sysctl -w net/ipv4/igmp_max_memberships=66

#install kernel module
sudo insmod aes67-linux-daemon/3rdparty/ravenna-alsa-lkm/driver/MergingRavennaALSA.ko

echo "Starting AES67 daemon ..."
aes67-linux-daemon/daemon/aes67-daemon -c daemon.conf
