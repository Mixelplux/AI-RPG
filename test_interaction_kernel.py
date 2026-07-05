from engine.interaction_kernel import process_player_input


mock_scene = {
    "scene_id": "north_gate",
    "location_name": "North Gate"
}


commands = [
    "look around",
    "talk to the guard",
    "go through the gate",
    "open the satchel",
    "",
    "dance in the snow"
]


for command in commands:
    result = process_player_input(command, mock_scene)
    print(command)
    print(result)
    print()