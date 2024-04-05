# Imperator Rome Game Object Class implementations

import os
import re
from colorsys import hsv_to_rgb
from typing import Union

import sublime

from .jomini import GameObjectBase, PdxScriptObject, PdxScriptObjectType

imperator_files_path = ""
imperator_mod_files = []


def plugin_loaded():
    global settings, imperator_files_path, imperator_mod_files
    settings = sublime.load_settings("Imperator Syntax.sublime-settings")
    imperator_files_path = settings.get("ImperatorFilesPath")
    imperator_mod_files = settings.get("PathsToModFiles")
    imperator_files_path = str(imperator_files_path)


class Ambition(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\ambitions")


class Building(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\buildings")


class CultureGroup(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\cultures")


class Culture(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=2)
        self.get_data("common\\cultures")


class CustomLoc(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files,
            imperator_files_path,
            ignored_files=["de_custom_loc.txt", "00_FR_custom_loc.txt"],
        )
        self.get_data("common\\customizable_localization")


class DeathReason(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\deathreasons")


class Deity(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\deities")


class DiplomaticStance(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\diplomatic_stances")


class EconomicPolicy(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\economic_policies")


class EventPicture(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\event_pictures")


class EventTheme(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\event_themes")


class Government(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\governments")


class GovernorPolicy(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\governor_policies")


class Heritage(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\heritage")


class Idea(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\ideas")


class Invention(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\inventions")


class Law(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\laws")


class LegionDistinction(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\legion_distinctions")


class LevyTemplate(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\levy_templates")


class Loyalty(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\loyalty")


class MilitaryTradition(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\military_traditions")


class Mission(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\missions")


class MissionTask(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data("common\\missions")


class Modifier(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files,
            imperator_files_path,
            ignored_files=["00_hardcoded.txt", "00_hardcoded_inv.txt"],
        )
        self.get_data("common\\modifiers")


class Opinion(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\opinions")


class Office(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\offices")


class Party(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\party_types")


class Pop(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\pop_types")


class Price(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\prices")


class ProvinceRank(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\province_ranks")


class Religion(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\religions")


class ScriptValue(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\script_values")


class ScriptedEffect(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_effects")


class ScriptedModifier(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_modifiers")


class ScriptedTrigger(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_triggers")


class SubjectType(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\subject_types")


class TechTable(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\technology_tables")


class Terrain(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\terrain_types")


class TradeGood(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\trade_goods")


class Trait(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\traits")


class Unit(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\units")


class Wargoal(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\wargoals")


class Area(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files, imperator_files_path, included_files=["areas.txt"]
        )
        self.get_data("map_data")


class Region(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files, imperator_files_path, included_files=["regions.txt"]
        )
        self.get_data("map_data")


class ScriptedList(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_lists")


class ScriptedGui(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data("common\\scripted_guis")


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


class NamedColor(GameObjectBase):
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


ImperatorObject = Union[
    GameObjectBase,
    Ambition,
    Building,
    CultureGroup,
    Culture,
    CustomLoc,
    DeathReason,
    Deity,
    DiplomaticStance,
    EconomicPolicy,
    EventPicture,
    EventTheme,
    Government,
    GovernorPolicy,
    Heritage,
    Idea,
    Invention,
    Law,
    LegionDistinction,
    LevyTemplate,
    Loyalty,
    MilitaryTradition,
    Mission,
    MissionTask,
    Modifier,
    Opinion,
    Office,
    Party,
    Pop,
    Price,
    ProvinceRank,
    Religion,
    ScriptValue,
    ScriptedEffect,
    ScriptedModifier,
    ScriptedTrigger,
    SubjectType,
    TechTable,
    Terrain,
    TradeGood,
    Trait,
    Unit,
    Wargoal,
    Area,
    Region,
    ScriptedList,
    ScriptedGui,
    NamedColor,
]
