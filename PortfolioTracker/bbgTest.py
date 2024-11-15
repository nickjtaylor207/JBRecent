from blp import blp
from datetime import datetime, timedelta

bquery = blp.BlpQuery().start()


start_datetime = datetime.now() - timedelta(days=1)  # Example: 1 day before today
end_datetime = datetime.now()

data = bquery.bdib(
    "EURUSD Curncy",
    event_type="TRADE",
    interval=60,
    start_datetime=start_datetime, # Different date format
    end_datetime=end_datetime, # Different date format
)

data























