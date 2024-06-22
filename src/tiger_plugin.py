"""
All the code for handling the integration of imperator-tiger into the plugin.
"""

import sublime
import sublime_plugin

from libjomini.src import (
    JominiTigerEventListener,
    JominiTigerOutputCommand,
    JominiExecuteTigerCommand,
    JominiRunTigerCommand,
    TigerInputHandler,
)


class ImperatorTigerEventListener(
    JominiTigerEventListener, sublime_plugin.EventListener
):
    def __init__(self):
        super().__init__("ImperatorTools")

    def on_load_async(self, view):
        settings = sublime.load_settings("Imperator.sublime-settings")
        self._on_load_async(view, settings)

    def on_hover(self, view, point, hover_zone):
        settings = sublime.load_settings("Imperator.sublime-settings")
        self._on_hover(view, point, hover_zone, settings)


class ImperatorTigerOutputCommand(
    JominiTigerOutputCommand, sublime_plugin.WindowCommand
):
    def __init__(self, window):
        self.window = window
        super().__init__(
            "ImperatorTools",
            sublime.load_settings("Imperator.sublime-settings"),
            "Imperator Tiger",
            self.window,
        )

    def run(self, view_type):  # type: ignore
        self._run(view_type)

    def input(self, args):
        if "view_type" not in args:
            return TigerInputHandler()


class ExecuteTigerCommand(JominiExecuteTigerCommand, sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window
        super().__init__("ImperatorTools", "imperator-tiger", self.window)

    def run(
        self,
        cmd=None,
        shell_cmd=None,
        working_dir="",
        encoding="utf-8",
        env={},
        word_wrap=True,
        syntax="Packages/JSON/JSON.sublime-syntax",
        **kwargs,
    ):
        self._run(
            cmd,
            shell_cmd,
            working_dir,
            encoding,
            env,
            word_wrap,
            syntax,
        )


class RunTigerCommand(JominiRunTigerCommand, sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window
        super().__init__(sublime.load_settings("Imperator.sublime-settings"))

    def run(self):
        self._run()


class EditTigerConfigCommand(sublime_plugin.WindowCommand):
    def run(self):
        conf_file = (
            sublime.packages_path()
            + "/ImperatorTools/ImperatorTiger/imperator-tiger.conf"
        )
        view = self.window.open_file(conf_file)
        view.assign_syntax("scope:source.ruby")
