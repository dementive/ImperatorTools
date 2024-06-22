import sublime

from libjomini.src import JominiPlugin
from .game_object_manager import GameObjectManager

manager = GameObjectManager()

class ImperatorPlugin(JominiPlugin):

	@property
	def name(self):
		return "ImperatorTools"

	@property
	def settings(self):
		return sublime.load_settings("Imperator.sublime-settings")

	@property
	def script_syntax_name(self):
		return "Imperator Script"

	@property
	def localization_syntax_name(self):
		return "Imperator Localization"
