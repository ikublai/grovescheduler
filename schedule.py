from datetime import datetime, timedelta
from croniter import croniter

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


class Schedule(object):
    """
    Class to parse cron schedule and create the reschedules
    for the given period (default to 3 hours prior and next 24 hours)
    """
    def __init__(self, id, name, type, schedule_cron):
        self.id = id
        self.name = name
        self.type = type
        self.schedule_cron = self.normalize_cron(schedule_cron)
        self.schedules = []

    def normalize_cron(self, schedule_cron):
        """
        Normalize a cron schedule to always have 5 parts
        :return:
        """
        items = schedule_cron.split(' ')
        if len(items) <= 4:
            missing_schedule = ' *' * (5-len(items))
            schedule_cron += missing_schedule
        return schedule_cron

    def get_schedules(self, base_time, previous_hours=3, next_hours=24):
        """
        Get the schedules previous_hours hours before and next next_hours hours
        :param base_time: the start schedule date time
        :param previous_hours: Include schedule previous_hours
        :param next_hours: Include schedules next_hours
        :return: List of schedules
        """
        start_time = base_time - timedelta(hours=previous_hours)
        end_time = base_time + timedelta(hours=next_hours)
        next_scheduled_datetime = start_time

        base_time = start_time.replace(microsecond=0)

        iter = croniter(self.schedule_cron, base_time)
        count = 0

        while next_scheduled_datetime <= end_time:
            next_scheduled_datetime = iter.get_next(datetime)
            if next_scheduled_datetime <= end_time:
                self.schedules.append((next_scheduled_datetime, self.id, self.name))
                #print('Date: {}, Task: {}, name: {}'.format(next_scheduled_datetime, self.id, self.name))
                count += 1

        print('Schedules for task {} are {}'.format(self.id, self.schedules))
        return self.schedules

    def __str__(self):
        return 'Task {}, name {}, cron {}, schedule {}'.format(self.id, self.name,
                                                               self.schedule_cron, self.schedules)