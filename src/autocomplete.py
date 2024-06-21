"""
Code for the autocomplete features of the plugin
"""

from JominiTools.src import JominiAutoComplete
from .game_object_manager import GameObjectManager


class AutoComplete(JominiAutoComplete):
    def init_autocomplete(self):
        manager = GameObjectManager()
        self.auto_complete_fields = {
            manager.ambition.name: [],
            manager.area.name: [],
            manager.building.name: [],
            manager.culture.name: [],
            manager.culture_group.name: [],
            manager.custom_loc.name: [],
            manager.death_reason.name: [],
            manager.deity.name: [],
            manager.diplo_stance.name: [],
            manager.econ_policy.name: [],
            manager.event_pic.name: [],
            manager.event_theme.name: [],
            manager.government.name: [],
            manager.governor_policy.name: [],
            manager.heritage.name: [],
            manager.idea.name: [],
            manager.invention.name: [],
            manager.law.name: [],
            manager.legion_distinction.name: [],
            manager.levy_template.name: [],
            manager.loyalty.name: [],
            manager.mil_tradition.name: [],
            manager.mission.name: [],
            manager.mission_task.name: [],
            manager.modifier.name: [],
            manager.named_colors.name: [],
            manager.office.name: [],
            manager.opinion.name: [],
            manager.party.name: [],
            manager.pop.name: [],
            manager.price.name: [],
            manager.province_rank.name: [],
            manager.region.name: [],
            manager.religion.name: [],
            manager.script_value.name: [],
            manager.scripted_gui.name: [],
            manager.subject_type.name: [],
            manager.tech_table.name: [],
            manager.terrain.name: [],
            manager.trade_good.name: [],
            manager.trait.name: [],
            manager.unit.name: [],
            manager.war_goal.name: [],
        }
        self.selector_flag_pairs = [
            ("meta.op.mod.bracket", manager.opinion.name, "modifier = "),
            ("meta.party.bracket", manager.party.name, "party = "),
            ("meta.pop.type.bracket", manager.pop.name, "type = "),
            ("meta.subject.type.bracket", manager.subject_type.name, "type = "),
            ("meta.tech.table.bracket", manager.tech_table.name, "technology = "),
            ("meta.trade.good.target.bracket", manager.trade_good.name, "target = "),
            ("meta.trade.good.bracket", manager.trade_good.name, "goods = "),
            ("meta.trait.bracket", manager.trait.name),
            ("meta.invention.bracket", manager.invention.name),
            ("meta.unit.bracket", manager.unit.name, "type = "),
        ]
        super().__init__(self.auto_complete_fields, self.selector_flag_pairs)
