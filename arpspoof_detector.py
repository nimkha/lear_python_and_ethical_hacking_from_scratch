#!/usr/bin/env python

import scapy.all as scapy
import scapy_http.http as http
from arp_spoof import get_mac_address


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2: # Catches ARP packets
        real_mac = get_mac_address(packet[scapy.ARP].psrc)
        response_mac = packet[scapy.ARP].hwsrc
        if real_mac != response_mac:
            print("[+] You are under attack")


def sniffer(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


if __name__ == "__main__":

    try:
        sniffer("eth0")
    except KeyboardInterrupt:
        print("[-] Exiting program")
