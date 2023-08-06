# Gradient-Statsd

Gradient-Statsd is a statsd agent allowing user defined metrics to be graphed within gradient jobs.
When creating a job on the gradient platform a user can specify a set of metrics strings. The user
can then use this package to write the same metrics strings in their jobs. The gradient platform 
will graph these metrics for you. 

# Usage
This client will automatically find the statsd server if it's being used via the gradient platform. We do provide a hostname and port override if you'd like to send metrics to your own statsd server. We require the environment variable `PS_JOB_ID` in order to tag the metrics correctly.

```
from gradient_statsd import Client
c = Client()
c.increment("myCustomMetric", 1)
```


# Publishing to PyPi
Update \_\_version\_\_ in gradient_statsd/\_\_init\_\_.py and execute the following:
```
pip install --user --upgrade twine
python setup.py sdist bdist_wheel
python3 -m twine upload dist/*
rm dist build gradient_statsd.egg-info/ -rf
```
Note that you will have to provide valid PyPi credentials
