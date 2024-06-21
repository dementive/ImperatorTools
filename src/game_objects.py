import sublime
from typing import Dict

from .game_object_manager import GameObjectManager
from .imperator_objects import ImperatorObject
from JominiTools.src import write_syntax


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
