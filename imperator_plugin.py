import sublime, sublime_plugin
import os, re, time, webbrowser, threading
import struct
import Default.exec
from colorsys import hsv_to_rgb
from collections import deque
from .jomini import GameObjectBase, PdxScriptObjectType, PdxScriptObject
from .jomini import dict_to_game_object as make_object
from .Utilities.game_data import GameData
from .object_cache import GameObjectCache

# ----------------------------------
# -          Plugin Setup          -
# ----------------------------------
settings = None
imperator_files_path = None
imperator_mod_files = None


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
        super().__init__(imperator_mod_files, imperator_files_path, included_files=["areas.txt"])
        self.get_data("map_data")


class ImperatorRegion(GameObjectBase):
    def __init__(self):
        super().__init__(imperator_mod_files, imperator_files_path, included_files=["regions.txt"])
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
                if split_color[2] == "187" and split_color[3] == "83" and split_color[4] == "146":
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
                            found_item = re.search(r"([A-Za-z_][A-Za-z_0-9]*)\s*=(.*)", line)
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
                                    obj_list.append(PdxColorObject(found_item, file_path, i + 1, item_color))
        return PdxScriptObjectType(obj_list)

    def should_read(self, x: str) -> bool:
        # Check if a line should be read
        return re.search(r"([A-Za-z_][A-Za-z_0-9]*)\s*=", x)


# Game Data class
GameData = GameData()

# Global Object Variables that get set on plugin_loaded

default_object = GameObjectBase()
ambition = building = culture = culture_group = death_reason = deity = diplo_stance = econ_policy = default_object
event_pic = event_theme = government = governor_policy = heritage = idea = invention = default_object
law = legion_distinction = levy_template = loyalty = mil_tradition = modifier = opinion = default_object
office = party = pop = price = province_rank = religion = script_value = scripted_effect = default_object
scripted_modifier = scripted_trigger = subject_type = tech_table = terrain = trade_good = trait = default_object
unit = war_goal = mission = mission_task = area = region = scripted_list_triggers = scripted_list_effects = default_object
named_colors = default_object

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
    mod_cache_path = sublime.packages_path() + f"/ImperatorTools/mod_cache.py"
    with open(mod_cache_path, "r+") as f:
        # Save lines without remake_cache function
        mod_cache = f.readlines()
        if mod_cache == "":
            f.write(f"def remake_cache():\n\treturn True")
            return True
        mod_cache = "".join(mod_cache[0 : len(mod_cache) - 2])
    with open(mod_cache_path, "w") as f:
        # Clear
        f.write("")

    for path in imperator_mod_files:
        stats_dict = dict()
        mod_name = path.replace("\\", "/").rstrip("/").rpartition("/")[2]
        mod_class_name = mod_name.replace(" ", "")
        for dirpath, dirnames, filenames in os.walk(path):
            mod_files = [x for x in filenames if x.endswith(".txt")]
            if mod_files:
                for i, j in enumerate(mod_files):
                    full_path = dirpath + "/" + mod_files[i]
                    stats_dict[full_path] = os.stat(full_path).st_mtime
        with open(mod_cache_path, "a") as f:
            f.write("#")
            for i in stats_dict:
                key = re.sub("\W|^(?=\d)", "_", i.split(mod_name)[1])
                value = stats_dict[i]
                f.write(f"{key}{value}")
            f.write("\n")

    with open(mod_cache_path, "r") as f:
        # Save written mod classes
        new_mod_cache = "".join(f.readlines())
    with open(mod_cache_path, "a") as f:
        # Write remake_cache function that indicates if new game objects need to be made
        f.write(f"def remake_cache():\n\treturn {True if mod_cache != new_mod_cache else False}")

    from .mod_cache import remake_cache

    return remake_cache()


def get_objects_from_cache():
    global ambition, building, culture, culture_group, death_reason, deity, diplo_stance, econ_policy, event_pic, event_theme, government, governor_policy, heritage, idea, invention, law, legion_distinction, levy_template, loyalty, mil_tradition, modifier, opinion, office, party, pop, price, province_rank, religion, script_value, scripted_effect, scripted_modifier, scripted_trigger, subject_type, tech_table, terrain, trade_good, trait, unit, war_goal, mission, mission_task, area, region, scripted_list_triggers, scripted_list_effects, named_colors

    object_cache = GameObjectCache()

    try:
        named_colors = make_named_color_object(object_cache.named_colors)
        ambition = make_object(object_cache.ambition)
        building = make_object(object_cache.building)
        culture = make_object(object_cache.culture)
        culture_group = make_object(object_cache.culture_group)
        death_reason = make_object(object_cache.death_reason)
        deity = make_object(object_cache.deity)
        diplo_stance = make_object(object_cache.diplo_stance)
        econ_policy = make_object(object_cache.econ_policy)
        event_pic = make_object(object_cache.event_pic)
        event_theme = make_object(object_cache.event_theme)
        government = make_object(object_cache.government)
        governor_policy = make_object(object_cache.governor_policy)
        heritage = make_object(object_cache.heritage)
        idea = make_object(object_cache.idea)
        invention = make_object(object_cache.invention)
        law = make_object(object_cache.law)
        legion_distinction = make_object(object_cache.legion_distinction)
        levy_template = make_object(object_cache.levy_template)
        loyalty = make_object(object_cache.loyalty)
        mil_tradition = make_object(object_cache.mil_tradition)
        modifier = make_object(object_cache.modifier)
        opinion = make_object(object_cache.opinion)
        office = make_object(object_cache.office)
        party = make_object(object_cache.party)
        pop = make_object(object_cache.pop)
        price = make_object(object_cache.price)
        province_rank = make_object(object_cache.province_rank)
        religion = make_object(object_cache.religion)
        script_value = make_object(object_cache.script_value)
        scripted_effect = make_object(object_cache.scripted_effect)
        scripted_modifier = make_object(object_cache.scripted_modifier)
        scripted_trigger = make_object(object_cache.scripted_trigger)
        subject_type = make_object(object_cache.subject_type)
        tech_table = make_object(object_cache.tech_table)
        terrain = make_object(object_cache.terrain)
        trade_good = make_object(object_cache.trade_good)
        trait = make_object(object_cache.trait)
        unit = make_object(object_cache.unit)
        war_goal = make_object(object_cache.war_goal)
        mission = make_object(object_cache.mission)
        mission_task = make_object(object_cache.mission_task)
        area = make_object(object_cache.area)
        region = make_object(object_cache.region)
        scripted_list_triggers = make_object(object_cache.scripted_list_triggers)
        scripted_list_effects = make_object(object_cache.scripted_list_effects)
    except AttributeError:
        # Something is wrong with the object cache, try to recreate objects
        sublime.set_timeout_async(lambda: create_game_objects(), 0)


def cache_all_objects():
    # Write all generated objects to cache
    path = sublime.packages_path() + f"/ImperatorTools/object_cache.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write("class GameObjectCache:\n\tdef __init__(self):")
        f.write(f"\n\t\tself.ambition = {ambition.to_json()}")
        f.write(f"\n\t\tself.building = {building.to_json()}")
        f.write(f"\n\t\tself.culture = {culture.to_json()}")
        f.write(f"\n\t\tself.culture_group = {culture_group.to_json()}")
        f.write(f"\n\t\tself.death_reason = {death_reason.to_json()}")
        f.write(f"\n\t\tself.deity = {deity.to_json()}")
        f.write(f"\n\t\tself.diplo_stance = {diplo_stance.to_json()}")
        f.write(f"\n\t\tself.econ_policy = {econ_policy.to_json()}")
        f.write(f"\n\t\tself.event_pic = {event_pic.to_json()}")
        f.write(f"\n\t\tself.event_theme = {event_theme.to_json()}")
        f.write(f"\n\t\tself.government = {government.to_json()}")
        f.write(f"\n\t\tself.governor_policy = {governor_policy.to_json()}")
        f.write(f"\n\t\tself.heritage = {heritage.to_json()}")
        f.write(f"\n\t\tself.idea = {idea.to_json()}")
        f.write(f"\n\t\tself.invention = {invention.to_json()}")
        f.write(f"\n\t\tself.law = {law.to_json()}")
        f.write(f"\n\t\tself.legion_distinction = {legion_distinction.to_json()}")
        f.write(f"\n\t\tself.levy_template = {levy_template.to_json()}")
        f.write(f"\n\t\tself.loyalty = {loyalty.to_json()}")
        f.write(f"\n\t\tself.mil_tradition = {mil_tradition.to_json()}")
        f.write(f"\n\t\tself.modifier = {modifier.to_json()}")
        f.write(f"\n\t\tself.opinion = {opinion.to_json()}")
        f.write(f"\n\t\tself.office = {office.to_json()}")
        f.write(f"\n\t\tself.party = {party.to_json()}")
        f.write(f"\n\t\tself.pop = {pop.to_json()}")
        f.write(f"\n\t\tself.price = {price.to_json()}")
        f.write(f"\n\t\tself.province_rank = {province_rank.to_json()}")
        f.write(f"\n\t\tself.religion = {religion.to_json()}")
        f.write(f"\n\t\tself.script_value = {script_value.to_json()}")
        f.write(f"\n\t\tself.scripted_effect = {scripted_effect.to_json()}")
        f.write(f"\n\t\tself.scripted_modifier = {scripted_modifier.to_json()}")
        f.write(f"\n\t\tself.scripted_trigger = {scripted_trigger.to_json()}")
        f.write(f"\n\t\tself.subject_type = {subject_type.to_json()}")
        f.write(f"\n\t\tself.tech_table = {tech_table.to_json()}")
        f.write(f"\n\t\tself.terrain = {terrain.to_json()}")
        f.write(f"\n\t\tself.trade_good = {trade_good.to_json()}")
        f.write(f"\n\t\tself.trait = {trait.to_json()}")
        f.write(f"\n\t\tself.unit = {unit.to_json()}")
        f.write(f"\n\t\tself.war_goal = {war_goal.to_json()}")
        f.write(f"\n\t\tself.mission = {mission.to_json()}")
        f.write(f"\n\t\tself.mission_task = {mission_task.to_json()}")
        f.write(f"\n\t\tself.area = {area.to_json()}")
        f.write(f"\n\t\tself.region = {region.to_json()}")
        f.write(f"\n\t\tself.scripted_list_triggers = {scripted_list_triggers.to_json()}")
        f.write(f"\n\t\tself.scripted_list_effects = {scripted_list_effects.to_json()}")
        f.write(f"\n\t\tself.named_colors = {named_colors.to_json()}")


