


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


	def filesize(self, include_units=False):
		m = re.search(r'^(\d+)(.*)$', self._filesize)
		num = int(m.group(1))
		return (num,m.group(2)) if include_units else num


	def _parse_preamble(self):
		# TODO
		pass


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





