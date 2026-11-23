


import re


class Entry(object):

	def __init__(self, content):
		self._raw_content = content
		self._partition()
		if self._partitioned_content:
			m = re.search(
				r'\(\s*(https.*?)\s*,\s*(.*)\)', 
				self._partitioned_content[-1]
				)
			if m:
				self._link, self._filesize = m.groups()


	def __str__(self):
		return '\n'.join(self._raw_content)


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