def create_game_objects():
    t0 = time.time()

    def load_first():
        global ambition, building, culture, culture_group, death_reason, deity, diplo_stance, econ_policy, event_pic
        ambition = ImperatorAmbition()
        building = ImperatorBuilding()
        culture = ImperatorCulture()
        culture_group = ImperatorCultureGroup()
        death_reason = ImperatorDeathReason()
        deity = ImperatorDeity()
        diplo_stance = ImperatorDiplomaticStance()
        econ_policy = ImperatorEconomicPolicy()
        event_pic = ImperatorEventPicture()

    def load_second():
        global event_theme, government, governor_policy, heritage, idea, invention, law, legion_distinction
        event_theme = ImperatorEventTheme()
        government = ImperatorGovernment()
        governor_policy = ImperatorGovernorPolicy()
        heritage = ImperatorHeritage()
        idea = ImperatorIdea()
        invention = ImperatorInvention()
        law = ImperatorLaw()
        legion_distinction = ImperatorLegionDistinction()

    def load_third():
        global levy_template, loyalty, mil_tradition, modifier, opinion, office, party, pop, scripted_list_triggers, scripted_list_effects
        levy_template = ImperatorLevyTemplate()
        loyalty = ImperatorLoyalty()
        mil_tradition = ImperatorMilitaryTradition()
        modifier = ImperatorModifier()
        opinion = ImperatorOpinion()
        office = ImperatorOffice()
        party = ImperatorParty()
        pop = ImperatorPop()
        scripted_list_triggers = ImperatorScriptedList()
        scripted_list_effects = ImperatorScriptedList()

        tri_list = []
        for obj in scripted_list_triggers:
            tri_list.append(PdxScriptObject("any_" + obj.key, obj.path, obj.line))
        scripted_list_triggers.clear()
        for i in tri_list:
            scripted_list_triggers.add(i)

        ef_list = []
        for obj in scripted_list_effects:
            ef_list.append(PdxScriptObject(f"random_{obj.key}", obj.path, obj.line))
            ef_list.append(PdxScriptObject(f"every_{obj.key}", obj.path, obj.line))
            ef_list.append(PdxScriptObject(f"ordered_{obj.key}", obj.path, obj.line))
        scripted_list_effects.clear()

        for i in ef_list:
            scripted_list_effects.add(i)
        for i in scripted_list_effects.keys():
            GameData.EffectsList[i] = "Scripted list effect"
        for i in scripted_list_triggers.keys():
            GameData.TriggersList[i] = "Scripted list trigger"

    def load_fourth():
        global price, province_rank, religion, script_value, scripted_effect, scripted_modifier, scripted_trigger, subject_type, named_colors
        price = ImperatorPrice()
        province_rank = ImperatorProvinceRank()
        religion = ImperatorReligion()
        script_value = ImperatorScriptValue()
        scripted_effect = ImperatorScriptedEffect()
        scripted_modifier = ImperatorScriptedModifier()
        scripted_trigger = ImperatorScriptedTrigger()
        subject_type = ImperatorSubjectType()
        named_colors = ImperatorNamedColor()

    def load_fifth():
        global terrain, trade_good, trait, unit, war_goal, tech_table, mission, mission_task, area, region
        terrain = ImperatorTerrain()
        trade_good = ImperatorTradeGood()
        trait = ImperatorTrait()
        unit = ImperatorUnit()
        war_goal = ImperatorWargoal()
        tech_table = ImperatorTechTable()
        mission = ImperatorMission()
        mission_task = ImperatorMissionTask()
        area = ImperatorArea()
        region = ImperatorRegion()

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
    else:
        # Load cached objects
        get_objects_from_cache()

    cache_size_limit = settings.get("MaxImageCacheSize")
    cache = sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/"
    cache_files = [x for x in os.listdir(cache) if x.endswith(".png")]
    if len(cache_files) > cache_size_limit:
        for i in cache_files:
            os.remove(os.path.join(cache, i))
        sublime.status_message("Cleared Image Cache")
    add_color_scheme_scopes()


def add_color_scheme_scopes():
    # Add scopes for yml text formatting to color scheme
    DEFAULT_CS = "Packages/Color Scheme - Default/Monokai.sublime-color-scheme"
    prefs = sublime.load_settings("Preferences.sublime-settings")
    cs = prefs.get("color_scheme", DEFAULT_CS)
    scheme_cache_path = os.path.join(sublime.packages_path(), "User", "PdxTools", cs).replace(
        "tmTheme", "sublime-color-scheme"
    )
    if not os.path.exists(scheme_cache_path):
        os.makedirs(os.path.dirname(scheme_cache_path), exist_ok=True)
        rules = """{"variables": {}, "globals": {},"rules": [{"scope": "text.format.white.yml","foreground": "rgb(250, 250, 250)",},{"scope": "text.format.grey.yml","foreground": "rgb(173, 165, 160)",},{"scope": "text.format.red.yml","foreground": "rgb(210, 40, 40)",},{"scope": "text.format.green.yml","foreground": "rgb(40, 210, 40)",},{"scope": "text.format.yellow.yml","foreground": "rgb(255, 255, 0)",},{"scope": "text.format.blue.yml","foreground": "rgb(51, 214, 255)",},{"scope": "text.format.gold.yml","foreground": "#ffb027",},{"scope": "text.format.bold.yml","font_style": "bold"},{"scope": "text.format.italic.yml","font_style": "italic"}]}"""
        with open(scheme_cache_path, "w") as f:
            f.write(rules)


