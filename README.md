# FamilyCalendar
Gathers events and appointment from various calendar apps of multiple persons and generates a picture with all of them

### Goals:
* Integrations:
    * Google Calendar ✓
    * WebUntis ✓
    * Outlook Calendar
    * Apple Calendar
    * ical, ics

* Picture Creation
    * Standalone ✓
    * Magic Mirror Module ~
    * epaper compatible

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
5. finish

##### Setup for use with Magic Mirror:
1. Install https://github.com/roramirez/MMM-ImagesPhotos to /path_to_mm/modules/
2. In config file of MM:
    {
        module: "MMM-ImagesPhotos",
        position: "top_left",
        config: {
            opacity: 1,
            animationSpeed: 0,
            updateInterval: 1500000,
        }
    },
3. Add cronjob:
    crontab -e
    */30 5-23 * * * /usr/bin/python /some_path/create_picture.py --mirror --names --path "/path_to_mm/modules/MMM-ImagesPhotos/uploads/time.png"
