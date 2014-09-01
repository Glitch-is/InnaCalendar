InnaCalendar
============

##Description
This python script uses extracted JSON data from Inna to create an iCalendar file that can be imported to iCalendar compatible application such as Google Calendar.

##Dependencies

####Python 3.x
Make sure you're running Python 3.x.

####iCalendar
You need the iCalendar Python module which can be installed with the following command
```
sudo pip install icalendar
```

##Usage
Extract your schedule from Inna so you're left with the JSON data and place it into 'Schedule.json', make sure it's in the same directory you're running the script from.
###Run the Script
```
python3 InnaCalendar.py
```
###Output
You will be left with an iCalendar file 'Calendar.ics'

###Import
Now that you have your iCalendar file you can import into any iCalendar compatible application such as Google Calendar.

#Bugs
If you find any bugs you can either report it here on GitHub or email me <Glitch@Glitch.is>

#Author
Glitch <Glitch@Glitch.is>
