# copyright @ Rajesh Kannan
 
from subprocess import call, run, check_output
from subprocess import PIPE, DEVNULL

'''
def check_admin():
    """ Force to start application with admin rights """
    try:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        isAdmin = False
    if not isAdmin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    '''

def add_rule(rule_name, description, dir, interface, action, profile, localip, remoteip, protocol):
    #""" Add rule to Windows Firewall """
    try:
        return_response = call(
        f'''
        netsh advfirewall firewall add rule 
        name={rule_name} 
        description={description} 
        dir={dir} 
        interfacetype={interface} 
        action={action} 
        enable=yes 
        localip={localip} 
        remoteip={remoteip}
        protocol={protocol} 
        profile={profile}, 
        shell=True, 
        stdout=DEVNULL, 
        stderr=DEVNULL
        '''
        )
    except Exception:
        return False
    
    return return_response


def fw_modify_rule(rule_name, state):
    try:
        state, message = ("yes", "Enabled") if state else ("no", "Disabled")
        """Enable or Disable a specific rule"""
        run(
        f'''netsh advfirewall firewall set rule 
        name={rule_name} 
        new enable={state}",
        shell=True,
        stdout=DEVNULL,
        stderr=DEVNULL
        '''
        )
    except Exception:
        return False
    
    return True

def fw_delete_rule(rule_name):
    try:
        """Enable or Disable a specific rule"""
        run(
        f'''netsh advfirewall firewall delete rule 
        name={rule_name},
        shell=True,
        stdout=DEVNULL,
        stderr=DEVNULL
        '''
        )
    except Exception:
        return False
    
    return True

def get_firewall_rules():
    firewall_rules = []
    result = check_output("powershell.exe Get-NetFirewallRule", shell=True)

    rule_lines = result.decode('utf-8').splitlines()
    firewall_rule = {}
    for line in rule_lines:
        if ":" in line:
            rule_name, _, rule_value = line.partition(":")
            firewall_rule[rule_name.strip()] = rule_value.strip()
        if line == "":
            firewall_rules.append(firewall_rule)
            firewall_rule = {}

    return firewall_rules


if __name__ == "__main__":
    pass