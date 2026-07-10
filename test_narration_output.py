from engine.game_engine import GameEngine
from engine.narration_output import (
    NARRATION_OUTPUT_ATMOSPHERE_EXAMPLE,
    NARRATION_OUTPUT_AUTHORITY,
    NARRATION_OUTPUT_DRIFT_LIMIT,
    NARRATION_OUTPUT_RULE,
    NARRATION_OUTPUT_SCHEMA,
    NARRATION_OUTPUT_VERSION,
    build_narration_output_packet,
)
from play_game import parse_narration_output_command


REGION_PATH = "data/regions/bryn_shander.json"


def main():
    engine = GameEngine(REGION_PATH)

    contract = engine.get_narration_output_contract()
    assert contract["schema"] == NARRATION_OUTPUT_SCHEMA
    assert contract["version"] == NARRATION_OUTPUT_VERSION
    assert contract["type"] == "read_only_narration_output_contract"
    assert contract["rule"] == NARRATION_OUTPUT_RULE
    assert contract["authority"] == NARRATION_OUTPUT_AUTHORITY
    assert contract["drift_limit"] == NARRATION_OUTPUT_DRIFT_LIMIT
    assert contract["atmosphere_example"] == (
        NARRATION_OUTPUT_ATMOSPHERE_EXAMPLE
    )
    assert "blizzard" in contract["atmosphere_example"]
    assert "gloves" in contract["atmosphere_example"]
    assert contract["required_fields"] == [
        "schema",
        "version",
        "narration_text",
    ]
    assert "world_state" in contract["forbidden_structured_fields"]
    assert "history" in contract["forbidden_structured_fields"]
    assert "advance_time" in contract["forbidden_structured_fields"]

    valid_output = {
        "schema": NARRATION_OUTPUT_SCHEMA,
        "version": NARRATION_OUTPUT_VERSION,
        "narration_text": "The street remains quiet."
    }
    accepted_output = engine.validate_narration_output(valid_output)
    assert accepted_output == build_narration_output_packet(
        "The street remains quiet."
    )
    assert accepted_output["contract"] == contract

    world_state_before_validation = engine.get_world_state()
    history_before_validation = engine.get_history()
    scene_before_validation = engine.get_scene_snapshot()
    repeated_output = engine.validate_narration_output(valid_output)
    assert repeated_output == accepted_output
    assert engine.get_world_state() == world_state_before_validation
    assert engine.get_history() == history_before_validation
    assert engine.get_scene_snapshot() == scene_before_validation

    mutable_output = engine.validate_narration_output(valid_output)
    mutable_output["narration_text"] = "Mutated output."
    mutable_output["contract"]["authority"] = "Mutated authority."
    assert engine.validate_narration_output(valid_output) == accepted_output
    assert engine.get_world_state() == world_state_before_validation
    assert engine.get_history() == history_before_validation

    invalid_outputs = [
        {
            **valid_output,
            "world_state": {"weather": "clear"}
        },
        {
            **valid_output,
            "history": [{"summary": "Created history."}]
        },
        {
            **valid_output,
            "advance_time": {"hours": 1}
        },
        {
            **valid_output,
            "quests": ["Find the lost satchel."]
        },
        {
            **valid_output,
            "rumors": ["The gate will open soon."]
        },
        {
            **valid_output,
            "pressures": [{"name": "storm"}]
        },
        {
            **valid_output,
            "actor_knowledge": {"guard": "player arrived"}
        },
        {
            **valid_output,
            "npc_schedules": {"guard": "patrol"}
        },
        {
            **valid_output,
            "evidence": ["footprints"]
        },
        {
            **valid_output,
            "consequences": ["alarm raised"]
        },
        {
            **valid_output,
            "new_entities": ["merchant"]
        },
        {
            **valid_output,
            "locations": ["hidden cellar"]
        },
        {
            **valid_output,
            "exits": ["east"]
        },
        {
            **valid_output,
            "inventory": ["gloves"]
        },
        {
            **valid_output,
            "player_conditions": ["cold"]
        },
        {
            **valid_output,
            "npc_relationships": {"guard": "friendly"}
        },
        {
            **valid_output,
            "metadata": {"world_state": {"weather": "clear"}}
        },
    ]

    for invalid_output in invalid_outputs:
        try:
            engine.validate_narration_output(invalid_output)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"Structured mutation should fail: {invalid_output}"
            )

    try:
        engine.validate_narration_output({
            **valid_output,
            "narration_text": ["not", "a", "string"]
        })
    except ValueError:
        pass
    else:
        raise AssertionError("Non-string narration text should fail.")

    try:
        engine.validate_narration_output({
            **valid_output,
            "schema": "wrong.schema"
        })
    except ValueError:
        pass
    else:
        raise AssertionError("Unsupported schema should fail.")

    try:
        engine.validate_narration_output({
            **valid_output,
            "version": 999
        })
    except ValueError:
        pass
    else:
        raise AssertionError("Unsupported version should fail.")

    assert engine.get_world_state() == world_state_before_validation
    assert engine.get_history() == history_before_validation
    assert engine.get_scene_snapshot() == scene_before_validation

    assert parse_narration_output_command("narration output") == {
        "sample": "valid"
    }
    assert parse_narration_output_command("narration output invalid") == {
        "sample": "invalid"
    }
    assert "error" in parse_narration_output_command(
        "narration output something else"
    )

    assert engine.get_narration_context("look around")["schema"] == (
        "ai_rpg.narration_context_packet"
    )

    print("Narration output test passed.")


if __name__ == "__main__":
    main()
