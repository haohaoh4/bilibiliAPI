import data

class video_data:
	def __init__(self):
		self._av = 0
		self.info = data.video_info

	def set_av(self, av):
		self._av = av
		try:
			self.info = data.get_video_info(av)
		except IOError, reason:
			raise IOError("av%s\t%s" % (av, reason))
		return self
