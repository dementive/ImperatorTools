"""
Miscellaneous imperator tools commands
"""

import os
import webbrowser

import sublime, sublime_plugin
import Default.exec


class GotoScriptObjectDefinitionCommand(sublime_plugin.WindowCommand):
    def run(self, path, line):
        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, line, 0)
            self.open_location(self.window, file_path)

    def open_location(self, window, l):
        flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP
        window.open_file(l, flags)


class GotoScriptObjectDefinitionRightCommand(sublime_plugin.WindowCommand):
    def run(self, path, line):
        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, line, 0)
            self.open_location(
                self.window, file_path, side_by_side=True, clear_to_right=True
            )

    def open_location(
        self, window, location, side_by_side=False, replace=False, clear_to_right=False
    ):
        flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP

        if side_by_side:
            flags |= sublime.ADD_TO_SELECTION | sublime.SEMI_TRANSIENT
            if clear_to_right:
                flags |= sublime.CLEAR_TO_RIGHT

        elif replace:
            flags |= sublime.REPLACE_MRU | sublime.SEMI_TRANSIENT

        window.open_file(location, flags)

class ImpMissionNameInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "name"

    def next_input(self, args):
        if "event_name" not in args:
            return ImpEventNameInputHandler()

    def placeholder(self):
        return "Mission Name"


class ImpEventNameInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "event_name"

    def placeholder(self):
        return "Event Name"


class ImpMissionCountInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "mission_count"

    def placeholder(self):
        return "Number of Missions"

    def validate(self, arg):
        try:
            arg = int(arg)
            return True
        except ValueError:
            sublime.set_timeout(
                lambda: sublime.status_message(
                    "Number of Missions must be an Integer!"
                ),
                0,
            )
            return False


class InsertTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.insert(edit, len(self.view), text)


class ImpMissionMakerCommand(sublime_plugin.TextCommand):
    def run(self, edit, name, event_name, mission_count):
        sublime.run_command("new_file")
        window = sublime.active_window()
        event_view = window.active_view()
        event_view.set_name("Events")
        text = "namespace = {}\n\n".format(event_name)
        event_view.run_command("insert_text", {"text": text})
        text = ""
        for i in range(int(mission_count)):
            i += 1
            text += '{event_name}.{i} = {{\n    type = country_event\n\n    title = {event_name}_{i}_title\n    desc = {event_name}_{i}_desc\n    picture = great_library\n\n    option = {{\n        name = "{event_name}_{i}.a"\n        custom_tooltip = {event_name}_{i}_tooltip\n\n    }}\n}}\n'.format(
                event_name=event_name, i=i
            )
        event_view.run_command("insert_text", {"text": text})

        window.run_command("new_file")
        loc_view = window.active_view()
        loc_view.set_encoding("UTF-8 with BOM")
        loc_view.set_name("Localization")
        capital_input = name.replace("_", " ").title()
        text = 'l_english:\n\n{name}:0 "{capital_input}"\n{name}_DESCRIPTION:0 "Mission description"\n{name}_CRITERIA_DESCRIPTION:0 "This mission will be completed when"\n{name}_BUTTON_TOOLTIP:0 ""\n\n#Missions\n\n'.format(
            name=name, capital_input=capital_input
        )
        loc_view.run_command("insert_text", {"text": text})
        for i in range(int(mission_count)):
            i += 1
            text = '{name}_{i}:0 ""\n{name}_DESC:0 ""\n\n'.format(i=i, name=name)
            loc_view.run_command("insert_text", {"text": text})
        text = "\n#Tooltips\n\n\n"
        loc_view.run_command("insert_text", {"text": text})
        text = "\n#Modifiers\n\n\n"
        loc_view.run_command("insert_text", {"text": text})
        text = "\n#Events\n"
        loc_view.run_command("insert_text", {"text": text})
        for i in range(int(mission_count)):
            i += 1
            text = '{event_name}_{i}_title:0 "${name}_task_{i}$"\n{event_name}_{i}_desc:0 ""\n{event_name}_{i}.a:0 ""\n{event_name}_{i}_tooltip:0 "The mission task \'#Y ${name}_task_{i}$#!\' has now been #G Completed#!!"\n\n'.format(
                name=name, i=i, event_name=event_name
            )
            loc_view.run_command("insert_text", {"text": text})

        window.run_command("new_file")
        mission_view = window.active_view()
        mission_view.set_name("Mission Tree")
        text = '{name} = {{\n    header = "mission_image_general"\n    icon = "general_1"\n\n    repeatable = no\n    chance = 1000\n\n    potential = {{\n        NOT = {{ has_variable = mission_cooldown_var }}\n    }}\n\n    abort = {{}}\n    on_start = {{\n        start_mission_ai_effect = yes\n    }}\n    on_abort = {{\n        custom_tooltip = general_mission_cooldown_tt\n        set_variable = {{\n            name = mission_cooldown_var\n            days = 7300\n        }}\n    }}\n    on_completion = {{}}'.format(
            name=name
        )
        mission_view.run_command("insert_text", {"text": text})
        for i in range(int(mission_count)):
            i += 1
            text = '\n    {name}_task_{i} = {{\n        icon = "task_political"\n        allow = {{}}\n        on_completion = {{\n            trigger_event = {event_name}.{i}\n            show_as_tooltip = {{\n\n            }}\n        }}\n    }}'.format(
                name=name, i=i, event_name=event_name
            )
            mission_view.run_command("insert_text", {"text": text})
        mission_view.run_command("insert_text", {"text": "\n}"})

    def input(self, args):
        if "name" not in args:
            return ImpMissionNameInputHandler()
        elif "event_name" not in args:
            return ImpEventNameInputHandler()
        elif "mission_count" not in args:
            return ImpMissionCountInputHandler()

    def input_description(self):
        return "Mission Creator"


