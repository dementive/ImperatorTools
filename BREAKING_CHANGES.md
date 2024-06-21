# Breaking Changes

1. Introduced JominiTools that will have to be installed in the sublime Lib/python38 directory. Users will have to install this for the plugins to work.

2. Renamed the settings file from `Imperator.sublime-settings` to `Imperator.sublime-settings`. This will break all existing configs and they will have to be redone by users.

3. Changed the names of all the Tiger settings keys, removed the Imperator prefix so the interface could be generic. Users may need to update their settings.

4. Changed the `ImperatorFilesPath` setting to `GameFilesPath`. Users will need to update their settings or the plugin will no longer work.

5. Added a dependency to ImageMagick and removed the old ConvertDDS program. Users will need to install ImageMagick on their system's PATH if they want to use the features that allow textures to be opened in sublime.


# Regressions

1. I broke the Show Inline part of the show textures command, it works but the toggle doesn't work properly. Also the delay on textures seems to not be working anymore...