# How to Install

Run the following script in the Sublime Text terminal ```(ctrl+` )``` which utilizes git clone for easy installation:
```
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/dementive/ImperatorTools', 'ImperatorTools'], 'working_dir': path})
```
This will only work with git installed on your system.

Alternatively you can download the zip file from github and put the ImperatorTools folder in the packages folder.
The packages folder can easily be found by going to ```preferences``` in the main menu and selecting ```Browse Packages```.
```
C:\Users\YOURUSERNAME\AppData\Roaming\Sublime Text 3\Packages\ImperatorTools
```

After installation go to:
```
Preferences -> Package Settings -> Imperator Tools -> Settings
```

Add the path to your mod folder to the "PathsToModFiles" setting list. Also ensure that the path in the "ImperatorFilesPath" setting is the correct path to the imperator game files on your computer. Without these 2 settings most plugin features will not work.

# Features

Complete sytnax highlighting for all effects, triggers, scopes, and many keywords. All game objects from the base game and your mods will automatically be added into the syntax highlighting as well. The syntax can be activated by going to:
```
main menu -> view -> syntax -> Open All with current extention as... -> Imperator Tools
```
Select ```Imperator Rome Scripting``` as the default syntax for .txt. 
For .yml files use ``` Imperator Localization ```.
For .log files use ```Imperator Log Syntax```.

In addition to syntax highlighting all effects, triggers, and scopes have been added to autocompletion. At any time you can press ```ctrl+space``` and start typing and autocompletion will open. Context aware autocompletions will also show up to fill in valid game objects
There are also autocompletions for some balancing effects and whole templates, like a country event templates for example.

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


![Script Screenshot](/assets/image1.png)

![Script Screenshot 2](/assets/image2.png)

![Script Screenshot 3](/assets/image3.png)