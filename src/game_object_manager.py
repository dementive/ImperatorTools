from .imperator_objects import *
from libjomini.src import JominiGameObjectManager, GameObjectData


class GameObjectManager(JominiGameObjectManager):
    def __init__(self):
        self.ambition = GameObjectData("ambition", Ambition, f"common{os.sep}ambitions")
        self.area = GameObjectData("area", Area, "map_data")
        self.building = GameObjectData("building", Building, f"common{os.sep}buildings")
        self.culture = GameObjectData("culture", Culture, f"common{os.sep}cultures")
        self.culture_group = GameObjectData(
            "culture_group", CultureGroup, f"common{os.sep}cultures"
        )
        self.custom_loc = GameObjectData(
            "custom_loc", CustomLoc, f"common{os.sep}customizable_localization"
        )
        self.death_reason = GameObjectData(
            "death_reason", DeathReason, f"common{os.sep}deathreasons"
        )
        self.deity = GameObjectData("deity", Deity, f"common{os.sep}deities")
        self.diplo_stance = GameObjectData(
            "diplo_stance", DiplomaticStance, f"common{os.sep}diplomatic_stances"
        )
        self.econ_policy = GameObjectData(
            "econ_policy", EconomicPolicy, f"common{os.sep}economic_policies"
        )
        self.event_pic = GameObjectData(
            "event_pic", EventPicture, f"common{os.sep}event_pictures"
        )
        self.event_theme = GameObjectData(
            "event_theme", EventTheme, f"common{os.sep}event_themes"
        )
        self.government = GameObjectData(
            "government", Government, f"common{os.sep}governments"
        )
        self.governor_policy = GameObjectData(
            "governor_policy", GovernorPolicy, f"common{os.sep}governor_policies"
        )
        self.heritage = GameObjectData("heritage", Heritage, f"common{os.sep}heritage")
        self.idea = GameObjectData("idea", Idea, f"common{os.sep}ideas")
        self.invention = GameObjectData(
            "invention", Invention, f"common{os.sep}inventions"
        )
        self.law = GameObjectData("law", Law, f"common{os.sep}laws")
        self.legion_distinction = GameObjectData(
            "legion_distinction",
            LegionDistinction,
            f"common{os.sep}legion_distinctions",
        )
        self.levy_template = GameObjectData(
            "levy_template", LevyTemplate, f"common{os.sep}levy_templates"
        )
        self.loyalty = GameObjectData("loyalty", Loyalty, f"common{os.sep}loyalty")
        self.mil_tradition = GameObjectData(
            "mil_tradition", MilitaryTradition, f"common{os.sep}military_traditions"
        )
        self.mission = GameObjectData("mission", Mission, f"common{os.sep}missions")
        self.mission_task = GameObjectData(
            "mission_task", MissionTask, f"common{os.sep}missions"
        )
        self.modifier = GameObjectData("modifier", Modifier, f"common{os.sep}modifiers")
        self.named_colors = GameObjectData(
            "named_colors", NamedColor, f"common{os.sep}named_colors"
        )
        self.office = GameObjectData("office", Office, f"common{os.sep}offices")
        self.opinion = GameObjectData("opinion", Opinion, f"common{os.sep}opinions")
        self.party = GameObjectData("party", Party, f"common{os.sep}party_types")
        self.pop = GameObjectData("pop", Pop, f"common{os.sep}pop_types")
        self.price = GameObjectData("price", Price, f"common{os.sep}prices")
        self.province_rank = GameObjectData(
            "province_rank", ProvinceRank, f"common{os.sep}province_ranks"
        )
        self.region = GameObjectData("region", Region, "map_data")
        self.religion = GameObjectData("religion", Religion, f"common{os.sep}religions")
        self.script_value = GameObjectData(
            "script_value", ScriptValue, f"common{os.sep}script_values"
        )
        self.scripted_effect = GameObjectData(
            "scripted_effect", ScriptedEffect, f"common{os.sep}scripted_effects"
        )
        self.scripted_gui = GameObjectData(
            "scripted_gui", ScriptedGui, f"common{os.sep}scripted_guis"
        )
        self.scripted_list_effects = GameObjectData(
            "scripted_list_effects", ScriptedList, f"common{os.sep}scripted_lists"
        )
        self.scripted_list_triggers = GameObjectData(
            "scripted_list_triggers", ScriptedList, f"common{os.sep}scripted_lists"
        )
        self.scripted_modifier = GameObjectData(
            "scripted_modifier", ScriptedModifier, f"common{os.sep}scripted_modifiers"
        )
        self.scripted_trigger = GameObjectData(
            "scripted_trigger", ScriptedTrigger, f"common{os.sep}scripted_triggers"
        )
        self.subject_type = GameObjectData(
            "subject_type", SubjectType, f"common{os.sep}subject_types"
        )
        self.tech_table = GameObjectData(
            "tech_table", TechTable, f"common{os.sep}technology_tables"
        )
        self.terrain = GameObjectData(
            "terrain", Terrain, f"common{os.sep}terrain_types"
        )
        self.trade_good = GameObjectData(
            "trade_good", TradeGood, f"common{os.sep}trade_goods"
        )
        self.trait = GameObjectData("trait", Trait, f"common{os.sep}traits")
        self.unit = GameObjectData("unit", Unit, f"common{os.sep}units")
        self.war_goal = GameObjectData("war_goal", Wargoal, f"common{os.sep}wargoals")
