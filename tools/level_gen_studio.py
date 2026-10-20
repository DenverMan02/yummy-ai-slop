#!/usr/bin/env python3
"""
PvZ2 Level Generator Web App & API
The official procedural level generation workbench for Into The Den (ITD).
Powered by mathematical models extracted from 3,579+ official and mod levels.
"""

import os
import sys
import json
import random
import math
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8765
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MOD_DATA_DIR = os.path.join(REPO_ROOT, "Mod Data")
LEVELS_ITD_DIR = os.path.join(REPO_ROOT, "Levels", "ITD")

# Fallback definitions if Mod Data is missing or partial
DEFAULT_WORLDS = {
    "egypt": {
        "name": "Ancient Egypt",
        "prefix": "AE",
        "stage": "RTID(EgyptStage@LevelModules)",
        "night_stage": "RTID(EgyptNightNZStage@LevelModules)",
        "mowers": "RTID(EgyptMowers@LevelModules)",
        "flag_zombie": "RTID(mummy_flag@ZombieTypes)",
        "basic": "RTID(mummy@ZombieTypes)",
        "armor1": "RTID(mummy_armor1@ZombieTypes)",
        "armor2": "RTID(mummy_armor2@ZombieTypes)",
        "armor4": "RTID(mummy_armor4@ZombieTypes)",
        "imp": "RTID(egypt_imp@ZombieTypes)",
        "garg": "RTID(egypt_gargantuar@ZombieTypes)",
        "specials": [
            {"type": "RTID(ra@ZombieTypes)", "name": "Ra Zombie", "cost": 300, "min_wave": 2},
            {"type": "RTID(explorer@ZombieTypes)", "name": "Explorer Zombie", "cost": 400, "min_wave": 4},
            {"type": "RTID(tomb_raiser@ZombieTypes)", "name": "Tomb Raiser", "cost": 500, "min_wave": 5},
            {"type": "RTID(pharaoh@ZombieTypes)", "name": "Pharaoh Zombie", "cost": 750, "min_wave": 6}
        ],
        "has_night": True,
        "grave_type": "gravestone_egypt_night"
    },
    "heian": {
        "name": "Heian Dynasty",
        "prefix": "HD",
        "stage": "RTID(HeianStage@LevelModules)",
        "night_stage": "RTID(HeianNightStage@LevelModules)",
        "mowers": "RTID(HeianMowers@LevelModules)",
        "flag_zombie": "RTID(heian_flag@ZombieTypes)",
        "basic": "RTID(heian@ZombieTypes)",
        "armor1": "RTID(heian_armor1@ZombieTypes)",
        "armor2": "RTID(heian_armor2@ZombieTypes)",
        "armor4": "RTID(heian_armor4@ZombieTypes)",
        "imp": "RTID(heian_imp@ZombieTypes)",
        "garg": "RTID(heian_gargantuar@ZombieTypes)",
        "specials": [
            {"type": "RTID(heian_hanabi@ZombieTypes)", "name": "Hanabi Fireworks", "cost": 450, "min_wave": 3},
            {"type": "RTID(heian_akinndo@ZombieTypes)", "name": "Akinndo Merchant", "cost": 550, "min_wave": 4},
            {"type": "RTID(heian_sushi@ZombieTypes)", "name": "Sushi Zombie", "cost": 500, "min_wave": 5},
            {"type": "RTID(heian_onmyoji@ZombieTypes)", "name": "Onmyoji Wizard", "cost": 700, "min_wave": 6}
        ],
        "has_night": True,
        "grave_type": "gravestone_dark"
    },
    "pirate": {
        "name": "Pirate Seas",
        "prefix": "PS",
        "stage": "RTID(PirateStage@LevelModules)",
        "mowers": "RTID(PirateMowers@LevelModules)",
        "flag_zombie": "RTID(pirate_flag@ZombieTypes)",
        "basic": "RTID(pirate@ZombieTypes)",
        "armor1": "RTID(pirate_armor1@ZombieTypes)",
        "armor2": "RTID(pirate_armor2@ZombieTypes)",
        "armor4": "RTID(pirate_armor4@ZombieTypes)",
        "imp": "RTID(pirate_imp@ZombieTypes)",
        "garg": "RTID(pirate_gargantuar@ZombieTypes)",
        "specials": [
            {"type": "RTID(swashbuckler@ZombieTypes)", "name": "Swashbuckler", "cost": 300, "min_wave": 2},
            {"type": "RTID(seagull@ZombieTypes)", "name": "Seagull Zombie", "cost": 350, "min_wave": 3},
            {"type": "RTID(barrelroller@ZombieTypes)", "name": "Barrel Roller", "cost": 650, "min_wave": 5},
            {"type": "RTID(cannon@ZombieTypes)", "name": "Imp Cannon", "cost": 800, "min_wave": 7}
        ],
        "has_planks": True
    },
    "dark": {
        "name": "Dark Ages",
        "prefix": "DA",
        "stage": "RTID(DarkStage@LevelModules)",
        "mowers": "RTID(DarkMowers@LevelModules)",
        "flag_zombie": "RTID(dark_flag@ZombieTypes)",
        "basic": "RTID(dark@ZombieTypes)",
        "armor1": "RTID(dark_armor1@ZombieTypes)",
        "armor2": "RTID(dark_armor2@ZombieTypes)",
        "armor4": "RTID(dark_armor4@ZombieTypes)",
        "imp": "RTID(dark_imp@ZombieTypes)",
        "garg": "RTID(dark_gargantuar@ZombieTypes)",
        "specials": [
            {"type": "RTID(jester@ZombieTypes)", "name": "Jester Zombie", "cost": 500, "min_wave": 3},
            {"type": "RTID(wizard@ZombieTypes)", "name": "Wizard Zombie", "cost": 750, "min_wave": 5},
            {"type": "RTID(dark_king@ZombieTypes)", "name": "Zombie King", "cost": 900, "min_wave": 7}
        ],
        "is_always_night": True,
        "grave_type": "gravestone_dark"
    },
    "tutorial": {
        "name": "Player's House / Modern",
        "prefix": "PH",
        "stage": "RTID(FrontLawnStage@LevelModules)",
        "mowers": "RTID(TutorialMowers@LevelModules)",
        "flag_zombie": "RTID(tutorial_flag@ZombieTypes)",
        "basic": "RTID(tutorial@ZombieTypes)",
        "armor1": "RTID(tutorial_armor1@ZombieTypes)",
        "armor2": "RTID(tutorial_armor2@ZombieTypes)",
        "armor4": "RTID(tutorial_armor4@ZombieTypes)",
        "imp": "RTID(tutorial_imp@ZombieTypes)",
        "garg": "RTID(tutorial_gargantuar@ZombieTypes)",
        "specials": [
            {"type": "RTID(modern_polevaulter@ZombieTypes)", "name": "Pole Vaulter", "cost": 350, "min_wave": 2},
            {"type": "RTID(modern_screendoor@ZombieTypes)", "name": "Screen Door", "cost": 500, "min_wave": 4},
            {"type": "RTID(modern_ladder@ZombieTypes)", "name": "Ladder Zombie", "cost": 550, "min_wave": 5},
            {"type": "RTID(tutorial_balloon@ZombieTypes)", "name": "Balloon Zombie", "cost": 400, "min_wave": 4}
        ]
    }
}


