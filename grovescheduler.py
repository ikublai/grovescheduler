# Program to read cron schedule
# Parse the cron and create schedules
# Display and also show notification
# for python, use queue?

import json
import ssl
import time
from collections import deque
from datetime import datetime, timedelta


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from schedule import Schedule


def read_schedules_from_url(schedule_url):
    """
    Get the task schedules from the provided URL
    :param schedule_url: URL to get the schedules which is in JSON format
    :return: schedule JSON
    """
    print('Loading data from URL {}'.format(schedule_url))
    # temp work around for ssl issue
    context = ssl._create_unverified_context()

    response = urlopen(schedule_url, context=context)
    schedule_data = json.loads(response.read())

    return schedule_data


def read_schedule(schedule_file):
    """
    Read the schedule JSON
    :param schedule_file: filename
    :return: schedule JSON
    """
    print('Loading data from file {}'.format(schedule_file))
    with open(schedule_file) as json_scheduler:
        raw_data = json_scheduler.read()
        schedule_data = json.loads(raw_data)

    return schedule_data


def get_schedules(schedule_data):
    """
    Parse the schedule data in JSON format and return the list of schedules
    :param schedule_data:
    :return:
    """
    schedules = []

    for each_schedule_data in schedule_data['data']:
        id = each_schedule_data['id']
        schedule_type = each_schedule_data['type']
        cron = each_schedule_data['attributes']['cron']
        name = each_schedule_data['attributes']['name']
        schedule = Schedule(id, name, schedule_type, cron)
        schedules.append(schedule)

    return schedules


def display_all_schedules_and_show_notification(previous_hours=3, next_hours=24):
    """
    Helper method to get the schedules and placed them on notification queue
    """
    all_schedules = []

    # schedule_data = read_schedule('schedule.json')
    schedule_data = read_schedules_from_url('https://scheduler-challenge.herokuapp.com/schedule')
    schedules = get_schedules(schedule_data)

    start_time = datetime.now()
    for schedule in schedules:
        # create schedule start 3 hours before and 24 hours after
        # store tuple of schedule name and starttime
        all_schedules.extend((schedule.get_schedules(start_time, previous_hours, next_hours)))

    print('Printing schedules...')
    # create a queue to store the sorted schedule by datetime
    schedule_queue = deque()
    for item in sorted(all_schedules, key=lambda x:x[0]):
        schedule_queue.append(item)
        print('Schedule {}, Task {} {}'.format(item[0], item[1], item[2]))

    # now check for the schedules and add those that are coming up to the notification list
    # Assumption: only one schedule is placed at a time.
    if len(all_schedules) > 0:
        start_notification = datetime.now()
        current_time = start_notification
        # stop after next amount of hours
        end_notification = datetime.now() + timedelta(hours=next_hours)
        print('Start loading notification: ', start_notification)

        while current_time <= end_notification:
            current_schedule = schedule_queue.popleft()
            current_time = datetime.now()
            print('Processing schedule {}'.format(current_schedule))

            if current_schedule[0] < start_notification:
                # ignore schedule that has passed
                print('Skipping schedule {} for task {}'.format(current_schedule[0], current_schedule[1]))
                continue
            else:
                print('Placing for notification {}'.format(current_schedule))
                sleep_amount_in_seconds = (current_schedule[0] - start_notification).seconds
                time.sleep(sleep_amount_in_seconds)
                print('** Notification: {}. Task {} is due'.format(current_schedule[0], current_schedule[2]))


if __name__ == '__main__':
    display_all_schedules_and_show_notification()