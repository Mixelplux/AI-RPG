from engine.interaction_kernel import process_player_input
from engine.world_update import apply_interaction


scene_snapshot = {
    "scene_id": "north_gate",
    "location_name": "North Gate",
    "weather": {
        "condition": "blizzard",
        "severity": 0.65
    }
}


commands = [
    "look around",
    "talk to the guard",
    "go north"
]


for command in commands:

    interaction = process_player_input(command, scene_snapshot)

    updated_scene = apply_interaction(
        scene_snapshot,
        interaction
    )

    print("=" * 50)
    print(command)
    print(updated_scene)