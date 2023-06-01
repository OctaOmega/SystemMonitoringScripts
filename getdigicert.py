# copyright @ Rajesh Kannan

import subprocess
import os

# Get Digital Certificate using PS Script
def getdigitalcerti(file_path):

    #Get PowerShell Digital Certi
    
    powershell_script = f'''
    $file = "{file_path}"
    $signature = Get-AuthenticodeSignature $file
    $certificate = $signature.SignerCertificate

    Write-Output "Subject: $($certificate.Subject)"
    Write-Output "Issuer: $($certificate.Issuer)"
    Write-Output "Thumbprint: $($certificate.Thumbprint)"
    Write-Output "NotBefore: $($certificate.NotBefore)"
    Write-Output "NotAfter: $($certificate.NotAfter)"
    '''

    curr_Wrk_dir = os.path.dirname(__file__)
    digiSigdata_dict ={}

    #Default value for Verification.
    digiSigdata_dict['MS_DA_Verification'] = "Not Verified"
    digiSigdata_dict['FilePath'] = file_path

    try:
        # Subprocess to run the script
        signtool_path = os.path.join(curr_Wrk_dir, "signtool", "signtool.exe")
        verification = subprocess.run([signtool_path, "verify", "/pa", file_path], stdout=subprocess.PIPE)
        msverify = (verification.stdout.decode('utf-8')).splitlines()
        
        for key in msverify:
            if ":" in key and "Successfully verified" in key:
                verify_msg, _, file_ver_path = key.partition(":")
                digiSigdata_dict['MS_DA_Verification'] = verify_msg.strip() #If cert verfied default value will be overwritten
                digiSigdata_dict['FilePath'] = file_ver_path.strip()
            else:
                pass


        result = subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-Command', powershell_script], stdout=subprocess.PIPE)
        #Return the list
        digiSigdata = []
        digiSigdata = (result.stdout.decode('utf-8')).splitlines()
        for line in digiSigdata:
            if ":" in line:
                filed_name, _, filed_value = line.partition(":")
                digiSigdata_dict[filed_name.strip()] = filed_value.strip()
    
    except Exception:
        digiSigdata_Error = {}
        digiSigdata_Error['MS_DA_Verification'] = "Not Verified"
        digiSigdata_Error['FilePath'] = file_path
        return digiSigdata_Error
    
    else:
        return digiSigdata_dict

if __name__ == "__main__":
    pass