def write_data_to_syntax():
    fake_syntax_path = (
        sublime.packages_path() + "/ImperatorTools/Imperator Script/ImperatorSyntax.fake-sublime-syntax"
    )
    real_syntax_path = (
        sublime.packages_path() + "/ImperatorTools/Imperator Script/ImperatorSyntax.sublime-syntax"
    )
    with open(fake_syntax_path, "r") as file:
        lines = file.read()

    # Append all game objects to auto-generated-content section
    lines += write_syntax(scripted_trigger.keys(), "Scripted Triggers", "string.scripted.trigger")
    lines += write_syntax(scripted_modifier.keys(), "Scripted Triggers", "string.scripted.modifier")
    lines += write_syntax(scripted_list_triggers.keys(), "Scripted List", "string.scripted.list")
    lines += write_syntax(scripted_effect.keys(), "Scripted Effects", "keyword.scripted.effect")
    lines += write_syntax(scripted_list_effects.keys(), "Scripted Effects", "keyword.scripted.list")
    lines += write_syntax(script_value.keys(), "Scripted Values", "storage.type.script.value")

    # All GameObjects get entity.name scope
    lines += write_syntax(ambition.keys(), "Ambition", "entity.name.imperator.ambition")
    lines += write_syntax(building.keys(), "Building", "entity.name.imperator.building")
    lines += write_syntax(culture.keys(), "Culture", "entity.name.imperator.culture")
    lines += write_syntax(culture_group.keys(), "Culture Group", "entity.name.imperator.culture.group")
    lines += write_syntax(death_reason.keys(), "Death Reason", "entity.name.imperator.death.reason")
    lines += write_syntax(deity.keys(), "Deity", "entity.name.imperator.deity")
    lines += write_syntax(diplo_stance.keys(), "Diplomatic Stance", "entity.name.imperator.diplo.stance")
    lines += write_syntax(econ_policy.keys(), "Economic Policy", "entity.name.imperator.econ.policy")
    lines += write_syntax(event_pic.keys(), "Event Picture", "entity.name.imperator.event.pic")
    lines += write_syntax(event_theme.keys(), "Event Theme", "entity.name.imperator.event.theme")
    lines += write_syntax(named_colors.keys(), "Named Colors", "entity.name.named.colors")
    lines += write_syntax(government.keys(), "Government", "entity.name.imperator.government")
    lines += write_syntax(governor_policy.keys(), "Governor Policy", "entity.name.imperator.governor.policy")
    lines += write_syntax(heritage.keys(), "Heritage", "entity.name.imperator.heritage")
    lines += write_syntax(idea.keys(), "Idea", "entity.name.imperator.idea")
    lines += write_syntax(invention.keys(), "Invention", "entity.name.imperator.invention")
    lines += write_syntax(law.keys(), "Law", "entity.name.imperator.law")
    lines += write_syntax(
        legion_distinction.keys(), "Legion Distinction", "entity.name.imperator.legion.distinction"
    )
    lines += write_syntax(levy_template.keys(), "Levy Template", "entity.name.imperator.levy.template")
    lines += write_syntax(loyalty.keys(), "Loyalty", "entity.name.imperator.loyalty")
    lines += write_syntax(mil_tradition.keys(), "Military Tradition", "entity.name.imperator.mil.tradition")
    lines += write_syntax(modifier.keys(), "Modifier", "entity.name.imperator.modifier")
    lines += write_syntax(opinion.keys(), "Opinion", "entity.name.imperator.opinion")
    lines += write_syntax(office.keys(), "Office", "entity.name.imperator.office")
    lines += write_syntax(party.keys(), "Party", "entity.name.imperator.party")
    lines += write_syntax(pop.keys(), "Pop Type", "entity.name.imperator.pop")
    lines += write_syntax(price.keys(), "Price", "entity.name.imperator.price")
    lines += write_syntax(province_rank.keys(), "Province Rank", "entity.name.imperator.province.rank")
    lines += write_syntax(religion.keys(), "Religion", "entity.name.imperator.religion")
    lines += write_syntax(subject_type.keys(), "Subject Type", "entity.name.imperator.subject.type")
    lines += write_syntax(tech_table.keys(), "Technology Table", "entity.name.imperator.tech.table")
    lines += write_syntax(terrain.keys(), "Terrain", "entity.name.imperator.terrain")
    lines += write_syntax(trade_good.keys(), "Trade Good", "entity.name.imperator.trade.good")
    lines += write_syntax(trait.keys(), "Trait", "entity.name.imperator.trait")
    lines += write_syntax(unit.keys(), "Unit", "entity.name.imperator.unit")
    lines += write_syntax(war_goal.keys(), "War Goal", "entity.name.imperator.war.goal")
    lines += write_syntax(mission.keys(), "Mission", "entity.name.imperator.mission")
    lines += write_syntax(mission_task.keys(), "Mission Task", "entity.name.imperator.mission.task")
    lines += write_syntax(mission.keys(), "Mission", "entity.name.imperator.mission")
    lines += write_syntax(area.keys(), "Area", "entity.name.imperator.area")
    lines += write_syntax(region.keys(), "Region", "entity.name.imperator.region")

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
        font-size: 1.0rem;
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
"""

FIND_SIMPLE_DECLARATION_RE = '\s?=\s?(")?'
FIND_ERROR_RE = '\s?=\s?"?([A-Za-z_][A-Za-z_0-9]*)"?'
FIND_SCOPE_RE = ':"?([A-Za-z_][A-Za-z_0-9]*)"?'


class ImperatorCompletionsEventListener(sublime_plugin.EventListener):
    def __init__(self):
        self.show_ambitions = False
        self.show_ambitions_views = []
        self.show_buildings = False
        self.show_buildings_views = []
        self.show_cultures = False
        self.show_cultures_views = []
        self.show_culture_groups = False
        self.show_culture_groups_views = []
        self.death_reasons = False
        self.death_reasons_views = []
        self.show_deities = False
        self.show_deities_views = []
        self.diplo_stances = False
        self.diplo_stances_views = []
        self.economic_policies = False
        self.economic_policies_views = []
        self.event_pics = False
        self.event_pics_views = []
        self.event_themes = False
        self.event_themes_views = []
        self.governements = False
        self.governements_views = []
        self.governor_policies = False
        self.governor_policies_views = []
        self.heritages = False
        self.heritage_views = []
        self.ideas = False
        self.ideas_views = []
        self.inventions = False
        self.inventions_views = []
        self.laws = False
        self.laws_views = []
        self.distinctions = False
        self.distinctions_views = []
        self.loyalties = False
        self.loyalties_views = []
        self.traditions = False
        self.traditions_views = []
        self.missions = False
        self.missions_views = []
        self.mission_tasks = False
        self.mission_tasks_views = []
        self.modifiers = False
        self.modifiers_views = []
        self.op_mods = False
        self.op_mods_views = []
        self.offices = False
        self.offices_views = []
        self.parties = False
        self.parties_views = []
        self.prices = False
        self.prices_views = []
        self.pop_types = False
        self.pop_types_views = []
        self.prov_ranks = False
        self.prov_ranks_views = []
        self.religions = False
        self.religions_views = []
        self.subjects = False
        self.subjects_views = []
        self.tech_tables = False
        self.tech_tables_views = []
        self.terrains = False
        self.terrains_views = []
        self.goods = False
        self.goods_views = []
        self.traits = False
        self.traits_views = []
        self.units = False
        self.units_views = []
        self.war_goals = False
        self.war_goals_views = []

        self.areas = False
        self.areas_views = []
        self.regions = False
        self.regions_views = []

        self.trigger_field = False
        self.trigger_views = []

        self.effect_field = False
        self.effect_views = []

        self.modifier_field = False
        self.modfier_views = []

        self.mtth_field = False
        self.mtth_views = []
        self.named_colors = False
        self.named_colors_views = []

    def on_deactivated_async(self, view):
        """
        Remove field states when view loses focus
        if cursor was in a field in the old view but not the new view the completions will still be accurate
        save the id of the view so it can be readded when it regains focus
        """
        vid = view.id()
        if self.named_colors:
            self.named_colors = False
            self.named_colors_views.append(vid)
        if self.trigger_field:
            self.trigger_field = False
            self.trigger_views.append(vid)
        if self.effect_field:
            self.effect_field = False
            self.effect_views.append(vid)
        if self.modifier_field:
            self.modifier_field = False
            self.modfier_views.append(vid)
        if self.mtth_field:
            self.mtth_field = False
            self.mtth_views.append(vid)
        if self.show_ambitions:
            self.show_ambitions = False
            self.show_ambitions_views.append(vid)
        if self.show_buildings:
            self.show_buildings = False
            self.show_buildings_views.append(vid)
        if self.show_cultures:
            self.show_cultures = False
            self.show_cultures_views.append(vid)
        if self.show_culture_groups:
            self.show_culture_groups = False
            self.show_culture_groups_views.append(vid)
        if self.show_deities:
            self.show_deities = False
            self.show_deities_views.append(vid)
        if self.death_reasons:
            self.death_reasons = False
            self.death_reasons_views.append(vid)
        if self.diplo_stances:
            self.diplo_stances = False
            self.diplo_stances_views.append(vid)
        if self.economic_policies:
            self.economic_policies = False
            self.economic_policies_views.append(vid)
        if self.event_pics:
            self.event_pics = False
            self.event_pics_views.append(vid)
        if self.event_themes:
            self.event_themes = False
            self.event_themes_views.append(vid)
        if self.governements:
            self.governements = False
            self.governements_views.append(vid)
        if self.governor_policies:
            self.governor_policies = False
            self.governor_policies_views.append(vid)
        if self.heritages:
            self.heritages = False
            self.heritage_views.append(vid)
        if self.ideas:
            self.ideas = False
            self.ideas_views.append(vid)
        if self.inventions:
            self.inventions = False
            self.inventions_views.append(vid)
        if self.laws:
            self.laws = False
            self.laws_views.append(vid)
        if self.distinctions:
            self.distinctions = False
            self.distinctions_views.append(vid)
        if self.loyalties:
            self.loyalties = False
            self.loyalties_views.append(vid)
        if self.traditions:
            self.traditions = False
            self.traditions_views.append(vid)
        if self.missions:
            self.missions = False
            self.missions_views.append(vid)
        if self.mission_tasks:
            self.mission_tasks = False
            self.mission_tasks_views.append(vid)
        if self.modifiers:
            self.modifiers = False
            self.modifiers_views.append(vid)
        if self.op_mods:
            self.op_mods = False
            self.op_mods_views.append(vid)
        if self.offices:
            self.offices = False
            self.offices_views.append(vid)
        if self.parties:
            self.parties = False
            self.parties_views.append(vid)
        if self.prices:
            self.prices = False
            self.prices_views.append(vid)
        if self.pop_types:
            self.pop_types = False
            self.pop_types_views.append(vid)
        if self.prov_ranks:
            self.prov_ranks = False
            self.prov_ranks_views.append(vid)
        if self.religions:
            self.religions = False
            self.religions_views.append(vid)
        if self.subjects:
            self.subjects = False
            self.subjects_views.append(vid)
        if self.tech_tables:
            self.tech_tables = False
            self.tech_tables_views.append(vid)
        if self.terrains:
            self.terrains = False
            self.terrains_views.append(vid)
        if self.goods:
            self.goods = False
            self.goods_views.append(vid)
        if self.traits:
            self.traits = False
            self.traits_views.append(vid)
        if self.units:
            self.units = False
            self.units_views.append(vid)
        if self.war_goals:
            self.war_goals = False
            self.war_goals_views.append(vid)
        if self.areas:
            self.areas = False
            self.areas_views.append(vid)
        if self.regions:
            self.regions = False
            self.regions_views.append(vid)

    def on_activated_async(self, view):
        vid = view.id()
        if vid in self.trigger_views:
            self.trigger_field = True
            self.trigger_views.remove(vid)
        if vid in self.effect_views:
            self.effect_field = True
            self.effect_views.remove(vid)
        if vid in self.modfier_views:
            self.modifier_field = True
            self.modfier_views.remove(vid)
        if vid in self.mtth_views:
            self.mtth_field = True
            self.mtth_views.remove(vid)
        if vid in self.show_ambitions_views:
            self.show_ambitions = True
            self.show_ambitions_views.remove(vid)
        if vid in self.show_buildings_views:
            self.show_buildings = True
            self.show_buildings_views.remove(vid)
        if vid in self.show_cultures_views:
            self.show_cultures = True
            self.show_cultures_views.remove(vid)
        if vid in self.show_deities_views:
            self.show_deities = True
            self.show_deities_views.remove(vid)
        if vid in self.show_culture_groups_views:
            self.show_culture_groups = True
            self.show_culture_groups_views.remove(vid)
        if vid in self.death_reasons_views:
            self.death_reasons = True
            self.death_reasons_views.remove(vid)
        if vid in self.diplo_stances_views:
            self.diplo_stances = True
            self.diplo_stances_views.remove(vid)
        if vid in self.economic_policies_views:
            self.economic_policies = True
            self.economic_policies_views.remove(vid)
        if vid in self.event_pics_views:
            self.event_pics = True
            self.event_pics_views.remove(vid)
        if vid in self.event_themes_views:
            self.event_themes = True
            self.event_themes_views.remove(vid)
        if vid in self.governements_views:
            self.governements = True
            self.governements_views.remove(vid)
        if vid in self.governor_policies_views:
            self.governor_policies = True
            self.governor_policies_views.remove(vid)
        if vid in self.heritage_views:
            self.heritages = True
            self.heritage_views.remove(vid)
        if vid in self.ideas_views:
            self.ideas = True
            self.ideas_views.remove(vid)
        if vid in self.inventions_views:
            self.inventions = True
            self.inventions_views.remove(vid)
        if vid in self.laws_views:
            self.laws = True
            self.laws_views.remove(vid)
        if vid in self.distinctions_views:
            self.distinctions = True
            self.distinctions_views.remove(vid)
        if vid in self.loyalties_views:
            self.loyalties = True
            self.loyalties_views.remove(vid)
        if vid in self.traditions_views:
            self.traditions = True
            self.traditions_views.remove(vid)
        if vid in self.traditions_views:
            self.traditions = True
            self.traditions_views.remove(vid)
        if vid in self.missions_views:
            self.missions = True
            self.missions_views.remove(vid)
        if vid in self.mission_tasks_views:
            self.mission_tasks = True
            self.mission_tasks_views.remove(vid)
        if vid in self.mission_tasks_views:
            self.mission_tasks = True
            self.mission_tasks_views.remove(vid)
        if vid in self.modifiers_views:
            self.modifiers = True
            self.modifiers_views.remove(vid)
        if vid in self.op_mods_views:
            self.op_mods = True
            self.op_mods_views.remove(vid)
        if vid in self.offices_views:
            self.offices = True
            self.offices_views.remove(vid)
        if vid in self.parties_views:
            self.parties = True
            self.parties_views.remove(vid)
        if vid in self.prices_views:
            self.prices = True
            self.prices_views.remove(vid)
        if vid in self.pop_types_views:
            self.pop_types = True
            self.pop_types_views.remove(vid)
        if vid in self.prov_ranks_views:
            self.prov_ranks = True
            self.prov_ranks_views.remove(vid)
        if vid in self.religions_views:
            self.religions = True
            self.religions_views.remove(vid)
        if vid in self.subjects_views:
            self.subjects = True
            self.subjects_views.remove(vid)
        if vid in self.tech_tables_views:
            self.tech_tables = True
            self.tech_tables_views.remove(vid)
        if vid in self.terrains_views:
            self.terrains = True
            self.terrains_views.remove(vid)
        if vid in self.goods_views:
            self.goods = True
            self.goods_views.remove(vid)
        if vid in self.traits_views:
            self.traits = True
            self.traits_views.remove(vid)
        if vid in self.units_views:
            self.units = True
            self.units_views.remove(vid)
        if vid in self.war_goals_views:
            self.war_goals = True
            self.war_goals_views.remove(vid)
        if vid in self.areas_views:
            self.areas = True
            self.areas_views.remove(vid)
        if vid in self.regions_views:
            self.regions = True
            self.regions_views.remove(vid)
        if self.named_colors_views:
            self.named_colors = True
            self.named_colors_views.remove(vid)

    def on_query_completions(self, view, prefix, locations):
        if not view:
            return None

        try:
            if view.syntax().name != "Imperator Script":
                return None
        except AttributeError:
            return None

        fname = view.file_name()

        if self.show_ambitions:
            a = ambition.keys()
            a = sorted(a)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "A", "Ambition"),
                        details=" ",
                    )
                    # Calling sorted() twice makes it so completions are ordered by
                    # 1. the number of times they appear in the current buffer
                    # 2. if they dont appear they show up alphabetically
                    for key in sorted(a)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.named_colors:
            self.named_colors = False
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=obj.key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "C", "Named Color"),
                        details=" ",
                        annotation=obj.color,
                    )
                    for obj in named_colors
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.show_buildings:
            b = building.keys()
            b = sorted(b)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "B", "Building"),
                        details=" ",
                    )
                    for key in sorted(b)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.show_cultures:
            c = culture.keys()
            c = sorted(c)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "C", "Culture"),
                        details=" ",
                    )
                    for key in sorted(c)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.show_culture_groups:
            cg = culture_group.keys()
            cg = sorted(cg)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "C", "Culture Group"),
                        details=" ",
                    )
                    for key in sorted(cg)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.death_reasons:
            dea = death_reason.keys()
            dea = sorted(dea)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_KEYWORD, "D", "Death Reason"),
                        details=" ",
                    )
                    for key in sorted(dea)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.show_deities:
            d = deity.keys()
            d = sorted(d)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "D", "Deity"),
                        details=" ",
                    )
                    for key in sorted(d)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.diplo_stances:
            dip = diplo_stance.keys()
            dip = sorted(dip)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "D", "Diplomatic Stance"),
                        details=" ",
                    )
                    for key in sorted(dip)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.economic_policies:
            econ = econ_policy.keys()
            econ = sorted(econ)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "E", "Economic Policy"),
                        details=" ",
                    )
                    for key in sorted(econ)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.event_pics and "events" in fname:
            evp = event_pic.keys()
            evp = sorted(evp)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "E", "Event Picture"),
                        details=" ",
                    )
                    for key in sorted(evp)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.event_themes:
            evt = event_theme.keys()
            evt = sorted(evt)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "E", "Event Theme"),
                        details=" ",
                    )
                    for key in sorted(evt)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.governements:
            gov = government.keys()
            gov = sorted(gov)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "G", "Government"),
                        details=" ",
                    )
                    for key in sorted(gov)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.governor_policies:
            gov_pol = governor_policy.keys()
            gov_pol = sorted(gov_pol)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "G", "Governor Policy"),
                        details=" ",
                    )
                    for key in sorted(gov_pol)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.heritages:
            her = heritage.keys()
            her = sorted(her)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "H", "Heritage"),
                        details=" ",
                    )
                    for key in sorted(her)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.ideas:
            ida = idea.keys()
            ida = sorted(ida)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "I", "Idea"),
                        details=" ",
                    )
                    for key in sorted(ida)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.inventions:
            inv = invention.keys()
            inv = sorted(inv)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "I", "Invention"),
                        details=" ",
                    )
                    for key in sorted(inv)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.laws:
            la = law.keys()
            la = sorted(la)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "L", "Law"),
                        details=" ",
                    )
                    for key in sorted(la)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.distinctions:
            dist = legion_distinction.keys()
            dist = sorted(dist)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_KEYWORD, "D", "Distinction"),
                        details=" ",
                    )
                    for key in sorted(dist)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.loyalties:
            loy = loyalty.keys()
            loy = sorted(loy)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "L", "Loyalty"),
                        details=" ",
                    )
                    for key in sorted(loy)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.traditions:
            trad = mil_tradition.keys()
            trad = sorted(trad)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_KEYWORD, "M", "Military Tradition"),
                        details=" ",
                    )
                    for key in sorted(trad)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.missions:
            miss = mission.keys()
            miss = sorted(miss)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "M", "Mission"),
                        details=" ",
                    )
                    for key in sorted(miss)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.mission_tasks:
            tasks = mission_task.keys()
            tasks = sorted(tasks)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "M", "Mission Task"),
                        details=" ",
                    )
                    for key in sorted(tasks)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.modifiers:
            mods = modifier.keys()
            mods = sorted(mods)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "M", "Modifier"),
                        details=" ",
                    )
                    for key in sorted(mods)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.op_mods:
            op_mod = opinion.keys()
            op_mod = sorted(op_mod)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "O", "Opinion Modifier"),
                        details=" ",
                    )
                    for key in sorted(op_mod)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.offices:
            of = office.keys()
            of = sorted(of)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "O", "Office"),
                        details=" ",
                    )
                    for key in sorted(of)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.parties:
            pa = party.keys()
            pa = sorted(pa)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "P", "Party"),
                        details=" ",
                    )
                    for key in sorted(pa)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.prices:
            pr = price.keys()
            pr = sorted(pr)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "P", "Price"),
                        details=" ",
                    )
                    for key in sorted(pr)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.pop_types:
            po = pop.keys()
            po = sorted(po)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "P", "Pop Type"),
                        details=" ",
                    )
                    for key in sorted(po)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.prov_ranks:
            pr = province_rank.keys()
            pr = sorted(pr)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "P", "Province Rank"),
                        details=" ",
                    )
                    for key in sorted(pr)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.religions:
            rel = religion.keys()
            rel = sorted(rel)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "R", "Religion"),
                        details=" ",
                    )
                    for key in sorted(rel)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.subjects:
            sub = subject_type.keys()
            sub = sorted(sub)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "S", "Subject Type"),
                        details=" ",
                    )
                    for key in sorted(sub)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.tech_tables:
            tech = tech_table.keys()
            tech = sorted(tech)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "T", "Technology Table"),
                        details=" ",
                    )
                    for key in sorted(tech)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.terrains:
            ter = terrain.keys()
            ter = sorted(ter)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "T", "Terrain"),
                        details=" ",
                    )
                    for key in sorted(ter)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.goods:
            good = trade_good.keys()
            good = sorted(good)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "T", "Trade Good"),
                        details=" ",
                    )
                    for key in sorted(good)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.traits:
            tr = trait.keys()
            tr = sorted(tr)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "C", "Character Trait"),
                        details=" ",
                    )
                    for key in sorted(tr)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.units:
            u = unit.keys()
            u = sorted(u)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "U", "Unit"),
                        details=" ",
                    )
                    for key in sorted(u)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.war_goals:
            w = war_goal.keys()
            w = sorted(w)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "W", "War Goal"),
                        details=" ",
                    )
                    for key in sorted(w)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.areas:
            are = area.keys()
            are = sorted(are)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "A", "Area"),
                        details=" ",
                    )
                    for key in sorted(are)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        elif self.regions:
            reg = region.keys()
            reg = sorted(reg)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "R", "Region"),
                        details=" ",
                    )
                    for key in sorted(reg)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        else:
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
                    flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
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
                "common(\\|/)\s?(modifiers|traits|buildings|governor_policies|trade_goods)", fname
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
                    flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
                )
            if "/events/" in fname:
                return sublime.CompletionList(
                    GameData.EventsList, flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_REORDER
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

    def simple_scope_match(self, view):
        view_region = sublime.Region(0, view.size())
        view_str = view.substr(view_region)

        # Get the starting bracket index from the syntax scopes
        start_trigger_brackets = view.find_by_selector("meta.trigger.bracket")
        trigger_regions = []
        for br in start_trigger_brackets:
            trigger_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

        start_effect_brackets = view.find_by_selector("meta.effect.bracket")
        effect_regions = []
        for br in start_effect_brackets:
            effect_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

        start_ai_brackets = view.find_by_selector("meta.ai.bracket")
        ai_regions = []
        for br in start_ai_brackets:
            ai_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

        start_modifier_brackets = view.find_by_selector("meta.modifier.bracket")
        modifier_regions = []
        for br in start_modifier_brackets:
            modifier_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

        selection = view.sel()
        if not selection[0].empty():
            return

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

        self.show_status(selection[0].a, ai_regions, "mean time to happen", view)

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
                elif status == "mean time to happen":
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
                elif status == "mean time to happen":
                    self.mtth_field = False

    def reset_shown(self):
        self.show_ambitions = False
        self.show_buildings = False
        self.show_cultures = False
        self.show_culture_groups = False
        self.death_reasons = False
        self.show_deities = False
        self.diplo_stances = False
        self.economic_policies = False
        self.event_pics = False
        self.event_themes = False
        self.governements = False
        self.governor_policies = False
        self.heritages = False
        self.ideas = False
        self.inventions = False
        self.laws = False
        self.distinctions = False
        self.loyalties = False
        self.traditions = False
        self.missions = False
        self.mission_tasks = False
        self.modifiers = False
        self.op_mods = False
        self.offices = False
        self.parties = False
        self.prices = False
        self.pop_types = False
        self.prov_ranks = False
        self.religions = False
        self.subjects = False
        self.tech_tables = False
        self.terrains = False
        self.goods = False
        self.traits = False
        self.units = False
        self.war_goals = False
        self.areas = False
        self.regions = False
        self.named_colors = False

    def check_for_simple_completions(self, view, point):
        """
        Check if the current cursor position should trigger a autocompletion item
        this is for simple declarations like: remove_building = CursorHere
        """
        self.reset_shown()

        if view.substr(point) == "=":
            return

        line = view.substr(view.line(point))

        named_colors = ["color", "color1", "color2", "color3", "color4", "color5"]
        a_list = ["set_ambition", "has_ambition"]
        b_list = ["can_build_building", "has_building", "add_building_level", "remove_building_level"]
        c_list = [
            "set_culture",
            "set_pop_culture",
            "set_primary_culture",
            "primary_culture",
            "dominant_province_culture",
        ]
        cg_list = ["has_culture_group"]
        death_list = ["death_reason"]
        diplo_list = ["diplomatic_stance"]
        econ_list = ["has_low_economic_policy", "has_mid_economic_policy", "has_high_economic_policy"]
        event_pic_list = ["picture"]
        event_theme_list = ["theme"]
        gov_list = ["government", "change_government"]
        gov_policy_list = ["governor_policy", "can_change_governor_policy"]
        heritage_list = ["heritage", "set_country_heritage"]
        idea_list = ["can_change_idea", "idea"]
        invention_list = ["invention"]
        law_list = ["has_law", "change_law"]
        distinction_list = ["has_distinction"]
        loyalty_list = ["can_add_entire_loyalty_bonus", "has_loyalty", "remove_loyalty", "add_loyalty"]
        tradition_list = ["has_military_bonus"]
        mission_list = ["has_completed_mission"]
        mission_task_list = ["has_completed_mission_task"]
        modifiers_list = [
            "has_unit_modifier",
            "has_country_modifier",
            "has_province_modifier",
            "has_character_modifier",
            "has_triggered_character_modifier",
            "has_state_modifier",
            "has_country_culture_modifier",
            "remove_triggered_character_modifier",
            "remove_country_modifier",
            "remove_province_modifier",
            "add_country_modifier",
            "remove_unit_modifier",
            "remove_character_modifier",
            "add_unit_modifier",
            "add_permanent_province_modifier",
            "add_province_modifier",
            "remove_state_modifier",
            "add_character_modifier",
            "add_state_modifier",
            "add_triggered_character_modifier",
        ]
        opinion_list = ["has_opinion"]
        office_list = ["give_office", "remove_office", "can_hold_office", "office_is_empty", "has_office"]
        party_list = [
            "remove_party_leadership",
            "party",
            "is_leader_of_party",
            "is_leader_of_party_type",
            "party_type",
            "has_party_type",
            "is_party_type",
        ]
        pop_list = [
            "create_pop",
            "set_pop_type",
            "create_state_pop",
            "pop_type",
            "has_pop_type_right",
            "is_pop_type_right",
        ]
        price_list = ["subject_pays", "pay_price", "refund_price", "can_pay_price"]
        prov_rank_list = ["set_city_status", "has_province_rank"]
        religion_list = [
            "set_character_religion",
            "set_pop_religion",
            "set_country_religion",
            "has_religion",
            "pop_religion",
            "religion",
            "dominant_province_religion",
            "deity_religion",
            "religion",
        ]
        subjects_list = ["is_subject_type"]
        tech_table_list = ["has_tech_office_of"]
        terrain_list = ["terrain"]
        goods_list = ["set_trade_goods", "can_import_trade_good", "trade_goods", "is_importing_trade_good"]
        traits_list = ["force_add_trait", "add_trait", "remove_trait", "has_trait"]
        unit_list = ["add_loyal_subunit", "add_subunit", "is_dominant_unit", "sub_unit_type"]
        wg_list = ["war_goal"]
        area_list = ["area", "is_in_area", "owns_or_subject_owns_area", "owns_area"]
        region_list = ["region", "owns_or_subject_owns_region", "owns_region", "is_in_region"]

        # Named Colors
        for i in named_colors:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.named_colors = True
                    view.run_command("auto_complete")
                    break
        # Ambition
        for i in a_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2  # move over another position if quote is present
                # Check if current point is in one of 3 positions: ={1nospace}{2space}{3quote}
                if idx == point or idx + y == point or idx + 1 == point:
                    # if len([x for x in ai_strats.keys() if x in line]) == 0:
                    self.show_ambitions = True
                    view.run_command("auto_complete")
                    break
        # Building
        for i in b_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.show_buildings = True
                    view.run_command("auto_complete")
                    break
        # Culture
        for i in c_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.show_cultures = True
                    view.run_command("auto_complete")
                    break
        # Death Reasons
        for i in death_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.death_reasons = True
                    view.run_command("auto_complete")
                    break
        # Diplomatic Stances
        for i in diplo_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.diplo_stances = True
                    view.run_command("auto_complete")
                    break
        # Economic Policies
        for i in econ_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.economic_policies = True
                    view.run_command("auto_complete")
                    break
        # Event Pictures
        for i in event_pic_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.event_pics = True
                    view.run_command("auto_complete")
                    break
        # Event Themes
        for i in event_theme_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.event_themes = True
                    view.run_command("auto_complete")
                    break
        # Governments
        for i in gov_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.governements = True
                    view.run_command("auto_complete")
                    break
        # Governor Policies
        for i in gov_policy_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.governor_policies = True
                    view.run_command("auto_complete")
                    break
        # Heritages
        for i in heritage_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.heritages = True
                    view.run_command("auto_complete")
                    break
        # Ideas
        for i in idea_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.ideas = True
                    view.run_command("auto_complete")
                    break
        # Inventions
        for i in invention_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.inventions = True
                    view.run_command("auto_complete")
                    break
        # Laws
        for i in law_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.laws = True
                    view.run_command("auto_complete")
                    break
        # Legion Distinctions
        for i in distinction_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.distinctions = True
                    view.run_command("auto_complete")
                    break
        # Loyalties
        for i in loyalty_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.loyalties = True
                    view.run_command("auto_complete")
                    break
        # Military Traditions
        for i in tradition_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.traditions = True
                    view.run_command("auto_complete")
                    break
        # Missions
        for i in mission_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.missions = True
                    view.run_command("auto_complete")
                    break
        # Mission Tasks
        for i in mission_task_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.mission_tasks = True
                    view.run_command("auto_complete")
                    break
        # Modifiers
        for i in modifiers_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.modifiers = True
                    view.run_command("auto_complete")
                    break
        # Opinions
        for i in opinion_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.op_mods = True
                    view.run_command("auto_complete")
                    break
        # Offices
        for i in office_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.offices = True
                    view.run_command("auto_complete")
                    break
        # Parties
        for i in party_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.parties = True
                    view.run_command("auto_complete")
                    break
        # Pop Types
        for i in pop_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.pop_types = True
                    view.run_command("auto_complete")
                    break
        # Prices
        for i in price_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.prices = True
                    view.run_command("auto_complete")
                    break
        # Province Ranks
        for i in prov_rank_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.prov_ranks = True
                    view.run_command("auto_complete")
                    break
        # Religions
        for i in religion_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.religions = True
                    view.run_command("auto_complete")
                    break
        # Subject Types
        for i in subjects_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.subjects = True
                    view.run_command("auto_complete")
                    break
        # Tech Tables
        for i in tech_table_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.tech_tables = True
                    view.run_command("auto_complete")
                    break
        # Terrain
        for i in terrain_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.terrains = True
                    view.run_command("auto_complete")
                    break
        # Trade Goods
        for i in goods_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.goods = True
                    view.run_command("auto_complete")
                    break
        # Traits
        for i in traits_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.traits = True
                    view.run_command("auto_complete")
                    break
        # Units
        for i in unit_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.units = True
                    view.run_command("auto_complete")
                    break
        # War Goals
        for i in wg_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.war_goals = True
                    view.run_command("auto_complete")
                    break
        # Areas
        for i in region_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.regions = True
                    view.run_command("auto_complete")
                    break
        # Regions
        for i in area_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.areas = True
                    view.run_command("auto_complete")
                    break
        # Culture Groups
        for i in cg_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.show_culture_groups = True
                    view.run_command("auto_complete")
                    break
        # Culture Scope
        if "culture:" in line:
            idx = (
                line.index("culture:") + view.line(point).a + len("culture:")
            )  # add the length of "culture:" so index is at the end where completion should happen
            if idx == point:
                self.show_cultures = True
                view.run_command("auto_complete")
        # Culture Group Scope
        if "culture_group:" in line:
            idx = line.index("culture_group:") + view.line(point).a + len("culture_group:")
            if idx == point:
                self.show_culture_groups = True
                view.run_command("auto_complete")
        # Deity Scope
        if "deity:" in line:
            idx = line.index("deity:") + view.line(point).a + len("deity:")
            if idx == point:
                self.show_deities = True
                view.run_command("auto_complete")
        # Party Scope
        if "party:" in line:
            idx = line.index("party:") + view.line(point).a + len("party:")
            if idx == point:
                self.parties = True
                view.run_command("auto_complete")
        if "religion:" in line:
            idx = line.index("religion:") + view.line(point).a + len("religion:")
            if idx == point:
                self.religions = True
                view.run_command("auto_complete")
        if "area:" in line:
            idx = line.index("area:") + view.line(point).a + len("area:")
            if idx == point:
                self.areas = True
                view.run_command("auto_complete")
        if "region:" in line:
            idx = line.index("region:") + view.line(point).a + len("region:")
            if idx == point:
                self.regions = True
                view.run_command("auto_complete")

    def check_for_complex_completions(self, view, point):
        view_str = view.substr(sublime.Region(0, view.size()))

        if "inventions" in view.file_name():
            for br in view.find_by_selector("meta.invention.bracket"):
                i = sublime.Region(br.a, self.getIndex(view_str, br.a))
                if i.contains(point):
                    self.inventions = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.op.mod.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            x = view.substr(i)
            to_find = "modifier = "
            if to_find in x:
                found_point = (x.index(to_find) + len(to_find)) + i.a
                if found_point == point:
                    self.op_mods = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.party.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            x = view.substr(i)
            to_find = "party = "
            if to_find in x:
                found_point = (x.index(to_find) + len(to_find)) + i.a
                if found_point == point:
                    self.parties = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.pop.type.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            x = view.substr(i)
            to_find = "type = "
            if to_find in x:
                found_point = (x.index(to_find) + len(to_find)) + i.a
                if found_point == point:
                    self.pop_types = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.subject.type.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            x = view.substr(i)
            to_find = "type = "
            if to_find in x:
                found_point = (x.index(to_find) + len(to_find)) + i.a
                if found_point == point:
                    self.subjects = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.tech.table.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            x = view.substr(i)
            to_find = "technology = "
            if to_find in x:
                found_point = (x.index(to_find) + len(to_find)) + i.a
                if found_point == point:
                    self.tech_tables = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.trade.good.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            x = view.substr(i)
            to_find = "target = "
            if to_find in x:
                found_point = (x.index(to_find) + len(to_find)) + i.a
                if found_point == point:
                    self.tech_tables = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.trait.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            if i.contains(point):
                self.traits = True
                view.run_command("auto_complete")

        for br in view.find_by_selector("meta.unit.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            x = view.substr(i)
            to_find = "type = "
            if to_find in x:
                found_point = (x.index(to_find) + len(to_find)) + i.a
                if found_point == point:
                    self.units = True
                    view.run_command("auto_complete")

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

    def validate(self, text):
        try:
            text = int(text)
            return True
        except ValueError:
            sublime.set_timeout(lambda: sublime.status_message("Number of Missions must be an Integer!"), 0)
            return False


class ImpMissionMakerCommand(sublime_plugin.TextCommand):
    def run(self, edit, name, event_name, mission_count):
        sublime.run_command("new_file")
        window = sublime.active_window()
        event_view = window.active_view()
        event_view.set_name("Events")
        text = "namespace = {}\n\n".format(event_name)
        event_view.insert(edit, len(event_view), text)
        for i in range(int(mission_count)):
            i += 1
            text = '{event_name}.{i} = {{\n    type = country_event\n\n    title = {event_name}_{i}_title\n    desc = {event_name}_{i}_desc\n    picture = great_library\n\n    option = {{\n        name = "{event_name}_{i}.a"\n        custom_tooltip = {event_name}_{i}_tooltip\n\n    }}\n}}\n'.format(
                event_name=event_name, i=i
            )
            event_view.insert(edit, len(event_view), text)

        window.run_command("new_file")
        loc_view = window.active_view()
        loc_view.set_name("Localization")
        capital_input = name.replace("_", " ").title()
        text = 'l_english:\n\n{name}:0 "{capital_input}"\n{name}_DESCRIPTION:0 "Mission description"\n{name}_CRITERIA_DESCRIPTION:0 "This mission will be completed when"\n{name}_BUTTON_TOOLTIP:0 ""\n\n#Missions\n\n'.format(
            name=name, capital_input=capital_input
        )
        loc_view.insert(edit, len(loc_view), text)
        for i in range(int(mission_count)):
            i += 1
            text = '{name}_task_{i}:0 ""\n{name}_DESC:0 ""\n\n'.format(i=i, name=name)
            loc_view.insert(edit, len(loc_view), text)
        text = "\n#Tooltips\n\n\n"
        loc_view.insert(edit, len(loc_view), text)
        text = "\n#Modifiers\n\n\n"
        loc_view.insert(edit, len(loc_view), text)
        text = "\n#Events\n"
        loc_view.insert(edit, len(loc_view), text)
        for i in range(int(mission_count)):
            i += 1
            text = '{event_name}_{i}_title:0 "${name}_task_{i}$"\n{event_name}_{i}_desc:0 ""\n{event_name}_{i}.a:0 ""\n{event_name}_{i}_tooltip:0 "The mission task \'#Y ${name}_task_{i}$#!\' has now been #G Completed#!!"\n\n'.format(
                name=name, i=i, event_name=event_name
            )
            loc_view.insert(edit, len(loc_view), text)

        window.run_command("new_file")
        mission_view = window.active_view()
        mission_view.set_name("Mission Tree")
        text = '{name} = {{\n    header = "mission_image_general"\n    icon = "general_1"\n\n    repeatable = no\n    chance = 1000\n\n    potential = {{\n        NOT = {{ has_variable = mission_cooldown_var }}\n    }}\n\n    abort = {{}}\n    on_start = {{\n        start_mission_ai_effect = yes\n    }}\n    on_abort = {{\n        custom_tooltip = general_mission_cooldown_tt\n        set_variable = {{\n            name = mission_cooldown_var\n            days = 7300\n        }}\n    }}\n    on_completion = {{}}'.format(
            name=name
        )
        mission_view.insert(edit, len(mission_view), text)
        for i in range(int(mission_count)):
            i += 1
            text = '\n    {name}_task_{i} = {{\n        icon = "task_political"\n        allow = {{}}\n        on_completion = {{\n            trigger_event = {event_name}.{i}\n            show_as_tooltip = {{\n\n            }}\n        }}\n    }}'.format(
                name=name, i=i, event_name=event_name
            )
            mission_view.insert(edit, len(mission_view), text)

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
        self.view = None
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
        with open(path, "r+b") as fp:
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
                        flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE),
                    )
                    panel.add_regions(
                        "encoding",
                        [sublime.Region(len(panel) - 30, len(panel) - 16)],
                        "underline.good",
                        flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE),
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
                        flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE),
                    )
                    # new good encoding
                    panel.add_regions(
                        "encoding",
                        [sublime.Region(len(panel) - 21, len(panel) - 16)],
                        "underline.good",
                        flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE),
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
        hoverBody = """
            <body id="vic-body">
                <style>%s</style>
                <p>%s</p>
            </body>
        """ % (
            style,
            desc,
        )

        view.show_popup(
            hoverBody,
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
            if view.match_selector(point, "keyword.effect") or view.match_selector(point, "support.function"):
                show_hover_docs(view, point, "keyword.effect", GameData.EffectsList)

            if view.match_selector(point, "string.trigger"):
                GameData.TriggersList.update(GameData.CustomTriggersList)
                show_hover_docs(view, point, "string.trigger", GameData.TriggersList)

            if view.match_selector(point, "storage.type.scope") or view.match_selector(point, "support.function.boolean"):
                GameData.ScopesList.update(GameData.CustomScopesList)
                show_hover_docs(view, point, "storage.type.scope", GameData.ScopesList)

            # Do everything that requires fetching GameObjects in non-blocking thread
            sublime.set_timeout_async(lambda: self.do_hover_async(view, point), 0)

        # Texture popups can happen for both script and gui files
        if settings.get("TextureOpenPopup") == True:
            posLine = view.line(point)
            if ".dds" in view.substr(posLine):
                texture_raw_start = view.find("gfx", posLine.a)
                texture_raw_end = view.find(".dds", posLine.a)
                texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
                texture_raw_path = view.substr(texture_raw_region)
                full_texture_path = imperator_files_path + "/" + texture_raw_path
                if not os.path.exists(full_texture_path):
                    # Check mod paths if it's not vanilla
                    for mod in imperator_mod_files:
                        if os.path.exists(mod):
                            if mod.endswith("mod"):
                                # if it is the path to the mod directory, get all directories in it
                                for directory in [f.path for f in os.scandir(mod) if f.is_dir()]:
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
                    self.show_texture_hover_popup(view, point, texture_name, full_texture_path)

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
                    view, point, word, PdxScriptObject(word, fname, current_line_num), "Saved Scope"
                )
            else:
                self.show_popup_default(
                    view, point, word, PdxScriptObject(word, fname, current_line_num), "Saved Variable"
                )

        if view.match_selector(point, "entity.name.function.var.declaration"):
            self.show_popup_default(
                view, point, word, PdxScriptObject(word, fname, current_line_num), "Saved Variable"
            )
        if view.match_selector(point, "entity.name.function.scope.declaration"):
            self.show_popup_default(
                view, point, word, PdxScriptObject(word, fname, current_line_num), "Saved Scope"
            )

        # Check if currently hovered word is equal to any game object and show goto definition popup if found
        if ambition.contains(word):
            a = ambition.access(word)
            self.show_popup_default(view, point, word, a, "Ambition")
            return

        if building.contains(word):
            b = building.access(word)
            self.show_popup_default(view, point, word, b, "Building")
            return

        if culture.contains(word):
            c = culture.access(word)
            self.show_popup_default(view, point, word, c, "Culture")
            return

        if culture_group.contains(word):
            cg = culture_group.access(word)
            self.show_popup_default(view, point, word, cg, "Culture Group")
            return

        if death_reason.contains(word):
            dea = death_reason.access(word)
            self.show_popup_default(view, point, word, dea, "Death Reason")
            return

        if deity.contains(word):
            dei = deity.access(word)
            self.show_popup_default(view, point, word, dei, "Deity")
            return

        if diplo_stance.contains(word):
            ds = diplo_stance.access(word)
            self.show_popup_default(view, point, word, ds, "Diplomatic Stance")
            return

        if econ_policy.contains(word):
            ecp = econ_policy.access(word)
            self.show_popup_default(view, point, word, ecp, "Economic Policy")
            return

        if event_pic.contains(word):
            evp = event_pic.access(word)
            self.show_popup_default(view, point, word, evp, "Event Picture")
            return

        if event_theme.contains(word):
            evt = event_theme.access(word)
            self.show_popup_default(view, point, word, evt, "Event Theme")
            return

        if government.contains(word):
            gov = government.access(word)
            self.show_popup_default(view, point, word, gov, "Government")
            return

        if governor_policy.contains(word):
            gov_pol = governor_policy.access(word)
            self.show_popup_default(view, point, word, gov_pol, "Governor Policy")
            return

        if heritage.contains(word):
            her = heritage.access(word)
            self.show_popup_default(view, point, word, her, "Heritage")
            return

        if named_colors.contains(word):
            self.show_popup_named_color(view, point, word, named_colors.access(word), "Named Color")

        if idea.contains(word):
            ide = idea.access(word)
            self.show_popup_default(view, point, word, ide, "Idea")
            return

        if invention.contains(word):
            inv = invention.access(word)
            self.show_popup_default(view, point, word, inv, "Invention")
            return

        if law.contains(word):
            la = law.access(word)
            self.show_popup_default(view, point, word, la, "law")
            return

        if legion_distinction.contains(word):
            leg = legion_distinction.access(word)
            self.show_popup_default(view, point, word, leg, "Legion Distinction")
            return

        if levy_template.contains(word):
            lev = levy_template.access(word)
            self.show_popup_default(view, point, word, lev, "Levy Template")
            return

        if loyalty.contains(word):
            loy = loyalty.access(word)
            self.show_popup_default(view, point, word, loy, "Loyalty")
            return

        if mil_tradition.contains(word):
            mil = mil_tradition.access(word)
            self.show_popup_default(view, point, word, mil, "Military Tradition")
            return

        if modifier.contains(word):
            mo = modifier.access(word)
            self.show_popup_default(view, point, word, mo, "Modifier")
            return

        if opinion.contains(word):
            op = opinion.access(word)
            self.show_popup_default(view, point, word, op, "Opinion")
            return

        if office.contains(word):
            of = office.access(word)
            self.show_popup_default(view, point, word, of, "Office")
            return

        if party.contains(word):
            pa = party.access(word)
            self.show_popup_default(view, point, word, pa, "Party")
            return

        if pop.contains(word):
            po = pop.access(word)
            self.show_popup_default(view, point, word, po, "Pop Type")
            return

        if price.contains(word):
            pr = price.access(word)
            self.show_popup_default(view, point, word, pr, "Price")
            return

        if province_rank.contains(word):
            pvr = province_rank.access(word)
            self.show_popup_default(view, point, word, pvr, "Province Rank")
            return

        if religion.contains(word):
            rel = religion.access(word)
            self.show_popup_default(view, point, word, rel, "Religion")
            return

        if script_value.contains(word):
            scv = script_value.access(word)
            self.show_popup_default(view, point, word, scv, "Script Value")
            return

        if scripted_effect.contains(word):
            sce = scripted_effect.access(word)
            self.show_popup_default(view, point, word, sce, "Scripted Effect")
            return

        if scripted_modifier.contains(word):
            scm = scripted_modifier.access(word)
            self.show_popup_default(view, point, word, scm, "Scripted Modifier")
            return

        if scripted_trigger.contains(word):
            sct = scripted_trigger.access(word)
            self.show_popup_default(view, point, word, sct, "Scripted Trigger")
            return

        if subject_type.contains(word):
            st = subject_type.access(word)
            self.show_popup_default(view, point, word, st, "Subject Type")
            return

        if tech_table.contains(word):
            tech = tech_table.access(word)
            self.show_popup_default(view, point, word, tech, "Technology Table")
            return

        if terrain.contains(word):
            ter = terrain.access(word)
            self.show_popup_default(view, point, word, ter, "Terrain")
            return

        if trade_good.contains(word):
            tr = trade_good.access(word)
            self.show_popup_default(view, point, word, tr, "Trade Good")
            return

        if trait.contains(word):
            c_trait = trait.access(word)
            self.show_popup_default(view, point, word, c_trait, "Trait")
            return

        if unit.contains(word):
            u = unit.access(word)
            self.show_popup_default(view, point, word, u, "Unit")
            return

        if war_goal.contains(word):
            w = war_goal.access(word)
            self.show_popup_default(view, point, word, w, "War Goal")
            return

        if mission.contains(word):
            m = mission.access(word)
            self.show_popup_default(view, point, word, m, "Mission")
            return

        if mission_task.contains(word):
            mt = mission_task.access(word)
            self.show_popup_default(view, point, word, mt, "Mission Task")
            return

        if area.contains(word):
            ar = area.access(word)
            self.show_popup_default(view, point, word, ar, "Area")
            return

        if region.contains(word):
            reg = region.access(word)
            self.show_popup_default(view, point, word, reg, "Region")
            return

        if scripted_list_triggers.contains(word):
            lit = scripted_list_triggers.access(word)
            self.show_popup_default(view, point, word, lit, "Scripted List")
            return

        if scripted_list_effects.contains(word):
            lie = scripted_list_effects.access(word)
            self.show_popup_default(view, point, word, lie, "Scripted List")
            return

    def show_popup_default(self, view, point, word, PdxObject, header):
        word_line_num = view.rowcol(point)[0] + 1
        word_file = view.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
        definition = ""
        definitions = []

        if header == "Saved Scope" or header == "Saved Variable":
            for win in sublime.windows():
                for i in [v for v in win.views() if v and v.file_name()]:
                    if i.file_name().endswith(".txt"):
                        variables = [
                            x
                            for x in i.find_by_selector("entity.name.function.var.declaration")
                            if i.substr(x) == PdxObject.key
                        ]
                        variables.extend(
                            [
                                x
                                for x in i.find_by_selector("entity.name.function.scope.declaration")
                                if i.substr(x) == PdxObject.key
                            ]
                        )
                        for r in variables:
                            line = i.rowcol(r.a)[0] + 1
                            path = i.file_name()
                            if line == word_line_num and path == PdxObject.path:
                                continue
                            else:
                                definitions.append(PdxScriptObject(PdxObject.key, path, line))

            if len(definitions) == 1:
                definition = (
                    f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                )
            elif len(definitions) > 1:
                definition = (
                    f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                )
            for obj in definitions:
                goto_args = {"path": obj.path, "line": obj.line}
                goto_url = sublime.command_url("goto_script_object_definition", goto_args)
                definition += """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;""" % (
                    goto_url,
                    obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    obj.line,
                    obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    obj.line,
                )
                goto_right_args = {"path": obj.path, "line": obj.line}
                goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )
        else:
            if word_line_num != PdxObject.line and view.file_name() != PdxObject.path:
                definition = (
                    f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                )

                goto_args = {"path": PdxObject.path, "line": PdxObject.line}
                goto_url = sublime.command_url("goto_script_object_definition", goto_args)
                definition += """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;""" % (
                    goto_url,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                )
                goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
                goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        references = []
        ref = ""
        for win in sublime.windows():
            for i in [v for v in win.views() if v and v.file_name()]:
                if i.file_name().endswith(".txt"):
                    view_region = sublime.Region(0, i.size())
                    view_str = i.substr(view_region)
                    for j, line in enumerate(view_str.splitlines()):
                        definition_found = False
                        if PdxObject.key in line and "#" not in line:
                            filename = i.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
                            line_num = j + 1
                            if definitions:
                                # Don't do definitions for scopes and variables
                                for obj in definitions:
                                    if obj.line == line_num and obj.path == i.file_name():
                                        definition_found = True
                            if word_line_num == line_num and word_file == filename:
                                # Don't do current word
                                continue
                            elif line_num == PdxObject.line and i.file_name() == PdxObject.path:
                                # Don't do definition
                                continue
                            if not definition_found:
                                references.append(f"{i.file_name()}|{line_num}")
        if references:
            ref = f'<p><b>References to&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for i in references:
                fname = i.split("|")[0]
                shortname = fname.replace("\\", "/").rstrip("/").rpartition("/")[2]
                line = i.split("|")[1]
                goto_args = {"path": fname, "line": line}
                goto_url = sublime.command_url("goto_script_object_definition", goto_args)
                ref += """<a href="%s" title="Open %s and goto line %s">%s:%s</a>&nbsp;""" % (
                    goto_url,
                    shortname,
                    line,
                    shortname,
                    line,
                )
                goto_right_args = {"path": fname, "line": line}
                goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
                ref += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        link = definition + ref
        if link:
            hoverBody = """
                <body id="vic-body">
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
                hoverBody,
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
        word_file = view.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
        definition = ""
        definitions = []
        if header == "Saved Scope" or header == "Saved Variable":
            for win in sublime.windows():
                for i in [v for v in win.views() if v and v.file_name()]:
                    if i.file_name().endswith(".txt") or i.file_name().endswith(".py"):
                        variables = [
                            x
                            for x in i.find_by_selector("entity.name.function.var.declaration")
                            if i.substr(x) == PdxObject.key
                        ]
                        variables.extend(
                            [
                                x
                                for x in i.find_by_selector("entity.name.function.scope.declaration")
                                if i.substr(x) == PdxObject.key
                            ]
                        )
                        for r in variables:
                            line = i.rowcol(r.a)[0] + 1
                            path = i.file_name()
                            if line == word_line_num and path == PdxObject.path:
                                continue
                            else:
                                definitions.append(PdxScriptObject(PdxObject.key, path, line))

            if len(definitions) == 1:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += (
                        f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                    )
                else:
                    definition = (
                        f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                    )
            elif len(definitions) > 1:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += (
                        f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                    )
                else:
                    definition = (
                        f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                    )
            for obj in definitions:
                goto_args = {"path": obj.path, "line": obj.line}
                goto_url = sublime.command_url("goto_script_object_definition", goto_args)
                definition += """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;""" % (
                    goto_url,
                    obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    obj.line,
                    obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    obj.line,
                )
                goto_right_args = {"path": obj.path, "line": obj.line}
                goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )
        else:
            if word_line_num != PdxObject.line and view.file_name() != PdxObject.path:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += (
                        f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                    )
                else:
                    definition = (
                        f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                    )
                goto_args = {"path": PdxObject.path, "line": PdxObject.line}
                goto_url = sublime.command_url("goto_script_object_definition", goto_args)
                definition += """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;""" % (
                    goto_url,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                )
                goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
                goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        return definition

    def show_texture_hover_popup(self, view, point, texture_name, full_texture_path):
        args = {"path": full_texture_path}
        open_texture_url = sublime.command_url("open_imperator_texture ", args)
        folder_args = {"path": full_texture_path, "folder": True}
        open_folder_url = sublime.command_url("open_imperator_texture ", folder_args)
        in_sublime_args = {"path": full_texture_path, "mode": "in_sublime"}
        inline_args = {"path": full_texture_path, "point": point}
        in_sublime_args = {"path": full_texture_path, "mode": "in_sublime"}
        open_in_sublime_url = sublime.command_url("open_imperator_texture ", in_sublime_args)
        open_inline_url = sublime.command_url("imperator_show_texture ", inline_args)
        hoverBody = """
            <body id=\"vic-body\">
                <style>%s</style>
                <h1>Open Texture</h1>
                <div></div>
                <a href="%s" title="Open folder containing the texture.">Open Folder</a>
                <br>
                <a href="%s" title="Open %s.dds in the default program">Open in default program</a>
                <br>
                <a href="%s" title="Convert %s.dds to PNG and open in sublime">Open in sublime</a>
                <br>
                <a href="%s" title="Convert %s.dds to PNG show at current selection">Show Inline</a>
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
            hoverBody,
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
            hoverBody = """
                <body id="vic-body">
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
                hoverBody,
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
        view = window.open_file(l, flags)


