###
# Author: Glitch <Glitch@Glitch.is>
# Name: InnaCalendar
# Description: Uses extracted JSON data from Inna to create a iCalendar file that can be imported to iCalendar compatible application such as Google Calendar.
# Usage: Extract your schedule from Inna so you're left with the JSON data and place it into 'Schedule.json', make sure it's in the same directory you're
#        running this script from. Run the script 'python3 InnaCalendar.py' which will leave you with an iCalendar file 'Calendar.ics', now you can import
#        that into the application of your choice such as Google Calendar.
#
# Report any bugs on GitHub <https://github.com/RuNnNy/InnaCalendar>
###


from icalendar import Calendar, Event
import json
import datetime

cal = Calendar() # Initiate a new Calander Object

schedule = "" # Declare a string for the JSON

with open("Schedule.json", 'r') as f: # Read the JSON data from a file
    for line in f: # Loop through lines, even there's only one..
        schedule += line
js = json.loads(schedule) # Load the JSON Object

for i in js: # Loop throught each class individually
    event = Event() # Create a new Event Object for the class
    event.add('summary', i["titleShort"] + " " + i["classroom"] + " " + i["teacher"]) # Add the Summary or Name of the Event which is gonna look something like "MATH101 S 1 ABC" and is formated like "<CLASS> <ROOM> <TEACHER>"
    event.add('dtstart', datetime.datetime.strptime(i["start"], "%m/%d/%Y %H:%M:%S")) # Add the start of the Event
    event.add('dtend', datetime.datetime.strptime(i["end"], "%m/%d/%Y %H:%M:%S")) # Add the end of the Event
    event.add('rrule', {'freq': 'weekly'}) # Make the Event repeat weekly so our calander doesn't get obsolete after a week

    cal.add_component(event) # Add the Event to our Calendar

with open("Calendar.ics", "wb") as f: # Open the iCalendar File
    f.write(cal.to_ical()) # Write our Calendar Object to the iCalendar file so it can be imported into iCalendar compatible applications (Google Calendar and more...)
