# How to Install

Run the following script in the Sublime Text terminal ```(ctrl+` )``` which utilizes git clone for easy installation:
```
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/dementive/JominiTools', 'JominiTools'], 'working_dir': path}); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/dementive/ImperatorTools', 'ImperatorTools'], 'working_dir': path})
```
This script will automatically clone the JominiTools and ImperatorTools packages into your sublime text packages folder. It will only work with git installed on your system. If you do not have git you will have to [install it](https://git-scm.com/downloads) prior to running the script.

Alternatively you can download the zip file from github and put the ImperatorTools folder in the packages folder. However, this is **NOT** recommended as you will not get automatic updates and will have to update the plugin manually, which could result in missing out on essential bug fixes.
The packages folder can easily be found by going to ```preferences``` in the main menu and selecting ```Browse Packages```.
```
C:\Users\YOURUSERNAME\AppData\Roaming\Sublime Text 3\Packages\ImperatorTools
```

Regardless of how you install you will need to make sure [JominiTools](https://github.com/dementive/JominiTools) is also cloned into your packages folder as all plugin functionality relies on it.

After installation go to:
```
Preferences -> Package Settings -> Imperator Tools -> Settings
```

Add the path to your mod folder to the "PathsToModFiles" setting list. Also ensure that the path in the "GameFilesPath" setting is the correct path to the imperator game files on your computer. Without these 2 settings most plugin features will not work.

# Features

Complete syntax highlighting for all effects, triggers, scopes, and many keywords. All game objects from the base game and your mods will automatically be added into the syntax highlighting as well. The syntax can be activated by going to:
```
main menu -> view -> syntax -> Open All with current extention as... -> Imperator Tools
```
Select ```Imperator Rome Scripting``` as the default syntax for .txt. 
For .yml files use ``` Imperator Localization ```.
For .log files use ```Imperator Log Syntax```.

In addition to syntax highlighting all effects, triggers, and scopes have been added to autocompletion.  
At any time you can press ```ctrl+space``` and start typing and autocompletion will open, autocomplete.  
Context aware autocompletions will also show up to fill in valid game objects.  
There are also snippets for some balancing effects and whole templates, like a country event templates for example.

Status bar text will indicate when your cursor is inside of an effect, trigger, modifier, or value block and appropriate autocompletion will be shown depending on the kind of block the cursor is in.

Goto Definition popups also have been added for all game objects and for saved scopes or variables.

Named colors have special goto definition popups that show the color in a small square in the popup when hovering over any named color. This way you can hover through files in the named_colors folder and see the exact color of each one to pick the perfect color or see the color of a flag directly in it's definition.

Hovering over texture paths will show a popup that lets you either open the folder the texture is in or open the texture directly in sublime by converting the dds to a png and showing it in a new tab.

Several commands have also been added to the command palette. Open it with `ctrl+shift+p` and then type in `Imperator:` to view all the commands
- Imperator Modding Index - Open the modding index your browser
- Imperator Wiki - Open the imperator wiki in your browser
- Localization Syntax Guide - Open the community made localization syntax guide in your browser
- Create Mission Tree - Creates mission tree localization, event, and mission files for you from quick panel input. All you need to know is the mission name, event namespace name, and number missions and your mission tree files will be automatically created.
- Reload Plugin - Reload all game objects and plugin features. If you add a new game object you can use this command to regenerate the syntax definition without restarting the app.
- Clear Image Cache - If you have images set to open in sublime they get cached so they open faster, this command clears the cache
- Toggle All Textures - This will show/hide all textures as inline right below the texture path. For example if you have a event pictures file open and use this command it will show all of the event pictures directly in the editor. The ShowInlineTexturesOnLoad setting can be set to `true` to automatically show all textures whenever a new file is opened.

# GUI and Shader Modding

The .gui, .shader, and .fxh syntaxes are part of the Victoria 3 sublime tools so to get them working you will need to download it and enable the `VictoriaGui` and `PdxShader` syntaxes found here:  
https://github.com/dementive/Victoria3Tools

# Imperator-tiger integration

[imperator-tiger](https://github.com/amtep/ck3-tiger) has been fully integrated into the plugin and provides validation for all of your mod files. The imperator-tiger binary comes with the plugin and it's usage within sublime can be configured with the plugin settings. The following settings can be adjusted to change the behavior of imperator-tiger:
- TigerModPath - The path to the mod you are currently working on that you want to be validated. If you do not put a valid path in this setting the plugin will not use imperator-tiger at all and validation will be ignored.
- TigerUseDefaultConfig - By default the plugin will call tiger with the default imperator-tiger.conf file which is located in your mod folder. If you set this setting to 'false' the plugin will instead use a common .conf file between all mods that can be edited with the `Imperator: Edit imperator-tiger.conf` command. For more information about the imperator-tiger.conf read [guide](https://github.com/amtep/ck3-tiger/blob/main/filter.md)
- TigerShowErrorsInline - When you open a new file that tiger has detected errors in a squiggly line will be drawn under all the errors in the file, you can hover over these to get more information about the error. If you want to disable this feature just set this setting to false.

When you have a valid path defined in the TigerModPath setting the plugin will automatically call imperator-tiger when you open sublime if changes have been detected in any of the mods you are currently working on. The following commands can be used to directly interact with imperator-tiger:
- `Imperator: Reload plugin objects and regenerate syntax` - The imperator-tiger output will be regenerated automatically by the plugin at the same time the syntax definition is. This means changes will only occur when sublime is first opened or when this reload objects command is run. If you have made some changes and you want imperator-tiger to validate them you can run this command to check if you made any mistakes.
- `Imperator: Show Tiger Output` - You can view the results of the tiger validation directly in sublime in either a panel at the bottom of the screen or in a new tab. This will display the validator output in the same style as tiger which replicated the style of Rust compiler errors. For each error an annotation will be draw that you can click on to open the source of the error in a new tab.

# Dependencies

Only 1 dependency is absolutely necessary for the plugin to work:

The [JominiTools]([JominiTools](https://github.com/dementive/JominiTools)) package. All of the core plugin functionality comes from JominiTools and the plugin will not work at all without it.

There are 2 additional dependencies that will add more functionality but are not necessary for the core features to work

- [Git]((https://git-scm.com/downloads)) - Git is used to automatically update the plugin whenever any changes are made. Without git you'll have to pull all changes manually which is not recommended because you may miss out on essential bug fixes.

- ImageMagick(https://imagemagick.org/script/download.php) - ImageMagick has to be installed on your system PATH, it is used to convert dds files to png so they can be displayed in sublime. This is only used when showing textures in sublime so if you don't use this feature it won't be necessary to install image magick.


# Images


![Script Screenshot](/assets/image1.png)

![Script Screenshot 2](/assets/image2.png)

![Script Screenshot 3](/assets/image3.png)

![Imperator Tiger Output](/assets/image4.png)