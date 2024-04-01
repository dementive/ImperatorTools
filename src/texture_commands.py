"""
Commands for opening and viewing textures in sublime or another program
"""

import os
import sys
import subprocess
import struct

import sublime, sublime_plugin
from .utils import get_syntax_name

class OpenImperatorTextureCommand(sublime_plugin.WindowCommand):
    def run(self, path: str, folder=False, mode="default_program"): # type: ignore
        if folder:
            end = path.rfind("/")
            path = path[0:end:]
            OpenImperatorTextureCommand.open_path(path)
        else:
            if mode == "default_program":
                OpenImperatorTextureCommand.open_path(path)
            elif mode == "in_sublime":
                simple_path = (
                    path.replace("\\", "/")
                    .rstrip("/")
                    .rpartition("/")[2]
                    .replace(".dds", ".png")
                )
                output_file = (
                    sublime.packages_path()
                    + "/ImperatorTools/Convert DDS/cache/"
                    + simple_path
                )
                exe_path = (
                    sublime.packages_path()
                    + "/ImperatorTools/Convert DDS/src/ConvertDDS.exe"
                )

                if not os.path.exists(output_file):
                    # Run dds to png converter
                    cmd = (
                        ["wine", exe_path, path, output_file]
                        if sublime.platform() == "linux"
                        else [exe_path, path, output_file]
                    )
                    self.window.run_command("quiet_execute", {"cmd": cmd})
                    self.window.destroy_output_panel("exec")
                    sublime.active_window().open_file(output_file)
                else:
                    # File is already in cache, don't need to convert
                    sublime.active_window().open_file(output_file)

    @staticmethod
    def open_path(path: str):
        system = sys.platform
        if system == "Darwin":  # macOS
            subprocess.Popen(("open", path))
        elif system == "Windows" or system == "win32" or system == "win":  # Windows
            os.startfile(path)
        else:  # Linux and other Unix-like systems
            subprocess.Popen(("xdg-open", path))


class ImperatorTextureEventListener(sublime_plugin.EventListener):
    def on_post_text_command(self, view: sublime.View, command_name: str, args):
        if command_name in ("left_delete", "insert"):
            if view.file_name() and get_syntax_name(view) == "Imperator Script":
                x = [v for v in views_with_shown_textures if v.id() == view.id()]
                if x:
                    x[0].update_line_count(view.rowcol(view.size())[0] + 1)

    def on_load_async(self, view: sublime.View):
        if not view:
            return

        if get_syntax_name(view) != "Imperator Script":
            return

        settings = sublime.load_settings("Imperator Syntax.sublime-settings")

        if settings.get("ShowInlineTexturesOnLoad"):
            sublime.active_window().run_command("imperator_show_all_textures")


views_with_shown_textures = set()


class ImperatorViewTextures(sublime.View):
    def __init__(self, id: int):
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
    total_conversion_attempts = 2 if sublime.platform() == "linux" else 6

    def show_texture(self, path: str, point: int):
        window = sublime.active_window()
        simple_path = (
            path.replace("\\", "/")
            .rstrip("/")
            .rpartition("/")[2]
            .replace(".dds", ".png")
        )
        output_file = (
            sublime.packages_path() + "/ImperatorTools/Convert DDS/cache/" + simple_path
        )
        exe_path = (
            sublime.packages_path() + "/ImperatorTools/Convert DDS/src/ConvertDDS.exe"
        )
        if not os.path.exists(output_file):
            cmd = (
                ["wine", exe_path, path, output_file]
                if sublime.platform() == "linux"
                else [exe_path, path, output_file]
            )
            window.run_command("quiet_execute", {"cmd": cmd})
            window.destroy_output_panel("exec")
            # Wait 100ms for conversion to finish
            timeout = 2000 if sublime.platform() == "linux" else 100
            sublime.set_timeout_async(
                lambda: self.toggle_async(
                    output_file, simple_path, point, window, path
                ),
                timeout,
            )
        else:
            self.toggle_async(output_file, simple_path, point, window, path)

    def toggle_async(self, output_file: str, simple_path: str, point: int, window: sublime.Window, original_path: str):
        # Try to convert for 500ms

        if (
            not os.path.exists(output_file)
            and self.conversion_iterations < self.total_conversion_attempts
        ):
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
            if view is None:
                return

            if os.path.exists(output_file):
                self.toggle(simple_path, view, html, point)

    def toggle(self, key: str, view: sublime.View, html: str, point: int):
        pid = key + "|" + str(view.rowcol(point)[0] + 1)
        x = ImperatorViewTextures(view.id())
        views_with_shown_textures.add(x)
        x = [v for v in views_with_shown_textures if v.id() == view.id()]
        current_view = ""
        if x:
            current_view = x[0]
        if not current_view:
            return

        if pid in current_view.textures:
            current_view.textures.remove(pid)
            view.erase_phantoms(key)
        else:
            current_view.textures.append(pid)
            line_region = view.line(point)
            # Find region of texture path declaration
            # Ex: [start]texture = "gfx/interface/icons/goods_icons/meat.dds"[end]
            start = view.find(
                r'[A-Za-z_][A-Za-z_0-9]*\s?=\s?"?/?(gfx)?', line_region.a
            ).a
            end = view.find('"|\n', start).a
            phantom_region = sublime.Region(start, end)
            view.add_phantom(key, phantom_region, html, sublime.LAYOUT_BELOW)

    def get_png_dimensions(self, path: str):
        height = 150
        width = 150
        file = open(path, "rb")
        try:
            head = file.read(31)
            size = len(head)
            if (
                size >= 24
                and head.startswith(b"\211PNG\r\n\032\n")
                and head[12:16] == b"IHDR"
            ):
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


class ImperatorShowTextureCommand(
    sublime_plugin.ApplicationCommand, ImperatorShowTextureBase
):
    def run(self, path: str, point: int): # type: ignore
        self.show_texture(path, point)


class ImperatorToggleAllTexturesCommand(sublime_plugin.ApplicationCommand):
    def __init__(self):
        self.shown = False

    def run(self):
        window = sublime.active_window()
        view = window.active_view()
        if not view:
            return None

        if get_syntax_name(view) != "Imperator Script":
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


class ImperatorShowAllTexturesCommand(
    sublime_plugin.WindowCommand, ImperatorShowTextureBase
):
    def run(self):
        view = self.window.active_view()
        if view is None:
            return

        texture_list = [
            x
            for x in view.lines(sublime.Region(0, view.size()))
            if ".dds" in view.substr(x)
        ]
        settings = sublime.load_settings("Imperator Syntax.sublime-settings")
        imperator_files_path = settings.get("ImperatorFilesPath")

        for line, i in zip(texture_list, range(settings.get("MaxToggleTextures"))): # type: ignore
            texture_raw_start = view.find("gfx", line.a)
            texture_raw_end = view.find(".dds", line.a)
            texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
            texture_raw_path = view.substr(texture_raw_region)
            full_texture_path = imperator_files_path + "/" + texture_raw_path # type: ignore
            full_texture_path = full_texture_path.replace("\\", "/")
            self.show_texture(full_texture_path, texture_raw_start.a)
