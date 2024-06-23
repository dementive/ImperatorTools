"""
The main event listener for the plugin, this is where most of the plugin features actually happen.
The init function of the event listener is treated as the main entry point for the plugin.
"""

import os
import re
import threading
import time
from typing import List, Tuple, Union

import sublime
import sublime_plugin

from JominiTools.src import encoding_check
from .autocomplete import AutoComplete
from .game_data import ImperatorGameData
from .game_objects import write_data_to_syntax
from .game_object_manager import GameObjectManager
from .imperator_objects import *
from .plugin import ImperatorPlugin
from JominiTools.src.jomini_objects import *
from JominiTools.src import (
    ScopeMatch,
    get_file_name,
    get_syntax_name,
    is_file_in_directory,
    GameObjectBase,
    PdxScriptObject,
    Hover,
    JominiEventListener,
)


class ImperatorEventListener(
    Hover,
    AutoComplete,
    ScopeMatch,
    JominiEventListener,
    sublime_plugin.EventListener,
):
    write_data_to_syntax = write_data_to_syntax

    def on_init(self, views):
        self.init(ImperatorPlugin())

    def init_game_object_manager(self):
        self.manager = GameObjectManager()

    def init_game_data(self):
        self.game_data = ImperatorGameData()

    def create_all_game_objects(self):
        t0 = time.time()

        def load_first():
            self.game_objects[self.manager.modifier.name] = Modifier()

        def load_second():
            self.game_objects[self.manager.mission_task.name] = MissionTask()
            self.game_objects[self.manager.subject_type.name] = SubjectType()
            self.game_objects[self.manager.diplo_stance.name] = DiplomaticStance()
            self.game_objects[self.manager.province_rank.name] = ProvinceRank()

        def load_third():
            self.game_objects[self.manager.script_value.name] = ScriptValue(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.heritage.name] = Heritage()
            self.game_objects[self.manager.mil_tradition.name] = MilitaryTradition()
            self.game_objects[self.manager.named_colors.name] = NamedColor(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.mission.name] = Mission()
            self.game_objects[self.manager.price.name] = Price()
            self.game_objects[self.manager.death_reason.name] = DeathReason()
            self.game_objects[self.manager.ambition.name] = Ambition()
            self.game_objects[self.manager.religion.name] = Religion()
            self.game_objects[self.manager.office.name] = Office()
            self.game_objects[self.manager.unit.name] = Unit()
            self.game_objects[self.manager.party.name] = Party()

        def load_fourth():
            self.game_objects[self.manager.deity.name] = Deity()
            self.game_objects[self.manager.custom_loc.name] = CustomLoc()
            self.game_objects[self.manager.opinion.name] = Opinion()
            self.game_objects[self.manager.culture.name] = Culture()
            self.game_objects[self.manager.event_pic.name] = EventPicture()
            self.game_objects[self.manager.trait.name] = Trait()
            self.game_objects[self.manager.law.name] = Law()
            self.game_objects[self.manager.scripted_gui.name] = ScriptedGui(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.culture_group.name] = CultureGroup()
            self.game_objects[self.manager.scripted_modifier.name] = ScriptedModifier(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.building.name] = Building()
            self.game_objects[self.manager.terrain.name] = Terrain()
            self.game_objects[self.manager.econ_policy.name] = EconomicPolicy()
            self.game_objects[self.manager.tech_table.name] = TechTable()
            self.game_objects[self.manager.war_goal.name] = Wargoal()

        def load_fifth():
            self.game_objects[self.manager.loyalty.name] = Loyalty()
            self.game_objects[self.manager.area.name] = Area()
            self.game_objects[self.manager.scripted_effect.name] = ScriptedEffect(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.invention.name] = Invention()
            self.game_objects[self.manager.scripted_trigger.name] = ScriptedTrigger(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.event_theme.name] = EventTheme()
            self.game_objects[self.manager.region.name] = Region()
            self.game_objects[self.manager.levy_template.name] = LevyTemplate()
            self.game_objects[self.manager.trade_good.name] = TradeGood()
            self.game_objects[self.manager.idea.name] = Idea()
            self.game_objects[self.manager.legion_distinction.name] = (
                LegionDistinction()
            )
            self.game_objects[self.manager.government.name] = Government()
            self.game_objects[self.manager.governor_policy.name] = GovernorPolicy()
            self.game_objects[self.manager.scripted_list_effects.name] = ScriptedList(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.scripted_list_triggers.name] = ScriptedList(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.pop.name] = Pop()

            tri_list = []
            for obj in self.game_objects["scripted_list_triggers"]:
                tri_list.append(PdxScriptObject("any_" + obj.key, obj.path, obj.line))
            self.game_objects["scripted_list_triggers"].clear()
            for i in tri_list:
                self.game_objects["scripted_list_triggers"].add(i)

            ef_list = []
            for obj in self.game_objects["scripted_list_effects"]:
                ef_list.append(PdxScriptObject(f"random_{obj.key}", obj.path, obj.line))
                ef_list.append(PdxScriptObject(f"every_{obj.key}", obj.path, obj.line))
                ef_list.append(
                    PdxScriptObject(f"ordered_{obj.key}", obj.path, obj.line)
                )
            self.game_objects["scripted_list_effects"].clear()

            for i in ef_list:
                self.game_objects["scripted_list_effects"].add(i)
            for i in self.game_objects["scripted_list_effects"].keys():
                self.game_data.game_effects[i] = "Scripted list effect"
            for i in self.game_objects["scripted_list_triggers"].keys():
                self.game_data.game_triggers[i] = "Scripted list trigger"

        thread1 = threading.Thread(target=load_first)
        thread2 = threading.Thread(target=load_second)
        thread3 = threading.Thread(target=load_third)
        thread4 = threading.Thread(target=load_fourth)
        thread5 = threading.Thread(target=load_fifth)
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()

        t1 = time.time()
        print("Time to load Imperator Rome objects: {:.3f} seconds".format(t1 - t0))

    def on_deactivated_async(self, view):
        super().on_deactivated_async(view)

    def on_activated_async(self, view):
        super().on_activated_async(view)

    def on_query_completions(
        self, view: sublime.View, prefix: str, locations: List[int]
    ) -> Union[
        None,
        List[Union[str, Tuple[str, str], sublime.CompletionItem]],
        Tuple[
            List[Union[str, Tuple[str, str], sublime.CompletionItem]],
            sublime.AutoCompleteFlags,
        ],
        sublime.CompletionList,
    ]:
        if not view:
            return None

        syntax_name = get_syntax_name(view)

        if not self.plugin.valid_syntax(syntax_name):
            return None

        if self.plugin.is_data_system_syntax(syntax_name):
            for flag, completion in self.game_data.data_system_completion_flag_pairs:
                completion_list = self.create_completion_list(flag, completion)  # type: ignore
                if completion_list is not None:
                    return completion_list
            return  # Don't need to check anything else for data system

        for flag, completion in self.game_data.completion_flag_pairs:
            completion_list = self.create_completion_list(flag, completion)  # type: ignore
            if completion_list is not None:
                return completion_list

        fname = get_file_name(view)
        if not fname:
            return

        if "script_values" in fname:
            e_list = []
            for i in self.game_data.game_effects:
                e_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=self.game_data.game_effects[i].split("<br>")[0],
                    )
                )
            t_list = []
            for i in self.game_data.game_triggers:
                t_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=self.game_data.game_triggers[i].split("<br>")[0],
                    )
                )

            return sublime.CompletionList(e_list + t_list)
        if "common/prices" in fname:
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion=key + " = ${1:5}",
                        completion_format=sublime.COMPLETION_FORMAT_SNIPPET,
                        kind=(sublime.KIND_ID_NAVIGATION, "P", "Price"),
                        annotation=" " + key.replace("_", " ").title(),
                        details=self.game_data.PricesDict[key],
                    )
                    for key in sorted(self.game_data.PricesDict)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if (
            self.trigger_field
            or "scripted_triggers" in fname
            or "scripted_modifiers" in fname
        ):
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=self.game_data.game_triggers[key].split("<br>")[0],
                    )
                    for key in sorted(self.game_data.game_triggers)
                ]
            )
        if self.mtth_field:
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=self.game_data.MtthList[key].split("<br>")[0],
                    )
                    for key in sorted(self.game_data.MtthList)
                ]
            )
        if self.effect_field or "scripted_effects" in fname:
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=self.game_data.game_effects[key].split("<br>")[0],
                    )
                    for key in sorted(self.game_data.game_effects)
                ]
            )
        if self.modifier_field or re.search(
            r"common\\(modifiers|traits|buildings|governor_policies|trade_goods)", fname
        ):
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "M", "Modifier"),
                        details=self.game_data.game_modifiers[key],
                        annotation=self.game_data.game_modifiers[key].replace(
                            "Category: ", ""
                        ),
                    )
                    for key in sorted(self.game_data.game_modifiers)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        return None

    def on_selection_modified_async(self, view: sublime.View):
        if not view:
            return

        syntax_name = get_syntax_name(view)

        if not self.plugin.valid_syntax(syntax_name):
            return

        if not self.plugin.is_data_system_syntax(syntax_name):
            self.simple_scope_match(view)

        # Only do when there is 1 selections, doens't make sense with multiple selections
        if len(view.sel()) == 1:
            point = view.sel()[0].a
            if (self.plugin.is_data_system_syntax(syntax_name)) and view.substr(
                point
            ) == "'":
                for i in self.game_data.data_system_completion_functions:
                    function_start = point - len(i[1] + "('")
                    if view.substr(view.word(function_start)) == i[1]:
                        setattr(self, i[0], True)
                        view.run_command("auto_complete")
                        return
            self.check_for_simple_completions(view, point)
            self.check_for_complex_completions(view, point)

    def check_for_simple_completions(self, view: sublime.View, point: int):
        """
        Check if the current cursor position should trigger a autocompletion item
        this is for simple declarations like: remove_building = CursorHere
        """
        self.reset_shown()

        if view.substr(point) == "=":
            return

        line = view.substr(view.line(point))

        for patterns, flag in self.game_data.simple_completion_pattern_flag_pairs:
            if self.check_for_patterns_and_set_flag(patterns, flag, view, line, point):
                return

        for pattern, flag in self.game_data.simple_completion_scope_pattern_flag_pairs:
            self.check_pattern_and_set_flag(pattern, flag, view, line, point)

    def on_hover(self, view: sublime.View, point: int, hover_zone: sublime.HoverZone):
        if not view:
            return

        syntax_name = get_syntax_name(view)

        if not self.plugin.valid_syntax(syntax_name):
            return

        # Do everything that requires fetching GameObjects in non-blocking thread
        hover_objects = []
        if self.plugin.script_syntax_name == syntax_name:
            hover_objects = self.game_data.script_hover_objects

        if self.plugin.is_data_system_syntax(syntax_name):
            hover_objects = self.game_data.data_system_hover_objects

        sublime.set_timeout_async(
            lambda: self.do_hover_async(view, point, hover_objects), 0
        )

        if syntax_name != self.plugin.script_syntax_name:
            # For yml only the saved scopes/variables/game objects get hover
            return

        if self.settings.get("DocsHoverEnabled"):
            if view.match_selector(point, "keyword.effect"):
                self.show_hover_docs(
                    view,
                    point,
                    "keyword.effect",
                    self.game_data.game_effects,
                    self.settings,
                )
                return

            if view.match_selector(point, "string.trigger"):
                self.show_hover_docs(
                    view,
                    point,
                    "string.trigger",
                    self.game_data.game_triggers,
                    self.settings,
                )
                return

            if view.match_selector(point, "storage.type.scope"):
                self.show_hover_docs(
                    view,
                    point,
                    "storage.type.scope",
                    self.game_data.game_scopes,
                    self.settings,
                )
                return

        # Texture popups can happen for both script and gui files
        if not self.settings.get("TextureOpenPopup"):
            return

        posLine = view.line(point)
        if ".dds" not in view.substr(posLine):
            return

        texture_raw_start = view.find("gfx", posLine.a)
        texture_raw_end = view.find(".dds", posLine.a)
        texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
        texture_raw_path = view.substr(texture_raw_region)
        full_texture_path = os.path.join(self.game_files_path, texture_raw_path)  # type: ignore

        if os.path.exists(full_texture_path):
            texture_name = view.substr(view.word(texture_raw_end.a - 1))
            self.show_texture_hover_popup(view, point, texture_name, full_texture_path)
            return

        # Check mod paths if it's not vanilla
        for mod in self.mod_files:
            if os.path.exists(mod) and mod.endswith("mod"):
                # if it is the path to the mod directory, get all directories in it
                for directory in [f.path for f in os.scandir(mod) if f.is_dir()]:
                    mod_path = os.path.join(directory, texture_raw_path)
                    if os.path.exists(mod_path):
                        full_texture_path = mod_path
            else:
                mod_path = os.path.join(mod, texture_raw_path)
                if os.path.exists(mod_path):
                    full_texture_path = mod_path

        # The path exists and the point in the view is inside of the path
        if texture_raw_region.contains(point):
            texture_name = view.substr(view.word(texture_raw_end.a - 1))
            self.show_texture_hover_popup(view, point, texture_name, full_texture_path)

    def on_post_save_async(self, view: sublime.View):
        if view is None:
            return
        if get_syntax_name(view) != self.game_data.script_hover_objects:
            return
        if not self.settings.get("ScriptValidator"):
            return

        mod_dir = [
            x for x in self.mod_files if is_file_in_directory(get_file_name(view), x)
        ]
        in_mod_dir = any(mod_dir)
        if not in_mod_dir:
            return

        encoding_check(view)

        if self.settings.get("UpdateObjectsOnSave"):
            self.update_saved_game_objects(view, mod_dir)

    def update_saved_game_objects(self, view: sublime.View, mod_dir: List[str]):
        dir_to_game_object_dict = self.manager.get_dir_to_game_object_dict()
        filename = get_file_name(view)
        if not filename:
            return
        relative_path = filename.replace(mod_dir[-1], "")[1:]
        directory_path = os.path.dirname(relative_path)
        if directory_path not in dir_to_game_object_dict:
            return

        write_syntax = self.settings.get("UpdateSyntaxOnNewObjectCreation")
        if write_syntax:
            changed_objects_set = self.jomini_game_object.check_mod_for_changes(
                self.mod_files,
                self.manager.get_dir_to_game_object_dict(),
                self.manager.get_game_object_dirs(),
            )
        else:
            changed_objects_set = self.jomini_game_object.check_mod_for_changes(
                self.mod_files,
                self.manager.get_dir_to_game_object_dict(),
                self.manager.get_game_object_dirs(),
            )
        if changed_objects_set:
            # This checks if an object has actually been added in this save

            game_object_to_check = dir_to_game_object_dict[directory_path]
            game_objects = self.game_objects[game_object_to_check].keys()
            game_objects_in_file = set()

            view_lines = view.lines(sublime.Region(0, len(view)))

            level_1_dirs = {
                f"common{os.sep}inventions",
                f"common{os.sep}laws",
                f"common{os.sep}military_traditions",
                f"common{os.sep}missions",
                f"common{os.sep}named_colors",
            }
            level_2_dirs = {"common{os.sep}cultures"}
            if relative_path in level_1_dirs:
                base_object = GameObjectBase(level=1)
            elif relative_path in level_2_dirs:
                base_object = GameObjectBase(level=2)
            else:
                base_object = GameObjectBase()
            for line in view_lines:
                line = view.substr(line)
                if base_object.should_read(line):
                    found_item = (
                        line.split("=").pop(0).replace(" ", "").replace("\t", "")
                    )
                    if not found_item:
                        continue
                    game_objects_in_file.add(found_item)

            common_objects = [x in game_objects for x in game_objects_in_file]

            # If the loaded objects from this file are not the same as the objects in the cache a new object has been added.
            if not all(common_objects):
                self.load_changed_objects(
                    changed_objects_set,
                    write_syntax,  # type: ignore
                )
