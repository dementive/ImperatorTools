"""
The main event listener for the plugin, this is where most of the plugin features actually happen.
The init function of the event listener is treated as the main entry point for the plugin.
"""

import os
import time
import threading
from typing import List, Set, Tuple, Union

import sublime, sublime_plugin
from .jomini import PdxScriptObject, GameObjectBase
from .imperator_objects import *
from .game_object_manager import GameObjectManager
from .game_objects import (
    get_objects_from_cache,
    write_data_to_syntax,
    cache_all_objects,
    add_color_scheme_scopes,
    handle_image_cache,
    check_mod_for_changes,
    check_for_syntax_changes,
    load_game_objects_json,
)
from .game_data import GameData
from .scope_match import ScopeMatch
from .autocomplete import AutoComplete
from .hover import Hover
from .encoding import encoding_check
from .utils import (
    get_default_game_objects,
    is_file_in_directory,
    get_syntax_name,
    get_game_object_to_class_dict,
    get_dir_to_game_object_dict,
)


class ImperatorEventListener(
    Hover, AutoComplete, ScopeMatch, sublime_plugin.EventListener
):
    def on_init(self, views: List[sublime.View]):
        self.game_objects = get_default_game_objects()
        self.GameData = GameData()
        self.settings = sublime.load_settings("Imperator Syntax.sublime-settings")
        self.imperator_files_path = self.settings.get("ImperatorFilesPath")
        self.imperator_mod_files = self.settings.get("PathsToModFiles")

        syntax_changes = check_for_syntax_changes()
        changed_objects_set = check_mod_for_changes(self.imperator_mod_files)
        if len(load_game_objects_json()) == 0:
            # Create all objects for the first time
            sublime.set_timeout_async(lambda: self.create_all_game_objects(), 0)
            sublime.active_window().run_command("run_tiger")
        elif changed_objects_set:
            self.load_changed_objects(changed_objects_set)
        else:
            # Load cached objects
            self.game_objects = get_objects_from_cache()
            if syntax_changes:
                sublime.set_timeout_async(
                    lambda: write_data_to_syntax(self.game_objects), 0
                )

        # Uncomment this and use the output to balance the load between the threads in create_all_game_objects
        # from .utils import print_load_balanced_game_object_creation
        # sublime.set_timeout_async(
        #     lambda: print_load_balanced_game_object_creation(self.game_objects), 0
        # )

        handle_image_cache(self.settings)
        add_color_scheme_scopes()

    def load_changed_objects(self, changed_objects_set: Set[str], write_syntax=True):
        # Load objects that have changed since they were last cached
        self.game_objects = get_objects_from_cache()

        sublime.set_timeout_async(
            lambda: self.create_game_objects(changed_objects_set), 0
        )
        if write_syntax:
            sublime.set_timeout_async(
                lambda: write_data_to_syntax(self.game_objects), 0
            )

        # Cache created objects
        sublime.set_timeout_async(lambda: cache_all_objects(self.game_objects), 0)

    def create_game_objects(
        self,
        changed_objects_set: Set[str],
    ):
        game_object_to_class_dict = get_game_object_to_class_dict()
        for i in changed_objects_set:
            # TODO - threading and load balancing here if the expected number of objects to be created is > 250
            self.game_objects[i] = game_object_to_class_dict[i]()

    # Game object creation, have to be very careful to balance the load between each function here.
    def create_all_game_objects(self):
        t0 = time.time()
        manager = GameObjectManager()


        def load_first():
            self.game_objects[manager.modifier.name] = Modifier()

        def load_second():
            self.game_objects[manager.mission_task.name] = MissionTask()
            self.game_objects[manager.subject_type.name] = SubjectType()
            self.game_objects[manager.diplo_stance.name] = DiplomaticStance()
            self.game_objects[manager.province_rank.name] = ProvinceRank()

        def load_third():
            self.game_objects[manager.script_value.name] = ScriptValue()
            self.game_objects[manager.heritage.name] = Heritage()
            self.game_objects[manager.mil_tradition.name] = MilitaryTradition()
            self.game_objects[manager.named_colors.name] = NamedColor()
            self.game_objects[manager.mission.name] = Mission()
            self.game_objects[manager.price.name] = Price()
            self.game_objects[manager.death_reason.name] = DeathReason()
            self.game_objects[manager.ambition.name] = Ambition()
            self.game_objects[manager.religion.name] = Religion()
            self.game_objects[manager.office.name] = Office()
            self.game_objects[manager.unit.name] = Unit()
            self.game_objects[manager.party.name] = Party()

        def load_fourth():
            self.game_objects[manager.deity.name] = Deity()
            self.game_objects[manager.custom_loc.name] = CustomLoc()
            self.game_objects[manager.opinion.name] = Opinion()
            self.game_objects[manager.culture.name] = Culture()
            self.game_objects[manager.event_pic.name] = EventPicture()
            self.game_objects[manager.trait.name] = Trait()
            self.game_objects[manager.law.name] = Law()
            self.game_objects[manager.scripted_gui.name] = ScriptedGui()
            self.game_objects[manager.culture_group.name] = CultureGroup()
            self.game_objects[manager.scripted_modifier.name] = ScriptedModifier()
            self.game_objects[manager.building.name] = Building()
            self.game_objects[manager.terrain.name] = Terrain()
            self.game_objects[manager.econ_policy.name] = EconomicPolicy()
            self.game_objects[manager.tech_table.name] = TechTable()
            self.game_objects[manager.war_goal.name] = Wargoal()

        def load_fifth():
            self.game_objects[manager.loyalty.name] = Loyalty()
            self.game_objects[manager.area.name] = Area()
            self.game_objects[manager.scripted_effect.name] = ScriptedEffect()
            self.game_objects[manager.invention.name] = Invention()
            self.game_objects[manager.scripted_trigger.name] = ScriptedTrigger()
            self.game_objects[manager.event_theme.name] = EventTheme()
            self.game_objects[manager.region.name] = Region()
            self.game_objects[manager.levy_template.name] = LevyTemplate()
            self.game_objects[manager.trade_good.name] = TradeGood()
            self.game_objects[manager.idea.name] = Idea()
            self.game_objects[manager.legion_distinction.name] = LegionDistinction()
            self.game_objects[manager.government.name] = Government()
            self.game_objects[manager.governor_policy.name] = GovernorPolicy()
            self.game_objects[manager.scripted_list_effects.name] = ScriptedList()
            self.game_objects[manager.scripted_list_triggers.name] = ScriptedList()
            self.game_objects[manager.pop.name] = Pop()

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
                self.GameData.EffectsList[i] = "Scripted list effect"
            for i in self.game_objects["scripted_list_triggers"].keys():
                self.GameData.TriggersList[i] = "Scripted list trigger"

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

        # Write syntax data after creating objects so they actually exist when writing
        sublime.set_timeout_async(lambda: write_data_to_syntax(self.game_objects), 0)

        t1 = time.time()
        print("Time to load Imperator Rome objects: {:.3f} seconds".format(t1 - t0))

        # Cache created objects
        sublime.set_timeout_async(lambda: cache_all_objects(self.game_objects), 0)
        sublime.set_timeout_async(
            lambda: check_mod_for_changes(self.imperator_mod_files), 0
        )  # Update hashes for each game object directory

    def on_deactivated_async(self, view: sublime.View):
        """
        Remove field states when view loses focus
        if cursor was in a field in the old view but not the new view the completions will still be accurate
        save the id of the view so it can be readded when it regains focus
        """
        vid = view.id()
        for field, views in self.auto_complete_fields.items():
            if getattr(self, field):
                setattr(self, field, False)
                views.append(vid)

    def on_activated_async(self, view: sublime.View):
        vid = view.id()
        for field, views in self.auto_complete_fields.items():
            if vid in views:
                setattr(self, field, True)
                views.remove(vid)

    def create_completion_list(self, flag_name: str, completion_kind: str):
        if not getattr(self, flag_name, False):
            return None

        completions = self.game_objects[flag_name].keys()
        completions = sorted(completions)
        return sublime.CompletionList(
            [
                sublime.CompletionItem(
                    trigger=key,
                    completion_format=sublime.COMPLETION_FORMAT_TEXT,
                    kind=completion_kind,
                    details=" ",
                )
                # Calling sorted() twice makes it so completions are ordered by
                # 1. the number of times they appear in the current buffer
                # 2. if they dont appear they show up alphabetically
                for key in sorted(completions)
            ],
            flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
            | sublime.INHIBIT_WORD_COMPLETIONS,
        )

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

        if (
            syntax_name != "Imperator Script"
            and syntax_name != "Imperator Localization"
            and syntax_name != "Jomini Gui"
        ):
            return None

        if syntax_name == "Jomini Gui" and not self.settings.get(
            "ImperatorGuiFeatures"
        ):
            return

        if syntax_name == "Imperator Localization" or syntax_name == "Jomini Gui":
            for flag, completion in self.GameData.data_system_completion_flag_pairs:
                completion_list = self.create_completion_list(flag, completion)
                if completion_list is not None:
                    return completion_list
            return  # Don't need to check anything else for data system

        for flag, completion in self.GameData.completion_flag_pairs:
            completion_list = self.create_completion_list(flag, completion)
            if completion_list is not None:
                return completion_list

        fname = view.file_name()
        if not fname:
            return

        if "script_values" in fname:
            e_list = []
            for i in self.GameData.EffectsList:
                e_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=self.GameData.EffectsList[i].split("<br>")[0],
                    )
                )
            t_list = []
            for i in self.GameData.TriggersList:
                t_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=self.GameData.TriggersList[i].split("<br>")[0],
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
                        details=self.GameData.PricesDict[key],
                    )
                    for key in sorted(self.GameData.PricesDict)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if (
            self.trigger_field
            or self.mtth_field
            or "scripted_triggers" in fname
            or "scripted_modifiers" in fname
        ):
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=self.GameData.TriggersList[key].split("<br>")[0],
                    )
                    for key in sorted(self.GameData.TriggersList)
                ]
            )
        if self.effect_field or "scripted_effects" in fname:
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=self.GameData.EffectsList[key].split("<br>")[0],
                    )
                    for key in sorted(self.GameData.EffectsList)
                ]
            )
        if self.modifier_field or re.search(
            r"modifiers|traits|buildings|governor_policies|trade_goods", fname
        ):
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "M", "Modifier"),
                        details=self.GameData.ModifersList[key],
                        annotation=self.GameData.ModifersList[key].replace(
                            "Category: ", ""
                        ),
                    )
                    for key in sorted(self.GameData.ModifersList)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if "/events/" in fname:
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=self.GameData.EventsList[key]["trigger"],
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=self.GameData.EventsList[key]["kind"],
                        details=self.GameData.EventsList[key]["details"],
                        annotation=self.GameData.EventsList[key]["annotation"],
                    )
                    for key in sorted(self.GameData.EventsList)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        return None

    def on_selection_modified_async(self, view: sublime.View):
        if not view:
            return

        syntax_name = get_syntax_name(view)

        if (
            syntax_name != "Imperator Script"
            and syntax_name != "Imperator Localization"
            and syntax_name != "Jomini Gui"
        ):
            return

        if (
            syntax_name == "Jomini Gui"
            and self.settings.get("ImperatorGuiFeatures") is not True
        ):
            return

        if syntax_name != "Imperator Localization" and syntax_name != "Jomini Gui":
            self.simple_scope_match(view)

        # Only do when there is 1 selections, doens't make sense with multiple selections
        if len(view.sel()) == 1:
            point = view.sel()[0].a
            if (
                syntax_name == "Imperator Localization" or syntax_name == "Jomini Gui"
            ) and view.substr(point) == "'":
                for i in self.GameData.data_system_completion_functions:
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

        for patterns, flag in self.GameData.simple_completion_pattern_flag_pairs:
            if self.check_for_patterns_and_set_flag(patterns, flag, view, line, point):
                return

        for pattern, flag in self.GameData.simple_completion_scope_pattern_flag_pairs:
            self.check_pattern_and_set_flag(pattern, flag, view, line, point)

    def on_hover(self, view: sublime.View, point: int, hover_zone: sublime.HoverZone):
        if not view:
            return

        syntax_name = get_syntax_name(view)

        if (
            syntax_name != "Imperator Script"
            and syntax_name != "Imperator Localization"
            and syntax_name != "Jomini Gui"
        ):
            return

        if (
            syntax_name == "Jomini Gui"
            and self.settings.get("ImperatorGuiFeatures") is not True
        ):
            return

        # Do everything that requires fetching GameObjects in non-blocking thread
        sublime.set_timeout_async(lambda: self.do_hover_async(view, point), 0)

        if syntax_name != "Imperator Script":
            # For yml only the saved scopes/variables/game objects get hover
            return

        if self.settings.get("DocsHoverEnabled") == True:
            if view.match_selector(point, "keyword.effect"):
                self.show_hover_docs(
                    view,
                    point,
                    "keyword.effect",
                    self.GameData.EffectsList,
                    self.settings,
                )
                return

            if view.match_selector(point, "string.trigger"):
                self.GameData.TriggersList.update(self.GameData.CustomTriggersList)
                self.show_hover_docs(
                    view,
                    point,
                    "string.trigger",
                    self.GameData.TriggersList,
                    self.settings,
                )
                return

            if view.match_selector(point, "storage.type.scope"):
                self.GameData.ScopesList.update(self.GameData.CustomScopesList)
                self.show_hover_docs(
                    view,
                    point,
                    "storage.type.scope",
                    self.GameData.ScopesList,
                    self.settings,
                )
                return

        # Texture popups can happen for both script and gui files
        if self.settings.get("TextureOpenPopup") != True:
            return

        posLine = view.line(point)
        if ".dds" not in view.substr(posLine):
            return

        texture_raw_start = view.find("gfx", posLine.a)
        texture_raw_end = view.find(".dds", posLine.a)
        texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
        texture_raw_path = view.substr(texture_raw_region)
        full_texture_path = os.path.join(self.imperator_files_path, texture_raw_path) # type: ignore

        if os.path.exists(full_texture_path):
            texture_name = view.substr(view.word(texture_raw_end.a - 1))
            self.show_texture_hover_popup(view, point, texture_name, full_texture_path)
            return

        # Check mod paths if it's not vanilla
        for mod in self.imperator_mod_files: # type: ignore
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

    def do_hover_async(self, view: sublime.View, point: int):
        word_region = view.word(point)
        word = view.substr(word_region)
        fname = view.file_name()
        current_line_num = view.rowcol(point)[0] + 1

        if view.match_selector(point, "comment.line"):
            return

        if (
            view.match_selector(point, "variable.parameter.scope.usage")
            or view.match_selector(point, "variable.parameter.remove.var")
            or view.match_selector(point, "variable.parameter.trigger.usage")
            or view.match_selector(point, "variable.parameter.var.usage")
        ):
            if fname and ("scripted_triggers" in fname or "scripted_effects" in fname or "scripted_modifiers" in fname):
                word = self.handle_scripted_args(view, point)

            if view.match_selector(point, "variable.parameter.scope.usage"):
                self.show_popup_default(
                    view,
                    point,
                    word,
                    PdxScriptObject(word, fname, current_line_num),
                    "Saved Scope",
                )
            else:
                self.show_popup_default(
                    view,
                    point,
                    word,
                    PdxScriptObject(word, fname, current_line_num),
                    "Saved Variable",
                )
            return

        if view.match_selector(point, "entity.name.function.var.declaration"):
            if fname and ("scripted_triggers" in fname or "scripted_effects" in fname or "scripted_modifiers" in fname):
                word = self.handle_scripted_args(view, point)
            self.show_popup_default(
                view,
                point,
                word,
                PdxScriptObject(word, fname, current_line_num),
                "Saved Variable",
            )
            return
        if view.match_selector(point, "entity.name.function.scope.declaration"):
            if fname and ("scripted_triggers" in fname or "scripted_effects" in fname or "scripted_modifiers" in fname):
                word = self.handle_scripted_args(view, point)
            self.show_popup_default(
                view,
                point,
                word,
                PdxScriptObject(word, fname, current_line_num),
                "Saved Scope",
            )
            return

        hover_objects = list()
        syntax_name = get_syntax_name(view)
        manager = GameObjectManager()
        if syntax_name == "Imperator Script":
            hover_objects = [
                (manager.ambition.name, "Ambition"),
                (manager.area.name, "Area"),
                (manager.building.name, "Building"),
                (manager.culture.name, "Culture"),
                (manager.culture_group.name, "Culture Group"),
                (manager.death_reason.name, "Death Reason"),
                (manager.deity.name, "Deity"),
                (manager.diplo_stance.name, "Diplomatic Stance"),
                (manager.econ_policy.name, "Economic Policy"),
                (manager.event_pic.name, "Event Picture"),
                (manager.event_theme.name, "Event Theme"),
                (manager.government.name, "Government"),
                (manager.governor_policy.name, "Governor Policy"),
                (manager.heritage.name, "Heritage"),
                (manager.idea.name, "Idea"),
                (manager.invention.name, "Invention"),
                (manager.law.name, "law"),
                (manager.legion_distinction.name, "Legion Distinction"),
                (manager.levy_template.name, "Levy Template"),
                (manager.loyalty.name, "Loyalty"),
                (manager.mil_tradition.name, "Military Tradition"),
                (manager.mission.name, "Mission"),
                (manager.mission_task.name, "Mission Task"),
                (manager.modifier.name, "Modifier"),
                (manager.named_colors.name, "Named Color"),
                (manager.office.name, "Office"),
                (manager.opinion.name, "Opinion"),
                (manager.party.name, "Party"),
                (manager.pop.name, "Pop Type"),
                (manager.price.name, "Price"),
                (manager.province_rank.name, "Province Rank"),
                (manager.region.name, "Region"),
                (manager.religion.name, "Religion"),
                (manager.scripted_gui.name, "Scripted Gui"),
                (manager.script_value.name, "Script Value"),
                (manager.scripted_effect.name, "Scripted Effect"),
                (manager.scripted_list_effects.name, "Scripted List"),
                (manager.scripted_list_triggers.name, "Scripted List"),
                (manager.scripted_modifier.name, "Scripted Modifier"),
                (manager.scripted_trigger.name, "Scripted Trigger"),
                (manager.subject_type.name, "Subject Type"),
                (manager.tech_table.name, "Technology Table"),
                (manager.terrain.name, "Terrain"),
                (manager.trade_good.name, "Trade Good"),
                (manager.trait.name, "Trait"),
                (manager.unit.name, "Unit"),
                (manager.war_goal.name, "War Goal"),
            ]

        if syntax_name == "Imperator Localization" or syntax_name == "Jomini Gui":
            hover_objects = [
                (manager.building.name, "Building"),
                (manager.culture.name, "Culture"),
                (manager.culture_group.name, "Culture Group"),
                (manager.custom_loc.name, "Culture"),
                (manager.deity.name, "Deity"),
                (manager.diplo_stance.name, "Diplomatic Stance"),
                (manager.heritage.name, "Heritage"),
                (manager.invention.name, "Invention"),
                (manager.legion_distinction.name, "Legion Distinction"),
                (manager.loyalty.name, "Loyalty"),
                (manager.mil_tradition.name, "Military Tradition"),
                (manager.modifier.name, "Modifier"),
                (manager.office.name, "Office"),
                (manager.price.name, "Price"),
                (manager.province_rank.name, "Province Rank"),
                (manager.religion.name, "Religion"),
                (manager.script_value.name, "Script Value"),
                (manager.scripted_gui.name, "Scripted Gui"),
                (manager.terrain.name, "Terrain"),
                (manager.trade_good.name, "Trade Good"),
                (manager.trait.name, "Trait"),
            ]

        # Iterate over the list and call show_popup_default for each game object
        for hover_object, name in hover_objects:
            if self.game_objects[hover_object].contains(word):
                self.show_popup_default(
                    view,
                    point,
                    word,
                    self.game_objects[hover_object].access(word),
                    name,
                )
                break

    def on_post_save_async(self, view: sublime.View):
        if view is None:
            return
        if get_syntax_name(view) != "Imperator Script":
            return
        if self.settings.get("ScriptValidator") == False:
            return

        mod_dir = [
            x
            for x in self.imperator_mod_files # type: ignore
            if is_file_in_directory(view.file_name(), x)
        ]
        in_mod_dir = any(mod_dir)
        if not in_mod_dir:
            return

        encoding_check(view)

        if self.settings.get("UpdateObjectsOnSave"):
            self.update_saved_game_objects(view, mod_dir)

    def update_saved_game_objects(self, view: sublime.View, mod_dir: List[str]):
        dir_to_game_object_dict = get_dir_to_game_object_dict()
        filename = view.file_name()
        if filename is None:
            return
        relative_path = filename.replace(mod_dir[-1], "")[1:]
        directory_path = os.path.dirname(relative_path)
        if directory_path not in dir_to_game_object_dict:
            return

        write_syntax = self.settings.get("UpdateSyntaxOnNewObjectCreation")
        if write_syntax:
            changed_objects_set = check_mod_for_changes(self.imperator_mod_files)
        else:
            changed_objects_set = check_mod_for_changes(self.imperator_mod_files, True)
        if changed_objects_set:
            # This checks if an object has actually been added in this save

            game_object_to_check = dir_to_game_object_dict[directory_path]
            game_objects = self.game_objects[game_object_to_check].keys()
            game_objects_in_file = set()

            view_lines = view.lines(sublime.Region(0, len(view)))

            level_1_dirs = {
                "common\\inventions",
                "common\\laws",
                "common\\military_traditions",
                "common\\missions",
                "common\\named_colors",
            }
            level_2_dirs = {"common\\cultures"}
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
                    write_syntax, # type: ignore
                )
