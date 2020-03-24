
import PolicyParser


class PolicyServer :
	def __init__(self, config = None) :
		self.config = config

	def start(self) :
		print("Policy Server started")
		print(self.config)
		"""
		Loop and call poll/or just start and wait for status change or do both.
		Or use framework.
		"""

	def poll(self) :
		pass

	def signal(self, iot_status_changes) :
		print("handle status changes");



if __name__ == "__main__" :
	config = PolicyParser.from_file("fileName")
	server = policyServer(config)
	server.start()


