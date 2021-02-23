#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="interface to change mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="value of new mac address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("Please enter interface, use --help for more information")
    elif not options.new_mac:
        parser.error("Please enter new MAC address use --help for more information")

    return options


def change_mac(interface, new_mac):
    print("changing mac address for " + interface + " to " + new_mac)

    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])


def get_current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["sudo", "ifconfig", interface])

    search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if search_result:
        return search_result.group(0)
    else:
        print("Could not read mac address")


options = get_arguments()
mac_address = get_current_mac_address(options.interface)

print("Current MAC address = " + str(mac_address))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac_address(options.interface)

if current_mac == options.new_mac:
    print("MAC address was successfully changed to " + current_mac)
else:
    print("MAC address did not change")