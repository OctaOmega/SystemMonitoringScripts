# copyright @ Rajesh Kannan

import psutil

# List all services
def listservices():
    services = []

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'status'])
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo['name'] in ['services.exe', 'svchost.exe']:
                for service in proc.children(recursive=True):
                    try:
                        service_info = service.as_dict(attrs=['pid', 'name', 'status', 'username'])
                    except psutil.NoSuchProcess:
                        pass
                    else:
                        services.append({
                            "name": service_info['name'],
                            "pid": service_info['pid'],
                            "status": service_info['status'],
                            "group": service_info['username']
                        })
    return services


def allservices():
    listservices = []
    for serv in psutil.win_service_iter():
        try:
            serinfo = dict(pid=serv.pid(),
                           name=serv.name(),
                           display_name=serv.display_name(),
                           binpath=serv.binpath(),
                           username=serv.username(),
                           start_type=serv.start_type(),
                           status=serv.status(),
                           description=serv.description())
        except psutil.NoSuchProcess:
            pass
        else:
            listservices.append({
                "name": serinfo['name'],
                "pid": str(serinfo['pid']).strip(),
                "status": serinfo['status'],
                "group": serinfo['username'],
                "start_type": serinfo['start_type'],
                "binnarypath": serinfo['binpath'],
                "displayName": str(serinfo['display_name']).strip(),    
                "description": str(serinfo['description']).strip()                 
            })
    
    return listservices


