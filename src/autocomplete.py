"""
Code for the autocomplete features of the plugin
"""

import re
from typing import List

import sublime

from .game_object_manager import GameObjectManager
from .utils import get_index


class AutoComplete:
    def __init__(self):
        self.trigger_field = False
        self.effect_field = False
        self.modifier_field = False
        self.mtth_field = False
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
        for field in self.auto_complete_fields.keys():
            setattr(self, field, False)

    def reset_shown(self):
        for i in self.auto_complete_fields.keys():
            setattr(self, i, False)

    def check_for_patterns_and_set_flag(
        self,
        patterns_list: List[str],
        flag_name: str,
        view: sublime.View,
        line: str,
        point: int,
    ):
        for pattern in patterns_list:
            r = re.search(rf'\b{pattern}\s?=\s?(")?', line)
            if not r:
                continue
            y = 0
            idx = line.index(pattern) + view.line(point).a + len(pattern) + 2
            if r.groups()[0] == '"':
                y = 2
            if idx == point or idx + y == point or idx + 1 == point:
                setattr(self, flag_name, True)
                view.run_command("auto_complete")
                return True
        return False

    def check_pattern_and_set_flag(
        self, pattern: str, flag_name: str, view: sublime.View, line: str, point: int
    ):
        if pattern in line:
            idx = line.index(pattern) + view.line(point).a + len(pattern)
            if idx == point:
                setattr(self, flag_name, True)
                view.run_command("auto_complete")

    def check_region_and_set_flag(
        self,
        selector: str,
        flag_name: str,
        view: sublime.View,
        view_str: str,
        point: int,
        string_check_and_move=None,
    ):
        for br in view.find_by_selector(selector):
            i = sublime.Region(br.a, get_index(view_str, br.a))
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

    def check_for_complex_completions(self, view: sublime.View, point: int):
        view_str = view.substr(sublime.Region(0, view.size()))
        filename = view.file_name()

        if filename and "inventions" in filename:
            for br in view.find_by_selector("meta.invention.bracket"):
                i = sublime.Region(br.a, get_index(view_str, br.a))
                if i.contains(point):
                    self.inventions = True
                    view.run_command("auto_complete")

        manager = GameObjectManager()
        selector_flag_pairs = [
            ("meta.op.mod.bracket", manager.opinion.name, "modifier = "),
            ("meta.party.bracket", manager.party.name, "party = "),
            ("meta.pop.type.bracket", manager.pop.name, "type = "),
            ("meta.subject.type.bracket", manager.subject_type.name, "type = "),
            ("meta.tech.table.bracket", manager.tech_table.name, "technology = "),
            ("meta.trade.good.bracket", manager.trade_good.name, "target = "),
            ("meta.trait.bracket", manager.trait.name),
            ("meta.unit.bracket", manager.unit.name, "type = "),
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
