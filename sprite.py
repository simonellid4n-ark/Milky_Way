import os
import pygame
from generate_assets import generate_all_assets

ASSETS_DIR = "assets"


class SpriteBank:
    def __init__(self):
        if not os.path.exists(ASSETS_DIR):
            generate_all_assets(ASSETS_DIR)

        self.cache = {}
        self.bg_base = self._load_image(os.path.join(ASSETS_DIR, "backgrounds", "bg_base.png"), alpha=False)
        self.ground_tile = self._load_image(os.path.join(ASSETS_DIR, "backgrounds", "ground_tile.png"), alpha=False)
        self.player_anims = self._load_player_sprites()
        self.projectiles = self._load_projectiles()
        self.ui_icons = self._load_ui_icons()

    def _load_image(self, path, alpha=True):
        if not os.path.exists(path):
            generate_all_assets(ASSETS_DIR)
        img = pygame.image.load(path)
        return img.convert_alpha() if alpha else img.convert()

    def get_themed_bg(self, theme):
        key = f"bg_{theme}"
        if key not in self.cache:
            path = os.path.join(ASSETS_DIR, "backgrounds", f"bg_{theme}.png")
            self.cache[key] = self._load_image(path, alpha=False)
        return self.cache[key]

    def _load_player_sprites(self):
        spec = {
            "idle": ["idle_0.png"],
            "run": ["run_0.png", "run_1.png", "run_2.png", "run_3.png"],
            "jump": ["jump_0.png"],
            "shoot": ["shoot_0.png", "shoot_1.png"],
            "up": ["up_0.png"],
            "down": ["down_0.png"],
            "melee": ["melee_0.png"],
            "dead": ["dead_0.png"],
        }
        anims = {}
        for state, files in spec.items():
            anims[state] = [
                self._load_image(os.path.join(ASSETS_DIR, "player", fname), alpha=True)
                for fname in files
            ]
            anims[state + "_left"] = [
                pygame.transform.flip(f, True, False) for f in anims[state]
            ]
        return anims

    def get_enemy_sprites(self, enemy_type, theme):
        key = f"enemy_{enemy_type}_{theme}"
        if key not in self.cache:
            self.cache[key] = [
                self._load_image(os.path.join(ASSETS_DIR, "enemies", f"{enemy_type}_{theme}_{idx}.png"), alpha=True)
                for idx in (0, 1)
            ]
        return self.cache[key]

    def get_boss_sprites(self, boss_id):
        key = f"boss_{boss_id}"
        if key not in self.cache:
            self.cache[key] = [
                self._load_image(os.path.join(ASSETS_DIR, "bosses", f"{boss_id}_{idx}.png"), alpha=True)
                for idx in (0, 1)
            ]
        return self.cache[key]

    def _load_projectiles(self):
        return {
            name: self._load_image(os.path.join(ASSETS_DIR, "projectiles", f"{name}.png"), alpha=True)
            for name in ("normal", "big", "missile", "enemy")
        }

    def _load_ui_icons(self):
        return {
            name: self._load_image(os.path.join(ASSETS_DIR, "ui", f"{name}.png"), alpha=True)
            for name in ("heart", "explosion", "big_shot", "missiles")
        }