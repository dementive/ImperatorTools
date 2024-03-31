How to add a new GameObject:

1. Make a new GameObject class in imperator_objects.py

2. Load the game object into the plugin by updating the create_game_objects function in event_listener.py

3. In utils.py update the game_objects dict, update the object_names dict in the print_load_balanced_game_object_creation function, and update the get_game_object_dirs function.

4. Update the write_data_to_syntax function in game_objects.py

5. Update the hover_objects list in event_listener.py

6. If the game object needs autocomplete:
	1. Add it to the auto_complete_fields dict in autocomplete.py. 
	2. Update the completion_flag_pairs and simple_completion_pattern_flag_pairs lists in game_data.py

7. If the game object is a scope update the simple_completion_scope_pattern_flag_pairs list in game_data.py

8. Uncomment the print_load_balanced_game_object_creation function in event_listener.py and copy the output into the create_game_objects function. This automatically balances the load when loading all the game objects so the threading is as efficient as possible.

Refactorings:


1. Create a get_syntax_name() function that returns the syntax name of a view. It should handle the AttributeError exception too.

2. Create Iterator classes to iterate over all views in a window and put it in utils. This is used in multiple places so would be nice to abstract. There may also be other common for loop operations that could use more convenient iterators.

3. Create a convenient API for getting the name of game objects ("custom_loc" for example), it is currently easy to make hard to debug errors by spelling one of these wrong. So having a common API to fetch the strings from would be more robust.

4. The GameObjectCache is pretty fast as it is and doesn't seem to be causing problems but the API can be cumbersome to deal with at times. Maybe we could use an actual database for this? SQLite should be part of the sublime python environment so this may be a better approach. Would be a huge refactor though. A database may be overkill here though since relationships between objects really don't need to be represented at all, perhaps just using JSON would be best instead...
