"""
Plugin features related to the game's data system functions.
Data system features that are not coupled to game objects should go here.
"""

from typing import List
import sublime
import sublime_plugin

from libjomini.src import JominiDataSystemEventListener
from .plugin import ImperatorPlugin


class ImperatorDataSystemEventListener(
    JominiDataSystemEventListener, sublime_plugin.EventListener
):
    def __init__(self):
        plugin = ImperatorPlugin()
        super().__init__(plugin.settings, plugin.script_syntax_name, plugin.localization_syntax_name)

    def on_selection_modified_async(self, view):
        super().on_selection_modified_async(view)

    def on_query_completions(
        self, view: sublime.View, prefix: str, locations: List[int]
    ):
        super().on_query_completions(view, prefix, locations)