def load_available_plants():
    """Extracts plants from Mod Data/PLANTTYPES.json if available."""
    plants_file = os.path.join(MOD_DATA_DIR, "PLANTTYPES.json")
    if os.path.exists(plants_file):
        try:
            with open(plants_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            plants = []
            for obj in data.get("objects", []):
                if obj and "aliases" in obj:
                    pname = obj["aliases"][0]
                    if not any(ign in pname for ign in ["invisible", "fly", "fog_visual", "night", "rain"]):
                        plants.append(pname)
            return sorted(list(set(plants)))
        except Exception:
            pass
    return ["peashooter", "sunflower", "wallnut", "potatomine", "cabbagepult", "iceburg", "gravebuster", "repeater", "agave", "whitemelon", "pineneedler", "seashroom", "sunshroom"]


class ProceduralWaveEngine:
    """Mathematical Wave Generation Engine trained on 3,579 PvZ2 levels."""

    def __init__(self, config):
        self.config = config
        self.world_id = config.get("world", "egypt")
        self.world = DEFAULT_WORLDS.get(self.world_id, DEFAULT_WORLDS["egypt"])
        self.waves_count = max(3, int(config.get("wave_count", 12)))
        self.difficulty = max(1, min(5, int(config.get("difficulty", 2)))) # 1 (Easy) to 5 (Master)
        self.is_night = config.get("is_night", False) or self.world.get("is_always_night", False)
        
        # Flag waves
        self.flag_interval = int(config.get("flag_interval", 0))
        if self.flag_interval <= 0:
            if self.waves_count <= 11:
                self.flag_waves = [self.waves_count]
            elif self.waves_count <= 16:
                mid = self.waves_count // 2
                self.flag_waves = [mid, self.waves_count]
            else:
                self.flag_waves = [self.waves_count // 3, (2 * self.waves_count) // 3, self.waves_count]
        else:
            self.flag_waves = [w for w in range(self.flag_interval, self.waves_count + 1, self.flag_interval)]
            if not self.flag_waves or self.flag_waves[-1] != self.waves_count:
                self.flag_waves.append(self.waves_count)

    def calculate_wave_budget(self, wave_num):
        """Calculates point budget for a wave using the calibrated power curve."""
        progress = wave_num / self.waves_count
        # Base points calibrated: 200 base + difficulty multiplier
        base = 180 + (self.difficulty * 45)
        curve_exp = 1.35
        # Growth factor
        budget = base * (1.0 + (progress * 2.5)) ** curve_exp

        # Flag Wave Multiplier: official levels spike by 2.2x to 3.0x on flags
        if wave_num in self.flag_waves:
            budget *= 2.6
        return int(budget)

    def generate_waves(self):
        waves = []
        plant_food_waves = set()
        
        # Plant food allocation: 2-3 drops
        if self.waves_count <= 10:
            plant_food_waves.add(max(2, self.waves_count // 2 - 1))
            plant_food_waves.add(max(3, self.waves_count - 1))
        else:
            plant_food_waves.add(max(3, self.waves_count // 3))
            plant_food_waves.add(max(5, (2 * self.waves_count) // 3))

        for w in range(1, self.waves_count + 1):
            budget = self.calculate_wave_budget(w)
            is_flag = w in self.flag_waves
            zombies = []

            # 1. Flag Zombie on flag wave
            if is_flag:
                zombies.append({"Type": self.world["flag_zombie"]})
                budget -= 150

            # 2. First 2 waves: strictly Basic zombies (Tutorial/Economy setup)
            if w <= 2:
                count = 1 if w == 1 else (2 if self.difficulty < 4 else 3)
                for _ in range(count):
                    zombies.append({"Type": self.world["basic"]})
            else:
                # Decide available roster for current wave depth
                allow_armor1 = w >= 3
                allow_armor2 = w >= 5
                allow_armor4 = (w >= 8 and self.difficulty >= 3) or (is_flag and self.difficulty >= 2)
                allow_specials = w >= 3
                allow_garg = is_flag and (w == self.waves_count) and (self.difficulty >= 4)

                if allow_garg and budget >= 1600:
                    zombies.append({"Type": self.world["garg"]})
                    budget -= 1500

                # Fill remaining budget
                while budget > 100:
                    candidates = [(self.world["basic"], 150, 40)]
                    if allow_armor1:
                        candidates.append((self.world["armor1"], 300, 30))
                    if allow_armor2 and budget >= 500:
                        candidates.append((self.world["armor2"], 550, 20))
                    if allow_armor4 and budget >= 900:
                        candidates.append((self.world["armor4"], 950, 10))
                    
                    if allow_specials:
                        for sp in self.world.get("specials", []):
                            if w >= sp.get("min_wave", 3) and budget >= sp.get("cost", 400):
                                candidates.append((sp["type"], sp["cost"], 15))

                    types, costs, weights = zip(*candidates)
                    chosen_type = random.choices(types, weights=weights, k=1)[0]
                    chosen_cost = costs[types.index(chosen_type)]

                    zombies.append({"Type": chosen_type})
                    budget -= chosen_cost

            # Plant food flag
            has_pf = 1 if w in plant_food_waves else 0

            waves.append({
                "wave_num": w,
                "is_flag": is_flag,
                "plant_food": has_pf,
                "zombies": zombies,
                "zombie_count": len(zombies)
            })

        return waves

    def assemble_level_json(self, waves_data):
        """Assembles the complete official PvZ2 Level JSON structure."""
        level_name = self.config.get("name", f"{self.world['prefix']} - Custom Level")
        desc = self.config.get("description", "{PLAYER}'s Quest Into The Den!")
        starting_sun = 0 if self.is_night else int(self.config.get("starting_sun", 50))

        stage_mod = self.world["night_stage"] if (self.is_night and "night_stage" in self.world) else self.world["stage"]

        modules = [
            "RTID(WidescreenFix@LevelModules)",
            self.world["mowers"],
            "RTID(StandardIntro@LevelModules)",
            "RTID(SeedBank@CurrentLevel)",
            "RTID(Escalation@CurrentLevel)",
            "RTID(NewWaves@CurrentLevel)",
            "RTID(ZombiesDeadWinCon@LevelModules)",
            "RTID(DefaultZombieWinCondition@LevelModules)"
        ]

        if self.is_night:
            modules.append("RTID(Night@LevelModules)")
        else:
            modules.append("RTID(DefaultSunDropper@LevelModules)")

        # Challenge / Protect Plant Support
        protect_plant = self.config.get("protect_plant")
        protect_x = int(self.config.get("protect_x", 3))
        protect_y = int(self.config.get("protect_y", 2))
        has_ipp = bool(protect_plant)

        if has_ipp:
            modules.insert(3, "RTID(ChallengeModule@CurrentLevel)")
            modules.insert(4, "RTID(IPP@CurrentLevel)")

        # Initial Grid Items (Gravestones or Planks)
        has_planks = self.world.get("has_planks", False)
        plank_rows = self.config.get("plank_rows", [0, 2, 3, 4]) if has_planks else []
        if has_planks:
            modules.insert(4, "RTID(Planks@CurrentLevel)")

        grave_count = int(self.config.get("initial_graves", 0))
        has_graves = grave_count > 0 and "grave_type" in self.world
        if has_graves:
            modules.insert(4, "RTID(GI@CurrentLevel)")

        # Build Objects list
        objects = []

        # 1. LevelDefinition
        level_def_obj = {
            "objclass": "LevelDefinition",
            "objdata": {
                "Description": desc,
                "FirstRewardType": self.config.get("reward_type", "coins"),
                "FirstRewardParam": self.config.get("reward_param", "1000"),
                "Loot": "RTID(DefaultLoot@LevelModules)",
                "Modules": modules,
                "Name": level_name,
                "StageModule": stage_mod,
                "StartingSun": starting_sun
            }
        }
        objects.append(level_def_obj)

        # 2. SeedBankProperties
        objects.append({
            "aliases": ["SeedBank"],
            "objclass": "SeedBankProperties",
            "objdata": {
                "PlantExcludeList": [],
                "SelectionMethod": "chooser"
            }
        })

        # 3. Protect The Plant Challenge (if enabled)
        if has_ipp:
            objects.append({
                "aliases": ["ChallengeModule"],
                "objclass": "StarChallengeModuleProperties",
                "objdata": {
                    "Challenges": [["RTID(BeatTheLevel@CurrentLevel)"]],
                    "ChallengesAlwaysAvailable": True
                }
            })
            objects.append({
                "aliases": ["BeatTheLevel"],
                "objclass": "StarChallengeBeatTheLevelProps",
                "objdata": {
                    "Description": f"Protect the endangered {protect_plant.title()}!",
                    "DescriptiveName": "Protect Endangered Plants"
                }
            })
            objects.append({
                "aliases": ["IPP"],
                "objclass": "ProtectThePlantChallengeProperties",
                "objdata": {
                    "MustProtectCount": 1,
                    "Plants": [{
                        "GridX": protect_x,
                        "GridY": protect_y,
                        "Level": 0,
                        "PlantType": protect_plant
                    }]
                }
            })

        # 4. Planks (if Pirate Seas)
        if has_planks:
            objects.append({
                "aliases": ["Planks"],
                "objclass": "PiratePlankProperties",
                "objdata": {
                    "PlankRows": plank_rows
                }
            })

        # 5. Initial Gravestones (if enabled)
        if has_graves:
            placements = []
            cols = [4, 5, 6, 7, 8]
            rows = [0, 1, 2, 3, 4]
            spots = [(c, r) for c in cols for r in rows]
            random.shuffle(spots)
            for i in range(min(grave_count, len(spots))):
                gx, gy = spots[i]
                placements.append({
                    "GridX": gx,
                    "GridY": gy,
                    "TypeName": self.world["grave_type"]
                })
            objects.append({
                "aliases": ["GI"],
                "objclass": "InitialGridItemProperties",
                "objdata": {
                    "InitialGridItemPlacements": placements
                }
            })

        # 6. Escalation Module
        flag_count = len(self.flag_waves)
        waves_per_flag = self.waves_count // flag_count if flag_count else self.waves_count
        objects.append({
            "aliases": ["Escalation"],
            "objclass": "LevelEscalationModuleProperties",
            "objdata": {
                "FlagCount": flag_count,
                "PlantfoodToSpawnCount": 0,
                "PointIncrementPerWave": 0,
                "StartingPoints": 0,
                "WaveManagerProps": "RTID(WaveManager@CurrentLevel)",
                "WavesPerFlag": waves_per_flag,
                "ZombiePool": ["RTID(tutorial@ZombieTypes)"]
            }
        })

        # 7. WaveManagerModuleProperties & WaveManagerProperties
        objects.append({
            "aliases": ["NewWaves"],
            "objclass": "WaveManagerModuleProperties",
            "objdata": {
                "WaveManagerProps": "RTID(WaveManager@CurrentLevel)"
            }
        })

        flag_interval = self.flag_waves[0] if len(self.flag_waves) == 1 else (self.flag_waves[1] - self.flag_waves[0] if len(self.flag_waves) > 1 else 10)
        
        wave_refs = [[f"RTID(Wave{w['wave_num']}@CurrentLevel)"] for w in waves_data]

        objects.append({
            "aliases": ["WaveManager"],
            "objclass": "WaveManagerProperties",
            "objdata": {
                "FlagWaveInterval": flag_interval,
                "MaxNextWaveHealthPercentage": 0.5,
                "MinNextWaveHealthPercentage": 0.45,
                "SuppressFlagZombie": False,
                "WaveCount": len(waves_data),
                "Waves": wave_refs
            }
        })

        # 8. Individual Wave Action Objects
        for w in waves_data:
            objects.append({
                "aliases": [f"Wave{w['wave_num']}"],
                "objclass": "SpawnZombiesJitteredWaveActionProps",
                "objdata": {
                    "AdditionalPlantfood": w["plant_food"],
                    "Zombies": w["zombies"]
                }
            })

        return {"#comment": "Generated with PvZ2 ITD Level Generator Workbench", "objects": objects, "version": 1}


# --- HTML5 / CSS3 / Vanilla JS Workbench UI ---
HTML_INTERFACE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PvZ2 ITD Level Generator Studio</title>
    <style>
        :root {
            --bg-base: #0f141c;
            --bg-card: #182232;
            --bg-card-sub: #202d42;
            --border-color: #2e3e58;
            --accent-green: #2ecc71;
            --accent-green-hover: #27ae60;
            --accent-cyan: #00d2d3;
            --accent-gold: #f39c12;
            --accent-red: #e74c3c;
            --text-main: #ecf0f1;
            --text-muted: #8fa0bc;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background: var(--bg-base); color: var(--text-main); line-height: 1.5; padding: 20px; }

        .container { max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 460px 1fr; gap: 24px; }
        
        header { grid-column: 1 / -1; display: flex; justify-content: space-between; align-items: center; padding-bottom: 16px; border-bottom: 2px solid var(--border-color); }
        .logo-group h1 { font-size: 26px; color: var(--accent-cyan); display: flex; align-items: center; gap: 10px; }
        .logo-group p { font-size: 13px; color: var(--text-muted); }
        .badge { background: #223a5e; color: var(--accent-cyan); padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }

        .card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
        .card h2 { font-size: 18px; margin-bottom: 14px; color: var(--accent-green); display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }

        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-size: 13px; font-weight: 600; color: var(--text-muted); margin-bottom: 6px; }
        input[type="text"], input[type="number"], select {
            width: 100%; background: var(--bg-card-sub); border: 1px solid var(--border-color); color: var(--text-main);
            padding: 10px 12px; border-radius: 6px; font-size: 14px; transition: border 0.2s;
        }
        input[type="text"]:focus, select:focus { border-color: var(--accent-cyan); outline: none; }

        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

        .range-slider-group { display: flex; align-items: center; gap: 12px; }
        .range-slider-group input[type="range"] { flex: 1; accent-color: var(--accent-green); }
        .slider-val { min-width: 32px; font-weight: bold; color: var(--accent-gold); text-align: right; }

        .checkbox-label { display: flex; align-items: center; gap: 8px; font-size: 14px; cursor: pointer; user-select: none; }
        .checkbox-label input[type="checkbox"] { width: 18px; height: 18px; accent-color: var(--accent-green); }

        .btn {
            display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-size: 14px; font-weight: bold;
            padding: 12px 20px; border-radius: 8px; border: none; cursor: pointer; transition: all 0.2s;
        }
        .btn-primary { background: var(--accent-green); color: #0b2214; width: 100%; font-size: 16px; }
        .btn-primary:hover { background: var(--accent-green-hover); transform: translateY(-1px); }
        .btn-secondary { background: var(--bg-card-sub); color: var(--text-main); border: 1px solid var(--border-color); }
        .btn-secondary:hover { background: #2a3c58; }
        .btn-save { background: var(--accent-cyan); color: #003738; }
        .btn-save:hover { background: #00b7b8; }

        /* Timeline & Wave Grid */
        .preview-pane { display: flex; flex-direction: column; gap: 20px; }
        .timeline-scroll { display: flex; gap: 12px; overflow-x: auto; padding: 10px 0 16px 0; }
        .wave-pill {
            flex: 0 0 160px; background: var(--bg-card-sub); border: 1px solid var(--border-color);
            border-radius: 8px; padding: 12px; font-size: 12px; display: flex; flex-direction: column; gap: 6px;
        }
        .wave-pill.is-flag { border-color: var(--accent-gold); background: #2d2616; }
        .wave-header { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; }
        .flag-tag { color: var(--accent-gold); font-size: 11px; font-weight: 800; }
        .pf-tag { color: var(--accent-green); font-size: 11px; }
        .zombie-list-tags { display: flex; flex-direction: column; gap: 4px; max-height: 180px; overflow-y: auto; }
        .z-tag { background: #131c28; padding: 3px 6px; border-radius: 4px; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        pre#jsonViewer {
            background: #0a0d14; border: 1px solid var(--border-color); border-radius: 8px;
            padding: 16px; font-family: "Courier New", monospace; font-size: 12px;
            max-height: 520px; overflow-y: auto; color: #a6e22e;
        }

        .action-bar { display: flex; gap: 12px; }
    </style>
</head>
<body>

<div class="container">
    <header>
        <div class="logo-group">
            <h1>🌿 PvZ2 ITD Level Generator Studio</h1>
            <p>Procedural Level Synthesizer for "Into The Den" & Modding Tools</p>
        </div>
        <div class="badge">Model: 3,579 Levels Analyzed</div>
    </header>

    <!-- LEFT: Parameters Configuration -->
    <div class="sidebar">
        <div class="card">
            <h2>🌍 World & Identity</h2>
            <div class="form-group">
                <label>World Archetype</label>
                <select id="selWorld" onchange="onWorldChange()">
                    <option value="egypt">Ancient Egypt (AE)</option>
                    <option value="heian">Heian Dynasty (HD)</option>
                    <option value="pirate">Pirate Seas (PS)</option>
                    <option value="dark">Dark Ages (DA)</option>
                    <option value="tutorial">Player's House / Modern (PH)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Level Name</label>
                <input type="text" id="txtName" value="AE - Day 11: Sandstorm Scramble">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Save Filename</label>
                    <input type="text" id="txtFilename" value="EGYPT11.json">
                </div>
                <div class="form-group">
                    <label>Starting Sun</label>
                    <input type="number" id="numSun" value="50" step="25">
                </div>
            </div>
            <div class="form-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="chkNight">
                    🌙 Night Level (No Falling Sun / Tombstone Stage)
                </label>
            </div>
        </div>

        <div class="card">
            <h2>⚔️ Wave & Difficulty Curve</h2>
            <div class="form-group">
                <label>Wave Count: <span id="lblWaves" class="slider-val">12</span></label>
                <div class="range-slider-group">
                    <input type="range" id="rngWaves" min="5" max="25" value="12" oninput="document.getElementById('lblWaves').innerText=this.value">
                </div>
            </div>
            <div class="form-group">
                <label>Difficulty Rating: <span id="lblDiff" class="slider-val">2 (Normal)</span></label>
                <div class="range-slider-group">
                    <input type="range" id="rngDiff" min="1" max="5" value="2" oninput="updateDiffLabel(this.value)">
                </div>
            </div>
            <div class="form-group">
                <label>Flag Wave Interval (0 = Auto-Paced)</label>
                <input type="number" id="numFlagInterval" value="0" min="0" max="25">
            </div>
        </div>

        <div class="card">
            <h2>🛡️ Special Challenges</h2>
            <div class="form-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="chkIPP" onchange="toggleIPP(this.checked)">
                    🌱 Protect Endangered Plant (Save Our Seeds)
                </label>
            </div>
            <div id="ippControls" style="display: none; padding-left: 12px; border-left: 2px solid var(--accent-green); margin-bottom: 12px;">
                <div class="form-group">
                    <label>Target Plant</label>
                    <select id="selPlant"></select>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Grid X (0-8)</label>
                        <input type="number" id="numGridX" value="3" min="0" max="8">
                    </div>
                    <div class="form-group">
                        <label>Grid Y (0-4)</label>
                        <input type="number" id="numGridY" value="2" min="0" max="4">
                    </div>
                </div>
            </div>
            <div class="form-group">
                <label>Initial Gravestones Count</label>
                <input type="number" id="numGraves" value="0" min="0" max="15">
            </div>
        </div>

        <button class="btn btn-primary" onclick="generateLevel()">⚡ Generate Level Procedurally</button>
    </div>

    <!-- RIGHT: Interactive Wave Preview & JSON Inspector -->
    <div class="preview-pane">
        <div class="card">
            <h2>📊 Wave Pacing Timeline</h2>
            <div id="timelineContainer" class="timeline-scroll">
                <div style="color: var(--text-muted); font-size: 14px; padding: 20px;">Click "Generate Level" to preview wave distributions.</div>
            </div>
        </div>

        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h2 style="margin: 0; border: none; padding: 0;">📜 Level JSON Blueprint</h2>
                <div class="action-bar">
                    <button class="btn btn-secondary" onclick="copyJSON()">📋 Copy</button>
                    <button class="btn btn-save" onclick="saveToDisk()">💾 Save to Levels/ITD/</button>
                </div>
            </div>
            <pre id="jsonViewer">// Generated PvZ2 level JSON will appear here...</pre>
        </div>
    </div>
</div>

<script>
    let currentLevelData = null;

    function updateDiffLabel(val) {
        const names = ["1 (Casual)", "2 (Standard)", "3 (Challenging)", "4 (Hardcore)", "5 (Master Nightmare)"];
        document.getElementById('lblDiff').innerText = names[val - 1];
    }

    function toggleIPP(enabled) {
        document.getElementById('ippControls').style.display = enabled ? 'block' : 'none';
    }

    function onWorldChange() {
        const w = document.getElementById('selWorld').value;
        const nameMap = {
            "egypt": { name: "AE - Day 11: Sandstorm Scramble", file: "EGYPT11.json", night: false },
            "heian": { name: "HD - Night 2: Cherry Blossoms", file: "HEIAN2.json", night: true },
            "pirate": { name: "PS - Day 8: Plunder and Planks", file: "PIRATE8.json", night: false },
            "dark": { name: "DA - Night 2: Shadow Swarm", file: "DARK2.json", night: true },
            "tutorial": { name: "PH - Day 6: Front Lawn Skirmish", file: "TUTORIAL6.json", night: false }
        };
        if (nameMap[w]) {
            document.getElementById('txtName').value = nameMap[w].name;
            document.getElementById('txtFilename').value = nameMap[w].file;
            document.getElementById('chkNight').checked = nameMap[w].night;
        }
    }

    async function loadModData() {
        try {
            const resp = await fetch('/api/mod_data');
            const data = await resp.json();
            const selPlant = document.getElementById('selPlant');
            selPlant.innerHTML = '';
            (data.plants || []).forEach(p => {
                const opt = document.createElement('option');
                opt.value = p;
                opt.innerText = p.charAt(0).toUpperCase() + p.slice(1);
                if (p === 'seashroom' || p === 'wallnut') opt.selected = true;
                selPlant.appendChild(opt);
            });
        } catch (e) {
            console.error('Failed to load mod data', e);
        }
    }

    async function generateLevel() {
        const payload = {
            world: document.getElementById('selWorld').value,
            name: document.getElementById('txtName').value,
            wave_count: document.getElementById('rngWaves').value,
            difficulty: document.getElementById('rngDiff').value,
            flag_interval: document.getElementById('numFlagInterval').value,
            starting_sun: document.getElementById('numSun').value,
            is_night: document.getElementById('chkNight').checked,
            protect_plant: document.getElementById('chkIPP').checked ? document.getElementById('selPlant').value : null,
            protect_x: document.getElementById('numGridX').value,
            protect_y: document.getElementById('numGridY').value,
            initial_graves: document.getElementById('numGraves').value
        };

        const resp = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const res = await resp.json();
        currentLevelData = res.level_json;
        document.getElementById('jsonViewer').innerText = JSON.stringify(currentLevelData, null, 2);

        // Render Timeline
        renderTimeline(res.waves_data);
    }

    function renderTimeline(waves) {
        const container = document.getElementById('timelineContainer');
        container.innerHTML = '';
        waves.forEach(w => {
            const pill = document.createElement('div');
            pill.className = 'wave-pill' + (w.is_flag ? ' is-flag' : '');
            
            let badges = '';
            if (w.is_flag) badges += '<span class="flag-tag">🚩 FLAG WAVE</span>';
            if (w.plant_food > 0) badges += '<span class="pf-tag">🍃 Plant Food</span>';

            const zTags = w.zombies.map(z => {
                const clean = z.Type.replace('RTID(', '').replace('@ZombieTypes)', '');
                return `<div class="z-tag" title="${clean}">${clean}</div>`;
            }).join('');

            pill.innerHTML = `
                <div class="wave-header">
                    <span>Wave ${w.wave_num}</span>
                    <span style="font-size: 11px; color: var(--text-muted);">${w.zombie_count}z</span>
                </div>
                ${badges}
                <div class="zombie-list-tags">${zTags}</div>
            `;
            container.appendChild(pill);
        });
    }

    function copyJSON() {
        if (!currentLevelData) return alert('Generate a level first!');
        navigator.clipboard.writeText(JSON.stringify(currentLevelData, null, 2));
        alert('Level JSON copied to clipboard!');
    }

    async function saveToDisk() {
        if (!currentLevelData) return alert('Generate a level first!');
        const filename = document.getElementById('txtFilename').value.trim();
        if (!filename.endsWith('.json')) return alert('Filename must end with .json');

        const resp = await fetch('/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename, content: currentLevelData })
        });
        const res = await resp.json();
        if (res.success) {
            alert(`✅ Level successfully saved to:\nLevels/ITD/${filename}`);
        } else {
            alert(`❌ Error saving level: ${res.error}`);
        }
    }

    window.onload = () => {
        loadModData();
        generateLevel();
    };
</script>
</body>
</html>
"""


class LevelGenHTTPHandler(BaseHTTPRequestHandler):
    """Zero-dependency HTTP API for the Level Generator Studio."""

    def _send_json(self, data, code=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            body = HTML_INTERFACE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif parsed.path == "/api/mod_data":
            plants = load_available_plants()
            self._send_json({"worlds": list(DEFAULT_WORLDS.keys()), "plants": plants})
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8")
        try:
            req_data = json.loads(post_body) if post_body else {}
        except Exception:
            req_data = {}

        if parsed.path == "/api/generate":
            engine = ProceduralWaveEngine(req_data)
            waves_data = engine.generate_waves()
            level_json = engine.assemble_level_json(waves_data)
            self._send_json({"waves_data": waves_data, "level_json": level_json})

        elif parsed.path == "/api/save":
            fname = req_data.get("filename", "CUSTOM_LEVEL.json")
            content = req_data.get("content")
            if not content:
                self._send_json({"success": False, "error": "No content provided"}, 400)
                return

            os.makedirs(LEVELS_ITD_DIR, exist_ok=True)
            target_path = os.path.join(LEVELS_ITD_DIR, os.path.basename(fname))
            try:
                with open(target_path, "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=2)
                self._send_json({"success": True, "saved_path": target_path})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, 500)
        else:
            self.send_error(404, "Unknown API Endpoint")


def run_server(port=PORT):
    server = HTTPServer(("127.0.0.1", port), LevelGenHTTPHandler)
    url = f"http://127.0.0.1:{port}"
    print(f"\n=======================================================")
    print(f"🌿 PvZ2 ITD Level Generator Studio running at:")
    print(f"   👉 {url}")
    print(f"=======================================================\n")
    print("Press Ctrl+C to stop the studio server.")
    
    # Open browser automatically if not in headless environment
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Level Generator Studio.")
        server.server_close()


def run_cli_generation(args):
    """Allows running level generation purely from command line."""
    world = args.world if hasattr(args, "world") else "egypt"
    waves = args.waves if hasattr(args, "waves") else 12
    diff = args.diff if hasattr(args, "diff") else 2
    out = args.output if hasattr(args, "output") else "GENERATED_LEVEL.json"

    cfg = {"world": world, "wave_count": waves, "difficulty": diff}
    engine = ProceduralWaveEngine(cfg)
    waves_data = engine.generate_waves()
    lvl = engine.assemble_level_json(waves_data)

    with open(out, "w", encoding="utf-8") as f:
        json.dump(lvl, f, indent=2)
    print(f"✅ Generated {waves}-wave level for world '{world}' saved to {out}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        import argparse
        parser = argparse.ArgumentParser(description="PvZ2 Level Generator CLI")
        parser.add_argument("--world", default="egypt", choices=list(DEFAULT_WORLDS.keys()))
        parser.add_argument("--waves", type=int, default=12)
        parser.add_argument("--diff", type=int, default=2)
        parser.add_argument("--output", default="CUSTOM_LEVEL.json")
        args = parser.parse_args(sys.argv[2:])
        run_cli_generation(args)
    else:
        run_server()
