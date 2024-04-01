from typing import Set, Tuple, Any
from .imperator_objects import *


class GameObjectData:
    def __init__(self, name: str, obj: Any, path: str):
        self.name = name
        self.obj = obj
        self.path = path


class GameObjectManager:
    def __init__(self):
        self.ambition = GameObjectData(
            "ambition", Ambition, "common\\ambitions"
        )
        self.area = GameObjectData("area", Area, "map_data")
        self.building = GameObjectData(
            "building", Building, "common\\buildings"
        )
        self.culture = GameObjectData("culture", Culture, "common\\cultures")
        self.culture_group = GameObjectData(
            "culture_group", CultureGroup, "common\\cultures"
        )
        self.custom_loc = GameObjectData(
            "custom_loc", CustomLoc, "common\\customizable_localization"
        )
        self.death_reason = GameObjectData(
            "death_reason", DeathReason, "common\\deathreasons"
        )
        self.deity = GameObjectData("deity", Deity, "common\\deities")
        self.diplo_stance = GameObjectData(
            "diplo_stance", DiplomaticStance, "common\\diplomatic_stances"
        )
        self.econ_policy = GameObjectData(
            "econ_policy", EconomicPolicy, "common\\economic_policies"
        )
        self.event_pic = GameObjectData(
            "event_pic", EventPicture, "common\\event_pictures"
        )
        self.event_theme = GameObjectData(
            "event_theme", EventTheme, "common\\event_themes"
        )
        self.government = GameObjectData(
            "government", Government, "common\\governments"
        )
        self.governor_policy = GameObjectData(
            "governor_policy", GovernorPolicy, "common\\governor_policies"
        )
        self.heritage = GameObjectData(
            "heritage", Heritage, "common\\heritage"
        )
        self.idea = GameObjectData("idea", Idea, "common\\ideas")
        self.invention = GameObjectData(
            "invention", Invention, "common\\inventions"
        )
        self.law = GameObjectData("law", Law, "common\\laws")
        self.legion_distinction = GameObjectData(
            "legion_distinction",
            LegionDistinction,
            "common\\legion_distinctions",
        )
        self.levy_template = GameObjectData(
            "levy_template", LevyTemplate, "common\\levy_templates"
        )
        self.loyalty = GameObjectData("loyalty", Loyalty, "common\\loyalty")
        self.mil_tradition = GameObjectData(
            "mil_tradition", MilitaryTradition, "common\\military_traditions"
        )
        self.mission = GameObjectData("mission", Mission, "common\\missions")
        self.mission_task = GameObjectData(
            "mission_task", MissionTask, "common\\missions"
        )
        self.modifier = GameObjectData(
            "modifier", Modifier, "common\\modifiers"
        )
        self.named_colors = GameObjectData(
            "named_colors", NamedColor, "common\\named_colors"
        )
        self.office = GameObjectData("office", Office, "common\\offices")
        self.opinion = GameObjectData("opinion", Opinion, "common\\opinions")
        self.party = GameObjectData("party", Party, "common\\party_types")
        self.pop = GameObjectData("pop", Pop, "common\\pop_types")
        self.price = GameObjectData("price", Price, "common\\prices")
        self.province_rank = GameObjectData(
            "province_rank", ProvinceRank, "common\\province_ranks"
        )
        self.region = GameObjectData("region", Region, "map_data")
        self.religion = GameObjectData(
            "religion", Religion, "common\\religions"
        )
        self.script_value = GameObjectData(
            "script_value", ScriptValue, "common\\script_values"
        )
        self.scripted_effect = GameObjectData(
            "scripted_effect", ScriptedEffect, "common\\scripted_effects"
        )
        self.scripted_gui = GameObjectData(
            "scripted_gui", ScriptedGui, "common\\scripted_guis"
        )
        self.scripted_list_effects = GameObjectData(
            "scripted_list_effects", ScriptedList, "common\\scripted_lists"
        )
        self.scripted_list_triggers = GameObjectData(
            "scripted_list_triggers", ScriptedList, "common\\scripted_lists"
        )
        self.scripted_modifier = GameObjectData(
            "scripted_modifier", ScriptedModifier, "common\\scripted_modifiers"
        )
        self.scripted_trigger = GameObjectData(
            "scripted_trigger", ScriptedTrigger, "common\\scripted_triggers"
        )
        self.subject_type = GameObjectData(
            "subject_type", SubjectType, "common\\subject_types"
        )
        self.tech_table = GameObjectData(
            "tech_table", TechTable, "common\\technology_tables"
        )
        self.terrain = GameObjectData(
            "terrain", Terrain, "common\\terrain_types"
        )
        self.trade_good = GameObjectData(
            "trade_good", TradeGood, "common\\trade_goods"
        )
        self.trait = GameObjectData("trait", Trait, "common\\traits")
        self.unit = GameObjectData("unit", Unit, "common\\units")
        self.war_goal = GameObjectData("war_goal", Wargoal, "common\\wargoals")

    def __iter__(self):
        for attr in self.__dict__:
            yield getattr(self, attr)

    def get_objects(self) -> Set[GameObjectData]:
        objects = set()
        for i in self:
            objects.add(i)
        return objects
