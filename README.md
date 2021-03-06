# FamilyCalendar
Gathers events and appointments from various calendar apps of multiple people and thus generates a perfect synchronized time table for the whole family.

![Example Image](https://github.com/Andy0n/FamilyCalendar/raw/master/img/time.png "Example Image")

### Goals:
* Integrations:
    * Google Calendar ✓
    * WebUntis ✓
    * Outlook Calendar
    * Apple Calendar
    * ical, ics ✓

* Picture Creation
    * Standalone ✓
    * Magic Mirror Module ✓ (Seperate Repository)
    * epaper compatible ✓

* Misc
    * Telegram Notification/Daily Reminder Bot
    * Creation of an ics Calendar
    
### Setup:
1. cp _config.py config.py
2. Configure the MATES dict with calenders and colors for each name
3. Download a font and copy it to ./assets/fonts/*.ttf and configure the filename in the config file
4. If using google calendars:
    1. Go to https://console.cloud.google.com
    2. Create Project, add Calendar API and download the credentials.json
    3. copy it to ./assets/credentials.json
    4. To generate the tokens for the specific calendars you must run this application in an environment with a GUI-enabled browser. 
    5. Follow the instructions in the CLI.
    6. If you want to use this program on another device, you can copy the tokens and assets folder there.
5. finish

##### Setup for use with Magic Mirror:
1. Install [MMM-FamilyCalendar](https://github.com/Andy0n/MMM-FamilyCalendar) to /path_to_mm/modules/
2. For specifics on the configuration see the [README of MMM-FamilyCalendar](https://github.com/Andy0n/MMM-FamilyCalendar)
   
![Example Mirror Image](https://github.com/Andy0n/FamilyCalendar/raw/master/img/time_mirror.png "Example Mirror Image")
