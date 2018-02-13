import pysnow
import shelve
import os.path
import pytz
from datetime import datetime


osPath = os.path.abspath(__file__)
filePath = osPath.rsplit('/',1)[0] + '/accountInfo'
# Fill parameters with saved one from the file if accountInfo exists
hostName = ()
userName = ()
password = ()
if os.path.isfile(filePath):
	# Reading data from existing file
	f=open(filePath)
	lines=f.readlines()
	hostName = lines[0].rstrip()
	userName = lines[1].rstrip()
	password = lines[2].rstrip()
	print 'Settings successfully loaded from configuration file'
    
else:
	# Reading input account data to write on disk
	print 'Please specify the host name you want to operate on'
	hostName = raw_input()
	with open (filePath, 'a') as f: f.write(hostName + '\n')
	print 'Please enter your username'
	userName = raw_input()
	with open (filePath, 'a') as f: f.write(userName + '\n')
	print 'Please enter your password'
	password = raw_input()
	with open (filePath, 'a') as f: f.write(password)
	# Account info is stored on the disk now
	print 'Configuration saved'


# Create client object
c = pysnow.Client(host=hostName, user=userName, password=password)

# Define a resource, here we'll use the sctask table API
sctask = c.resource(api_path='/table/sc_task')
changeRQ = c.resource(api_path='/table/change_request')

print 'Waiting for a reference ticket number'
chgNumber = raw_input()
print 'Ticket number received: ' + chgNumber
print 'Working now...'

# Quering for CHG and CHG's details
responseCHG = changeRQ.get(query={'number': chgNumber})
responseCHGDict = (responseCHG.one())

# Working out the time differences, server is running on UTC
est = pytz.timezone('America/New_York')
utc = pytz.utc
fmt = '%Y-%m-%d %H:%M:%S'

startTimeEDT = datetime.strptime(responseCHGDict['start_date'], '%Y-%m-%d %H:%M:%S')
endTimeEDT = datetime.strptime(responseCHGDict['end_date'], '%Y-%m-%d %H:%M:%S')

startTimeEDT = startTimeEDT.replace(tzinfo=utc)
endTimeEDT = endTimeEDT.replace(tzinfo=utc)

startTimeEDTs = str(startTimeEDT.astimezone(est).strftime(fmt))
endTimeEDTs = str(endTimeEDT.astimezone(est).strftime(fmt))


# Set the payload
new_record = {
    'short_description': 'Pre-clone checklist for ' + chgNumber,
    'description': 'Please perform pre-clone checklist for '+ chgNumber + '\nChange Request start time: ' + startTimeEDTs + '\nChange Request end time: ' + endTimeEDTs,
    'company': 'Data Intensity',
    'task_for': 'ankovalev',
    'cmdb_ci': 'zzData Intensity - Infrastructure',
    # This one is working but we don't need it
    'assignment_group': 'System Administration Tier 1'
}

# Creating a new sctask record
resultSR = sctask.create(payload=new_record)

# Printing result
print 'Pre-clone checklist available at: ' + resultSR['number']
