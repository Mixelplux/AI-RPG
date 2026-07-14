# PT-001 Authored Text Correction

Status: Corrected — awaiting owner retest.

The Region Pack contains the accepted curly quotation marks (U+2018 and
U+2019), JSON loading preserves them, and the engine result preserves them.
No tracked player-facing authored mojibake was found. Save version 1, gameplay
state transitions, and persistent state are unchanged.

## Diagnosis

Immediately before the final player-facing write, the clue-presentation
response was the correct Python Unicode string:

```text
repr: "Captain Darvin Grey studies the trail, then nods. ‘That is enough to confirm the report. I will send a patrol west at once.’"
quotation code points: U+2018 and U+2019
```

The official process initially reported `sys.stdout.encoding='cp1252'`, while
the active console output encoding was UTF-8. The defect was therefore at the
repository-controlled CLI output boundary, not in authored content, JSON
loading, or the engine response.

## Correction

`play_game.main()` now configures a reconfigurable `sys.stdout` for UTF-8
before output. The exact presentation path is:

```text
play_game.main()
  -> GameEngine.process_command(player_input)
  -> interaction_result["presentation"]
  -> play_game.print_clue_presentation(presentation)
  -> print(response_text)
```

There is no encode/decode conversion or formatter between the engine response
and this final write. The CLI-path regression drives that full command path,
asserts the exact response with U+2018/U+2019, and rejects both observed
sequences: `Ã¢â‚¬Ëœ` and `Ã¢â‚¬â„¢`.

## Manual official-interpreter reproduction

Started with:

```powershell
.\.venv\Scripts\python.exe play_game.py
```

Entered:

```text
talk to captain
investigate
present The Captain's Deliberate Trail to captain
quit
```

Reported after the CLI output configuration:

```text
sys.stdout.encoding=utf-8
```

Displayed response:

```text
Captain Darvin Grey studies the trail, then nods. ‘That is enough to confirm the report. I will send a patrol west at once.’
```

Neither `Ã¢â‚¬Ëœ` nor `Ã¢â‚¬â„¢` appeared.
