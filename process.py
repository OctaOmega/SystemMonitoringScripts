# copyright @ Rajesh Kannan

import psutil
import hashlib
import getdigicert
from datetime import datetime


class processManage():

    #list the process
    def listProcess():
        processes = []
        hash = hashlib.md5()
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                pinfo['createtime'] = datetime.utcfromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')
                pinfo['status'] = proc.status()
                if (proc.parent()) is None:
                    pinfo['parent_name'] = "No Parent"
                else:
                    pinfo['parent_name'] = proc.parent().name()
                    pinfo['parent_pid'] = proc.ppid()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess,FileNotFoundError):
                pinfo = 'N/A'
            else:
                processes.append(pinfo)
        return processes



    def check_process_dt(pid):
        
        processes = []
        P_Netcon = {}
        P_Netcon_list = []
        Parent_Netcon = {}
        Parent_Netcon_list = []
        P_listParents = {}
        P_listParents_list = []
        P_Children = {}
        P_Children_list = []
        hash = hashlib.md5()
        for proc in psutil.process_iter():
            if proc.pid == pid:
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                    try:
                        pinfo['p_status'] = proc.status()
                        pinfo['p_createtime'] = datetime.utcfromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')
                        pinfo['p_cwd'] = proc.cwd()
                        pinfo['p_cmdline'] = proc.cmdline()
                        pinfo['p_openfiles'] = proc.open_files()
                        pinfo['p_envars'] = proc.environ()
                        pinfo['p_digicert'] = getdigicert.getdigitalcerti(f'{proc.cwd()}\{proc.name()}')
                    except Exception:
                        pass
                    
                    Proc_NetConnection = proc.connections()

                    if Proc_NetConnection:
                        for connections in Proc_NetConnection:
                            P_Netcon['Protocol'] = connections.type.denominator
                            try:
                                P_Netcon['LocalIP'] = connections.laddr.ip
                                P_Netcon['LocalPort'] = connections.laddr.port
                                P_Netcon['RemoteIP'] = connections.raddr.ip
                                P_Netcon['RemotePort'] = connections.raddr.port
                                P_Netcon['Status'] = connections.status
                            except Exception:
                                pass
                            
                            if P_Netcon not in P_Netcon_list:
                                P_Netcon_list.append(P_Netcon)

                        pinfo['p_connections'] = P_Netcon_list
                    else:
                        pinfo['p_connections'] = "No network connections found"

                    if (proc.parent()) is None:
                        pinfo['parent_name'] = "No Parent"
                    else:
                        try:
                            pinfo['parent_name'] = proc.parent().name()
                            pinfo['parent_pid'] = proc.ppid()
                            pinfo['parent_createdtime'] = datetime.utcfromtimestamp(proc.parent().create_time()).strftime('%Y-%m-%d %H:%M:%S')
                            pinfo['parent_status'] = proc.parent().status()
                            pinfo['parent_cmdline'] = proc.parent().cmdline()
                            pinfo['parent_envars'] = proc.parent().environ()
                            pinfo['parent_connections'] = Parent_Netcon_list
                            pinfo['parent_cwd'] = proc.parent().cwd()
                            pinfo['parent_digicert'] = getdigicert.getdigitalcerti(f'{proc.parent().cwd()}\{proc.parent().name()}')
                        except Exception:
                            pass
                        
                        Parent_NetConnection = proc.parent().connections()

                        if Parent_NetConnection:
                            for connections in Parent_NetConnection:
                                try:
                                    Parent_Netcon['Protocol'] = connections.type.denominator
                                    Parent_Netcon['LocalIP'] = connections.laddr.ip
                                    Parent_Netcon['LocalPort'] = connections.laddr.port
                                    Parent_Netcon['RemoteIP'] = connections.raddr.ip
                                    Parent_Netcon['RemotePort'] = connections.raddr.port
                                    Parent_Netcon['Status'] = connections.status
                                except Exception:
                                    pass
                                
                                if Parent_Netcon not in Parent_Netcon_list:
                                    Parent_Netcon_list.append(Parent_Netcon)
                        else:
                            pinfo['parent_connections'] = "No network connections found"

                    PParents = proc.parents()
 
                    if PParents:
                        for parents in PParents:
                            try:
                                P_listParents['PPid'] = parents.pid
                                P_listParents['PName'] = parents.name()
                                P_listParents['PStatus'] = parents.status()
                            except Exception:
                                pass
                            if P_listParents not in P_listParents_list:
                                P_listParents_list.append(P_listParents)

                        pinfo['p_parents'] = P_listParents_list
                    else:
                        pinfo['p_parents'] = "No Parents"
                    
                    Process_Childs = proc.children()

                    if Process_Childs:
                        for pchild in Process_Childs:
                            try:
                                P_Children['CPID'] = pchild.pid
                                P_Children['CName'] = pchild.name()
                                P_Children['CStatus'] = pchild.status()
                                P_Children['CCreated'] = datetime.utcfromtimestamp(pchild.create_time()).strftime('%Y-%m-%d %H:%M:%S')
                                P_Children['CCWD'] = pchild.cwd()
                                P_Children['CCmdline'] = pchild.cmdline()
                            except Exception:
                                pass

                            if P_Children not in P_Children_list:
                                P_Children_list.append(P_Children)

                        pinfo['ChildName'] =  P_Children_list
                    else:
                        pinfo['ChildName'] =  "No Children"

                    hash.update(proc.exe().encode())
                    pinfo['p_MD5hash'] = hash.hexdigest()

                    try:
                        hash.update(proc.parent().exe().encode())
                        pinfo['parent_MD5hash'] = hash.hexdigest()
                    except Exception:
                        pinfo['parent_MD5hash'] = "Unable to Calculate MD5 Hash for the Parent"

                except (Exception, psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, FileNotFoundError) as e:
                    print(e)
                else:
                    processes.append(pinfo)
        
        return processes
    