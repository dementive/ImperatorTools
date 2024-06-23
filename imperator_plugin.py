import os
import sys
import subprocess

import sublime

# clear modules cache if package is reloaded
prefix = __package__ + ".src"  # don't clear the base package
for module_name in [
    module_name for module_name in sys.modules if module_name.startswith(prefix)
]:
    del sys.modules[module_name]
del prefix


def jomini_repo_exists(destination_dir):
    return os.path.exists(os.path.join(destination_dir, "JominiTools"))


def clone_jomini_repo(destination_dir):
    # Clone the JominiTools dependency
    repository_url = "https://github.com/dementive/JominiTools"
    subprocess.run(["git", "clone", repository_url, destination_dir], check=True)
    subprocess.run(["git", "-C", destination_dir, "checkout", "main"], check=True)
    subprocess.run(["git", "-C", destination_dir, "pull"], check=True)


if not jomini_repo_exists(sublime.packages_path()):
    clone_jomini_repo(os.path.join(sublime.packages_path(), "JominiTools"))
else:
    from JominiTools.src.plugin_manager import PluginManager

    jomini_repository_url = "https://github.com/dementive/JominiTools"
    plugin_repository_url = "https://github.com/dementive/ImperatorTools"

    jomini_repository_path = os.path.join(sublime.packages_path(), "JominiTools")
    plugin_repository_path = os.path.join(sublime.packages_path(), "ImperatorTools")

    jomini_tools_manager = PluginManager(jomini_repository_path, jomini_repository_url)
    imperator_tools_manager = PluginManager(
        plugin_repository_path, plugin_repository_url
    )

    sublime.set_timeout_async(lambda: jomini_tools_manager.auto_update_plugin(), 0)
    sublime.set_timeout_async(lambda: imperator_tools_manager.auto_update_plugin(), 0)

from .src import *
