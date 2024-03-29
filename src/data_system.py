"""
Plugin features related to the game's data system functions.
"""

import sublime, sublime_plugin


class ImperatorDataSystemEventListener(sublime_plugin.EventListener):
    def on_selection_modified_async(self, view):
        if not view:
            return

        try:
            if view.syntax().name != "Imperator Localization":
                return
        except AttributeError:
            return

        if len(view.sel()) == 1:
            point = view.sel()[0].a
            if view.match_selector(point, "empty.scope.prompt") or view.match_selector(
                point, "empty.scope.variable"
            ):
                view.run_command("auto_complete")

    def on_query_completions(self, view, prefix, locations):
        if not view:
            return None

        try:
            if view.syntax().name != "Imperator Localization":
                return None
        except AttributeError:
            return None

        fname = view.file_name()
        if not fname:
            return

        if len(view.sel()) == 1:
            point = view.sel()[0].a
            if view.match_selector(point, "empty.scope.prompt"):
                return self.get_prompt_completions(
                    "Scope", "entity.name.function.scope.declaration"
                )
            if view.match_selector(point, "empty.scope.variable"):
                return self.get_prompt_completions(
                    "Variable", "entity.name.function.var.declaration"
                )

    def get_prompt_completions(self, kind, selector):
        found_words = set()

        for win in sublime.windows():
            for view in [v for v in win.views() if v and v.syntax()]:
                if view.syntax().name != "Imperator Script":
                    continue

                scope_regions = view.find_by_selector(selector)
                for region in scope_regions:
                    found_words.add(view.substr(region))

        if not found_words:
            return None

        return sublime.CompletionList(
            [
                sublime.CompletionItem(
                    trigger=key,
                    completion=key,
                    completion_format=sublime.COMPLETION_FORMAT_SNIPPET,
                    kind=(sublime.KIND_ID_NAMESPACE, kind[0], kind),
                )
                for key in sorted(found_words)
            ],
            flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
            | sublime.INHIBIT_WORD_COMPLETIONS,
        )
