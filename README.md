# Timely

Track how you spend your time.

```
$ ./manage.py -h
usage: manage.py [-h] [--list] [--current] [--add] [--stop] [--name NAME]

Track your time efficiently

optional arguments:
  -h, --help   show this help message and exit
  --list       Lists out all the activity for the day
  --current    Current task
  --add        Add a new task
  --stop       stop all running tasks
  --name NAME  Activity name
```

Run configure script to add cron job, which resets the log at the end of the day.
