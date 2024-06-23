# Imperator Rome Game Object Class implementations

import os
from typing import Union

import sublime

from libjomini.src import GameObjectBase
from libjomini.src.jomini_objects import JominiObject

imperator_files_path = ""
imperator_mod_files = []


def plugin_loaded():
    global settings, imperator_files_path, imperator_mod_files
    settings = sublime.load_settings("Imperator.sublime-settings")
    imperator_files_path = settings.get("GameFilesPath")
    imperator_mod_files = settings.get("PathsToModFiles")
    imperator_files_path = str(imperator_files_path)


class Ambition(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}ambitions")


class Building(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}buildings")


class CultureGroup(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}cultures")


class Culture(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=2)
        self.get_data(f"common{os.sep}cultures")


class CustomLoc(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files,
            imperator_files_path,
            ignored_files=["de_custom_loc.txt", "00_FR_custom_loc.txt"],
        )
        self.get_data(f"common{os.sep}customizable_localization")


class DeathReason(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}deathreasons")


class Deity(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}deities")


class DiplomaticStance(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}diplomatic_stances")


class EconomicPolicy(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}economic_policies")


class EventPicture(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}event_pictures")


class EventTheme(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}event_themes")


class Government(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}governments")


class GovernorPolicy(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}governor_policies")


class Heritage(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}heritage")


class Idea(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}ideas")


class Invention(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data(f"common{os.sep}inventions")


class Law(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data(f"common{os.sep}laws")


class LegionDistinction(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}legion_distinctions")


class LevyTemplate(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}levy_templates")


class Loyalty(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}loyalty")


class MilitaryTradition(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data(f"common{os.sep}military_traditions")


class Mission(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}missions")


class MissionTask(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, level=1)
        self.get_data(f"common{os.sep}missions")


class Modifier(GameObjectBase):
    def __init__(self):
        super().__init__(
            imperator_mod_files,
            imperator_files_path,
            ignored_files=["00_hardcoded.txt", "00_hardcoded_inv.txt"],
        )
        self.get_data(f"common{os.sep}modifiers")


class Opinion(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}opinions")


class Office(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}offices")


class Party(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}party_types")


class Pop(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}pop_types")


class Price(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}prices")


class ProvinceRank(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}province_ranks")


class Religion(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}religions")


class SubjectType(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}subject_types")


class TechTable(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}technology_tables")


class Terrain(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}terrain_types")


class TradeGood(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}trade_goods")


class Trait(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}traits")


class Unit(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}units")


class Wargoal(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path)
        self.get_data(f"common{os.sep}wargoals")


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


ImperatorObject = Union[
    GameObjectBase,
    JominiObject,
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
    SubjectType,
    TechTable,
    Terrain,
    TradeGood,
    Trait,
    Unit,
    Wargoal,
    Area,
    Region,
]
