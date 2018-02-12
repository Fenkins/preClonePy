import pysnow
import shelve
import os.path

osPath = os.path.abspath(__file__)
filePath = osPath.rsplit('/',1)[0] + '/accountInfo'
# Fill parameters with saved one from the file if accountInfo exists
hostName = ()
userName = ()
password = ()
if os.path.isfile(filePath):
# reading data from existing file
	f=open(filePath)
	lines=f.readlines()
	hostName = lines[0].rstrip()
	userName = lines[1].rstrip()
	password = lines[2].rstrip()

    
else:
	# Reading account data to save on disk
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

# Here is what we got so far
print(hostName)
print(userName)
print(password)

# Create client object
c = pysnow.Client(host=hostName, user=userName, password=password)

# Define a resource, here we'll use the sctask table API
sctask = c.resource(api_path='/table/sc_task')
changeRQ = c.resource(api_path='table/change_request')
# CHG0055854

print 'Waiting for the reference ticket number'
x = raw_input()
print 'Ticket number received, ' + x


# Set the payload
new_record = {
    'short_description': 'Pre-clone checklist for ' + x,
    'description': 'Please perform pre-clone checklist for '+ x,
    'company': 'Data Intensity',
    'task_for': 'ankovalev',
    'cmdb_ci': 'zzData Intensity - Infrastructure',
    # This one is working but we don't need it
    'assignment_group': 'System Administration Tier 1'
}

# Create a new sctask record
result = sctask.create(payload=new_record)

# Printing result
print 'Here is your ticket:'
print result['number']