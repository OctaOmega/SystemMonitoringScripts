# copyright @ Rajesh Kannan

import socket
import time
import re

# the public network interface
HOST = socket.gethostbyname(socket.gethostname())

# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.INADDR_ANY)
s.bind((HOST, 0))

# receive all packets
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

sessions = {}

while True:
    try:
        # receive data
        data, addr = s.recvfrom(65535)

        # extract source and destination IP and port
        src_ip = addr[0]
        src_port = 0
        dst_ip = socket.inet_ntoa(data[16:20])
        dst_port = 0

        domain_name = ""

        # extract source and destination port for TCP packets
        if data[9] == 6:
            pronto = 'tcp'
            src_port = int.from_bytes(data[20:22], byteorder="big")
            dst_port = int.from_bytes(data[22:24], byteorder="big")

            if src_port == 80 or dst_port == 80:
                pronto = 'http'
                http_data = (data[38:].decode('utf-8', errors='ignore')).split('\r\n')

                for line in http_data:
                    if 'Host:' in line:
                       domain_name = line.split(":")[1].strip()
            if src_port == 443 or dst_port == 443:
                pronto = 'tls'
                tls_header_offset = 41  # Offset to the start of TLS record header
                
                # Check if it's a valid TLS record
                if tls_header_offset < len(data):
                    tls_record_type = int.from_bytes(data[40:41], byteorder="big")
                    tls_handshake_type = int.from_bytes(data[45:46], byteorder="big")

                    # Check if it's a Handshake record and a Client Hello message
                    if tls_record_type == 22 and tls_handshake_type == 1:
                        tls_Server_extn = (data[100:220].decode('utf-8', errors='ignore'))
                        domain_name = str(re.findall(r'[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+', tls_Server_extn)[0])

        # extract source and destination port for UDP packets
        elif data[9] == 17:
            pronto = 'udp'
            src_port = int.from_bytes(data[20:22], byteorder="big")
            dst_port = int.from_bytes(data[22:24], byteorder="big")

        elif data[9] == 1:
            pronto = 'icmp'
        else:
            pronto = data[9]
        
        packet_time = time.time()
        tcp_flags = int.from_bytes(data[33:34], byteorder="big")
        
        if not src_ip in sessions or not src_port in sessions[src_ip]:
            sessions.setdefault(src_ip, {}).setdefault(src_port, {"start_time": packet_time, "tcp_fin": False, "domain":""})
        elif sessions[src_ip][src_port]["tcp_fin"]:
                # If TCP FIN flag is set, remove the session data
                del sessions[src_ip][src_port]
        
        start_time = sessions[src_ip][src_port]["start_time"]
        end_time = packet_time
        duration = end_time - start_time

        if domain_name != "":
            sessions[src_ip][src_port]["domain"] = domain_name

        webflow_data = [{
                "Proto":pronto,
                "SrcIP": src_ip,
                "SrcPort":src_port,
                "DstIP":dst_ip,
                "DstPort":dst_port,
                "Sess_st_time":start_time,
                "Sess_end_time":end_time,
                "Sess_dution":duration,
                "domain": sessions[src_ip][src_port]["domain"] if pronto in ["http","tls"] else "N/A" 
            }]
        
        # Check if TCP FIN flag is set
        if data[9] == 6 and tcp_flags & 0x01:
            # Set TCP FIN flag in the session data
            sessions[src_ip][src_port]["tcp_fin"] = True

        print(webflow_data)  

    except (Exception) as e:
        print(e)
