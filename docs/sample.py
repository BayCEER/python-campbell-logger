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