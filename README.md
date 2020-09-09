## Python Campbell Logger Client

A library to communicate with campbell CR loggers over http.

```python
from campbell.logger import CrLogger

cr = CrLogger("http://cr3000")

# Gets the 1000 most recent records of table test as a dictionary 
data = cr.dataMostRecent('dl:test',1000)


```


## Authors 
* **Oliver Archner** - *Developer* - [BayCEER, University of Bayreuth](https://www.bayceer.uni-bayreuth.de)

