
import os, re

from datetime import datetime


_get_preprints_filename = lambda dt: os.path.join('preprints', f'{dt.month}-{dt.day}-{dt.year}')


class Parser(object):

	def __init__(self):
		self._content = []
		self._unread_dates = []
		self._curline = 0

	
	def _read_content(self, dt):
		f = _get_preprints_filename(dt)
		if not os.path.exists(f):
			raise OSError(f"the file '{f}' is not found.")
		with open(f,'r') as f:
			self._content.extend(f.readlines())


	def feed(self, day=None, month=None, year=None, dt=None):
		'''
		dt: datetime instance
		if dt is specified, the day, month, year arguments are ignored
		otherwise, if any of day, month, year are not specified,
		they will default according to the current local time.
		'''
		if dt is None:
			today = datetime.today()
			dt = datetime(
				day = today.day if day is None else day,
				month = today.month if month is None else month,
				year = today.year if year is None else year
				)
		self._unread_dates.append(dt)
		'''
		if self._curline>=len(self._content):
			self._content = []
			self._curline = 0 
			if not self._unread_dates:
				self._read_content(dt)
			else:
				self._read_content(self._unread_dates.pop(0))
				self._unread_dates.append(dt)
		else:
			self._unread_dates.append(dt)
		'''

	def fetch_next_entry(self):
		while 1:
			if self._curline>=len(self._content):
				self._content = []
				self._curline = 0 
				if not self._unread_dates:
					return None
				self._read_content(self._unread_dates.pop(0))
			entry = []
			while self._curline<len(self._content):
				line = self._content[self._curline].strip()
				if not line:
					self._curline+=1
					continue
				if re.search('^(-|%)*$', line):
					self._curline+=1
					return entry
				else:
					entry.append(line)
				self._curline+=1






