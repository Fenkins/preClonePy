import pysnow
import shelve
import os.path

import time
time.gmtime()
current_time = time.localtime()
utc = '{}{:0>2}{:0>2}'.format('-' if time.altzone > 0 else '+', abs(time.altzone) // 3600, abs(time.altzone // 60) % 60)
print(utc)
print(type(utc))
print(int(utc))
print(int('-0500'))

offset =int()
# Setting the timeModifier
if utc!='-0500':
	# Need to calculate time offset
	print 'Triggered 1'
	offset = -int(utc) + int('-0500')
	print('Offset is:')
	print(offset)
else:
	# No need to do shit
	print 'Triggered 2'

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
changeRQ = c.resource(api_path='/table/change_request')
# CHG0055854

print 'Waiting for the reference ticket number'
chgNumber = raw_input()
print 'Ticket number received, ' + chgNumber

responseCHG = changeRQ.get(query={'number': chgNumber})

responseCHGDict = (responseCHG.one())
print responseCHGDict['start_date']
print responseCHGDict['end_date']
# Response received
print(type(responseCHGDict['end_date']))
print(str(responseCHGDict['end_date']))
print'integer'


# Calculating proper start/end time 
datePartStart = str(responseCHGDict['start_date'])[:11]
print(datePartStart)
# Received date in format of 2018-06-01
timePartStart = str(responseCHGDict['start_date'])[11:]
print(timePartStart)
# Received time in format of 14:00:00
datePartEnd = str(responseCHGDict['end_date'])[:11]
timePartEnd = str(responseCHGDict['end_date'])[:11]

# Set the payload
new_record = {
    'short_description': 'Pre-clone checklist for ' + chgNumber,
    'description': 'Please perform pre-clone checklist for '+ chgNumber + '\nChange Request start time: ' + responseCHGDict['start_date'] + '\nChange Request end time: ' + responseCHGDict['end_date'],
    'company': 'Data Intensity',
    'task_for': 'ankovalev',
    'cmdb_ci': 'zzData Intensity - Infrastructure',
    # This one is working but we don't need it
    'assignment_group': 'System Administration Tier 1'
}

# Create a new sctask record
resultSR = sctask.create(payload=new_record)

# Printing result
print 'Here is your ticket:'
print resultSR['number']
#print (responseCHG.one())