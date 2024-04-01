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


1. Create Iterator classes to iterate over all views in a window and put it in utils. This is used in multiple places so would be nice to abstract. There may also be other common for loop operations that could use more convenient iterators.
