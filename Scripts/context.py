from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from config import TZ_NAME, DATE_FMT_API, DAYS_OFFSET

@dataclass(frozen=True)
class RunContext:
    start_utc_dt: datetime
    end_utc_dt: datetime
    start_utc_time: str
    day_label: str

def _compute() -> RunContext:
    tz = ZoneInfo(TZ_NAME)
    base = datetime.now(tz) - timedelta(days=DAYS_OFFSET)
    start_dt = base.replace(hour=0, minute=0, second=0, microsecond=0)
    end_dt   = base.replace(hour=23, minute=59, second=59, microsecond=0)
    return RunContext(
        start_utc_dt=start_dt,
        end_utc_dt=end_dt,
        start_utc_time=start_dt.strftime(DATE_FMT_API),
        day_label=str(start_dt.date()),
    )

#this line runs the function _compute(), and stores result in ctx. Use in other scripts from context import ctx
ctx: RunContext = _compute()


#any script can now use these directly:
# ctx.start_utc_dt
# ctx.end_utc_dt
# ctx.start_utc_time
# ctx.day_label
