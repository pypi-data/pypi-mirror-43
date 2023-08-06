# autoformat
Automatic, range-aware formatting of time-axis labels for timeseries data using matplotlib.

This package is supported for Python 3 only. This project works for time ranges on the order of milliseconds or millenia, and produces a decent-looking result with a few lines:

```python
from autoformat import autoformat

autoformat.scale(start_date, end_date)
# your matplotlib plotting code here

```

## Installation

```
pip install autoformat 
```

## Worked example

```python
import math
import datetime
import matplotlib.pyplot as plt
from autoformat import autoformat

def get_test_data():
    times = []
    data = []
    start_time = datetime.datetime.utcnow()
    for x in range(0,20):
        next_time = start_time + datetime.timedelta(hours=x)
        times.append(next_time)
        data.append(math.cos(x / 10.0))
    return times, data

def plot(filename):
    times, data = get_test_data()
    start = times[0]
    end = times[len(times)-1]
    autoformat.scale(start, end)
    plt.plot(times, data)
    plt.savefig(filename)
    plt.close()

plot("sample.png")
```

![](examples/sample.png?raw=true)
