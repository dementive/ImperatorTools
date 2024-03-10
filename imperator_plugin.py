import sublime, sublime_plugin
import os, re, time, webbrowser, threading, sys, subprocess
import struct
import json
import Default.exec
from colorsys import hsv_to_rgb
from collections import deque
import hashlib
from .jomini import GameObjectBase, PdxScriptObjectType, PdxScriptObject
from .jomini import dict_to_game_object as make_object
from .Utilities.game_data import GameData
from .object_cache import GameObjectCache
from .ImperatorTiger.tiger import TigerJsonObject

# ----------------------------------
# -          Plugin Setup          -
# ----------------------------------
settings = sublime.Settings(9999)
imperator_files_path = ""
imperator_mod_files = list()
tiger_objects = dict()


# Imperator Rome Game Object Class implementations


class ImperatorAmbition(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\ambitions")


class ImperatorBuilding(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\buildings")


class ImperatorCultureGroup(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\cultures")


class ImperatorCulture(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=2)
        self.get_data("common\\cultures")


class ImperatorDeathReason(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\deathreasons")


class ImperatorDeity(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\deities")


class ImperatorDiplomaticStance(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\diplomatic_stances")


class ImperatorEconomicPolicy(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\economic_policies")


class ImperatorEventPicture(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\event_pictures")


class ImperatorEventTheme(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\event_themes")


class ImperatorGovernment(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\governments")


class ImperatorGovernorPolicy(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\governor_policies")


class ImperatorHeritage(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\heritage")


class ImperatorIdea(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\ideas")


class ImperatorInvention(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\inventions")


class ImperatorLaw(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\laws")


class ImperatorLegionDistinction(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\legion_distinctions")


class ImperatorLevyTemplate(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\levy_templates")


class ImperatorLoyalty(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\loyalty")


class ImperatorMilitaryTradition(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\military_traditions")


class ImperatorMission(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\missions")


class ImperatorMissionTask(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\missions")


class ImperatorModifier(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files,
            imperator_files_path,
            ignored_files=["00_hardcoded.txt", "00_hardcoded_inv.txt"],
        )
        self.get_data("common\\modifiers")


class ImperatorOpinion(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\opinions")


class ImperatorOffice(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\offices")


class ImperatorParty(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\party_types")


class ImperatorPop(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\pop_types")


class ImperatorPrice(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\prices")


class ImperatorProvinceRank(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\province_ranks")


class ImperatorReligion(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\religions")


class ImperatorScriptValue(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\script_values")


class ImperatorScriptedEffect(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_effects")


class ImperatorScriptedModifier(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_modifiers")


class ImperatorScriptedTrigger(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_triggers")


class ImperatorSubjectType(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\subject_types")


class ImperatorTechTable(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\technology_tables")


class ImperatorTerrain(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\terrain_types")


class ImperatorTradeGood(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\trade_goods")


class ImperatorTrait(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\traits")


class ImperatorUnit(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\units")


class ImperatorWargoal(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\wargoals")


class ImperatorArea(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files, imperator_files_path, included_files=["areas.txt"]
        )
        self.get_data("map_data")


class ImperatorRegion(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files, imperator_files_path, included_files=["regions.txt"]
        )
        self.get_data("map_data")


class ImperatorScriptedList(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_lists")


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))


class PdxColorObject(PdxScriptObject):
    def __init__(self, key, path, line, color):
        super().__init__(key, path, line)
        self.color = color
        self.rgb_color = self.get_rgb_color()

    def get_rgb_color(self):
        """
        Color Formats:
                color1 = hsv { 1.0 1.0 1.0 }
                color2 = hsv360 { 360 100 100 }
                color3 = { 255 255 255 }
                color4 = rgb { 255 255 255 }
                color5 = hex { aabbccdd }
        This function merges all of these formats into one and returns (r, g, b) tuple
        """
        object_color = self.color
        try:
            if object_color.startswith("rgb") or object_color.startswith("{"):
                split_color = object_color.split("{")[1].replace(" }", "")
                split_color = split_color.split(" ")
                r = float(split_color[1].replace("o", ""))
                g = float(split_color[2].replace("o", ""))
                b = float(split_color[3].replace("o", ""))
            if re.search(r"\bhsv\b", object_color):
                split_color = object_color.split("{")[1].replace(" }", "")
                split_color = object_color.split(" ")
                h = float(split_color[2].replace("o", ""))
                s = float(split_color[3].replace("o", ""))
                v = float(split_color[4].replace("o", ""))
                rgb = hsv2rgb(h, s, v)
                r = rgb[0]
                g = rgb[1]
                b = rgb[2]
            if re.search(r"\bhsv360\b", object_color):
                split_color = object_color.split("{")[1].replace(" }", "")
                split_color = object_color.split(" ")
                h = float(split_color[2].replace("o", "")) / 360
                s = float(split_color[3].replace("o", "")) / 100
                v = float(split_color[4].replace("o", "")) / 100
                rgb = hsv2rgb(h, s, v)
                r = rgb[0]
                g = rgb[1]
                b = rgb[2]
                if (
                    split_color[2] == "187"
                    and split_color[3] == "83"
                    and split_color[4] == "146"
                ):
                    r = 230
                    g = 0
                    b = 230
            if re.search(r"\bhex\b", object_color):
                split_color = object_color.split("{")[1].replace(" }", "")
                split_color = split_color.split("#").replace(" ", "")
                return tuple(int(split_color[i : i + 2], 16) for i in (0, 2, 4))
        except IndexError:
            r = 255
            g = 255
            b = 0
        return (r, g, b)

    def __eq__(self, other):
        if isinstance(other, ImperatorNamedColor):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, ImperatorNamedColor):
            return self.key < other.key
        elif isinstance(other, str):
            return self.key < other
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, ImperatorNamedColor):
            return self.key > other.key
        elif isinstance(other, str):
            return self.key > other
        else:
            return False


def make_named_color_object(objects: dict) -> GameObjectBase:
    obj_list = list()
    for i in objects:
        obj_list.append(PdxColorObject(i, objects[i][0], objects[i][1], objects[i][2]))
    game_object = GameObjectBase()
    game_object.main = PdxScriptObjectType(obj_list)
    return game_object


class ImperatorNamedColor(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\named_colors")

    def to_dict(self) -> dict:
        d = dict()
        for i in self.main.objects:
            d[i.key] = [i.path, i.line, i.color]
        return d

    def get_pdx_object_list(self, path: str) -> PdxScriptObjectType:
        obj_list = list()
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in [f for f in filenames if f.endswith(".txt")]:
                if filename in self.ignored_files:
                    continue
                file_path = os.path.join(dirpath, filename)
                if self.included_files:
                    if filename not in self.included_files:
                        continue
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    for i, line in enumerate(file):
                        if self.should_read(line):
                            found_item = re.search(
                                r"([A-Za-z_][A-Za-z_0-9]*)\s*=(.*)", line
                            )
                            if found_item and found_item.groups()[0]:
                                item_color = found_item.groups()[1]
                                found_item = found_item.groups()[0]
                                item_color = item_color.strip().split("#")[0]
                                item_color = item_color.rpartition("}")[0]
                                if not item_color:
                                    continue
                                else:
                                    item_color = item_color.replace("\t", " ") + " }"
                                    item_color = re.sub(r"\s+", " ", item_color)
                                    obj_list.append(
                                        PdxColorObject(
                                            found_item, file_path, i + 1, item_color
                                        )
                                    )
        return PdxScriptObjectType(obj_list)

    def should_read(self, x: str) -> bool:
        # Check if a line should be read
        if re.search(r"([A-Za-z_][A-Za-z_0-9]*)\s*=", x):
            return True
        return False


# Game Data class
GameData = GameData()

base_object = GameObjectBase()

# global dictionary of game objects used everywhere
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

# Function to fill all global game objects that get set in non-blocking async function on plugin_loaded
# Setting all the objects can be slow and doing it on every hover (when they are actually used) is even slower,
# so loading it all in on plugin init makes popups actually responsive


def check_mod_for_changes():
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

        with open(mod_cache_path, "a") as f:
            f.write(hashlib.sha256(stats_string.encode()).hexdigest())
            f.write("\n")

    with open(mod_cache_path, "r") as f:
        # Save written mod classes
        new_mod_cache = "".join(f.readlines())

    return True if mod_cache != new_mod_cache else False


def get_objects_from_cache():
    global game_objects
    object_cache = GameObjectCache()

    for i in game_objects:
        game_objects[i] = make_object(getattr(object_cache, i))


def cache_all_objects():
    # Write all generated objects to cache
    path = sublime.packages_path() + f"/ImperatorTools/object_cache.py"
    with open(path, "w") as f:
        f.write("class GameObjectCache:\n\tdef __init__(self):")
        for i in game_objects:
            f.write(f"\n\t\tself.{i} = {game_objects[i].to_json()}")


def create_game_objects():
    t0 = time.time()

    def load_first():
        global game_objects
        game_objects["ambition"] = ImperatorAmbition()
        game_objects["building"] = ImperatorBuilding()
        game_objects["culture"] = ImperatorCulture()
        game_objects["culture_group"] = ImperatorCultureGroup()
        game_objects["death_reason"] = ImperatorDeathReason()
        game_objects["deity"] = ImperatorDeity()
        game_objects["diplo_stance"] = ImperatorDiplomaticStance()
        game_objects["econ_policy"] = ImperatorEconomicPolicy()
        game_objects["event_pic"] = ImperatorEventPicture()

    def load_second():
        global game_objects
        game_objects["event_theme"] = ImperatorEventTheme()
        game_objects["government"] = ImperatorGovernment()
        game_objects["governor_policy"] = ImperatorGovernorPolicy()
        game_objects["heritage"] = ImperatorHeritage()
        game_objects["idea"] = ImperatorIdea()
        game_objects["invention"] = ImperatorInvention()
        game_objects["law"] = ImperatorLaw()
        game_objects["legion_distinction"] = ImperatorLegionDistinction()

    def load_third():
        global game_objects
        game_objects["levy_template"] = ImperatorLevyTemplate()
        game_objects["loyalty"] = ImperatorLoyalty()
        game_objects["mil_tradition"] = ImperatorMilitaryTradition()
        game_objects["modifier"] = ImperatorModifier()
        game_objects["opinion"] = ImperatorOpinion()
        game_objects["office"] = ImperatorOffice()
        game_objects["party"] = ImperatorParty()
        game_objects["pop"] = ImperatorPop()
        game_objects["scripted_list_triggers"] = ImperatorScriptedList()
        game_objects["scripted_list_effects"] = ImperatorScriptedList()

        tri_list = []
        for obj in game_objects["scripted_list_triggers"]:
            tri_list.append(PdxScriptObject("any_" + obj.key, obj.path, obj.line))
        game_objects["scripted_list_triggers"].clear()
        for i in tri_list:
            game_objects["scripted_list_triggers"].add(i)

        ef_list = []
        for obj in game_objects["scripted_list_effects"]:
            ef_list.append(PdxScriptObject(f"random_{obj.key}", obj.path, obj.line))
            ef_list.append(PdxScriptObject(f"every_{obj.key}", obj.path, obj.line))
            ef_list.append(PdxScriptObject(f"ordered_{obj.key}", obj.path, obj.line))
        game_objects["scripted_list_effects"].clear()

        for i in ef_list:
            game_objects["scripted_list_effects"].add(i)
        for i in game_objects["scripted_list_effects"].keys():
            GameData.EffectsList[i] = "Scripted list effect"
        for i in game_objects["scripted_list_triggers"].keys():
            GameData.TriggersList[i] = "Scripted list trigger"

    def load_fourth():
        global game_objects
        game_objects["price"] = ImperatorPrice()
        game_objects["province_rank"] = ImperatorProvinceRank()
        game_objects["religion"] = ImperatorReligion()
        game_objects["script_value"] = ImperatorScriptValue()
        game_objects["scripted_effect"] = ImperatorScriptedEffect()
        game_objects["scripted_modifier"] = ImperatorScriptedModifier()
        game_objects["scripted_trigger"] = ImperatorScriptedTrigger()
        game_objects["subject_type"] = ImperatorSubjectType()
        game_objects["named_colors"] = ImperatorNamedColor()

    def load_fifth():
        global game_objects
        game_objects["terrain"] = ImperatorTerrain()
        game_objects["trade_good"] = ImperatorTradeGood()
        game_objects["trait"] = ImperatorTrait()
        game_objects["unit"] = ImperatorUnit()
        game_objects["war_goal"] = ImperatorWargoal()
        game_objects["tech_table"] = ImperatorTechTable()
        game_objects["mission"] = ImperatorMission()
        game_objects["mission_task"] = ImperatorMissionTask()
        game_objects["area"] = ImperatorArea()
        game_objects["region"] = ImperatorRegion()

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
    sublime.set_timeout_async(lambda: write_data_to_syntax(), 0)

    t1 = time.time()
    print("Time to load Imperator Rome objects: {:.3f} seconds".format(t1 - t0))

    # Cache created objects
    sublime.set_timeout_async(lambda: cache_all_objects(), 0)


def plugin_loaded():
    global settings, imperator_files_path, imperator_mod_files
    settings = sublime.load_settings("Imperator Syntax.sublime-settings")
    imperator_files_path = settings.get("ImperatorFilesPath")
    imperator_mod_files = settings.get("PathsToModFiles")
    if check_mod_for_changes():
        # Create new objects
        sublime.set_timeout_async(lambda: create_game_objects(), 0)
        sublime.active_window().run_command("run_tiger")
    else:
        # Load cached objects
        get_objects_from_cache()
        sublime.set_timeout_async(lambda: get_tiger_objects(), 0)

    cache_size_limit = settings.get("MaxImageCacheSize")
    cache = sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/"
    cache_files = [x for x in os.listdir(cache) if x.endswith(".png")]
    if len(cache_files) > cache_size_limit:
        for i in cache_files:
            os.remove(os.path.join(cache, i))
        sublime.status_message("Cleared Image Cache")
    add_color_scheme_scopes()


def get_tiger_objects():
    global tiger_objects
    path = sublime.packages_path() + f"/ImperatorTools/tiger.json"
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for i in data:
        # Add location data to list in the same way the display() function does so the indexes stay the same
        previous_locations = list()
        for j in i["locations"]:
            fullpath = j["fullpath"]
            if fullpath not in previous_locations:
                if fullpath in tiger_objects:
                    old_data = tiger_objects[j["fullpath"]]
                    new_data = {
                        "severity": i["severity"],
                        "key": i["key"],
                        "info": i["info"],
                        "message": i["message"],
                        "linenr": j["linenr"],
                        "column": j["column"],
                        "length": j["length"],
                    }
                    if type(old_data) == list:
                        old_data.append(new_data)
                    else:
                        old_data = [old_data, new_data]

                    tiger_objects[j["fullpath"]] = old_data
                else:
                    tiger_objects[j["fullpath"]] = {
                        "severity": i["severity"],
                        "key": i["key"],
                        "info": i["info"],
                        "message": i["message"],
                        "linenr": j["linenr"],
                        "column": j["column"],
                        "length": j["length"],
                    }

            previous_locations.append(j["fullpath"])


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


def write_data_to_syntax():
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


# css for non-documentation popups
css_basic_style = """
    body {
        font-family: system;
        margin: 0;
        padding: 0.35rem;
        background-color: rgb(25, 25, 25);
    }
    p {
        font-size: 1.0rem;
        margin-top: 5;
        margin-bottom: 5;
    }
    h1 {
        font-size: 1.2rem;
        margin: 0;
        padding-bottom: 0.05rem;
    }
    h2 {
        font-size: 1.1rem;
        margin: 0;
    }
    a {
        font-size: 1.0rem;
    }
    span {
        padding-right: 0.3rem;
    }
    div {
        padding: 0.1rem;
    }
    .icon {
        text-decoration: none;
        font-size: 1em;
    }
    .variable {
        font-size: 1.0rem;
        color: rgb(150, 150, 150);
    }
    .codebox {
        border: 2px solid rgb(5, 5, 5);
        border-style: groove;
        background-color: rgb(40, 40, 40);
        white-space: pre-line;
        padding: 5px;
        margin-right: 8px;
        margin-left: 1px;
        margin-top: 2px;
        display: inline-block;
        font-family: "Courier New", Courier, monospace;
    }
    .box-for-codebox {
        margin-bottom: 14px;
    }
    .codedesc {
        margin-left: 4px;
        margin-right: 4px;
        margin-top: 2px;
        margin-bottom: 2px;
    }
    .code {
        font-family: monospace;
    }
    .code-header {
        margin-left: 5px;
    }
    /* Monokai color scheme text colors */
    .red-text {
        color: hsl(0, 93%, 59%);
    }
    .yellow-text {
        color: hsl(54, 70%, 68%);
    }
    .blue-text {
        color: hsl(170, 60%, 56%);
        font-style: italic;
    }
    .green-text {
        color: hsl(80, 76%, 53%);
    }
    .orange-text {
        color: hsl(32, 98%, 56%);
    }
    .purple-text {
        color: hsl(261, 100%, 75%);
    }
"""


class ImperatorCompletionsEventListener(sublime_plugin.EventListener):
    def __init__(self):
        self.trigger_field = False
        self.effect_field = False
        self.modifier_field = False
        self.mtth_field = False
        self.fields = {
            "ambition": [],
            "area": [],
            "building": [],
            "culture": [],
            "culture_group": [],
            "death_reason": [],
            "deity": [],
            "diplo_stance": [],
            "econ_policy": [],
            "event_pic": [],
            "event_theme": [],
            "government": [],
            "governor_policy": [],
            "heritage": [],
            "idea": [],
            "invention": [],
            "law": [],
            "legion_distinction": [],
            "levy_template": [],
            "loyalty": [],
            "mil_tradition": [],
            "mission": [],
            "mission_task": [],
            "modifier": [],
            "named_colors": [],
            "office": [],
            "opinion": [],
            "party": [],
            "pop": [],
            "price": [],
            "province_rank": [],
            "region": [],
            "religion": [],
            "subject_type": [],
            "tech_table": [],
            "terrain": [],
            "trade_good": [],
            "trait": [],
            "unit": [],
            "war_goal": [],
        }
        for field in self.fields.keys():
            setattr(self, field, False)

    def on_deactivated_async(self, view):
        """
        Remove field states when view loses focus
        if cursor was in a field in the old view but not the new view the completions will still be accurate
        save the id of the view so it can be readded when it regains focus
        """
        vid = view.id()
        for field, views in self.fields.items():
            if getattr(self, field):
                setattr(self, field, False)
                views.append(vid)

    def on_activated_async(self, view):
        vid = view.id()
        for field, views in self.fields.items():
            if vid in views:
                setattr(self, field, True)
                views.remove(vid)

    def create_completion_list(self, flag_name, completion_kind):
        if not getattr(self, flag_name, False):
            return None

        completions = game_objects[flag_name].keys()
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

        try:
            if view.syntax().name != "Imperator Script":
                return None
        except AttributeError:
            return None

        completion_flag_pairs = [
            ("ambition", (sublime.KIND_ID_FUNCTION, "A", "Ambitions")),
            ("area", (sublime.KIND_ID_SNIPPET, "A", "Areas")),
            ("building", (sublime.KIND_ID_FUNCTION, "B", "Buildings")),
            ("culture", (sublime.KIND_ID_TYPE, "C", "Culture Groups")),
            ("culture_group", (sublime.KIND_ID_VARIABLE, "C", "Cultures")),
            ("death_reason", (sublime.KIND_ID_KEYWORD, "D", "Death Reasons")),
            ("deity", (sublime.KIND_ID_TYPE, "D", "Deities")),
            ("diplo_stance", (sublime.KIND_ID_SNIPPET, "D", "Diplo Stances")),
            ("econ_policy", (sublime.KIND_ID_KEYWORD, "E", "Economic Policies")),
            ("event_pic", (sublime.KIND_ID_MARKUP, "E", "Event Picture")),
            ("event_theme", (sublime.KIND_ID_TYPE, "E", "Event Themes")),
            ("government", (sublime.KIND_ID_VARIABLE, "E", "Governements")),
            ("governor_policy", (sublime.KIND_ID_TYPE, "G", "Governor Policies")),
            ("heritage", (sublime.KIND_ID_VARIABLE, "G", "Heritages")),
            ("idea", (sublime.KIND_ID_SNIPPET, "G", "Ideas")),
            ("invention", (sublime.KIND_ID_MARKUP, "H", "Inventions")),
            ("law", (sublime.KIND_ID_VARIABLE, "I", "Laws")),
            ("legion_distinction", (sublime.KIND_ID_TYPE, "I", "Legion Distinction")),
            ("levy_template", (sublime.KIND_ID_SNIPPET, "L", "Levy Templates")),
            ("loyalty", (sublime.KIND_ID_VARIABLE, "L", "Loyalties")),
            ("mil_tradition", (sublime.KIND_ID_VARIABLE, "L", "Military Traditions")),
            ("mission", (sublime.KIND_ID_SNIPPET, "M", "Missions")),
            ("mission_task", (sublime.KIND_ID_SNIPPET, "M", "Mission Tasks")),
            ("modifier", (sublime.KIND_ID_MARKUP, "M", "Modifiers")),
            ("named_colors", (sublime.KIND_ID_VARIABLE, "N", "Named Colors")),
            ("office", (sublime.KIND_ID_NAMESPACE, "O", "Offices")),
            ("opinion", (sublime.KIND_ID_VARIABLE, "O", "Opinions")),
            ("party", (sublime.KIND_ID_TYPE, "P", "Parties")),
            ("pop", (sublime.KIND_ID_VARIABLE, "P", "Pops")),
            ("price", (sublime.KIND_ID_NAVIGATION, "P", "Prices")),
            ("province_rank", (sublime.KIND_ID_VARIABLE, "P", "Province Ranks")),
            ("region", (sublime.KIND_ID_SNIPPET, "R", "Regions")),
            ("religion", (sublime.KIND_ID_VARIABLE, "R", "Religions")),
            ("subject_type", (sublime.KIND_ID_SNIPPET, "S", "Subject Types")),
            ("tech_table", (sublime.KIND_ID_VARIABLE, "T", "Tech Tables")),
            ("terrain", (sublime.KIND_ID_SNIPPET, "T", "Terrains")),
            ("trade_good", (sublime.KIND_ID_KEYWORD, "T", "Trade Goods")),
            ("trait", (sublime.KIND_ID_VARIABLE, "T", "Traits")),
            ("unit", (sublime.KIND_ID_FUNCTION, "U", "Units")),
            ("war_goal", (sublime.KIND_ID_FUNCTION, "W", "War Goals")),
        ]

        for flag, completion in completion_flag_pairs:
            completion_list = self.create_completion_list(flag, completion)
            if completion_list is not None:
                return completion_list

        fname = view.file_name()
        if not fname:
            return

        if "script_values" in fname:
            e_list = []
            for i in GameData.EffectsList:
                e_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=GameData.EffectsList[i].split("<br>")[0],
                    )
                )
            t_list = []
            for i in GameData.TriggersList:
                t_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=GameData.TriggersList[i].split("<br>")[0],
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
                        details=GameData.PricesDict[key],
                    )
                    for key in sorted(GameData.PricesDict)
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
                        details=GameData.TriggersList[key].split("<br>")[0],
                    )
                    for key in sorted(GameData.TriggersList)
                ]
            )
        if self.effect_field or "scripted_effects" in fname:
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=GameData.EffectsList[key].split("<br>")[0],
                    )
                    for key in sorted(GameData.EffectsList)
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
                        details=GameData.ModifersList[key],
                        annotation=GameData.ModifersList[key].replace("Category: ", ""),
                    )
                    for key in sorted(GameData.ModifersList)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if "/events/" in fname:
            return sublime.CompletionList(
                GameData.EventsList,
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_REORDER,
            )
        return None

    # Get the index of a closing bracket in a string given the starting brackets index
    def getIndex(self, string, index):
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

    def get_regions(self, view, selector, view_str):
        start_brackets = view.find_by_selector(selector)
        return [
            sublime.Region(br.a, self.getIndex(view_str, br.a)) for br in start_brackets
        ]

    def simple_scope_match(self, view):
        selection = view.sel()
        if not selection[0].empty():
            return

        view_str = view.substr(sublime.Region(0, view.size()))

        # Get the starting bracket index from the syntax scopes
        trigger_regions = self.get_regions(view, "meta.trigger.bracket", view_str)
        effect_regions = self.get_regions(view, "meta.effect.bracket", view_str)
        value_regions = self.get_regions(view, "meta.value.bracket", view_str)
        modifier_regions = self.get_regions(view, "meta.modifier.bracket", view_str)

        self.show_status(selection[0].a, trigger_regions, "trigger", view)

        # Have to account for trigger fields inside of effect fields, definetly a better way to do this.
        for block in effect_regions:
            if block.a <= selection[0].a <= block.b:
                view.set_status("effect", "Effect Field")
                self.effect_field = True
                for block in trigger_regions:
                    if block.a <= selection[0].a <= block.b:
                        view.erase_status("effect")
                        self.effect_field = False
                        view.set_status("trigger", "Trigger Field")
                        self.trigger_field = True
                        break
                    else:
                        view.erase_status("trigger")
                        self.trigger_field = False
                break
            else:
                view.erase_status("effect")
                self.effect_field = False

        self.show_status(selection[0].a, modifier_regions, "modifier", view)

        self.show_status(selection[0].a, value_regions, "value", view)

        # For actual mtth fields that have a modifier = {} block inside of them, remove the modifier status
        if self.mtth_field and self.modifier_field:
            view.erase_status("modifier")

    def show_status(self, selection, regions, status, view):
        for block in regions:
            if block.a <= selection <= block.b:
                view.set_status(status, status.title() + " Field")
                if status == "trigger":
                    self.trigger_field = True
                elif status == "effect":
                    self.effect_field = True
                elif status == "modifier":
                    self.modifier_field = True
                elif status == "value":
                    self.mtth_field = True
                break
            else:
                view.erase_status(status)
                if status == "trigger":
                    self.trigger_field = False
                elif status == "effect":
                    self.effect_field = False
                elif status == "modifier":
                    self.modifier_field = False
                elif status == "value":
                    self.mtth_field = False

    def reset_shown(self):
        for i in self.fields.keys():
            setattr(self, i, False)

    def check_for_patterns_and_set_flag(
        self, patterns_list, flag_name, view, line, point
    ):
        for pattern in patterns_list:
            r = re.search(f'{pattern}\s?=\s?(")?', line)
            if r:
                y = 0
                idx = line.index(pattern) + view.line(point).a + len(pattern) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    setattr(self, flag_name, True)
                    view.run_command("auto_complete")
                    return True
        return False

    def check_pattern_and_set_flag(self, pattern, flag_name, view, line, point):
        if pattern in line:
            idx = line.index(pattern) + view.line(point).a + len(pattern)
            if idx == point:
                setattr(self, flag_name, True)
                view.run_command("auto_complete")

    def check_for_simple_completions(self, view, point):
        """
        Check if the current cursor position should trigger a autocompletion item
        this is for simple declarations like: remove_building = CursorHere
        """
        self.reset_shown()

        if view.substr(point) == "=":
            return

        line = view.substr(view.line(point))

        for patterns, flag in GameData.simple_completion_pattern_flag_pairs:
            if self.check_for_patterns_and_set_flag(patterns, flag, view, line, point):
                return

        for pattern, flag in GameData.simple_completion_scope_pattern_flag_pairs:
            self.check_pattern_and_set_flag(pattern, flag, view, line, point)

    def check_region_and_set_flag(
        self, selector, flag_name, view, view_str, point, string_check_and_move=None
    ):
        for br in view.find_by_selector(selector):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            s = view.substr(i)
            if string_check_and_move and string_check_and_move in s:
                fpoint = (
                    s.index(string_check_and_move) + len(string_check_and_move)
                ) + i.a
                if fpoint == point:
                    setattr(self, flag_name, True)
                    view.run_command("auto_complete")
            elif i.contains(point) and not string_check_and_move:
                setattr(self, flag_name, True)
                view.run_command("auto_complete")

    def check_for_complex_completions(self, view, point):
        view_str = view.substr(sublime.Region(0, view.size()))

        if "inventions" in view.file_name():
            for br in view.find_by_selector("meta.invention.bracket"):
                i = sublime.Region(br.a, self.getIndex(view_str, br.a))
                if i.contains(point):
                    self.inventions = True
                    view.run_command("auto_complete")

        selector_flag_pairs = [
            ("meta.op.mod.bracket", "opinion", "modifier = "),
            ("meta.party.bracket", "party", "party = "),
            ("meta.pop.type.bracket", "pop", "type = "),
            ("meta.subject.type.bracket", "subject_type", "type = "),
            ("meta.tech.table.bracket", "tech_table", "technology = "),
            ("meta.trade.good.bracket", "trade_good", "target = "),
            ("meta.trait.bracket", "trait"),
            ("meta.unit.bracket", "unit", "type = "),
        ]

        for pair in selector_flag_pairs:
            if len(pair) == 3:
                selector, flag, string_check_and_move = pair
                self.check_region_and_set_flag(
                    selector, flag, view, view_str, point, string_check_and_move
                )
            else:
                selector, flag = pair
                self.check_region_and_set_flag(selector, flag, view, view_str, point)

    def on_selection_modified_async(self, view):
        if not view:
            return

        try:
            if view.syntax().name != "Imperator Script":
                return
        except AttributeError:
            return

        self.simple_scope_match(view)
        # Only do when there is 1 selections, doens't make sense with multiple selections
        if len(view.sel()) == 1:
            self.check_for_simple_completions(view, view.sel()[0].a)
            self.check_for_complex_completions(view, view.sel()[0].a)


# ----------------------------------
# -     Text & Window Commands     -
# ----------------------------------


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


# ----------------------------------
# -            Validator           -
# ----------------------------------


class ValidatorOnSaveListener(sublime_plugin.EventListener):
    def __init__(self):
        self.view: sublime.View
        self.view_str = None

    def on_post_save_async(self, view):
        if view is None:
            return
        try:
            if view.syntax().name != "Imperator Script":
                return
        except AttributeError:
            return
        if settings.get("ScriptValidator") == False:
            return

        self.view = view
        self.view_str = view.substr(sublime.Region(0, view.size()))

        self.encoding_check()

    def encoding_check(self):
        # Check that the current filepath is in a folder that should use UTF-8 with BOM
        # If it should be UTF-8 with BOM and it is not create error panel
        path = self.view.file_name()
        # Coat of arms is the only files that are only UTF-8 not UTF-8 with BOM
        utf8_paths = re.search(r"(common/coat_of_arms)", path)
        bom_paths = re.search(r"(events|common|music|localization)", path)

        old_encoding = self.view.encoding()
        if not old_encoding == "UTF-8 with BOM":
            if bom_paths is not None and utf8_paths is None:
                # is not bom and should be
                self.view.set_encoding("UTF-8 with BOM")
                error_message = f"EncodingError: Encoding is {old_encoding}, files in {bom_paths.group()} should be UTF-8 with BOM, resave to fix."

                panel = self.create_error_panel()
                panel.set_read_only(False)
                panel.run_command("append", {"characters": error_message})
                panel.add_regions(
                    "bad_encoding",
                    [sublime.Region(27, 27 + len(old_encoding))],
                    "underline.bad",
                    flags=(
                        sublime.DRAW_SOLID_UNDERLINE
                        | sublime.DRAW_NO_FILL
                        | sublime.DRAW_NO_OUTLINE
                    ),
                )
                panel.add_regions(
                    "encoding",
                    [sublime.Region(len(panel) - 30, len(panel) - 16)],
                    "underline.good",
                    flags=(
                        sublime.DRAW_SOLID_UNDERLINE
                        | sublime.DRAW_NO_FILL
                        | sublime.DRAW_NO_OUTLINE
                    ),
                )
                panel.set_read_only(True)

            if utf8_paths is not None and not old_encoding == "UTF-8":
                # is not utf-8 and should be
                self.view.set_encoding("UTF-8")
                error_message = f"EncodingError: Encoding is {old_encoding}, files in {utf8_paths.group()} should be UTF-8, resave to fix."

                panel = self.create_error_panel()
                panel.set_read_only(False)
                panel.run_command("append", {"characters": error_message})
                # bad encoding
                panel.add_regions(
                    "bad_encoding",
                    [sublime.Region(27, 27 + len(old_encoding))],
                    "underline.bad",
                    flags=(
                        sublime.DRAW_SOLID_UNDERLINE
                        | sublime.DRAW_NO_FILL
                        | sublime.DRAW_NO_OUTLINE
                    ),
                )
                # new good encoding
                panel.add_regions(
                    "encoding",
                    [sublime.Region(len(panel) - 21, len(panel) - 16)],
                    "underline.good",
                    flags=(
                        sublime.DRAW_SOLID_UNDERLINE
                        | sublime.DRAW_NO_FILL
                        | sublime.DRAW_NO_OUTLINE
                    ),
                )
                panel.set_read_only(True)

    def create_error_panel(self):
        window = sublime.active_window()
        panel = window.create_output_panel("error", unlisted=True)
        panel.assign_syntax("scope:text.error")
        panel.settings().set("color_scheme", "ErrorPanel.hidden-color-scheme")
        panel.settings().set("gutter", False)
        window.run_command("show_panel", {"panel": "output.error"})
        window.focus_view(panel)
        return panel


# ----------------------------------
# -           Hover Docs           -
# ----------------------------------


def show_hover_docs(view, point, scope, collection):
    style = settings.get("DocsPopupStyle")
    if style == "dark":
        style = """
                    body {
                        font-family: system;
                        margin: 0;
                        padding: 0.35rem;
                        border: 0.2rem solid rgb(46, 46, 46);
                        background-color: rgb(5, 5, 5);
                    }
                    p {
                        font-size: 1.0rem;
                        margin: 0;
                    }
                """
    elif style == "none":
        style = """
                    body {
                        font-family: system;
                    }
                    p {
                        font-size: 1.0rem;
                        margin: 0;
                    }
                """
    elif style == "dynamic":
        if scope == "keyword.effect":
            style = """
                        body {
                            font-family: system;
                            margin: 0;
                            padding: 0.35rem;
                            border: 0.15rem solid rgb(128, 26, 0);
                            background-color: rgb(10, 10, 10);
                        }
                        p {
                            font-size: 1.0rem;
                            margin: 0;
                        }
                    """
        elif scope == "string.trigger":
            style = """
                        body {
                            font-family: system;
                            margin: 0;
                            padding: 0.35rem;
                            border: 0.15rem solid rgb(123, 123, 0);
                            background-color: rgb(10, 10, 10);
                        }
                        p {
                            font-size: 1.0rem;
                            margin: 0;
                        }
                    """
        elif scope == "storage.type.scope":
            style = """
                        body {
                            font-family: system;
                            margin: 0;
                            padding: 0.35rem;
                            border: 0.15rem solid rgb(0, 122, 153);
                            background-color: rgb(10, 10, 10);
                        }
                        p {
                            font-size: 1.0rem;
                            margin: 0;
                        }
                    """
    item = view.substr(view.word(point))
    if item in collection:
        desc = collection[item]
        hover_body = """
            <body id="imperator-body">
                <style>%s</style>
                <p>%s</p>
            </body>
        """ % (
            style,
            desc,
        )

        view.show_popup(
            hover_body,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=1024,
        )
        return


class ScriptHoverListener(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        if not view:
            return

        try:
            if view.syntax().name == "Imperator Script":
                pass
            else:
                return
        except AttributeError:
            return

        if settings.get("DocsHoverEnabled") == True:
            if view.match_selector(point, "keyword.effect"):
                show_hover_docs(view, point, "keyword.effect", GameData.EffectsList)
                return

            if view.match_selector(point, "string.trigger"):
                GameData.TriggersList.update(GameData.CustomTriggersList)
                show_hover_docs(view, point, "string.trigger", GameData.TriggersList)
                return

            if view.match_selector(point, "storage.type.scope"):
                GameData.ScopesList.update(GameData.CustomScopesList)
                show_hover_docs(view, point, "storage.type.scope", GameData.ScopesList)
                return

            # Do everything that requires fetching GameObjects in non-blocking thread
            sublime.set_timeout_async(lambda: self.do_hover_async(view, point), 0)

        # Texture popups can happen for both script and gui files
        if settings.get("TextureOpenPopup") == True:
            posLine = view.line(point)
            if ".dds" in view.substr(posLine):
                texture_raw_start = view.find("gfx", posLine.a)
                texture_raw_end = view.find(".dds", posLine.a)
                texture_raw_region = sublime.Region(
                    texture_raw_start.a, texture_raw_end.b
                )
                texture_raw_path = view.substr(texture_raw_region)
                full_texture_path = imperator_files_path + "/" + texture_raw_path
                if not os.path.exists(full_texture_path):
                    # Check mod paths if it's not vanilla
                    for mod in imperator_mod_files:
                        if os.path.exists(mod):
                            if mod.endswith("mod"):
                                # if it is the path to the mod directory, get all directories in it
                                for directory in [
                                    f.path for f in os.scandir(mod) if f.is_dir()
                                ]:
                                    mod_path = directory + "/" + texture_raw_path
                                    if os.path.exists(mod_path):
                                        full_texture_path = mod_path
                            else:
                                mod_path = mod + "/" + texture_raw_path
                                if os.path.exists(mod_path):
                                    full_texture_path = mod_path
                # The path exists and the point in the view is inside of the path
                if texture_raw_region.__contains__(point):
                    texture_name = view.substr(view.word(texture_raw_end.a - 1))
                    self.show_texture_hover_popup(
                        view, point, texture_name, full_texture_path
                    )

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

        hover_objects = [
            ("ambition", "Ambition"),
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
            ("named_colors", "Named Color"),
            ("idea", "Idea"),
            ("invention", "Invention"),
            ("law", "law"),
            ("legion_distinction", "Legion Distinction"),
            ("levy_template", "Levy Template"),
            ("loyalty", "Loyalty"),
            ("mil_tradition", "Military Tradition"),
            ("modifier", "Modifier"),
            ("opinion", "Opinion"),
            ("office", "Office"),
            ("party", "Party"),
            ("pop", "Pop Type"),
            ("price", "Price"),
            ("province_rank", "Province Rank"),
            ("religion", "Religion"),
            ("script_value", "Script Value"),
            ("scripted_effect", "Scripted Effect"),
            ("scripted_modifier", "Scripted Modifier"),
            ("scripted_trigger", "Scripted Trigger"),
            ("subject_type", "Subject Type"),
            ("tech_table", "Technology Table"),
            ("terrain", "Terrain"),
            ("trade_good", "Trade Good"),
            ("trait", "Trait"),
            ("unit", "Unit"),
            ("war_goal", "War Goal"),
            ("mission", "Mission"),
            ("mission_task", "Mission Task"),
            ("area", "Area"),
            ("region", "Region"),
            ("scripted_list_triggers", "Scripted List"),
            ("scripted_list_effects", "Scripted List"),
        ]

        # Iterate over the list and call show_popup_default for each game object
        for hover_object, name in hover_objects:
            if game_objects[hover_object].contains(word):
                self.show_popup_default(
                    view, point, word, game_objects[hover_object].access(word), name
                )

    def show_popup_default(self, view, point, word, PdxObject, header):
        if view.file_name() is None:
            return

        link = self.get_definitions_for_popup(
            view, point, PdxObject, header
        ) + self.get_references_for_popup(view, point, PdxObject)
        if link:
            hover_body = """
                <body id="imperator-body">
                    <style>%s</style>
                    <h1>%s</h1>
                    %s
                </body>
            """ % (
                css_basic_style,
                header,
                link,
            )

            view.show_popup(
                hover_body,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )

    def get_definitions_for_popup(self, view, point, PdxObject, header, def_value=""):
        word_line_num = view.rowcol(point)[0] + 1
        definition = ""
        definitions = []
        if header == "Saved Scope" or header == "Saved Variable":
            for win in sublime.windows():
                for i in [v for v in win.views() if v and v.file_name()]:
                    if i.file_name().endswith(".txt") or i.file_name().endswith(".py"):
                        variables = [
                            x
                            for x in i.find_by_selector(
                                "entity.name.function.var.declaration"
                            )
                            if i.substr(x) == PdxObject.key
                        ]
                        variables.extend(
                            [
                                x
                                for x in i.find_by_selector(
                                    "entity.name.function.scope.declaration"
                                )
                                if i.substr(x) == PdxObject.key
                            ]
                        )
                        for r in variables:
                            line = i.rowcol(r.a)[0] + 1
                            path = i.file_name()
                            if line == word_line_num and path == PdxObject.path:
                                continue
                            else:
                                definitions.append(
                                    PdxScriptObject(PdxObject.key, path, line)
                                )

            if len(definitions) == 1:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                else:
                    definition = f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            elif len(definitions) > 1:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                else:
                    definition = f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for obj in definitions:
                goto_args = {"path": obj.path, "line": obj.line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                definition += (
                    """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""
                    % (
                        goto_url,
                        obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                        obj.line,
                        obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                        obj.line,
                    )
                )
                goto_right_args = {"path": obj.path, "line": obj.line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )
        else:
            if word_line_num != PdxObject.line and view.file_name() != PdxObject.path:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                else:
                    definition = f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                goto_args = {"path": PdxObject.path, "line": PdxObject.line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                definition += (
                    """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""
                    % (
                        goto_url,
                        PdxObject.path.replace("\\", "/")
                        .rstrip("/")
                        .rpartition("/")[2],
                        PdxObject.line,
                        PdxObject.path.replace("\\", "/")
                        .rstrip("/")
                        .rpartition("/")[2],
                        PdxObject.line,
                    )
                )
                goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        return definition

    def get_references_for_popup(self, view, point, PdxObject):
        word_line_num = view.rowcol(point)[0] + 1
        word_file = view.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
        references = []
        ref = ""
        for win in sublime.windows():
            for i in [v for v in win.views() if v and v.file_name()]:
                if i.file_name().endswith(".txt"):
                    view_region = sublime.Region(0, i.size())
                    view_str = i.substr(view_region)
                    for j, line in enumerate(view_str.splitlines()):
                        if re.search(r"\b" + re.escape(PdxObject.key) + r"\b", line):
                            filename = (
                                i.file_name()
                                .replace("\\", "/")
                                .rstrip("/")
                                .rpartition("/")[2]
                            )
                            line_num = j + 1
                            if word_line_num == line_num and word_file == filename:
                                # Don't do current word
                                continue
                            elif (
                                line_num == PdxObject.line
                                and i.file_name() == PdxObject.path
                            ):
                                # Don't do definition
                                continue
                            else:
                                references.append(f"{i.file_name()}|{line_num}")
        if references:
            ref = f'<p><b>References to&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for i in references:
                fname = i.split("|")[0]
                shortname = fname.replace("\\", "/").rstrip("/").rpartition("/")[2]
                line = i.split("|")[1]
                goto_args = {"path": fname, "line": line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                ref += (
                    """<a href="%s" title="Open %s and goto line %s">%s:%s</a>&nbsp;"""
                    % (
                        goto_url,
                        shortname,
                        line,
                        shortname,
                        line,
                    )
                )
                goto_right_args = {"path": fname, "line": line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                ref += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        return ref

    def show_texture_hover_popup(self, view, point, texture_name, full_texture_path):
        args = {"path": full_texture_path}
        open_texture_url = sublime.command_url("open_victoria_texture ", args)
        folder_args = {"path": full_texture_path, "folder": True}
        open_folder_url = sublime.command_url("open_victoria_texture ", folder_args)
        in_sublime_args = {"path": full_texture_path, "mode": "in_sublime"}
        inline_args = {"path": full_texture_path, "point": point}
        open_in_sublime_url = sublime.command_url(
            "open_victoria_texture ", in_sublime_args
        )
        open_inline_url = sublime.command_url("v3_show_texture ", inline_args)
        hover_body = """
            <body id=\"imperator-body\">
                <style>%s</style>
                <h1>Open Texture</h1>
                <div></div>
                <a href="%s" title="Open folder containing the texture.">Open Folder</a>
                <br>
                <a href="%s" title="Open %s in the default program">Open in default program</a>
                <br>
                <a href="%s" title="Open %s in sublime">Open in sublime</a>
                <br>
                <a href="%s" title="Show %s at current selection">Show Inline</a>
            </body>
        """ % (
            css_basic_style,
            open_folder_url,
            open_texture_url,
            texture_name,
            open_in_sublime_url,
            texture_name,
            open_inline_url,
            texture_name,
        )

        view.show_popup(
            hover_body,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=802,
        )

    def show_popup_named_color(self, view, point, word, PdxObject, header):
        if view.file_name() is None:
            return

        object_color = PdxObject.color
        css_color = PdxObject.rgb_color

        # print(css_color)

        r = css_color[0]
        g = css_color[1]
        b = css_color[2]
        icon_color = f"rgb({r},{g},{b})"
        color = f'<a class="icon"style="color:{icon_color}">■</a>\t\t\t<code>{object_color}</code>'

        link = self.get_definitions_for_popup(view, point, PdxObject, header, color)
        if link:
            hover_body = """
                <body id="imperator-body">
                    <style>%s</style>
                    <h1>%s</h1>
                    %s
                </body>
            """ % (
                css_basic_style,
                header,
                link,
            )

            view.show_popup(
                hover_body,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )


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


class OpenImperatorTextureCommand(sublime_plugin.WindowCommand):
    def run(self, path, folder=False, mode="default_program"):
        if folder:
            end = path.rfind("/")
            path = path[0:end:]
            OpenImperatorTextureCommand.open_path(path)
        else:
            if mode == "default_program":
                OpenImperatorTextureCommand.open_path(path)
            elif mode == "in_sublime":
                simple_path = (
                    path.replace("\\", "/")
                    .rstrip("/")
                    .rpartition("/")[2]
                    .replace(".dds", ".png")
                )
                output_file = (
                    sublime.packages_path()
                    + "/ImperatorTools/Convert DDS/cache/"
                    + simple_path
                )
                exe_path = (
                    sublime.packages_path()
                    + "/ImperatorTools/Convert DDS/src/ConvertDDS.exe"
                )

                if not os.path.exists(output_file):
                    # Run dds to png converter
                    cmd = (
                        ["wine", exe_path, path, output_file]
                        if sublime.platform() == "linux"
                        else [exe_path, path, output_file]
                    )
                    self.window.run_command("quiet_execute", {"cmd": cmd})
                    self.window.destroy_output_panel("exec")
                    sublime.active_window().open_file(output_file)
                else:
                    # File is already in cache, don't need to convert
                    sublime.active_window().open_file(output_file)

    @staticmethod
    def open_path(path):
        system = sys.platform
        if system == "Darwin":  # macOS
            subprocess.Popen(("open", path))
        elif system == "Windows" or system == "win32" or system == "win":  # Windows
            os.startfile(path)
        else:  # Linux and other Unix-like systems
            subprocess.Popen(("xdg-open", path))


class ImpClearImageCacheCommand(sublime_plugin.WindowCommand):
    def run(self):
        dir_name = sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/"
        ld = os.listdir(dir_name)
        for item in ld:
            if item.endswith(".png"):
                os.remove(os.path.join(dir_name, item))
        sublime.status_message("Cleared Image Cache")


class ImpReloadPluginCommand(sublime_plugin.WindowCommand):
    def run(self):
        plugin_loaded()


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


class ImperatorTextureFileLoadEventListener(sublime_plugin.EventListener):
    def on_load_async(self, view):
        if not view:
            return None

        try:
            if view.syntax().name != "Imperator Script":
                return None
        except AttributeError:
            return None

        if settings.get("ShowInlineTexturesOnLoad"):
            sublime.active_window().run_command("imperator_show_all_textures")


class ImperatorTextureEventListener(sublime_plugin.EventListener):
    def on_post_text_command(self, view, command_name, args):
        if command_name in ("left_delete", "insert"):
            if view.file_name() and view.syntax().name == "Imperator Script":
                x = [v for v in views_with_shown_textures if v.id() == view.id()]
                if x:
                    x[0].update_line_count(view.rowcol(view.size())[0] + 1)


views_with_shown_textures = set()


class ImperatorViewTextures(sublime.View):
    def __init__(self, id):
        super(ImperatorViewTextures, self).__init__(id)
        self.textures = []
        self.line_count = self.rowcol(self.size())[0] + 1

    def update_line_count(self, new_count):
        diff = new_count - self.line_count
        self.line_count += diff
        to_update = []
        for i, tex in enumerate(self.textures):
            tex = tex.split("|")
            key = tex[0]
            line = int(tex[1])
            point = self.view.text_point(line, 1)
            if self.find(key, point):
                # Texture is still on the same line, dont need to update
                return
            else:
                current_selection_line = self.rowcol(self.sel()[0].a)[0] + 1
                if current_selection_line < line:
                    line += diff
                    out = key + "|" + str(line)
                    to_update.append((i, out))
        for i in to_update:
            index = i[0]
            replacement = i[1]
            views_with_shown_textures.discard(self)
            self.textures[index] = replacement
            views_with_shown_textures.add(self)


class ImperatorShowTextureBase:
    conversion_iterations = 0
    total_conversion_attempts = 2 if sublime.platform() == "linux" else 6

    def show_texture(self, path, point):
        window = sublime.active_window()
        simple_path = (
            path.replace("\\", "/")
            .rstrip("/")
            .rpartition("/")[2]
            .replace(".dds", ".png")
        )
        output_file = (
            sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/" + simple_path
        )
        exe_path = (
            sublime.packages_path() + "/ImperatorTools/Convert DDS/src/ConvertDDS.exe"
        )
        if not os.path.exists(output_file):
            cmd = (
                ["wine", exe_path, path, output_file]
                if sublime.platform() == "linux"
                else [exe_path, path, output_file]
            )
            window.run_command("quiet_execute", {"cmd": cmd})
            window.destroy_output_panel("exec")
            # Wait 100ms for conversion to finish
            timeout = 2000 if sublime.platform() == "linux" else 100
            sublime.set_timeout_async(
                lambda: self.toggle_async(
                    output_file, simple_path, point, window, path
                ),
                timeout,
            )
        else:
            self.toggle_async(output_file, simple_path, point, window, path)

    def toggle_async(self, output_file, simple_path, point, window, original_path):
        # Try to convert for 500ms

        if (
            not os.path.exists(output_file)
            and self.conversion_iterations < self.total_conversion_attempts
        ):
            self.conversion_iterations += 1
            self.show_texture(original_path, point)
        elif os.path.exists(output_file):
            self.conversion_iterations = 0
            image = f"file://{output_file}"
            dimensions = self.get_png_dimensions(output_file)
            width = dimensions[0]
            height = dimensions[1]
            html = f'<img src="{image}" width="{width}" height="{height}">'
            view = window.active_view()
            if os.path.exists(output_file):
                self.toggle(simple_path, view, html, point)

    def toggle(self, key, view, html, point):
        pid = key + "|" + str(view.rowcol(point)[0] + 1)
        x = ImperatorViewTextures(view.id())
        views_with_shown_textures.add(x)
        x = [v for v in views_with_shown_textures if v.id() == view.id()]
        current_view = ""
        if x:
            current_view = x[0]
        if not current_view:
            return

        if pid in current_view.textures:
            current_view.textures.remove(pid)
            view.erase_phantoms(key)
        else:
            current_view.textures.append(pid)
            line_region = view.line(point)
            # Find region of texture path declaration
            # Ex: [start]texture = "gfx/interface/icons/goods_icons/meat.dds"[end]
            start = view.find(
                '[A-Za-z_][A-Za-z_0-9]*\s?=\s?"?/?(gfx)?', line_region.a
            ).a
            end = view.find('"|\n', start).a
            phantom_region = sublime.Region(start, end)
            view.add_phantom(key, phantom_region, html, sublime.LAYOUT_BELOW)

    def get_png_dimensions(self, path):
        height = 150
        width = 150
        file = open(path, "rb")
        try:
            head = file.read(31)
            size = len(head)
            if (
                size >= 24
                and head.startswith(b"\211PNG\r\n\032\n")
                and head[12:16] == b"IHDR"
            ):
                try:
                    width, height = struct.unpack(">LL", head[16:24])
                except struct.error:
                    pass
            elif size >= 16 and head.startswith(b"\211PNG\r\n\032\n"):
                try:
                    width, height = struct.unpack(">LL", head[8:16])
                except struct.error:
                    pass
        finally:
            file.close()

        # Scale down so image doens't take up entire viewport
        if width > 150 and height > 150:
            width /= 1.75
            height /= 1.75
        return int(width), int(height)


class ImperatorShowTextureCommand(
    sublime_plugin.ApplicationCommand, ImperatorShowTextureBase
):
    def run(self, path, point):
        self.show_texture(path, point)


class ImperatorToggleAllTexturesCommand(sublime_plugin.ApplicationCommand):
    def __init__(self):
        self.shown = False

    def run(self):
        window = sublime.active_window()
        view = window.active_view()
        if not view:
            return None

        try:
            if view.syntax().name != "Imperator Script":
                return None
        except AttributeError:
            return None

        if self.shown or len(views_with_shown_textures) > 0:
            self.shown = False
            window.run_command("imperator_clear_all_textures")
        else:
            self.shown = True
            window.run_command("imperator_show_all_textures")


class ImperatorClearAllTexturesCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        keys = []
        for view in views_with_shown_textures:
            for i in view.textures:
                tex = i.split("|")
                key = tex[0]
                keys.append(key)
        for view in sublime.active_window().views():
            for i in keys:
                view.erase_phantoms(i)
        views_with_shown_textures.clear()


class ImperatorShowAllTexturesCommand(
    sublime_plugin.WindowCommand, ImperatorShowTextureBase
):
    def run(self):
        view = self.window.active_view()
        texture_list = [
            x
            for x in view.lines(sublime.Region(0, view.size()))
            if ".dds" in view.substr(x)
        ]
        for line, i in zip(texture_list, range(settings.get("MaxToggleTextures"))):
            texture_raw_start = view.find("gfx", line.a)
            texture_raw_end = view.find(".dds", line.a)
            texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
            texture_raw_path = view.substr(texture_raw_region)
            full_texture_path = imperator_files_path + "/" + texture_raw_path
            full_texture_path = full_texture_path.replace("\\", "/")
            self.show_texture(full_texture_path, texture_raw_start.a)


class ImperatorTigerEventListener(sublime_plugin.EventListener):
    def on_load_async(self, view):
        path = view.file_name()
        if path not in tiger_objects:
            return

        file_errors = tiger_objects[path]
        error_regions = list()
        warning_regions = list()
        tips_regions = list()
        if type(file_errors) == list:
            for i in file_errors:
                point = view.text_point(i["linenr"] - 1, i["column"] - 1)
                if i["severity"] == "fatal" or i["severity"] == "error":
                    error_regions.append(sublime.Region(point, point + i["length"]))
                if i["severity"] == "warning" or i["severity"] == "untidy":
                    warning_regions.append(sublime.Region(point, point + i["length"]))
                if i["severity"] == "tips":
                    tips_regions.append(sublime.Region(point, point + i["length"]))
        else:
            point = view.text_point(
                file_errors["linenr"] - 1, file_errors["column"] - 1
            )
            if file_errors["severity"] == "fatal" or file_errors["severity"] == "error":
                error_regions.append(
                    sublime.Region(point, point + file_errors["length"])
                )
            if (
                file_errors["severity"] == "warning"
                or file_errors["severity"] == "untidy"
            ):
                warning_regions.append(
                    sublime.Region(point, point + file_errors["length"])
                )
            if file_errors["severity"] == "tips":
                tips_regions.append(
                    sublime.Region(point, point + file_errors["length"])
                )

        if error_regions:
            self.add_error(view, error_regions, "region.redish")
        if warning_regions:
            self.add_error(view, warning_regions, "region.yellowish")
        if tips_regions:
            self.add_error(view, tips_regions, "region.greenish")

    def add_error(self, view, regions, scope):
        view.add_regions(
            scope,
            regions,
            scope,
            flags=(
                sublime.DRAW_NO_FILL
                | sublime.DRAW_NO_OUTLINE
                | sublime.DRAW_SQUIGGLY_UNDERLINE
            ),
        )

    def on_hover(self, view, point, hover_zone):
        if not view:
            return

        path = view.file_name()
        if path not in tiger_objects:
            return

        file_errors = tiger_objects[path]
        file_error = ""
        if type(file_errors) == list:
            for i in file_errors:
                # We can deduce the current error being hovered over by knowing the Region of the row and column it is in
                region_start = view.text_point(i["linenr"] - 1, i["column"] - 1)
                region_end = region_start + i["length"]
                error_region = sublime.Region(region_start, region_end)
                if error_region.contains(point):
                    file_error = i
        else:
            region_start = view.text_point(
                file_errors["linenr"] - 1, file_errors["column"] - 1
            )
            region_end = region_start + file_errors["length"]
            error_region = sublime.Region(region_start, region_end)
            if error_region.contains(point):
                file_error = file_errors

        if not file_error:
            return

        error = [x for x in view.get_regions("region.redish") if x.contains(point)]
        warning = [x for x in view.get_regions("region.yellowish") if x.contains(point)]
        tips = [x for x in view.get_regions("region.greenish") if x.contains(point)]

        info = file_error["info"]
        if not info:
            info = ""
        info = "<p>" + info + "</p>"

        header_color = ""
        if error:
            header_color = "red"
        if warning:
            header_color = "yellow"
        if tips:
            header_color = "green"

        header = f"{file_error['severity']}({file_error['key']})"
        example = f'<h2 class="code-header {header_color}-text">{header}</h2>'
        example += f'<div class="box-for-codebox"><div class="codebox"><code>{file_error["message"]}</code><br><code>{info}</code></div></div>'
        hover_body = """
            <body id="imperator-body">
                <style>%s</style>
                %s
            </body>
        """ % (
            css_basic_style,
            example,
        )

        view.show_popup(
            hover_body,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=1024,
        )


class ImpTigerInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "view_type"

    def list_items(self):
        return ["Panel", "Tab"]


class ShowTigerOutputCommand(sublime_plugin.WindowCommand):
    def run(self, view_type):
        path = sublime.packages_path() + f"/ImperatorTools/tiger.json"
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        view_text = str()
        self.path_locations = list()
        for i in data:
            # Add location data to list in the same way the display() function does so the indexes stay the same
            previous_locations = list()
            for j in i["locations"]:
                if j["fullpath"] not in previous_locations:
                    self.path_locations.append((j["linenr"], j["column"]))
                previous_locations.append(j["fullpath"])

            obj = TigerJsonObject(
                i["confidence"],
                i["info"],
                i["key"],
                i["locations"],
                i["message"],
                i["severity"],
            )

            view_text += obj.display()

        if view_type == "Panel":
            if self.window.find_output_panel("exec") is None:
                self.output_view = self.window.create_output_panel("exec")
                self.window.run_command("show_panel", {"panel": "output.exec"})
            else:
                self.window.destroy_output_panel("exec")
                self.output_view = self.window.create_output_panel("exec")
                self.window.run_command("show_panel", {"panel": "output.exec"})
        else:
            self.output_view = self.window.new_file(flags=sublime.TRANSIENT)
            self.output_view.set_name("Tiger Output")
            self.output_view.set_scratch(True)

        if self.output_view:
            self.view_creation(view_text)

    def input(self, args):
        if "view_type" not in args:
            return ImpTigerInputHandler()

    def view_creation(self, view_text):
        self.window.focus_view(self.output_view)
        self.output_view.set_read_only(True)
        self.output_view.assign_syntax("Tiger.sublime-syntax")
        s = self.output_view.settings()
        s.set("word_wrap", True)
        s.set("line_numbers", False)
        s.set("gutter", False)
        s.set("scroll_past_end", False)
        self.output_view.run_command(
            "append", {"characters": view_text, "force": True, "scroll_to_end": True}
        )

        self.add_annotations()

    def add_annotations(self):
        regions = self.output_view.find_by_selector("string.file.path")
        annotations = list()

        for i in range(len(regions)):
            href_str = (
                self.output_view.substr(regions[i]).lstrip(" ")
                + ":"
                + str(self.path_locations[i][0])
                + ":"
                + str(self.path_locations[i][1])
            )
            annotation_body = """
                <body id="imperator-body">
                    <style>%s</style>
                    <a href="%s" >Open %s</a>
                </body>
            """ % (
                css_basic_style,
                href_str,
                self.output_view.substr(regions[i]),
            )
            annotations.append(annotation_body)

        self.output_view.add_regions(
            "file_to_open",
            regions,
            "string.file.path",
            flags=(sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE),
            annotations=annotations,
            on_navigate=self.annotation_callback,
        )

    def annotation_callback(self, string):
        string = string.replace("\n", "").split(":")
        print(string)
        path = settings.get("ImperatorTigerModPath") + "\\" + string[0]

        if not os.path.exists(path):
            path = imperator_files_path + "\\" + string[0]

        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, string[1], string[2])
            flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP
            self.window.open_file(file_path, flags)


class ExecuteTigerCommand(sublime_plugin.WindowCommand):
    """
    Version of Default.exec.py specifically for executing tiger and piping it's output to a file.
    It is basically the same except it does not pull up the output panel and it only outputs the text the subprocess sends.
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
        word_wrap=True,
        syntax="Packages/JSON/JSON.sublime-syntax",
        **kwargs,
    ):
        self.output_view = self.window.find_output_panel("exec")
        if self.output_view is None:
            # Try not to call get_output_panel until the regexes are assigned
            self.output_view = self.window.create_output_panel("exec")

        # Default the to the current files directory if no working directory
        # was given
        if (
            working_dir == ""
            and self.window.active_view()
            and self.window.active_view().file_name()
        ):
            working_dir = os.path.dirname(self.window.active_view().file_name())

        self.output_view.settings().set("result_base_dir", working_dir)
        self.output_view.settings().set("word_wrap", word_wrap)
        self.output_view.settings().set("line_numbers", False)
        self.output_view.settings().set("gutter", False)
        self.output_view.settings().set("scroll_past_end", False)
        self.output_view.assign_syntax(syntax)

        # Call create_output_panel a second time after assigning the above
        # settings, so that it'll be picked up as a result buffer
        self.window.create_output_panel("exec")

        self.window.focus_view(self.output_view)

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

    def write(self, characters):
        self.output_view.run_command(
            "append", {"characters": characters, "force": True, "scroll_to_end": True}
        )

    def on_data(self, proc, data):
        if proc != self.proc:
            return

        self.write(data)

    def on_finished(self, proc):
        if proc != self.proc:
            return

        text = self.output_view.substr(sublime.Region(0, self.output_view.size()))
        # Find where the json starts by splitting off the header output
        # This will break if there is a "[" in the header but that should never happen
        json_start_index = text.find("[")

        if json_start_index != -1:
            tiger_json_output = text[json_start_index:]
            output_file = sublime.packages_path() + f"/ImperatorTools/tiger.json"
            with open(output_file, "w") as f:
                f.write(tiger_json_output)
            sublime.status_message("imperator-tiger.exe has finished running.")
            sublime.set_timeout_async(lambda: get_tiger_objects(), 0)


class RunTigerCommand(sublime_plugin.WindowCommand):
    def run(self):
        mod_path = settings.get("ImperatorTigerModPath")

        if not os.path.exists(mod_path):
            return

        tiger_exe_path = (
            sublime.packages_path()
            + f"/ImperatorTools/ImperatorTiger/imperator-tiger.exe"
        )
        window = sublime.active_window()

        if not settings.get("ImperatorTigerUseDefaultConfig"):
            conf_file = (
                sublime.packages_path()
                + f"/ImperatorTools/ImperatorTiger/imperator-tiger.conf"
            )
            cmd = [tiger_exe_path, mod_path, "--json", "--config", conf_file]
        else:
            cmd = [tiger_exe_path, mod_path, "--json"]

        sublime.status_message("imperator-tiger.exe has started running...")
        window.run_command("execute_tiger", {"cmd": cmd})


class EditTigerConfigCommand(sublime_plugin.WindowCommand):
    def run(self):
        conf_file = (
            sublime.packages_path()
            + f"/ImperatorTools/ImperatorTiger/imperator-tiger.conf"
        )
        view = self.window.open_file(conf_file)
        view.assign_syntax("scope:source.ruby")
        self.write_load_mods_to_tiger_config()

    def write_load_mods_to_tiger_config(self):
        tiger_main_mod = settings.get("ImperatorTigerModPath")
        if not os.path.exists(tiger_main_mod):
            return  # Not using tiger

        pattern = r"load_mod = \{[^}]*\}"
        conf_file = (
            sublime.packages_path()
            + f"/ImperatorTools/ImperatorTiger/imperator-tiger.conf"
        )
        with open(conf_file, "r") as file:
            file_content = file.read()

        modified_content = re.sub(pattern, "", file_content, flags=re.DOTALL)

        for i in settings.get("ImperatorTigerLoadedMods"):
            if not os.path.exists(i) and i.endswith(".mod"):
                continue
            label = os.path.splitext(os.path.basename(i))[0]
            block = f'load_mod = {{\n\tlabel = "{label}"\n\tmodfile = "{i}"\n}}'
            modified_content += block

        with open(conf_file, "w") as file:
            file.write(modified_content)
