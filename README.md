## Python Campbell Logger Client

A library to communicate with Campbell Scientific CR loggers over http. The library was developed on base of the Campbell Scientific Web Interface documentation and has been tested with CR3000 loggers. Other logger types may work. A logger classes is provided to communicate with the logger.

```python
# Sample script to access campbell logger

from campbell.logger import Logger
from datetime import timedelta

l = Logger("http://cr3000")
d
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

## Installation

### Installing on Linux

- Install basic tools for installation  
  `apt-get update`  
  `apt-get install wget gnupg`
- Import the repository key  
  `wget -O - http://www.bayceer.uni-bayreuth.de/repos/apt/conf/bayceer_repo.gpg.key |apt-key add -`
- Add the BayCEER Debian repository  
  `echo "deb http://www.bayceer.uni-bayreuth.de/repos/apt/debian $(lsb_release -c -s) main" | tee /etc/apt/sources.list.d/bayceer.list`
- Update your repository cache  
  `apt-get update`
- Install the package  
  `apt-get install python3-campbell-logger`

### Installation on Windows

```
git clone https://github.com/BayCEER/python-campbell-logger.git
cd python-campbell-logger
python -m pip install .

```

## Authors

- **Oliver Archner** - _Developer_ - [BayCEER, University of Bayreuth](https://www.bayceer.uni-bayreuth.de)

## Version History

### Version 1.2.1, Nov 14, 2025

- Installation changed to pip
- Demo changed
- Package name without release

### Version 1.2, Sept 19, 2022

- Timeout parameter added for all requests

### Version 1.1, June 6, 2022

- New Debian package
- Dropped FrameLogger to reduce dependecies

### Version 1.0, Sep 9, 2020

- Initial release

## License

GNU LESSER GENERAL PUBLIC LICENSE
