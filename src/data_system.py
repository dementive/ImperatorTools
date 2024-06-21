"""
Plugin features related to the game's data system functions.
Data system features that are not coupled to game objects should go here.
"""

from typing import List
import sublime, sublime_plugin
from JominiTools.src import JominiDataSystemEventListener

class ImperatorDataSystemEventListener(JominiDataSystemEventListener, sublime_plugin.EventListener):
    def __init__(self):
        settings = sublime.load_settings("Imperator Syntax.sublime-settings")
        super().__init__(settings)

    def on_selection_modified_async(self, view):
        self._on_selection_modified_async(view)

    def on_query_completions( self, view: sublime.View, prefix: str, locations: List[int]):
        self._on_query_completions(view, prefix, locations)
