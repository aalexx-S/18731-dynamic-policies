
# redesign if you think it doesn't make sense.
class Policy :
	def __init__(self, rule, condion) :
		self.rule = rule
		self.condion = condion

	def eavlCond(self) :
		"""
		evaluate codition
		- read variable from DB
		- evaluate conditon
		"""
		return True # or False

	def active(self) :
		# active rule on Firewall (call Firewall object?)
		pass

	def deactive(self) :
		pass

	def apply(self) :
		if self.eavlCond() :
			self.active()
		else
			self.deactive()