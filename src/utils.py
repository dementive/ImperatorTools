"""
Utility functions used in various places
"""

import os
from collections import deque
from .jomini import GameObjectBase


def get_default_game_objects():
    base_object = GameObjectBase()

    game_objects = {
        "ambition": base_object,
        "area": base_object,
        "building": base_object,
        "culture": base_object,
        "culture_group": base_object,
        "custom_loc": base_object,
        "death_reason": base_object,
        "deity": base_object,
        "diplo_stance": base_object,
        "econ_policy": base_object,
        "event_pic": base_object,
        "event_theme": base_object,
        "government": base_object,
        "governor_policy": base_object,
        "heritage": base_object,
        "idea": base_object,
        "invention": base_object,
        "law": base_object,
        "legion_distinction": base_object,
        "levy_template": base_object,
        "loyalty": base_object,
        "mil_tradition": base_object,
        "mission": base_object,
        "mission_task": base_object,
        "modifier": base_object,
        "named_colors": base_object,
        "office": base_object,
        "opinion": base_object,
        "party": base_object,
        "pop": base_object,
        "price": base_object,
        "province_rank": base_object,
        "region": base_object,
        "religion": base_object,
        "script_value": base_object,
        "scripted_effect": base_object,
        "scripted_gui": base_object,
        "scripted_list_effects": base_object,
        "scripted_list_triggers": base_object,
        "scripted_modifier": base_object,
        "scripted_trigger": base_object,
        "subject_type": base_object,
        "tech_table": base_object,
        "terrain": base_object,
        "trade_good": base_object,
        "trait": base_object,
        "unit": base_object,
        "war_goal": base_object,
    }

    return game_objects


def is_file_in_directory(file_path, directory_path):
    if not os.path.exists(file_path):
        return False

    if not os.path.exists(directory_path):
        return False

    absolute_file_path = os.path.abspath(file_path)
    absolute_directory_path = os.path.abspath(directory_path)

    common_path = os.path.commonpath([absolute_file_path, absolute_directory_path])

    return common_path == absolute_directory_path


def get_syntax_name(view):
    syntax = view.syntax()
    if syntax is None:
        return ""

    name = view.syntax().name
    return name


# Get the index of a closing bracket in a string given the starting brackets index
def get_index(string, index):
    if string[index] != "{":
        return -1
    d = deque()
    for k in range(index, len(string)):
        if string[k] == "}":
            d.popleft()
        elif string[k] == "{":
            d.append(string[index])
        if not d:
            return k + 1
    return -1


def print_load_balanced_game_object_creation(game_objects):
    """
    Algorithm to balance the load between between the functions that load game objects
    Distributes game objects to the functions as evenly as possible based on the total number of objects within them.
    """
    object_names = {
        "ambition": "ImperatorAmbition",
        "area": "ImperatorArea",
        "building": "ImperatorBuilding",
        "culture": "ImperatorCulture",
        "culture_group": "ImperatorCultureGroup",
        "custom_loc": "ImperatorCustomLoc",
        "death_reason": "ImperatorDeathReason",
        "deity": "ImperatorDeity",
        "diplo_stance": "ImperatorDiplomaticStance",
        "econ_policy": "ImperatorEconomicPolicy",
        "event_pic": "ImperatorEventPicture",
        "event_theme": "ImperatorEventTheme",
        "government": "ImperatorGovernment",
        "governor_policy": "ImperatorGovernorPolicy",
        "heritage": "ImperatorHeritage",
        "idea": "ImperatorIdea",
        "invention": "ImperatorInvention",
        "law": "ImperatorLaw",
        "legion_distinction": "ImperatorLegionDistinction",
        "levy_template": "ImperatorLevyTemplate",
        "loyalty": "ImperatorLoyalty",
        "mil_tradition": "ImperatorMilitaryTradition",
        "mission": "ImperatorMission",
        "mission_task": "ImperatorMissionTask",
        "modifier": "ImperatorModifier",
        "named_colors": "ImperatorNamedColor",
        "office": "ImperatorOffice",
        "opinion": "ImperatorOpinion",
        "party": "ImperatorParty",
        "pop": "ImperatorPop",
        "price": "ImperatorPrice",
        "province_rank": "ImperatorProvinceRank",
        "region": "ImperatorRegion",
        "religion": "ImperatorReligion",
        "script_value": "ImperatorScriptValue",
        "scripted_effect": "ImperatorScriptedEffect",
        "scripted_gui": "ImperatorScriptedGui",
        "scripted_list_effects": "ImperatorScriptedList",
        "scripted_list_triggers": "ImperatorScriptedList",
        "scripted_modifier": "ImperatorScriptedModifier",
        "scripted_trigger": "ImperatorScriptedTrigger",
        "subject_type": "ImperatorSubjectType",
        "tech_table": "ImperatorTechTable",
        "terrain": "ImperatorTerrain",
        "trade_good": "ImperatorTradeGood",
        "trait": "ImperatorTrait",
        "unit": "ImperatorUnit",
    }

    object_values = dict()

    for i in object_names.keys():
        object_values[i] = int(game_objects[i].length())

    sorted_values = sorted(object_values.items(), key=lambda x: x[1], reverse=True)
    groups = [[] for _ in range(5)]

    for i in sorted_values:
        key = i[0]
        value = i[1]
        min_group = min(groups, key=lambda group: sum(int(item[1]) for item in group))
        min_group.append((key, value))

    suffixes = {
        1: "first",
        2: "second",
        3: "third",
        4: "fourth",
        5: "fifth",
    }

    for i, group in enumerate(groups, 1):
        print(f"def load_{suffixes[i]}():")
        for key, value in group:
            object_class = object_names[key]
            print(f'    self.game_objects["{key}"] = {object_class}()')
        print()
