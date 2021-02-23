#!/usr/bin/env python

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", dest="ip", help="IP address to be scanned")
    options = parser.parse_args()

    if not options.ip:
        parser.error("Please enter a valid IP address")

    return options


def scan(ip):
    if not ip:
        print("No input given. Exiting program")
        exit()

    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)

    return client_list


def print_scan_result(list):
    print("IP\t\t\tMAC address")
    print("=================================================")

    for client in list:
        print(client["ip"] + "\t\t" + client["mac"])


arguments = get_arguments()
scan_results = scan(arguments.ip)

print_scan_result(scan_results)