## Python Campbell Logger Client

A library to communicate with Campbell Scientific CR loggers over http. The library was developed on base of the Campbell Scientific Web Interface documentation and has been tested with CR3000 loggers. Other logger types may work. Two main logger classes are provided to communicate with the logger.

### 1. Class Logger
Base class to communicate with the logger. Sample usage:
```python
from campbell.logger import Logger
from datetime import timedelta

l = Logger("http://cr3000")

# Get all table uris
tabs = l.getTableUris()

# Get the 10 most recent records of the first table as a dictionary
data = l.dataMostRecent(tabs[0],10)

# Get all records of the first table since a specific time  
clock = l.getClock()
data = l.dataSinceTime(tabs[0], clock - timedelta(seconds=120))

# Get all records of the first table with record nr >= 10
data = l.dataSinceRecord(tabs[0],10)

# Get all records stored since the last 2 minutes 
data = l.dataBackfill(tabs[0],120)
```

### 2. Class FrameLogger
Extended version of class campbell.Logger. Provides query methods returning values of  type [Pandas DataFrame](https://pandas.pydata.org/docs/reference/frame.html). Those methods are named with a frame prefix.

Sample usage:
```python
from campbell.logger import FrameLogger
l = FrameLogger("http://cr3000",timeZone="UTC")
# Gets all records stored since 120 secs as a Pandas DataFrame
data = l.frameBackfill('dl:test',120)
```

## Installation 
Install the package by a git clone request followed by a run of setup.py:
``` 
git clone https://github.com/BayCEER/python-campbell-logger.git
cd python-campbell-logger
python setup.py install
```

## Authors 
* **Oliver Archner** - *Developer* - [BayCEER, University of Bayreuth](https://www.bayceer.uni-bayreuth.de)

## Version History 

### Version 1.0, Sep 9, 2020
- Initial release 

## License
GNU LESSER GENERAL PUBLIC LICENSE
