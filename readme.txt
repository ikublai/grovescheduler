Grove scheduler
===============

# To run

* Run pip install croniter
* Run python grovescheduler.py. Croniter works with in python 2.7 and 3.x the pip install may only work for 2.7.x version on mac
* Run for test cases pytest tests/test_grovesscheduler.py

# Assumptions

* All schedules have 5 sections, if there are less than that, pad " *" for each missing one
* No schedules from the different tasks overlap. Hence, the simplistic while loop and timer concept is sufficient
* The croniter version works for 2.7