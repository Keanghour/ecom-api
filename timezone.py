from datetime import datetime
import pytz

# Set the timezone to UTC+7 (Bangkok, for example)
tz = pytz.timezone('Asia/Bangkok')
utc_time = datetime.now(pytz.utc)  
local_time = utc_time.astimezone(tz)
print(local_time)



