How to add a new GameObject:

1. Make a new GameObject class in imperator_objects.py

2. Load the game object into the plugin by updating the create_game_objects function in event_listener.py

3. Update the game_objects dict in utils.py

4. Update the write_data_to_syntax function in game_objects.py

5. Update the hover_objects list in event_listener.py

6. If the game object needs autocomplete:
	1. Add it to the auto_complete_fields dict in autocomplete.py. 
	2. Update the completion_flag_pairs and simple_completion_pattern_flag_pairs lists in game_data.py

7. If the game object is a scope update the simple_completion_scope_pattern_flag_pairs list in game_data.py
