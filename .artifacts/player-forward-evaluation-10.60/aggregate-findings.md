# Sprint 10.60 Aggregate Player-Forward Findings

| Rank | Finding | Likely existing layer | Evidence |
|---|---|---|---|
| blocking_player_flow | Scenes omit exits, destinations, and an actionable West Gate route. | player-facing action affordance; movement/transition presentation | Scenes say only `What do you do?`; direct west reaches the inn, while successful travel is south/east/north. |
| major_player_friction | Scenes do not surface next actions around report, clue, Elin, or investigation. | player-facing action affordance; discovery presentation/use; conversation presentation | Progress needs guessed `investigate`, exact presentation syntax, and `talk to elin`. |
| major_player_friction | Elapsed North Gate changes are causally under-presented. | elapsed-time presentation; world-memory projection | Grey disappears without explanation; second-hour change is behind repeat investigation; time is raw dictionary data. |
| minor_player_friction | Memory evidence is hidden behind repeated investigation. | world-memory projection; discovery presentation/use | West Gate orders and patrol marker work once explicitly investigated. |
| no_material_issue | Resolved consequences are deterministic and connected. | deterministic simulation/context | Grey's response, North Gate observation, Elin at West Gate, patrol order, and road marker form a coherent chain once found. |

Recommendation: select one narrowly bounded **player-facing scene affordance and transition presentation** package to project existing exits, contextual actions, and legible elapsed-time change. Do not add commands, generic UI, parser changes, or simulation mechanics.
