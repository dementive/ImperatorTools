"""
Commands for opening and viewing textures in sublime or another program
"""

from typing import List
import sublime
import sublime_plugin

from libjomini.src import (
    JominiShowAllTexturesCommand,
    JominiTextureEventListener,
    JominiToggleAllTexturesCommand,
)


class ImperatorTextureEventListener(
    JominiTextureEventListener, sublime_plugin.EventListener
):
    def on_init(self, views: List[sublime.View]):
        settings = sublime.load_settings("Imperator.sublime-settings")
        self.init(settings)

    def on_post_text_command(self, view: sublime.View, command_name: str, args):
        self._on_post_text_command(view, command_name, args)

    def on_load_async(self, view: sublime.View):
        self._on_load_async(view)


class ImperatorToggleAllTexturesCommand(
    JominiToggleAllTexturesCommand, sublime_plugin.ApplicationCommand
):
    def __init__(self):
        super().__init__()

    def run(self):
        self._run()


class ImperatorShowAllTexturesCommand(
    JominiShowAllTexturesCommand, sublime_plugin.WindowCommand
):
    def run(self):
        print("RUNNNING SHOW FUCKING TEXTGDUJSEIOPTJSEptuj")
        settings = sublime.load_settings("Imperator.sublime-settings")
        self._run(self.window, settings)
