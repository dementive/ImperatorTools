"""
Miscellaneous imperator tools commands
"""

import os
import webbrowser
from typing import Any, Dict, List

import sublime
import sublime_plugin


class ImpMissionNameInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "name"

    def next_input(self, args: List[Any]):
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

    def validate(self, text: str):
        try:
            text = int(text)  # type: ignore
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
    def run(self, edit: sublime.Edit, text: str):  # type: ignore
        self.view.insert(edit, len(self.view), text)


class ImpMissionMakerCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, name: str, event_name: str, mission_count: str):  # type: ignore
        sublime.run_command("new_file")
        window = sublime.active_window()
        event_view = window.active_view()
        if event_view is None:
            return

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
        if loc_view is None:
            return

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
        if mission_view is None:
            return

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

    def input(self, args: Dict[Any, Any]):
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
