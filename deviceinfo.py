# copyright @ Rajesh Kannan

import platform
import socket
import os
import ctypes
import uuid 
import psutil
from datetime import datetime


def getsysteminfo():
    systemdata = {}
    # Get computer info
    mac = (hex(uuid.getnode()))
    systemdata['mac_address'] = ':'.join(map('{}{}'.format, *(mac[::2], mac[1::2]))) 
    systemdata['computer_name'] = socket.gethostname()
    systemdata['operating_system'] = platform.system()
    systemdata['os_version'] = platform.version()
    systemdata['processor'] = platform.processor()
    systemdata['ip_address'] = socket.gethostbyname(systemdata['computer_name'])
    systemdata['CPU_usage'] = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    systemdata['MEM_usage'] = memory.used / memory.total * 100
    disk = psutil.disk_usage('/')
    systemdata['Disk_usage'] = disk.used / disk.total * 100
    ethernet = psutil.net_io_counters()
    systemdata['ETH_usage'] = ethernet.bytes_sent + ethernet.bytes_recv

    return [systemdata]

def userinfo():
    
    userdata = {}
    userdata['username'] = os.getlogin()
    userdata['Isadmin'] = 'Yes' if ctypes.windll.shell32.IsUserAnAdmin() else 'No'
    UserLoginTime =  str(psutil.users()).split(',')[3].split('=')[1]
    userdata['Lastlogin'] = datetime.utcfromtimestamp(float(UserLoginTime)).strftime('%Y-%m-%d %H:%M:%S')

    
    return [userdata]
