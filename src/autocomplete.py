"""
Code for the autocomplete features of the plugin
"""

import re
import sublime, sublime_plugin
from .utils import get_index


class AutoComplete:
    def __init__(self):
        self.trigger_field = False
        self.effect_field = False
        self.modifier_field = False
        self.mtth_field = False
        self.auto_complete_fields = {
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
            "script_value": [],
            "scripted_gui": [],
            "subject_type": [],
            "tech_table": [],
            "terrain": [],
            "trade_good": [],
            "trait": [],
            "unit": [],
            "war_goal": [],
        }
        for field in self.auto_complete_fields.keys():
            setattr(self, field, False)

    def reset_shown(self):
        for i in self.auto_complete_fields.keys():
            setattr(self, i, False)

    def check_for_patterns_and_set_flag(
        self, patterns_list, flag_name, view, line, point
    ):
        for pattern in patterns_list:
            r = re.search(fr'{pattern}\s?=\s?(")?', line)
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

    def check_region_and_set_flag(
        self, selector, flag_name, view, view_str, point, string_check_and_move=None
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

    def check_for_complex_completions(self, view, point):
        view_str = view.substr(sublime.Region(0, view.size()))

        if "inventions" in view.file_name():
            for br in view.find_by_selector("meta.invention.bracket"):
                i = sublime.Region(br.a, get_index(view_str, br.a))
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
