"""
Utility functions used in various places
"""

import os
from collections import deque
from .imperator_objects import *
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


def get_game_object_dirs():
    return {
        "common\\ambitions": "",
        "common\\buildings": "",
        "common\\cultures": "",
        "common\\customizable_localization": "",
        "common\\deathreasons": "",
        "common\\deities": "",
        "common\\diplomatic_stances": "",
        "common\\economic_policies": "",
        "common\\event_pictures": "",
        "common\\event_themes": "",
        "common\\governments": "",
        "common\\governor_policies": "",
        "common\\heritage": "",
        "common\\ideas": "",
        "common\\inventions": "",
        "common\\laws": "",
        "common\\legion_distinctions": "",
        "common\\levy_templates": "",
        "common\\loyalty": "",
        "common\\military_traditions": "",
        "common\\missions": "",
        "common\\modifiers": "",
        "common\\named_colors": "",
        "common\\offices": "",
        "common\\opinions": "",
        "common\\party_types": "",
        "common\\pop_types": "",
        "common\\prices": "",
        "common\\province_ranks": "",
        "common\\religions": "",
        "common\\script_values": "",
        "common\\scripted_effects": "",
        "common\\scripted_guis": "",
        "common\\scripted_lists": "",
        "common\\scripted_modifiers": "",
        "common\\scripted_triggers": "",
        "common\\subject_types": "",
        "common\\technology_tables": "",
        "common\\terrain_types": "",
        "common\\trade_goods": "",
        "common\\traits": "",
        "common\\units": "",
        "common\\wargoals": "",
        "map_data": "",
    }


def get_dir_to_game_object_dict():
    return {
        "common\\ambitions": "ambition",
        "map_data": "area",
        "common\\buildings": "building",
        "common\\cultures": "culture",
        "common\\cultures": "culture_group",
        "common\\customizable_localization": "custom_loc",
        "common\\deathreasons": "death_reason",
        "common\\deities": "deity",
        "common\\diplomatic_stances": "diplo_stance",
        "common\\economic_policies": "econ_policy",
        "common\\event_pictures": "event_pic",
        "common\\event_themes": "event_theme",
        "common\\governments": "government",
        "common\\governor_policies": "governor_policy",
        "common\\heritage": "heritage",
        "common\\ideas": "idea",
        "common\\inventions": "invention",
        "common\\laws": "law",
        "common\\legion_distinctions": "legion_distinction",
        "common\\levy_templates": "levy_template",
        "common\\loyalty": "loyalty",
        "common\\military_traditions": "mil_tradition",
        "common\\missions": "mission",
        "common\\missions": "mission_task",
        "common\\modifiers": "modifier",
        "common\\named_colors": "named_colors",
        "common\\offices": "office",
        "common\\opinions": "opinion",
        "common\\party_types": "party",
        "common\\pop_types": "pop",
        "common\\prices": "price",
        "common\\province_ranks": "province_rank",
        "map_data": "region",
        "common\\religions": "religion",
        "common\\script_values": "script_value",
        "common\\scripted_effects": "scripted_effect",
        "common\\scripted_guis": "scripted_gui",
        "common\\scripted_lists": "scripted_list_effects",
        "common\\scripted_lists": "scripted_list_triggers",
        "common\\scripted_modifiers": "scripted_modifier",
        "common\\scripted_triggers": "scripted_trigger",
        "common\\subject_types": "subject_type",
        "common\\technology_tables": "tech_table",
        "common\\terrain_types": "terrain",
        "common\\trade_goods": "trade_good",
        "common\\traits": "trait",
        "common\\units": "unit",
        "common\\wargoals": "war_goal",
    }


