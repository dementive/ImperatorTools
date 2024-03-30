"""
Code related to loading, saving, and caching imperator game objects
"""
import sublime
import os
import hashlib

from ImperatorTools.object_cache import GameObjectCache
from .jomini import dict_to_game_object as make_object
from .utils import get_default_game_objects


def check_mod_for_changes(imperator_mod_files):
    """
    Check if any changes have been made to mod files
    if changes have been made new game objects need to be generated and cached
    """
    object_cache_path = sublime.packages_path() + f"/ImperatorTools/object_cache.py"
    if os.stat(object_cache_path).st_size < 200:
        # If there are no objects in the cache, they need to be created
        return True
    mod_cache_path = sublime.packages_path() + f"/ImperatorTools/mod_cache.txt"
    with open(mod_cache_path, "r") as f:
        # Save lines before writing
        mod_cache = "".join(f.readlines())
    with open(mod_cache_path, "w") as f:
        # Clear
        f.write("")

    # Add the names and output of os.stat.st_mtime together for all the files in your current mods into stats_string
    for path in imperator_mod_files:
        stats_dict = dict()
        mod_name = path.replace("\\", "/").rstrip("/").rpartition("/")[2]
        for dirpath, dirnames, filenames in os.walk(path):
            mod_files = [
                x for x in filenames if x.endswith(".txt") or x.endswith(".gui")
            ]
            if mod_files:
                for i, j in enumerate(mod_files):
                    full_path = dirpath + "/" + mod_files[i]
                    stats_dict[full_path] = os.stat(full_path).st_mtime
        stats_string = str()
        for i in stats_dict:
            value = stats_dict[i]
            stats_string += f"{mod_name}{value}"

        # Encode stats_string and save it for later use
        with open(mod_cache_path, "a") as f:
            f.write(hashlib.sha256(stats_string.encode()).hexdigest())
            f.write("\n")

    with open(mod_cache_path, "r") as f:
        # Save written mod classes
        new_mod_cache = "".join(f.readlines())

    return True if mod_cache != new_mod_cache else False


def get_objects_from_cache():
    object_cache = GameObjectCache()
    game_objects = get_default_game_objects()

    for i in game_objects:
        game_objects[i] = make_object(getattr(object_cache, i))

    return game_objects


def cache_all_objects(game_objects):
    # Write all generated objects to cache
    path = sublime.packages_path() + f"/ImperatorTools/object_cache.py"
    with open(path, "w") as f:
        f.write("class GameObjectCache:\n\tdef __init__(self):")
        for i in game_objects:
            f.write(f"\n\t\tself.{i} = {game_objects[i].to_json()}")


def handle_image_cache(settings):
    cache_size_limit = settings.get("MaxImageCacheSize")
    cache = sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/"
    cache_files = [x for x in os.listdir(cache) if x.endswith(".png")]
    if len(cache_files) > cache_size_limit:
        for i in cache_files:
            os.remove(os.path.join(cache, i))
        sublime.status_message("Cleared Image Cache")


def add_color_scheme_scopes():
    # Add scopes for yml text formatting to color scheme
    DEFAULT_CS = "Packages/Color Scheme - Default/Monokai.sublime-color-scheme"
    prefs = sublime.load_settings("Preferences.sublime-settings")
    cs = prefs.get("color_scheme", DEFAULT_CS)
    scheme_cache_path = os.path.join(
        sublime.packages_path(), "User", "PdxTools", cs
    ).replace("tmTheme", "sublime-color-scheme")
    if not os.path.exists(scheme_cache_path):
        os.makedirs(os.path.dirname(scheme_cache_path), exist_ok=True)
        rules = """{"variables": {}, "globals": {},"rules": [{"scope": "text.format.white.yml","foreground": "rgb(250, 250, 250)",},{"scope": "text.format.grey.yml","foreground": "rgb(173, 165, 160)",},{"scope": "text.format.red.yml","foreground": "rgb(210, 40, 40)",},{"scope": "text.format.green.yml","foreground": "rgb(40, 210, 40)",},{"scope": "text.format.yellow.yml","foreground": "rgb(255, 255, 0)",},{"scope": "text.format.blue.yml","foreground": "rgb(51, 214, 255)",},{"scope": "text.format.gold.yml","foreground": "#ffb027",},{"scope": "text.format.bold.yml","font_style": "bold"},{"scope": "text.format.italic.yml","font_style": "italic"}]}"""
        with open(scheme_cache_path, "w") as f:
            f.write(rules)


