###
# Author: Glitch <Glitch@Glitch.is>
# Name: InnaCalendar
# Description: Uses extracted JSON data from Inna to create an iCalendar file that can be imported to iCalendar compatible application such as Google Calendar.
# Usage: Run the script with the following command 'python3 InnaCalendar.py'. Enter your username and password and let the script do it's work, it will leave
# you with an iCalendar file 'Calendar.ics', now you can import that into the application of your choice such as Google Calendar.
#
# Report any bugs on GitHub <https://github.com/Glitch-is/InnaCalendar>
###

import os
import json
import datetime
import requests
from getpass import getpass
from icalendar import Calendar, Event

while True:
    u = input("Kennitala: ") # Prompt the user for their social security number
    p = getpass() # Prompt the user for their password wich doesn't get displayed thanks to the getpass module

    payload = {
        'Kennitala': u,
        'Lykilord': p,
        '_ROWOPERATION': 'Staðfesta'
    } # Initialize the login payload

    print("Attempting to log into inna.is")

    login = requests.post('https://www.inna.is/login.jsp', data=payload) # Login to the old Inna login system with the payload

    if("Innskráning tókst ekki" in login.text):
        print("Login Failed. Please try again...")
    else:
        print("Login Successful")
        break;


cookie = {"JSESSIONID": login.cookies["JSESSIONID"]} # Get the Session from the response cookie to use for next step of the login

oldInna = requests.get('https://www.inna.is/opna.jsp?adgangur=0', cookies=cookie) # Tell inna we want to use the new site so it will send us a token to skip the new inna authentication, how convienient?
activate = oldInna.text.split("'")[1] # Parse the link to the new inna with our token

# using a session here because normal get request wasn't working
session = requests.Session()
response = session.get(activate)

newCookie = {"JSESSIONID": session.cookies.get_dict()["JSESSIONID"]} # Store our new session in a cookie

studentInfo = requests.get('https://nam.inna.is/api/UserData/GetLoggedInUser', cookies=newCookie) # Get the student info
studentId = studentInfo.json()['studentId'] # Parse the studentId from the studentInfo

now =datetime.datetime.now()
later = now + datetime.timedelta(days=6)
schedulePayload = {
    'staff_id':'',
    'student_id':str(studentId),
    'date_from': '%s.%s.%s' % (str(now.day).zfill(2), str(now.month).zfill(2), str(now.year).zfill(2)),
    'date_to': '%s.%s.%s' % (str(later.day).zfill(2), str(later.month).zfill(2), str(later.year).zfill(2)),
    'attendanceOverview':'0'
} # Initialize the Schedule payload

print("Fetching Schedule...")

schedule = requests.get("https://nam.inna.is/api/Timetable/GetTimetable", params=schedulePayload, cookies=newCookie) # Get the user schedule with our payload
js = schedule.json() # Store our JSON Object

print("Saving JSON...")
with open('schedule.json', 'w') as f:
  json.dump(js, f, ensure_ascii=False)

print("Starting to build Schedule...")

cal = Calendar() # Initiate a new Calander Object

for i in js: # Loop through each class individually
    # putting teacher in a variable to catch exceptions. Sometimes no teacher is registered and we get keyerror
    teacher = " " + i["teacher"] if 'teacher' in i else ""

    title = i["titleShort"] + " " + i["classroom"] + teacher # Title of the event
    print("Adding Event: " + title)
    start = datetime.datetime.strptime(i["start"], "%m/%d/%Y %H:%M:%S") # Time when the event starts
    end = datetime.datetime.strptime(i["end"], "%m/%d/%Y %H:%M:%S") # Time when event ends

    event = Event() # Create a new Event Object for the class
    event.add('summary', title) # Add the Summary or Name of the Event which is gonna look something like "MATH101 S 1 ABC" and is formated like "<CLASS> <ROOM> <TEACHER>"
    event.add('dtstart', start) # Add the start of the Event
    event.add('dtend', end) # Add the end of the Event
    event.add('rrule', {'freq': 'weekly'}) # Make the Event repeat weekly so our calander doesn't get obsolete after a week

    cal.add_component(event) # Add the Event to our Calendar

print("Writing Schedule to '" + os.getcwd() + "/Calendar.ics'")

with open("Calendar.ics", "wb") as f: # Open the iCalendar File
    f.write(cal.to_ical()) # Write our Calendar Object to the iCalendar file so it can be imported into iCalendar compatible applications (Google Calendar and more...)

print("Finished")
