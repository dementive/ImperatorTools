# ImperatorTools
Syntax, autocompletion, and several useful commands for Imperator Rome scripting.


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

# Features

Complete sytnax highlighting for all effects, triggers, scopes, and many keywords. 3 Unique sytaxes have been made, 1 for .txt files, 1 for .gui files, and another one for .log files. The syntaxes can be activated by going to:
```
main menu -> view -> syntax -> Open All with current extention as... -> Imperator Tools
```
Select ```Imperator Rome Scripting``` as the default syntax for .txt and .gui files. For .log files use the ```Imperator Log Syntax```.

In addition to syntax highlighting all effects, triggers, and scopes have been added to autocompletion. At any time you can press ```ctrl+space``` and start typing and autocompletion will open.
There are also autocompletions for some balancing effects and whole templates, like a country event templates for example.
Autocompletion features are only for .txt files.

Several commands have also been added to the context menu that is opened by simply right clicking the text area. A menu titled ```Imperator``` has been added with the following commands in it:
- Imperator Modding Index - Open the modding index your browser
- Imperator Wiki - Open the imperator wiki in your browser
- Localization Syntax Guide - Open the community made localization syntax guide in your browser
- Imperator Effect - Opens a quick panel that is filled with each category of effect. Then quickly open a popup that shows all effects in a category. For example clicking State Effects in the quick panel will show all of the state effects that are in the game from the documentation.
- Create Mission Tree - Creates mission tree localization, event, and mission files for you from quick panel input. All you need to know is the mission name, event namespace name, and number missions and your mission tree files will be automatically created.

# Other Packages

If you are working with shader files that have the .shader or .fxh extention I highly recommend downloading this plugin:
https://packagecontrol.io/packages/HLSL%20Syntax
It provides syntax highlighting and some other very useful features and commands for working with shaders.