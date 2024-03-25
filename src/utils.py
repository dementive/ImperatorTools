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
        "building": base_object,
        "culture": base_object,
        "culture_group": base_object,
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
        "modifier": base_object,
        "opinion": base_object,
        "office": base_object,
        "party": base_object,
        "pop": base_object,
        "price": base_object,
        "province_rank": base_object,
        "religion": base_object,
        "script_value": base_object,
        "scripted_effect": base_object,
        "scripted_modifier": base_object,
        "scripted_trigger": base_object,
        "subject_type": base_object,
        "tech_table": base_object,
        "terrain": base_object,
        "trade_good": base_object,
        "trait": base_object,
        "unit": base_object,
        "war_goal": base_object,
        "mission": base_object,
        "mission_task": base_object,
        "area": base_object,
        "region": base_object,
        "scripted_list_triggers": base_object,
        "scripted_list_effects": base_object,
        "named_colors": base_object,
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
