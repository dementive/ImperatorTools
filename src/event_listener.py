"""
The main event listener for the plugin, this is where most of the plugin features actually happen.
The init function of the event listener is treated as the main entry point for the plugin.
"""

import os
import time
import threading

import sublime, sublime_plugin
from .jomini import PdxScriptObject
from .imperator_objects import *
from .game_objects import (
    get_objects_from_cache,
    write_data_to_syntax,
    cache_all_objects,
    add_color_scheme_scopes,
    handle_image_cache,
    check_mod_for_changes,
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
)
from ImperatorTools.object_cache import GameObjectCache


class ImperatorEventListener(
    Hover, AutoComplete, ScopeMatch, sublime_plugin.EventListener
):
    def on_init(self, views):
        self.game_objects = get_default_game_objects()
        self.GameData = GameData()
        self.settings = sublime.load_settings("Imperator Syntax.sublime-settings")
        self.imperator_files_path = self.settings.get("ImperatorFilesPath")
        self.imperator_mod_files = self.settings.get("PathsToModFiles")

        changed_objects_set = check_mod_for_changes(self.imperator_mod_files)
        if len(GameObjectCache().__dict__) == 0:
            # Create all objects for the first time
            sublime.set_timeout_async(lambda: self.create_all_game_objects(), 0)
            sublime.active_window().run_command("run_tiger")
        elif changed_objects_set:
            # Load objects that have changed since they were last cached
            self.game_objects = get_objects_from_cache()
            t0 = time.time()

            sublime.set_timeout_async(
                lambda: self.create_game_objects(changed_objects_set), 0
            )
            sublime.set_timeout_async(
                lambda: write_data_to_syntax(self.game_objects), 0
            )

            t1 = time.time()
            print("Time to load Imperator Rome objects: {:.3f} seconds".format(t1 - t0))

            # Cache created objects
            sublime.set_timeout_async(lambda: cache_all_objects(self.game_objects), 0)
        else:
            # Load cached objects
            self.game_objects = get_objects_from_cache()

        # Uncomment this and use the output to balance the load between the threads in create_all_game_objects
        # from .utils import print_load_balanced_game_object_creation
        # sublime.set_timeout_async(
        #     lambda: print_load_balanced_game_object_creation(self.game_objects), 0
        # )

        handle_image_cache(self.settings)
        add_color_scheme_scopes()

    def create_game_objects(
        self,
        changed_objects_set,
    ):
        game_object_to_class_dict = get_game_object_to_class_dict()
        for i in changed_objects_set:
            # TODO - threading and load balancing here if the expected number of objects to be created is > 250
            self.game_objects[i] = game_object_to_class_dict[i]()

    # Game object creation, have to be very careful to balance the load between each function here.
    def create_all_game_objects(self):
        t0 = time.time()

        def load_first():
            self.game_objects["modifier"] = ImperatorModifier()

        def load_second():
            self.game_objects["mission_task"] = ImperatorMissionTask()
            self.game_objects["subject_type"] = ImperatorSubjectType()
            self.game_objects["diplo_stance"] = ImperatorDiplomaticStance()
            self.game_objects["province_rank"] = ImperatorProvinceRank()

        def load_third():
            self.game_objects["script_value"] = ImperatorScriptValue()
            self.game_objects["heritage"] = ImperatorHeritage()
            self.game_objects["mil_tradition"] = ImperatorMilitaryTradition()
            self.game_objects["named_colors"] = ImperatorNamedColor()
            self.game_objects["mission"] = ImperatorMission()
            self.game_objects["price"] = ImperatorPrice()
            self.game_objects["death_reason"] = ImperatorDeathReason()
            self.game_objects["ambition"] = ImperatorAmbition()
            self.game_objects["religion"] = ImperatorReligion()
            self.game_objects["office"] = ImperatorOffice()
            self.game_objects["unit"] = ImperatorUnit()
            self.game_objects["party"] = ImperatorParty()

        def load_fourth():
            self.game_objects["deity"] = ImperatorDeity()
            self.game_objects["custom_loc"] = ImperatorCustomLoc()
            self.game_objects["opinion"] = ImperatorOpinion()
            self.game_objects["culture"] = ImperatorCulture()
            self.game_objects["event_pic"] = ImperatorEventPicture()
            self.game_objects["trait"] = ImperatorTrait()
            self.game_objects["law"] = ImperatorLaw()
            self.game_objects["scripted_gui"] = ImperatorScriptedGui()
            self.game_objects["culture_group"] = ImperatorCultureGroup()
            self.game_objects["scripted_modifier"] = ImperatorScriptedModifier()
            self.game_objects["building"] = ImperatorBuilding()
            self.game_objects["terrain"] = ImperatorTerrain()
            self.game_objects["econ_policy"] = ImperatorEconomicPolicy()
            self.game_objects["tech_table"] = ImperatorTechTable()
            self.game_objects["war_goal"] = ImperatorWargoal()

        def load_fifth():
            self.game_objects["loyalty"] = ImperatorLoyalty()
            self.game_objects["area"] = ImperatorArea()
            self.game_objects["scripted_effect"] = ImperatorScriptedEffect()
            self.game_objects["invention"] = ImperatorInvention()
            self.game_objects["scripted_trigger"] = ImperatorScriptedTrigger()
            self.game_objects["event_theme"] = ImperatorEventTheme()
            self.game_objects["region"] = ImperatorRegion()
            self.game_objects["levy_template"] = ImperatorLevyTemplate()
            self.game_objects["trade_good"] = ImperatorTradeGood()
            self.game_objects["idea"] = ImperatorIdea()
            self.game_objects["legion_distinction"] = ImperatorLegionDistinction()
            self.game_objects["government"] = ImperatorGovernment()
            self.game_objects["governor_policy"] = ImperatorGovernorPolicy()
            self.game_objects["scripted_list_effects"] = ImperatorScriptedList()
            self.game_objects["scripted_list_triggers"] = ImperatorScriptedList()
            self.game_objects["pop"] = ImperatorPop()

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

    def on_deactivated_async(self, view):
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

    def on_activated_async(self, view):
        vid = view.id()
        for field, views in self.auto_complete_fields.items():
            if vid in views:
                setattr(self, field, True)
                views.remove(vid)

    def create_completion_list(self, flag_name, completion_kind):
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

    def on_query_completions(self, view, prefix, locations):
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
                self.GameData.EventsList,
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_REORDER,
            )
        return None

    def on_selection_modified_async(self, view):
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

    def check_for_simple_completions(self, view, point):
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

    def on_hover(self, view, point, hover_zone):
        if not view:
            return

        syntax_name = get_syntax_name(view)

        if (
            syntax_name == "Imperator Script"
            or syntax_name == "Imperator Localization"
            or syntax_name == "Jomini Gui"
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
        full_texture_path = os.path.join(self.imperator_files_path, texture_raw_path)

        if os.path.exists(full_texture_path):
            texture_name = view.substr(view.word(texture_raw_end.a - 1))
            self.show_texture_hover_popup(view, point, texture_name, full_texture_path)
            return

        # Check mod paths if it's not vanilla
        for mod in imperator_mod_files:
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

    def do_hover_async(self, view, point):
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
            self.show_popup_default(
                view,
                point,
                word,
                PdxScriptObject(word, fname, current_line_num),
                "Saved Variable",
            )
            return
        if view.match_selector(point, "entity.name.function.scope.declaration"):
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
        if syntax_name == "Imperator Script":
            hover_objects = [
                ("ambition", "Ambition"),
                ("area", "Area"),
                ("building", "Building"),
                ("culture", "Culture"),
                ("culture_group", "Culture Group"),
                ("death_reason", "Death Reason"),
                ("deity", "Deity"),
                ("diplo_stance", "Diplomatic Stance"),
                ("econ_policy", "Economic Policy"),
                ("event_pic", "Event Picture"),
                ("event_theme", "Event Theme"),
                ("government", "Government"),
                ("governor_policy", "Governor Policy"),
                ("heritage", "Heritage"),
                ("idea", "Idea"),
                ("invention", "Invention"),
                ("law", "law"),
                ("legion_distinction", "Legion Distinction"),
                ("levy_template", "Levy Template"),
                ("loyalty", "Loyalty"),
                ("mil_tradition", "Military Tradition"),
                ("mission", "Mission"),
                ("mission_task", "Mission Task"),
                ("modifier", "Modifier"),
                ("named_colors", "Named Color"),
                ("office", "Office"),
                ("opinion", "Opinion"),
                ("party", "Party"),
                ("pop", "Pop Type"),
                ("price", "Price"),
                ("province_rank", "Province Rank"),
                ("region", "Region"),
                ("religion", "Religion"),
                ("scripted_gui", "Scripted Gui"),
                ("script_value", "Script Value"),
                ("scripted_effect", "Scripted Effect"),
                ("scripted_list_effects", "Scripted List"),
                ("scripted_list_triggers", "Scripted List"),
                ("scripted_modifier", "Scripted Modifier"),
                ("scripted_trigger", "Scripted Trigger"),
                ("subject_type", "Subject Type"),
                ("tech_table", "Technology Table"),
                ("terrain", "Terrain"),
                ("trade_good", "Trade Good"),
                ("trait", "Trait"),
                ("unit", "Unit"),
                ("war_goal", "War Goal"),
            ]

        if syntax_name == "Imperator Localization" or syntax_name == "Jomini Gui":
            hover_objects = [
                ("building", "Building"),
                ("culture", "Culture"),
                ("culture_group", "Culture Group"),
                ("custom_loc", "Culture"),
                ("deity", "Deity"),
                ("diplo_stance", "Diplomatic Stance"),
                ("heritage", "Heritage"),
                ("invention", "Invention"),
                ("legion_distinction", "Legion Distinction"),
                ("loyalty", "Loyalty"),
                ("mil_tradition", "Military Tradition"),
                ("modifier", "Modifier"),
                ("office", "Office"),
                ("price", "Price"),
                ("province_rank", "Province Rank"),
                ("religion", "Religion"),
                ("script_value", "Script Value"),
                ("scripted_gui", "Scripted Gui"),
                ("terrain", "Terrain"),
                ("trade_good", "Trade Good"),
                ("trait", "Trait"),
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

    def on_post_save_async(self, view):
        if view is None:
            return
        if get_syntax_name(view) != "Imperator Script":
            return
        if self.settings.get("ScriptValidator") == False:
            return

        in_mod_dir = any(
            [
                x
                for x in self.imperator_mod_files
                if is_file_in_directory(view.file_name(), x)
            ]
        )

        if in_mod_dir:
            encoding_check(view)