class ImperatorWikiSearchCommand(sublime_plugin.WindowCommand):
    def run(self):
        webbrowser.open_new_tab("https://imperator.paradoxwikis.com/Imperator_Wiki")


class ImperatorLocalizationGuideCommand(sublime_plugin.WindowCommand):
    def run(self):
        webbrowser.open_new_tab(
            "https://docs.google.com/document/d/1JZ-_oxhAikNGLw-6HnVDgyeYEbvPmgbdsLCAcbQ0Da0/edit"
        )


class ImperatorModdingIndexCommand(sublime_plugin.WindowCommand):
    def run(self):
        webbrowser.open_new_tab(
            "https://forum.paradoxplaza.com/forum/threads/imperator-modding-guide-index.1274242/"
        )


class ImpClearImageCacheCommand(sublime_plugin.WindowCommand):
    def run(self):
        dir_name = sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/"
        ld = os.listdir(dir_name)
        for item in ld:
            if item.endswith(".png"):
                os.remove(os.path.join(dir_name, item))
        sublime.status_message("Cleared Image Cache")


class QuietExecuteCommand(sublime_plugin.WindowCommand):
    """
    Simple version of Default.exec.py that only runs the process and shows no panel or messages
    """

    def __init__(self, window):
        super().__init__(window)
        self.proc = None

    def run(
        self,
        cmd=None,
        shell_cmd=None,
        working_dir="",
        encoding="utf-8",
        env={},
        **kwargs,
    ):
        self.encoding = encoding
        merged_env = env.copy()
        if self.window.active_view():
            user_env = self.window.active_view().settings().get("build_env")
            if user_env:
                merged_env.update(user_env)

        if working_dir != "":
            os.chdir(working_dir)

        try:
            # Run process
            self.proc = Default.exec.AsyncProcess(
                cmd, shell_cmd, merged_env, self, **kwargs
            )
            self.proc.start()
        except Exception as e:
            sublime.status_message("Build error")

    def on_data(self, proc, data):
        return

    def on_finished(self, proc):
        return
