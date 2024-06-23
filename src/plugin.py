import sublime

from JominiTools.src import JominiPlugin


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