class GotoScriptObjectDefinitionRightCommand(sublime_plugin.WindowCommand):
    def run(self, path, line):
        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, line, 0)
            self.open_location(self.window, file_path, side_by_side=True, clear_to_right=True)

    def open_location(self, window, l, side_by_side=False, replace=False, clear_to_right=False):
        flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP

        if side_by_side:
            flags |= sublime.ADD_TO_SELECTION | sublime.SEMI_TRANSIENT
            if clear_to_right:
                flags |= sublime.CLEAR_TO_RIGHT

        elif replace:
            flags |= sublime.REPLACE_MRU | sublime.SEMI_TRANSIENT
        view = window.open_file(l, flags)


class OpenImperatorTextureCommand(sublime_plugin.WindowCommand):
    def run(self, path, folder=False, mode="default_program"):
        if folder:
            end = path.rfind("/")
            path = path[0:end:]
            os.startfile(path)
        else:
            if mode == "default_program":
                os.startfile(path)
            elif mode == "in_sublime":
                simple_path = path.replace("\\", "/").rstrip("/").rpartition("/")[2].replace(".dds", ".png")
                output_file = sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/" + simple_path
                exe_path = sublime.packages_path() + "/ImperatorTools/Convert DDS/src/ConvertDDS.exe"

                if not os.path.exists(output_file):
                    # Run dds to png converter
                    self.window.run_command("exec", {"cmd": [exe_path, path, output_file], "quiet": True})
                    self.window.destroy_output_panel("exec")
                    sublime.active_window().open_file(output_file)
                else:
                    # File is already in cache, don't need to convert
                    sublime.active_window().open_file(output_file)


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

    def run(self, cmd=None, shell_cmd=None, working_dir="", encoding="utf-8", env={}, **kwargs):
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
            self.proc = Default.exec.AsyncProcess(cmd, shell_cmd, merged_env, self, **kwargs)
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
            point = self.text_point(line, 1)
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

    def show_texture(self, path, point):
        window = sublime.active_window()
        simple_path = path.replace("\\", "/").rstrip("/").rpartition("/")[2].replace(".dds", ".png")
        output_file = sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/" + simple_path
        exe_path = sublime.packages_path() + "/ImperatorTools/Convert DDS/src/ConvertDDS.exe"
        if not os.path.exists(output_file):
            window.run_command("quiet_execute", {"cmd": [exe_path, path, output_file]})
            # Wait 100ms for conversion to finish
            sublime.set_timeout_async(
                lambda: self.toggle_async(output_file, simple_path, point, window, path), 100
            )
        else:
            self.toggle_async(output_file, simple_path, point, window, path)

    def toggle_async(self, output_file, simple_path, point, window, original_path):
        # Try to convert for 500ms
        if not os.path.exists(output_file) and self.conversion_iterations < 6:
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
        if x:
            current_view = x[0]
        if pid in current_view.textures:
            current_view.textures.remove(pid)
            view.erase_phantoms(key)
        else:
            current_view.textures.append(pid)
            line_region = view.line(point)
            # Find region of texture path declaration
            # Ex: [start]texture = "gfx/interface/icons/goods_icons/meat.dds"[end]
            start = view.find('[A-Za-z_][A-Za-z_0-9]*\s?=\s?"?/?(gfx)?', line_region.a).a
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
            if size >= 24 and head.startswith(b"\211PNG\r\n\032\n") and head[12:16] == b"IHDR":
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


class ImperatorShowTextureCommand(sublime_plugin.ApplicationCommand, ImperatorShowTextureBase):
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


class ImperatorShowAllTexturesCommand(sublime_plugin.WindowCommand, ImperatorShowTextureBase):
    def run(self):
        view = self.window.active_view()
        texture_list = [x for x in view.lines(sublime.Region(0, view.size())) if ".dds" in view.substr(x)]
        for line, i in zip(texture_list, range(settings.get("MaxToggleTextures"))):
            texture_raw_start = view.find("gfx", line.a)
            texture_raw_end = view.find(".dds", line.a)
            texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
            texture_raw_path = view.substr(texture_raw_region)
            full_texture_path = imperator_files_path + "/" + texture_raw_path
            full_texture_path = full_texture_path.replace("\\", "/")
            self.show_texture(full_texture_path, texture_raw_start.a)
