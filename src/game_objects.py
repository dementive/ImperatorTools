"""
Code related to loading, saving, and caching imperator game objects
"""
import sublime
import os
import hashlib
import json
import ast
from typing import Dict, List

from .game_object_manager import GameObjectManager
from .imperator_objects import ImperatorObject
from .jomini import dict_to_game_object as make_object
from .utils import (
    get_default_game_objects,
    get_game_object_dirs,
    get_dir_to_game_object_dict,
)


def check_mod_for_changes(imperator_mod_files: List[str], write_syntax=False):
    """
    Check if any changes have been made to mod files
    if changes have been made this returns a set of game objects that need to be recreated and cached
    """
    object_cache_path = sublime.packages_path() + f"/ImperatorTools/object_cache.json"
    if os.stat(object_cache_path).st_size < 200:
        # If there are no objects in the cache, they all need to be created
        return set(get_dir_to_game_object_dict().values())
    mod_cache_path = sublime.packages_path() + f"/ImperatorTools/mod_cache.json"
    with open(mod_cache_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    game_object_dirs = get_game_object_dirs()
    # Add the names and output of os.stat.st_mtime together for all the files in the current mods into stats_string
    for path in imperator_mod_files:
        mod_name = path.replace("\\", "/").rstrip("/").rpartition("/")[2]
        for dirpath, dirnames, filenames in os.walk(path):
            relative_path = dirpath.replace(path, "")[1:]
            if relative_path not in game_object_dirs:
                continue

            mod_files = [
                x for x in filenames if x.endswith(".txt") or x.endswith(".gui")
            ]

            if not mod_files:
                continue

            stats_string = str()
            for i in mod_files:
                full_path = dirpath + "/" + i
                value = os.stat(full_path).st_mtime
                stats_string += f"{mod_name}{value}"

            # Encode stats_string for each game object directory
            game_object_dirs[relative_path] = hashlib.sha256(
                stats_string.encode()
            ).hexdigest()

    with open(mod_cache_path, "w") as f:
        if write_syntax:
            json_to_write = [game_object_dirs, "write_syntax"]
        else:
            json_to_write = [game_object_dirs]

        f.write(json.dumps(json_to_write))

    changed_objects = set()
    dir_to_game_object_dict = get_dir_to_game_object_dict()

    for i in compare_dicts(game_object_dirs, data[0]):
        if i in dir_to_game_object_dict:
            changed_objects.add(dir_to_game_object_dict[i])

    return changed_objects


def compare_dicts(dict1: Dict, dict2: Dict):
    # Compare two dictionaries and return a set of all the keys with values that are not the same in both
    common_keys = set(dict1.keys()) & set(dict2.keys())
    unequal_keys = set()

    for key in common_keys:
        if dict1[key] != dict2[key]:
            unequal_keys.add(key)

    return unequal_keys


def check_for_syntax_changes():
    mod_cache_path = sublime.packages_path() + f"/ImperatorTools/mod_cache.json"
    with open(mod_cache_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if len(data) > 1:
        return True
    return False


def load_game_objects_json():
    path = sublime.packages_path() + f"/ImperatorTools/object_cache.json"
    with open(path, "r") as f:
        data = json.load(f)
    return data


def get_objects_from_cache():
    path = sublime.packages_path() + f"/ImperatorTools/object_cache.json"
    game_objects = get_default_game_objects()
    with open(path, "r") as f:
        data = json.load(f)
    for i in game_objects:
        if i in data:
            game_objects[i] = make_object(ast.literal_eval(data[i]))

    return game_objects


def cache_all_objects(game_objects: Dict[str, ImperatorObject]):
    # Write all generated objects to cache
    path = sublime.packages_path() + f"/ImperatorTools/object_cache.json"
    objects = dict()
    for i in game_objects:
        objects[i] = game_objects[i].to_json()
    with open(path, "w") as f:
        f.write(json.dumps(objects))


def handle_image_cache(settings: sublime.Settings):
    cache_size_limit = settings.get("MaxImageCacheSize")
    cache = sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/"
    cache_files = [x for x in os.listdir(cache) if x.endswith(".png")]
    if len(cache_files) > cache_size_limit: # type: ignore
        for i in cache_files:
            os.remove(os.path.join(cache, i))
        sublime.status_message("Cleared Image Cache")


def add_color_scheme_scopes():
    # Add scopes for yml text formatting to color scheme
    DEFAULT_CS = "Packages/Color Scheme - Default/Monokai.sublime-color-scheme"
    prefs = sublime.load_settings("Preferences.sublime-settings")
    cs = prefs.get("color_scheme", DEFAULT_CS)
    scheme_cache_path = os.path.join(
        sublime.packages_path(), "User", "PdxTools", cs  # type: ignore
    ).replace("tmTheme", "sublime-color-scheme")
    if not os.path.exists(scheme_cache_path):
        os.makedirs(os.path.dirname(scheme_cache_path), exist_ok=True)
        rules = """{"variables": {}, "globals": {},"rules": [{"scope": "text.format.white.yml","foreground": "rgb(250, 250, 250)",},{"scope": "text.format.grey.yml","foreground": "rgb(173, 165, 160)",},{"scope": "text.format.red.yml","foreground": "rgb(210, 40, 40)",},{"scope": "text.format.green.yml","foreground": "rgb(40, 210, 40)",},{"scope": "text.format.yellow.yml","foreground": "rgb(255, 255, 0)",},{"scope": "text.format.blue.yml","foreground": "rgb(51, 214, 255)",},{"scope": "text.format.gold.yml","foreground": "#ffb027",},{"scope": "text.format.bold.yml","font_style": "bold"},{"scope": "text.format.italic.yml","font_style": "italic"}]}"""
        with open(scheme_cache_path, "w") as f:
            f.write(rules)


def write_data_to_syntax(game_objects: Dict[str, ImperatorObject]):
    fake_syntax_path = (
        sublime.packages_path()
        + "/ImperatorTools/Imperator Script/ImperatorSyntax.fake-sublime-syntax"
    )
    real_syntax_path = (
        sublime.packages_path()
        + "/ImperatorTools/Imperator Script/ImperatorSyntax.sublime-syntax"
    )
    with open(fake_syntax_path, "r") as file:
        lines = file.read()

    manager = GameObjectManager()

    # Append all game objects to auto-generated-content section
    lines += write_syntax(
        game_objects[manager.scripted_trigger.name].keys(),
        "Scripted Triggers",
        "string.scripted.trigger",
    )
    lines += write_syntax(
        game_objects[manager.scripted_modifier.name].keys(),
        "Scripted Triggers",
        "string.scripted.modifier",
    )
    lines += write_syntax(
        game_objects[manager.scripted_list_triggers.name].keys(),
        "Scripted List",
        "string.scripted.list",
    )
    lines += write_syntax(
        game_objects[manager.scripted_effect.name].keys(),
        "Scripted Effects",
        "keyword.scripted.effect",
    )
    lines += write_syntax(
        game_objects[manager.scripted_list_effects.name].keys(),
        "Scripted Effects",
        "keyword.scripted.list",
    )
    lines += write_syntax(
        game_objects[manager.script_value.name].keys(),
        "Scripted Values",
        "storage.type.script.value",
    )

    # All GameObjects get entity.name scope
    lines += write_syntax(
        game_objects[manager.ambition.name].keys(),
        "Ambition",
        "entity.name.imperator.ambition",
    )
    lines += write_syntax(
        game_objects[manager.building.name].keys(),
        "Building",
        "entity.name.imperator.building",
    )
    lines += write_syntax(
        game_objects[manager.culture.name].keys(),
        "Culture",
        "entity.name.imperator.culture",
    )
    lines += write_syntax(
        game_objects[manager.culture_group.name].keys(),
        "Culture Group",
        "entity.name.imperator.culture.group",
    )
    lines += write_syntax(
        game_objects[manager.death_reason.name].keys(),
        "Death Reason",
        "entity.name.imperator.death.reason",
    )
    lines += write_syntax(
        game_objects[manager.deity.name].keys(), "Deity", "entity.name.imperator.deity"
    )
    lines += write_syntax(
        game_objects[manager.diplo_stance.name].keys(),
        "Diplomatic Stance",
        "entity.name.imperator.diplo.stance",
    )
    lines += write_syntax(
        game_objects[manager.econ_policy.name].keys(),
        "Economic Policy",
        "entity.name.imperator.econ.policy",
    )
    lines += write_syntax(
        game_objects[manager.event_pic.name].keys(),
        "Event Picture",
        "entity.name.imperator.event.pic",
    )
    lines += write_syntax(
        game_objects[manager.event_theme.name].keys(),
        "Event Theme",
        "entity.name.imperator.event.theme",
    )
    lines += write_syntax(
        game_objects[manager.named_colors.name].keys(),
        "Named Colors",
        "entity.name.named.colors",
    )
    lines += write_syntax(
        game_objects[manager.government.name].keys(),
        "Government",
        "entity.name.imperator.government",
    )
    lines += write_syntax(
        game_objects[manager.governor_policy.name].keys(),
        "Governor Policy",
        "entity.name.imperator.governor.policy",
    )
    lines += write_syntax(
        game_objects[manager.heritage.name].keys(),
        "Heritage",
        "entity.name.imperator.heritage",
    )
    lines += write_syntax(
        game_objects[manager.idea.name].keys(), "Idea", "entity.name.imperator.idea"
    )
    lines += write_syntax(
        game_objects[manager.invention.name].keys(),
        "Invention",
        "entity.name.imperator.invention",
    )
    lines += write_syntax(
        game_objects[manager.law.name].keys(), "Law", "entity.name.imperator.law"
    )
    lines += write_syntax(
        game_objects[manager.legion_distinction.name].keys(),
        "Legion Distinction",
        "entity.name.imperator.legion.distinction",
    )
    lines += write_syntax(
        game_objects[manager.levy_template.name].keys(),
        "Levy Template",
        "entity.name.imperator.levy.template",
    )
    lines += write_syntax(
        game_objects[manager.loyalty.name].keys(),
        "Loyalty",
        "entity.name.imperator.loyalty",
    )
    lines += write_syntax(
        game_objects[manager.mil_tradition.name].keys(),
        "Military Tradition",
        "entity.name.imperator.mil.tradition",
    )
    lines += write_syntax(
        game_objects[manager.modifier.name].keys(),
        "Modifier",
        "entity.name.imperator.modifier",
    )
    lines += write_syntax(
        game_objects[manager.opinion.name].keys(),
        "Opinion",
        "entity.name.imperator.opinion",
    )
    lines += write_syntax(
        game_objects[manager.office.name].keys(),
        "Office",
        "entity.name.imperator.office",
    )
    lines += write_syntax(
        game_objects[manager.party.name].keys(), "Party", "entity.name.imperator.party"
    )
    lines += write_syntax(
        game_objects[manager.pop.name].keys(), "Pop Type", "entity.name.imperator.pop"
    )
    lines += write_syntax(
        game_objects[manager.price.name].keys(), "Price", "entity.name.imperator.price"
    )
    lines += write_syntax(
        game_objects[manager.province_rank.name].keys(),
        "Province Rank",
        "entity.name.imperator.province.rank",
    )
    lines += write_syntax(
        game_objects[manager.religion.name].keys(),
        "Religion",
        "entity.name.imperator.religion",
    )
    lines += write_syntax(
        game_objects[manager.subject_type.name].keys(),
        "Subject Type",
        "entity.name.imperator.subject.type",
    )
    lines += write_syntax(
        game_objects[manager.tech_table.name].keys(),
        "Technology Table",
        "entity.name.imperator.tech.table",
    )
    lines += write_syntax(
        game_objects[manager.terrain.name].keys(),
        "Terrain",
        "entity.name.imperator.terrain",
    )
    lines += write_syntax(
        game_objects[manager.trade_good.name].keys(),
        "Trade Good",
        "entity.name.imperator.trade.good",
    )
    lines += write_syntax(
        game_objects[manager.trait.name].keys(), "Trait", "entity.name.imperator.trait"
    )
    lines += write_syntax(
        game_objects[manager.unit.name].keys(), "Unit", "entity.name.imperator.unit"
    )
    lines += write_syntax(
        game_objects[manager.war_goal.name].keys(),
        "War Goal",
        "entity.name.imperator.war.goal",
    )
    lines += write_syntax(
        game_objects[manager.mission.name].keys(),
        "Mission",
        "entity.name.imperator.mission",
    )
    lines += write_syntax(
        game_objects[manager.mission_task.name].keys(),
        "Mission Task",
        "entity.name.imperator.mission.task",
    )
    lines += write_syntax(
        game_objects[manager.mission.name].keys(),
        "Mission",
        "entity.name.imperator.mission",
    )
    lines += write_syntax(
        game_objects[manager.area.name].keys(), "Area", "entity.name.imperator.area"
    )
    lines += write_syntax(
        game_objects[manager.region.name].keys(),
        "Region",
        "entity.name.imperator.region",
    )
    lines += write_syntax(
        game_objects[manager.scripted_gui.name].keys(),
        "Scripted Gui",
        "entity.name.imperator.scripted.gui",
    )
    lines += write_syntax(
        game_objects[manager.custom_loc.name].keys(),
        "Custom Loc",
        "entity.name.imperator.custom.loc",
    )

    with open(real_syntax_path, "r") as file:
        real_lines = file.read()

    if real_lines != lines:
        with open(real_syntax_path, "w", encoding="utf-8") as file:
            file.write(lines)


def write_syntax(li: List[str], header: str, scope: str):
    string = ""
    count = 0
    string += f"\n    # Generated {header}\n    - match: \\b("
    for i in li:
        count += 1
        # Count is needed to split because columns are waaay too long for syntax regex
        if count == 0:
            string = f")\\b\n      scope: {scope}\n"
            string += f"    # Generated {header}\n    - match: \\b({i}|"
        elif count == 75:
            string += f")\\b\n      scope: {scope}\n"
            string += f"    # Generated {header}\n    - match: \\b({i}|"
            count = 1
        else:
            string += f"{i}|"
    string += f")\\b\n      scope: {scope}"
    return string
