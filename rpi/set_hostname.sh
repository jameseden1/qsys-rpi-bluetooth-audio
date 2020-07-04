#!/bin/bash
# /usr/sbin/change_hostname.sh - program to permanently change hostname.  Permissions
# are set so that www-user can `sudo` this specific program.
# https://stackoverflow.com/a/49284621

# args:
# $1 - new hostname, should be a legal hostname

raspi-config nonint do_hostname "$1"
hostnamectl set-hostname --pretty "$2"
