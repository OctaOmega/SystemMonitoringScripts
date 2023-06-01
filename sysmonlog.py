# copyright @ Rajesh Kannan

from html.parser import HTMLParser
import subprocess
from datetime import datetime

# Create HTMLParser Class
class MyHTMLParser(HTMLParser):

    # __init__ function
    def __init__(self):
        super().__init__()
        self.Eventdata = []
        self.key = "NA"
        self.Tattrib = "NA"
        self.Events = {}
    
    #Add key value to dict
    def add(self, skey, svalue):
        self.Events[skey] = svalue
        self.Eventdata.append(self.Events)
        
    #handle starting tag
    def handle_starttag(self, tag, attrs):
        if 'data' not in tag:
            self.key = tag
        for attr in attrs:
            if attr[0] == 'name':
                self.Tattrib = attr[1]
            else:
                self.Tattrib = attr[0]

    #Handle Data
    def handle_data(self, data):
        if "NA" not in self.key:
            self.add(self.key,data)
            self.key = "NA"
        elif "NA" not in self.Tattrib:
            self.add(self.Tattrib,data)
            self.Tattrib ="NA"

def _logfeeder(log_name,last_system_time):
    # Define the wevtutil command to retrieve the events in XML format
    wevtutil_cmd = "wevtutil qe "+log_name+ " \"/q:*[System[TimeCreated[@SystemTime>'"+last_system_time+"']]]\" /rd:true /f:xml"
    # Execute the command and capture the output
    output = subprocess.check_output(wevtutil_cmd, shell=True)
    return output


#Return data
def getparsedAllEvents(systime=datetime(1970, 1, 1, 0, 0, 0)):
    
    last_system_time = datetime.min
    # Get the last processed SystemTime from arg
    last_system_time = datetime.strptime(str(systime), "%Y-%m-%d %H:%M:%S")
    

    # Define the Sysmon event log name
    log_name = "Microsoft-Windows-Sysmon/Operational"

    #Feed the log
    output = _logfeeder(log_name,last_system_time.strftime("%Y-%m-%dT%H:%M:%S"))

    #Output Normalization
    decoded_output =  output.decode("utf-8", errors="ignore").strip()
    
    # Parse the XML output and extract the events and their fields
    parser = MyHTMLParser()
    parser.feed(decoded_output)
   
    return parser.Eventdata