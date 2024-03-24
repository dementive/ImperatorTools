"""
Code to handle the UTF8-BOM encoding of imperator script files
"""
import sublime, sublime_plugin
import re


def encoding_check(view):
    # Check that the current filepath is in a folder that should use UTF-8 with BOM
    # If it should be UTF-8 with BOM and it is not create error panel
    path = view.file_name()
    utf8_paths = re.search(
        r"(common/coat_of_arms|map_data/regions|map_data/areas)", path
    )  # A few special files/folders don't need BOM
    bom_paths = re.search(r"(events|common|music|localization)", path)

    old_encoding = view.encoding()
    if not old_encoding == "UTF-8 with BOM":
        if bom_paths is not None and utf8_paths is None:
            # is not bom and should be
            view.set_encoding("UTF-8 with BOM")
            error_message = f"EncodingError: Encoding is {old_encoding}, files in {bom_paths.group()} should be UTF-8 with BOM, resave to fix."

            panel = create_error_panel()
            panel.set_read_only(False)
            panel.run_command("append", {"characters": error_message})
            panel.add_regions(
                "bad_encoding",
                [sublime.Region(27, 27 + len(old_encoding))],
                "underline.bad",
                flags=(
                    sublime.DRAW_SOLID_UNDERLINE
                    | sublime.DRAW_NO_FILL
                    | sublime.DRAW_NO_OUTLINE
                ),
            )
            panel.add_regions(
                "encoding",
                [sublime.Region(len(panel) - 30, len(panel) - 16)],
                "underline.good",
                flags=(
                    sublime.DRAW_SOLID_UNDERLINE
                    | sublime.DRAW_NO_FILL
                    | sublime.DRAW_NO_OUTLINE
                ),
            )
            panel.set_read_only(True)

        if utf8_paths is not None and not old_encoding == "UTF-8":
            # is not utf-8 and should be
            view.set_encoding("UTF-8")
            error_message = f"EncodingError: Encoding is {old_encoding}, files in {utf8_paths.group()} should be UTF-8, resave to fix."

            panel = create_error_panel()
            panel.set_read_only(False)
            panel.run_command("append", {"characters": error_message})
            # bad encoding
            panel.add_regions(
                "bad_encoding",
                [sublime.Region(27, 27 + len(old_encoding))],
                "underline.bad",
                flags=(
                    sublime.DRAW_SOLID_UNDERLINE
                    | sublime.DRAW_NO_FILL
                    | sublime.DRAW_NO_OUTLINE
                ),
            )
            # new good encoding
            panel.add_regions(
                "encoding",
                [sublime.Region(len(panel) - 21, len(panel) - 16)],
                "underline.good",
                flags=(
                    sublime.DRAW_SOLID_UNDERLINE
                    | sublime.DRAW_NO_FILL
                    | sublime.DRAW_NO_OUTLINE
                ),
            )
            panel.set_read_only(True)


def create_error_panel():
    window = sublime.active_window()
    panel = window.create_output_panel("error", unlisted=True)
    panel.assign_syntax("scope:text.error")
    panel.settings().set("color_scheme", "ErrorPanel.hidden-color-scheme")
    panel.settings().set("gutter", False)
    window.run_command("show_panel", {"panel": "output.error"})
    window.focus_view(panel)
    return panel
