# Class to hold css styles for sublime plugin

from sublime import packages_path

class CSS():
	def __init__(self):
		self.default = None
		self.get_styles()

	def get_styles(self):
		default_path = packages_path() + "/ImperatorTools/src/styles/default.css"

		with open(default_path, "r") as file:
			self.default = file.read()