def write_data_to_syntax(game_objects):
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

    # Append all game objects to auto-generated-content section
    lines += write_syntax(
        game_objects["scripted_trigger"].keys(),
        "Scripted Triggers",
        "string.scripted.trigger",
    )
    lines += write_syntax(
        game_objects["scripted_modifier"].keys(),
        "Scripted Triggers",
        "string.scripted.modifier",
    )
    lines += write_syntax(
        game_objects["scripted_list_triggers"].keys(),
        "Scripted List",
        "string.scripted.list",
    )
    lines += write_syntax(
        game_objects["scripted_effect"].keys(),
        "Scripted Effects",
        "keyword.scripted.effect",
    )
    lines += write_syntax(
        game_objects["scripted_list_effects"].keys(),
        "Scripted Effects",
        "keyword.scripted.list",
    )
    lines += write_syntax(
        game_objects["script_value"].keys(),
        "Scripted Values",
        "storage.type.script.value",
    )

    # All GameObjects get entity.name scope
    lines += write_syntax(
        game_objects["ambition"].keys(), "Ambition", "entity.name.imperator.ambition"
    )
    lines += write_syntax(
        game_objects["building"].keys(), "Building", "entity.name.imperator.building"
    )
    lines += write_syntax(
        game_objects["culture"].keys(), "Culture", "entity.name.imperator.culture"
    )
    lines += write_syntax(
        game_objects["culture_group"].keys(),
        "Culture Group",
        "entity.name.imperator.culture.group",
    )
    lines += write_syntax(
        game_objects["death_reason"].keys(),
        "Death Reason",
        "entity.name.imperator.death.reason",
    )
    lines += write_syntax(
        game_objects["deity"].keys(), "Deity", "entity.name.imperator.deity"
    )
    lines += write_syntax(
        game_objects["diplo_stance"].keys(),
        "Diplomatic Stance",
        "entity.name.imperator.diplo.stance",
    )
    lines += write_syntax(
        game_objects["econ_policy"].keys(),
        "Economic Policy",
        "entity.name.imperator.econ.policy",
    )
    lines += write_syntax(
        game_objects["event_pic"].keys(),
        "Event Picture",
        "entity.name.imperator.event.pic",
    )
    lines += write_syntax(
        game_objects["event_theme"].keys(),
        "Event Theme",
        "entity.name.imperator.event.theme",
    )
    lines += write_syntax(
        game_objects["named_colors"].keys(), "Named Colors", "entity.name.named.colors"
    )
    lines += write_syntax(
        game_objects["government"].keys(),
        "Government",
        "entity.name.imperator.government",
    )
    lines += write_syntax(
        game_objects["governor_policy"].keys(),
        "Governor Policy",
        "entity.name.imperator.governor.policy",
    )
    lines += write_syntax(
        game_objects["heritage"].keys(), "Heritage", "entity.name.imperator.heritage"
    )
    lines += write_syntax(
        game_objects["idea"].keys(), "Idea", "entity.name.imperator.idea"
    )
    lines += write_syntax(
        game_objects["invention"].keys(), "Invention", "entity.name.imperator.invention"
    )
    lines += write_syntax(
        game_objects["law"].keys(), "Law", "entity.name.imperator.law"
    )
    lines += write_syntax(
        game_objects["legion_distinction"].keys(),
        "Legion Distinction",
        "entity.name.imperator.legion.distinction",
    )
    lines += write_syntax(
        game_objects["levy_template"].keys(),
        "Levy Template",
        "entity.name.imperator.levy.template",
    )
    lines += write_syntax(
        game_objects["loyalty"].keys(), "Loyalty", "entity.name.imperator.loyalty"
    )
    lines += write_syntax(
        game_objects["mil_tradition"].keys(),
        "Military Tradition",
        "entity.name.imperator.mil.tradition",
    )
    lines += write_syntax(
        game_objects["modifier"].keys(), "Modifier", "entity.name.imperator.modifier"
    )
    lines += write_syntax(
        game_objects["opinion"].keys(), "Opinion", "entity.name.imperator.opinion"
    )
    lines += write_syntax(
        game_objects["office"].keys(), "Office", "entity.name.imperator.office"
    )
    lines += write_syntax(
        game_objects["party"].keys(), "Party", "entity.name.imperator.party"
    )
    lines += write_syntax(
        game_objects["pop"].keys(), "Pop Type", "entity.name.imperator.pop"
    )
    lines += write_syntax(
        game_objects["price"].keys(), "Price", "entity.name.imperator.price"
    )
    lines += write_syntax(
        game_objects["province_rank"].keys(),
        "Province Rank",
        "entity.name.imperator.province.rank",
    )
    lines += write_syntax(
        game_objects["religion"].keys(), "Religion", "entity.name.imperator.religion"
    )
    lines += write_syntax(
        game_objects["subject_type"].keys(),
        "Subject Type",
        "entity.name.imperator.subject.type",
    )
    lines += write_syntax(
        game_objects["tech_table"].keys(),
        "Technology Table",
        "entity.name.imperator.tech.table",
    )
    lines += write_syntax(
        game_objects["terrain"].keys(), "Terrain", "entity.name.imperator.terrain"
    )
    lines += write_syntax(
        game_objects["trade_good"].keys(),
        "Trade Good",
        "entity.name.imperator.trade.good",
    )
    lines += write_syntax(
        game_objects["trait"].keys(), "Trait", "entity.name.imperator.trait"
    )
    lines += write_syntax(
        game_objects["unit"].keys(), "Unit", "entity.name.imperator.unit"
    )
    lines += write_syntax(
        game_objects["war_goal"].keys(), "War Goal", "entity.name.imperator.war.goal"
    )
    lines += write_syntax(
        game_objects["mission"].keys(), "Mission", "entity.name.imperator.mission"
    )
    lines += write_syntax(
        game_objects["mission_task"].keys(),
        "Mission Task",
        "entity.name.imperator.mission.task",
    )
    lines += write_syntax(
        game_objects["mission"].keys(), "Mission", "entity.name.imperator.mission"
    )
    lines += write_syntax(
        game_objects["area"].keys(), "Area", "entity.name.imperator.area"
    )
    lines += write_syntax(
        game_objects["region"].keys(), "Region", "entity.name.imperator.region"
    )
    lines += write_syntax(
        game_objects["scripted_gui"].keys(), "Scripted Gui", "entity.name.imperator.scripted.gui"
    )
    lines += write_syntax(
        game_objects["custom_loc"].keys(), "Custom Loc", "entity.name.imperator.custom.loc"
    )

    with open(real_syntax_path, "r") as file:
        real_lines = file.read()

    if real_lines != lines:
        with open(real_syntax_path, "w", encoding="utf-8") as file:
            file.write(lines)


def write_syntax(li, header, scope):
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
