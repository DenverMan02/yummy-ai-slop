# 🧟 Plants vs. Zombies 2: Into The Den (Modding Tools & Datasets) 🌿

Welcome to the development & tooling repository for the **Into The Den (ITD)** PvZ2 mod!

---

## 🛠️ Tooling & Utilities

### 🌿 Level Generator Studio (`tools/level_gen_studio.py`)
A visual, web-based procedurally generated level studio built on mathematical models extracted from **3,579+ official and mod levels**.

#### Features:
- **Interactive Visual Studio UI:** Dark-mode workbench with live wave pacing timeline, zombie composition tags, flag wave indicators, and Plant Food drops.
- **World Presets:** Native support for Ancient Egypt (Day/Night), Heian Dynasty (Day/Night), Pirate Seas (with plank configurations), Dark Ages, and Modern Day.
- **Mod Roster Integration:** Direct support for custom mod zombies (Armor 4 tiers, Heian imports, female zombies, specials) and plants (`agave`, `whitemelon`, `seashroom`, `pineneedler`).
- **Challenge Injectors:** Save Our Seeds (`ProtectThePlantChallengeProperties`), tombstone spawns, and night stages.
- **1-Click Disk Sync:** Save generated levels directly to `Levels/ITD/<filename>.json`.

#### How to Launch the Web Studio:
```bash
python3 tools/level_gen_studio.py
```
*Opens automatically at `http://127.0.0.1:8765` in your browser.*

#### CLI Mode (for batch generation or automated scripts):
```bash
# Generate a 14-wave Heian Dynasty level with difficulty 3
python3 tools/level_gen_studio.py --cli --world heian --waves 14 --diff 3 --output Levels/ITD/HEIAN2.json
```

---

## 🔄 Git Sync Helper (`github.py`)
Run `python3 github.py` for the interactive Git menu (push, pull, force-pull with LFS, and automatic asset compilation hooks).
