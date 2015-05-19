
import dateutil.tz
import datetime
import time

class DateUtil:
	def __init__(self, x = 1):
		self.curr_utc_dt = datetime.datetime.utcnow()
		self.prev_day_utc_dt = self.curr_utc_dt - datetime.timedelta(x)

	def get_pretty_ymd_str(self):
		local_tm = time.localtime()
		return str(local_tm.tm_year) + '.' + str(local_tm.tm_mon) + '.' + str(local_tm.tm_mday) + \
				' ' + str(local_tm.tm_hour) + ':' + str(local_tm.tm_min) + ':' + str(local_tm.tm_sec)

	def get_utc_ymd_str(self):
		return str(self.curr_utc_dt.year) + str(self.curr_utc_dt.month).zfill(2) + str(self.curr_utc_dt.day).zfill(2)

	def get_utc_prev_day_ymd_str(self):
		return str(self.prev_day_utc_dt.year) + str(self.prev_day_utc_dt.month).zfill(2) + str(self.prev_day_utc_dt.day).zfill(2)

	def get_utc_ymd_str_pretty(self):
		return str(self.curr_utc_dt.day).zfill(2) + '.' + str(self.curr_utc_dt.month).zfill(2) + '.' + str(self.curr_utc_dt.year).zfill(2)

	def get_utc_prev_day_ymd_str_pretty(self):
		return str(self.prev_day_utc_dt.day).zfill(2) + '.' + str(self.prev_day_utc_dt.month).zfill(2) + '.' + str(self.curr_utc_dt.year).zfill(2)		

	def get_left_hours_in_curr_day(self):
		return int(24 - self.curr_utc_dt.hour)

	def get_local_offset_from_utc(self):
		localtz = dateutil.tz.tzlocal()
		localoffset = localtz.utcoffset(datetime.datetime.now(localtz))
		return localoffset.total_seconds() / 3600

