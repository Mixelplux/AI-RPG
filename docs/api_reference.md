# API Reference

Version: 0.2

## Public Entry Point

### engine.game_engine.GameEngine

Responsibilities:

-   Load Region Packs
-   Maintain Scene Snapshot
-   Build Player Perception
-   Build Narration
-   Process Player Commands
-   Apply World Updates

Gameplay front ends should interact with GameEngine rather than
individual engine modules.
