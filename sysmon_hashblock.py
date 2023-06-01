# copyright @ Rajesh Kannan

import xml.etree.ElementTree as ET
import subprocess

SYSMON_CONFIG_PATH = (r"C:\Users\testwindows\Desktop\Sysmon\sysmonconfig.xml")

def update_sysmon_config(hash_value):
    tree = ET.parse(SYSMON_CONFIG_PATH)
    root = tree.getroot()
    event_filtering = root.find('EventFiltering')
    rule_group = None
    for child in event_filtering:
        if child.attrib.get('groupRelation') == 'or' and child[0].attrib.get('value') == 'Process Create (1)':
            rule_group = child
            break
    if rule_group is None:
        rule_group = ET.SubElement(event_filtering, 'RuleGroup')
        rule_group.set('groupRelation', 'or')
        process_create = ET.SubElement(rule_group, 'ProcessCreate')
        process_create.set('onmatch', 'exclude')
        process_create.set('value', 'Process Create (1)')
    new_rule = ET.SubElement(rule_group, 'Rule')
    new_condition = ET.SubElement(new_rule, 'Image')
    new_condition.set('condition', 'is')
    new_condition.text = hash_value
    tree.write(SYSMON_CONFIG_PATH)
    powershell_script = f"runas /noprofile /user:DESKTOP-2NSFENJ\usocadmin sysmon -c {SYSMON_CONFIG_PATH}"
    subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-Command', powershell_script])


update_sysmon_config('FC6F9DBDF4B9F8DD1F5F3A74CB6E55119D3FE2C9DB52436E10BA07842E6C3D7C')