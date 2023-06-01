# copyright @ Rajesh Kannan

import json
import process
import deviceinfo
import listerningip
import lstservices
import listapps
import fw
from flask import Flask, request, Response
import getdigicert
import remoteadmin


app = Flask(__name__)

LOCALHOST_ADD = ['127.0.0.1', 'localhost']
WHITELIST_REMOTE_ADD = ['192.168.30.1']

# main index 
@app.route('/devicehome', methods=['GET'])
def index():
    deviceinfo_list = systeminfo()
    application_list = applications()
    process_list = listprocess()
    user_list = deviceinfo.userinfo()
    connect_list = listerningip.list_connected_ips()
    Foreignip_list = listerningip.list_foreign_ips()
    listofapplication = listapps.allapps()
    appcount = 0
    for list in application_list:
        for apps in list:
            if isinstance(apps,dict):
                  appcount+= 1
    proc_count=0
    
    for proc in process_list:
        if isinstance(proc,dict):
            proc_count+=1

    con_count = 0
    for connection in connect_list:
        if isinstance(connection,dict):
            con_count+=1

    Foreignip_count = 0
    for foreignip in Foreignip_list:
        if isinstance(foreignip,dict):
            Foreignip_count+=1
    device_data = [deviceinfo_list,appcount,proc_count,user_list,con_count,Foreignip_count,Foreignip_list,listofapplication]
    if request.remote_addr not in LOCALHOST_ADD and request.remote_addr in WHITELIST_REMOTE_ADD:
        return json.dumps(device_data)
    else:
        return json.dumps("Access Denied")

#List Process
@app.route("/listprocess", methods=['GET'])
def listprocess():
    processes = []
    processes = process.processManage.listProcess()
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(processes)
        

#check Process
@app.route("/checkproc/<int:pid>", methods=['GET'])
def checkproc(pid):
    checkproc = []
    checkproc = process.processManage.check_process_dt(pid)
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(checkproc)

#Get Digital Certificates
@app.route("/digitalcert/<path>", methods=['GET'])
def digitalcert(path):
    digitalcert = []
    digitalcert = getdigicert.getdigitalcerti(path)
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(digitalcert)

#List Systeminfo
@app.route("/systeminfo", methods=['GET'])
def systeminfo():
    systemdata = []
    systemdata = deviceinfo.getsysteminfo()
    request.url_root
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(systemdata)

#List list_foreign_ips
@app.route("/listfgnips", methods=['GET'])
def listfgnips():
    listfgnips = []
    listfgnips = listerningip.list_foreign_ips()
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(listfgnips)

#List All Connected IPs
@app.route("/connips", methods=['GET'])
def connips():
    connips = []
    connips = listerningip.list_connected_ips()
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(connips)  

#Running Services
@app.route("/runservices", methods=['GET'])
def runservices():
    runservices = []
    runservices = lstservices.listservices()
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(runservices)

#All Services
@app.route("/allservices", methods=['GET'])
def allservices():
    allservices = []
    allservices = lstservices.allservices()
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(allservices)  
        

#All Application
@app.route("/applications", methods=['GET'])
def applications():
    applications = []

    applications = listapps.allapps()
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(applications) 
    

#Get Digicert verification
@app.route("/digicert/<path>", methods=['GET'])
def digicert(path):
    digicert = []
    digicert = getdigicert.getdigitalcerti(path)
    if request.remote_addr not in LOCALHOST_ADD:
        return json.dumps(digicert)  

# Function to stream the video to the web page
@app.route('/video_feed')
def video_feed():
    try:
        return Response(remoteadmin.remotewebcam(True),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception:
        return "No webcam found !"


#Firewall Rules
@app.route("/firewall/<ruleAction>/<data>", methods=['GET'])
def firewall(ruleAction,data):
    dict_values = eval(data)
    firewallData = []

    try:
        if ruleAction == "add":
            for fields in dict_values:
                rule_name = dict_values['rule_name']
                description = dict_values['description']
                dir = dict_values['dir']
                interface = dict_values['interface']
                action = dict_values['action']
                profile = dict_values['profile']
                localip = dict_values['localip']
                remoteip = dict_values['remoteip']
                protocol = dict_values['protocol']
            
            firewallData = fw.add_rule(rule_name, description, dir, interface, action, profile, localip, remoteip, protocol)
            
        if ruleAction == "modify":
            for fields in dict_values:
                rule_name = dict_values['rule_name']
                rule_state = dict_values['rule_state']

            firewallData = fw.fw_modify_rule(rule_name, rule_state)

        if ruleAction == "remove":
            for fields in dict_values:
                rule_name = dict_values['rule_name']

            firewallData = fw.fw_modify_rule(rule_name)
        
        if ruleAction == "show":
            rule_name = dict_values['rule_name']
            firewallData = fw.get_firewall_rules()
            if request.remote_addr not in LOCALHOST_ADD:           
                return json.dumps(firewallData)

    except Exception as e:
        json.dumps(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)