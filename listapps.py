# copyright @ Rajesh Kannan


import winreg
from datetime import datetime

def apps(hive, flag, installer):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                        0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]
    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)

            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
            software['installer'] = installer
            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            try:
                software['InstallDate'] = datetime.strptime(winreg.QueryValueEx(asubkey, "InstallDate")[0], '%Y%m%d').strftime("%Y-%m-%d")
            except EnvironmentError:
                software['InstallDate'] = 'undefined'    
            try:
                software['InstallLocation'] = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
                if software['InstallLocation'] == '' or software['InstallLocation'] == None:
                    software['InstallLocation'] = 'undefined'
            except:
                try:
                    software['InstallLocation'] = winreg.QueryValueEx(asubkey, "InstallDir")[0]
                    if software['InstallLocation'] == '' or software['InstallLocation'] == None:
                        software['InstallLocation'] = 'undefined'
                except:
                    try:
                        software['InstallLocation'] = winreg.QueryValueEx(asubkey, "DisplayIcon")[0]
                        if software['InstallLocation'] == '' or software['InstallLocation'] == None:
                            software['InstallLocation'] = 'undefined'
                    except:
                        software['InstallLocation'] = 'undefined'

            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

def allapps():
    appslist =[]
    
    system32 = apps(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY, 'System 32Bit') 
    system64 = apps(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY, 'System 64Bit') 
    user = apps(winreg.HKEY_CURRENT_USER, 0, 'User')

    appslist.append(system32)
    appslist.append(system64)
    appslist.append(user)

    return appslist