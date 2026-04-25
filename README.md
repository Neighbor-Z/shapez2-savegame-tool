# Shapez 2 Savegame Tool

A Python+Flask web tool for exploring or upgrading `shapez 2` `.spz2` save files.

> [!IMPORTANT]
>
> This tool is for **research** purposes on Shapez 2 game saves **ONLY**. Any illegal modification or cracking of the game itself destroys the game experience and should be avoided.
>
> Use this tool **at your own risk**.

## Overview
Shapez 2 is a highly acclaimed factory automation game. Its saves (`.spz2`) are standard ZIP archives containing a mix of readable JSON files and custom binary serialized files. This tool provides a safe, web-based interface for viewing game progress information stored in readable JSON files (such as `savegame.json`, `local-player.json`, `research.json`), or migrating data from older version saves to newer versions.

## Features
- **Data Viewing:** Upload `.spz2` files and automatically extract their contents.
- **Legacy Save Migration:** Safely migrate progress data from older game versions (0.0.7~0.1.1) to the new version (1.0+). For specific steps, please see the [Save Upgrade and Migration](#save-upgrade-and-migration) section.

## Installation and Setup

**Prerequisites:**
- Python 3.x (tested on version 3.12)
- pip
- A game save exported from Shapez 2 (theoretically supports all game save versions between 0.0.7~1.0.2)

**Installation Steps:**
```bash
# Clone and enter the project directory
cd shapez2-save-editor

# Install the required Flask dependencies
pip install -r requirements.txt
```

## Running the Program

1. Start the Flask server:
```bash
python3 app.py
```
2. Open your browser and visit: [http://127.0.0.1:6004](http://127.0.0.1:6004).
3. Follow the prompts to open your Shapez 2 `.spz2` save file.
4. View the data within it in the browser tabs.

## Save Upgrade and Migration

The game version 1.0 is declared officially to be completely incompatible with game saves generated in previous versions. Although players can switch to the legacy branch to continue accessing old game saves, in a vote of about 2500 people, approximately 15% of players still expressed that they could not easily accept this situation, which is a pity for players who hope to directly inherit older game saves.

The good news is, after my preliminary exploration, upgrading and migrating legacy saves is not entirely hopeless. The new save format indeed changed a lot of content, and the entire map section has been completely reworked, which means that all buildings on the map, including trains and train tracks, cannot be directly migrated. Fortunately, most blueprints are compatible, **so by following the steps below, you still have a way to solve this!** In addition, in the save data, ResearchProgress, LinearUpgrades, GoalLevels, and HUDData also have significant changes and require safe migration using this tool.

> [!NOTE]
>
> This solution is not and will not be perfect. Always remember to backup your game saves.

#### Compatibility Note

Theoretically this tool supports upgrading and migrating all versions of game saves between 0.0.7~0.1.1. RegularGameMode has been tested; Not sure about other scenarios except default.

#### Steps

1. Launch the old version of the game and load the legacy save, select the buildings in the old save, and save them as a blueprint. (If you have many buildings, this step will make the computer very laggy, so please be patient and do not repeat operations.) Then export the old save you want to upgrade and migrate from the old version.
2. Open the old save with this project tool, select `savegame.json`, find and open the `Parameters` node, and record the `GameModeId` (game mode) and `Seed` (map seed).
3. Continue to open `ScenarioParameters > MapGenerationParameters`, take a note and write down all map generation parameters therein.
4. Upgrade to the new version of the game and launch it, create a new save, choose the **same** game mode as the old save, fill in the map seed recorded earlier, and set the map generation parameters on the left to the previously recorded parameters, and **turn off SpiralGeneration**.
5. Save and export the newly created save, rename it to `template-v1.spz2`, and place it in the folder of this project.
6. Return to the web page of this project tool and click the "Migrate" button at the bottom of the page. If everything good, the page should automatically "download" a processed save.
7. Import this processed save into the new version of the game, and you should be able to see that most of the previous progress data has been migrated!
8. Place your previously saved blueprints (again, if you have many buildings, this step will make the computer very laggy, so please be patient and do not repeat operations) at where they were on the map.
9. Enjoy playing in the new version!

## License

[?](https://github.com/Neighbor-Z/shapez2-savegame-tool/blob/main/LICENSE)

---

**About AI**: AI assistance involved; each code segment has undergone manual review and testing.

**Need help?** If you encounter any issues, please open an [Issue](https://github.com/Neighbor-Z/shapez2-savegame-tool/issues).

**Support project**: [☕️ Buy Me a Coffee](https://buymeacoffee.com/neighbor_z)