def get_game_object_to_class_dict():
    return {
        "ambition": ImperatorAmbition,
        "area": ImperatorArea,
        "building": ImperatorBuilding,
        "culture": ImperatorCulture,
        "culture_group": ImperatorCultureGroup,
        "custom_loc": ImperatorCustomLoc,
        "death_reason": ImperatorDeathReason,
        "deity": ImperatorDeity,
        "diplo_stance": ImperatorDiplomaticStance,
        "econ_policy": ImperatorEconomicPolicy,
        "event_pic": ImperatorEventPicture,
        "event_theme": ImperatorEventTheme,
        "government": ImperatorGovernment,
        "governor_policy": ImperatorGovernorPolicy,
        "heritage": ImperatorHeritage,
        "idea": ImperatorIdea,
        "invention": ImperatorInvention,
        "law": ImperatorLaw,
        "legion_distinction": ImperatorLegionDistinction,
        "levy_template": ImperatorLevyTemplate,
        "loyalty": ImperatorLoyalty,
        "mil_tradition": ImperatorMilitaryTradition,
        "mission": ImperatorMission,
        "mission_task": ImperatorMissionTask,
        "modifier": ImperatorModifier,
        "named_colors": ImperatorNamedColor,
        "office": ImperatorOffice,
        "opinion": ImperatorOpinion,
        "party": ImperatorParty,
        "pop": ImperatorPop,
        "price": ImperatorPrice,
        "province_rank": ImperatorProvinceRank,
        "region": ImperatorRegion,
        "religion": ImperatorReligion,
        "script_value": ImperatorScriptValue,
        "scripted_effect": ImperatorScriptedEffect,
        "scripted_gui": ImperatorScriptedGui,
        "scripted_list_effects": ImperatorScriptedList,
        "scripted_list_triggers": ImperatorScriptedList,
        "scripted_modifier": ImperatorScriptedModifier,
        "scripted_trigger": ImperatorScriptedTrigger,
        "subject_type": ImperatorSubjectType,
        "tech_table": ImperatorTechTable,
        "terrain": ImperatorTerrain,
        "trade_good": ImperatorTradeGood,
        "trait": ImperatorTrait,
        "unit": ImperatorUnit,
        "war_goal": ImperatorWargoal,
    }


def get_expected_number_of_objects_dict():
    return {
        "modifier": 4952,
        "mission_task": 4151,
        "script_value": 1839,
        "deity": 1296,
        "area": 994,
        "loyalty": 828,
        "heritage": 754,
        "scripted_effect": 644,
        "custom_loc": 643,
        "event_pic": 600,
        "opinion": 582,
        "culture": 502,
        "invention": 492,
        "mil_tradition": 478,
        "event_theme": 434,
        "scripted_trigger": 390,
        "scripted_gui": 379,
        "named_colors": 360,
        "trait": 327,
        "scripted_list_effects": 237,
        "mission": 228,
        "law": 193,
        "region": 132,
        "price": 118,
        "levy_template": 97,
        "death_reason": 81,
        "scripted_list_triggers": 79,
        "religion": 59,
        "culture_group": 58,
        "trade_good": 56,
        "ambition": 47,
        "building": 43,
        "idea": 36,
        "government": 32,
        "scripted_modifier": 30,
        "legion_distinction": 30,
        "office": 24,
        "unit": 22,
        "terrain": 21,
        "governor_policy": 13,
        "subject_type": 11,
        "war_goal": 11,
        "diplo_stance": 8,
        "econ_policy": 7,
        "party": 6,
        "pop": 5,
        "tech_table": 4,
        "province_rank": 3,
    }


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
    object_names = get_game_object_to_class_dict()
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

    expected_values_dict = dict()
    for i, group in enumerate(groups, 1):
        for key, value in group:
            expected_values_dict[key] = value

        print(f"def load_{suffixes[i]}():")
        for key, value in group:
            object_class = object_names[key].__name__
            print(f'    self.game_objects["{key}"] = {object_class}()')

    print(
        dict(
            sorted(expected_values_dict.items(), key=lambda item: item[1], reverse=True)
        )
    )
