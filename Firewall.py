 
# Interface for changing rule on firewall. * Just a draft.

# You can change if you want
# Or inherit this class and call it SNORT_firewall or something.

class Firewall :
	def __init__(self, something=None) :
		# initialize 
		# May be delete all existing rules?
		# May be add default rule?
		# or may be read existing rules?
		# Just to make sure the firewall consistense 
		# Or may be make a connection to firewall if it a remote.

	def addRule(self, rule_file) :
		print("add " + rule_file)

	def deleteRule(self, rule_file) :
		print("delete " + rule_file)

	def enableRule(self, rule_something) :
		print("enable " + rule_something)

	def disableRule(self, rule_something) :
		print("disable " + rule_something)