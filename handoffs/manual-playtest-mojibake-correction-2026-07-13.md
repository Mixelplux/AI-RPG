# PT-001 Authored Text Correction

Status: Corrected — awaiting manual retest.

The Region Pack contains the accepted curly quotation marks (U+2018 and
U+2019), and the loaded engine result preserves them. No mojibake was found in
tracked player-facing authored content. The narrow correction makes Region Pack
loading explicitly UTF-8 and strengthens the exact clue-presentation response
assertion, including rejection of the observed mojibake fragment. Gameplay,
save version 1, and persistent state are unchanged.
