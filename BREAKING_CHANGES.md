# Breaking Changes

1. Introduced JominiTools that will have to be installed in the sublime Lib/python38 directory. Users will have to install this for the plugins to work.

2. Renamed the settings file from `Imperator.sublime-settings` to `Imperator.sublime-settings`. This will break all existing configs and they will have to be redone by users.

3. Changed the names of all the Tiger settings keys, removed the Imperator prefix so the interface could be generic. Users may need to update their settings.

4. Changed the `ImperatorFilesPath` setting to `GameFilesPath`. Users will need to update their settings or the plugin will no longer work.
