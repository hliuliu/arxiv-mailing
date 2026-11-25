


import re


class Entry(object):

	def __init__(self, content):
		self._raw_content = content
		self._partition()
		if len(self._partitioned_content)>=3:
			m = re.search(
				r'\(\s*(https.*?)\s*,\s*(.*)\)', 
				self._partitioned_content[-1]
				)
			if m:
				self._link, self._filesize = m.groups()
			else:
				raise Error('Invalid Content Format')
			self._preamble = self._partitioned_content[1]
			self._parse_preamble()
			if len(self._partitioned_content)>3:
				self._abstract = ' '.join(self._partitioned_content[3])
			else:
				self._abstract = None

		else:
			raise Error('Invalid Content Format')


	def __str__(self):
		return '\n'.join(self._raw_content)


	@property
	def abstract(self):
		return self._abstract

	@property
	def link(self):
		return self._link

	@property
	def title(self):
		return self._title
	

	@property
	def comment(self):
		return self._comment
	

	def filesize(self, include_units=False):
		m = re.search(r'^(\d+)(.*)$', self._filesize)
		num = int(m.group(1))
		return (num,m.group(2)) if include_units else num

	@staticmethod
	def _parse_authors(authors):
		#TODO
		return authors # do nothing for now

	def _parse_preamble(self):
		self._title = None
		self._comment = None
		for line in self._preamble:
			if ':' in line:
				key, value = re.split(r':\s*', line, maxsplit=1)
				key = key.strip().lower()
				if key=='title':
					self._title = value.strip()
				if key=='comments':
					self._comment = value.strip()
				if key=='authors':
					self._author_list = self._parse_authors(value)
				# TODO
		


	def _partition(self):
		self._partitioned_content = []
		block = []
		for line in self._raw_content:
			if re.search(r'^\\', line):
				if block: 
					self._partitioned_content.append(block)
				block = []
				self._partitioned_content.append(line)
			else:
				block.append(line)





