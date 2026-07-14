\# Manual Playtest Findings — 2026-07-13



Repository HEAD: 0c97f8c7b1363cfbb247682b99fc1318fb47b048

Save version: 1



\## PT-001 — Authored quotation marks display as corrupted characters



\*\*Severity:\*\* Player-visible defect  

\*\*Status:\*\* Open  

\*\*Reproducible:\*\* Yes



\### Action



present The Captain's Deliberate Trail to captain



\### Expected



Captain Darvin Grey studies the trail, then nods. ‘That is enough to confirm the report. I will send a patrol west at once.’



\### Observed



Captain Darvin Grey studies the trail, then nods. â€˜That is enough to confirm the report. I will send a patrol west at once.â€™



\### Troubleshooting attempted



\- Changed the terminal code page to UTF-8.

\- Enabled Python UTF-8 mode.

\- Set PowerShell input and output encoding to UTF-8.

\- Started Python with `-X utf8`.

\- The problem remained.



\### Assessment



The terminal configuration did not fix the output. The authored text is probably already corrupted in the Region Pack or is decoded incorrectly before display.



\### Player impact



The response remains understandable, but the corrupted punctuation reduces presentation quality and immersion.



\## Overall playtest result



The complete implemented gameplay loop worked as intended. No other defects were found.

