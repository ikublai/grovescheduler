import json
import logging
import unittest
from schedule import Schedule
from datetime import datetime

logger = logging.getLogger(__name__)


class SchedulerTest(unittest.TestCase):
    """
    Test cases for various cron schedule.
    Not all of the 7 types are tested. I pick a few for these tests but would do all and more for production
    """
    def setUp(self):
        self.schedul_data = {}

        with open('tests/fixtures.txt') as json_scheduler:
            raw_data = json_scheduler.read()
            self.schedule_data = json.loads(raw_data)['data']

        print(self.schedule_data)

    def test_load_schedule(self):
        self.assertEqual(7, len(self.schedule_data))

    def test_schedules_for_task_0(self):
        task_schedule = self.schedule_data[0]
        self.assertEqual('0', task_schedule['id'])
        self.assertEqual('task', task_schedule['type'])
        self.assertEqual('0 7 14 3 *', task_schedule['attributes']['cron'])
        self.assertEqual('Repot Sunny the Succulent', task_schedule['attributes']['name'])

        schedule = Schedule(task_schedule['id'],
                            task_schedule['attributes']['name'],
                            task_schedule['type'],
                            task_schedule['attributes']['cron'])

        cron_schedule = schedule.normalize_cron(task_schedule['attributes']['cron'])
        self.assertEqual('0 7 14 3 *', cron_schedule)

        start_time = datetime(2018, 3, 13, 7, 0)
        schedules = schedule.get_schedules(start_time, 3, 24)
        self.assertEqual(1, len(schedules))
        self.assertEqual(datetime(2018, 3, 14, 7, 0), schedules[0][0])

    def test_schedules_for_task_1(self):
        task_schedule = self.schedule_data[1]
        self.assertEqual('1', task_schedule['id'])
        self.assertEqual('task', task_schedule['type'])
        self.assertEqual('0 18 20 * *', task_schedule['attributes']['cron'])
        self.assertEqual('Pick up Grove order from mailroom', task_schedule['attributes']['name'])

        schedule = Schedule(task_schedule['id'],
                            task_schedule['attributes']['name'],
                            task_schedule['type'],
                            task_schedule['attributes']['cron'])

        cron_schedule = schedule.normalize_cron(task_schedule['attributes']['cron'])
        self.assertEqual('0 18 20 * *', cron_schedule)

        start_time = datetime(2018, 8, 20)
        schedules = schedule.get_schedules(start_time)
        self.assertEqual(1, len(schedules))
        self.assertEqual(datetime(2018, 8, 20, 18, 0), schedules[0][0])

    def test_schedules_for_task_4(self):
        task_schedule = self.schedule_data[4]
        self.assertEqual('4', task_schedule['id'])
        self.assertEqual('task', task_schedule['type'])
        self.assertEqual('0 14 * *', task_schedule['attributes']['cron'])
        self.assertEqual("Farmer's Market", task_schedule['attributes']['name'])

        schedule = Schedule(task_schedule['id'],
                            task_schedule['attributes']['name'],
                            task_schedule['type'],
                            task_schedule['attributes']['cron'])

        cron_schedule = schedule.normalize_cron(task_schedule['attributes']['cron'])
        # assert normalize to 6 sections
        self.assertEqual('0 14 * * *', cron_schedule)

        start_time = datetime(2018, 8, 6)
        schedules = schedule.get_schedules(start_time)
        print('Start time {} schedules {}'.format(start_time, schedules))
        self.assertEqual(1, len(schedules))
        self.assertEqual(datetime(2018, 8, 6, 14, 0), schedules[0][0])

    def tearDown(self):
        pass