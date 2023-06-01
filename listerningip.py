# copyright @ Rajesh Kannan

import socket
import psutil
import json
import urllib.request
import ipaddress
import dns.resolver


def is_private_ip(ip):
    private_ips = [
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16',
        '127.0.0.0/8'
    ]
    for private_ip in private_ips:
        if ipaddress.ip_address(ip) in ipaddress.ip_network(private_ip):
            return True
    return False

def get_ip_lookup(ip):
    """
    Get IP lookup details
    """
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        response = json.loads(urllib.request.urlopen(url).read())
        return response
    except:
       return []

def list_foreign_ips():
    """
    List all foreign IPs connected to the computer
    """
    # Get local IP address
    local_ip = socket.gethostbyname(socket.gethostname())

    # Get all active connections
    connections = psutil.net_connections()

    foreign_ips = []
    
    # Iterate through connections
    while True:
      try:
        for conn in connections:
            # Check if connection is IPV4 and not local
            if conn.family == socket.AF_INET and conn.laddr and conn.laddr[0] == local_ip and conn.raddr:
                # Get process details
                process = psutil.Process(conn.pid)
                # Get IP lookup details
                if is_private_ip(conn.raddr[0]):
                    IP_ISPNAme = 'Local IP'
                    IP_Country = 'Local IP'
                    IP_State = 'Local IP'
                    IP_City = 'Local IP'
                else:
                    ip_lookup = get_ip_lookup(conn.raddr[0])
                    IP_ISPNAme = ip_lookup.get('isp', 'N/A')
                    IP_Country = ip_lookup.get('country', 'N/A')
                    IP_State = ip_lookup.get('regionName', 'N/A')
                    IP_City = ip_lookup.get('city', 'N/A')

                try:
                   remoteport = conn.raddr.port
                except Exception:
                   pass

                foreign_ips.append({
                    "PID": conn.pid,
                    "ProcessName": process.name(),
                    "Protocol": conn.type.value,
                    "Status": conn.status,
                    "RemoteIP": conn.raddr[0] if conn.raddr else "N/A",
                    "RemotePort": conn.raddr[1] if conn.raddr else "N/A",
                    "ISP": IP_ISPNAme,
                    "Country": IP_Country,
                    "State": IP_State,
                    "City": IP_City
                })
      
        return foreign_ips
         
      except Exception:
        pass

def list_connected_ips():
    """
    List all IPs connected to the computer
    """
    # Get all active connections
    connections = psutil.net_connections()

    ips = []
    
    # Iterate through connections
    while True:
      try:
        for conn in connections:
            # Check if connection is IPV4
            if conn.family == socket.AF_INET:
                # Get process details
                process = psutil.Process(conn.pid)

                # Get IP lookup details
                ips.append({
                        "PID": conn.pid,
                        "ProcessName": process.name(),
                        "Protocol": conn.type.denominator,
                        "Status": conn.status,
                        "LocalIP": conn.laddr[0] if conn.laddr else "N/A",
                        "LocalPort": conn.laddr[1] if conn.laddr else "N/A",
                        "RemoteIP": conn.raddr[0] if conn.raddr else "N/A",
                        "RemotePort": conn.raddr[1] if conn.raddr else "N/A"
                })
                
        return (ips)
                
      except Exception:
        pass
    