import os
import pygame
<<<<<<< HEAD
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, PALETTE
=======
from generate_assets import generate_all_assets

ASSETS_DIR = "assets"
>>>>>>> da45a41 (Novo commit fresco)


class SpriteBank:
    def __init__(self):
<<<<<<< HEAD
        self.cache = {}
        self.bg_base = self._load_or_build_bg()
        self.ground_tile = self._load_or_build_ground()
        self.player_anims = self._build_player_sprites()
        self.projectiles = self._build_projectiles()
        self.ui_icons = self._build_ui_icons()

    def _px_surface(self, w, h, scale=3):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        return surf, scale

    def _finalize(self, surf, scale=3, flip_x=False):
        if flip_x:
            surf = pygame.transform.flip(surf, True, False)
        return pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))

    def _load_or_build_bg(self):
        if os.path.exists("background.png"):
            try:
                img = pygame.image.load("background.png").convert()
                return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except Exception:
                pass
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surf.fill(PALETTE["sky_light"])
        pygame.draw.rect(surf, (235, 210, 245), (260, 40, 240, 140))
        pygame.draw.rect(surf, PALETTE["sky_mid"], (0, 250, SCREEN_WIDTH, 290))
        buildings = [
            (20, 40, 65, 300, False), (150, 40, 75, 300, False),
            (230, 110, 70, 260, True), (320, 190, 75, 180, True),
            (410, 110, 70, 260, True), (500, 110, 75, 260, True),
            (590, 190, 70, 180, True), (680, 110, 70, 260, True),
            (770, 110, 70, 260, True), (860, 190, 70, 180, True),
        ]
        for bx, by, bw, bh, lit in buildings:
            pygame.draw.rect(surf, PALETTE["building_dark"], (bx, by, bw, bh))
            if lit:
                for wy in range(by + 25, by + bh - 45, 45):
                    pygame.draw.rect(surf, PALETTE["window_orange"], (bx + 14, wy, 12, 28))
                    pygame.draw.rect(surf, PALETTE["window_orange"], (bx + 38, wy, 12, 28))
        pygame.draw.rect(surf, (92, 46, 86), (0, 360, SCREEN_WIDTH, 180))
        return surf

    def _load_or_build_ground(self):
        if os.path.exists("chao.png"):
            try:
                img = pygame.image.load("chao.png").convert()
                return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
            except Exception:
                pass
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
        surf.fill(PALETTE["ground_dark"])
        pygame.draw.rect(surf, PALETTE["ground_trim"], (0, 0, SCREEN_WIDTH, 6))
        return surf

    def get_themed_bg(self, theme):
        key = f"bg_{theme}"
        if key in self.cache:
            return self.cache[key]
        bg = self.bg_base.copy()
        tint = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        if theme == "tutorial":
            tint.fill((40, 20, 60, 35))
            bg.blit(tint, (0, 0))
            pygame.draw.rect(bg, (30, 22, 42), (620, 290, 190, 160))
            pygame.draw.rect(bg, PALETTE["neon_cyan"], (630, 300, 170, 26), 2)
        elif theme == "noroeste":
            tint.fill((120, 65, 15, 55))
            bg.blit(tint, (0, 0))
            pygame.draw.line(bg, (235, 175, 40), (140, 380), (220, 90), 6)
            pygame.draw.line(bg, (235, 175, 40), (160, 110), (420, 110), 5)
            pygame.draw.line(bg, (200, 200, 210), (390, 110), (390, 220), 2)
        elif theme == "nordeste":
            tint.fill((110, 15, 95, 65))
            bg.blit(tint, (0, 0))
            pygame.draw.polygon(bg, (255, 70, 180, 45), [(200, 450), (80, 0), (260, 0)])
            pygame.draw.polygon(bg, (60, 235, 255, 45), [(720, 450), (580, 0), (820, 0)])
        elif theme == "sul":
            tint.fill((15, 45, 110, 70))
            bg.blit(tint, (0, 0))
            for sx in range(80, 900, 220):
                pygame.draw.rect(bg, (35, 48, 82), (sx, 240, 90, 210), 3)
        elif theme == "final":
            tint.fill((130, 15, 30, 80))
            bg.blit(tint, (0, 0))
            pygame.draw.circle(bg, (255, 60, 80), (480, 130), 55)
        self.cache[key] = bg
        return bg

    def _draw_pur_frame(self, leg_offset=0, arm_mode="normal", jump=False, dead=False):
        s, scale = self._px_surface(24, 28, scale=3)
        O = PALETTE["outline"]
        OR = PALETTE["pur_orange"]
        DO = PALETTE["pur_dark_orange"]
        CR = PALETTE["pur_cream"]
        SH = PALETTE["pur_shirt"]
        PA = PALETTE["pur_pants"]
        CA = PALETTE["pur_cannon"]
        CH = PALETTE["pur_cannon_hi"]
        CY = PALETTE["goggle_cyan"]
        BL = PALETTE["blush"]

        if dead:
            pygame.draw.rect(s, O, (2, 18, 20, 9))
            pygame.draw.rect(s, OR, (3, 19, 8, 7))
            pygame.draw.rect(s, CR, (4, 20, 5, 4))
            pygame.draw.rect(s, SH, (11, 20, 6, 6))
            pygame.draw.rect(s, PA, (17, 21, 4, 5))
            s.set_at((5, 21), O)
            s.set_at((7, 23), O)
            s.set_at((7, 21), O)
            s.set_at((5, 23), O)
            return self._finalize(s, scale)

        y_shift = -1 if jump else 0

        # Orelhas
        pygame.draw.polygon(s, O, [(2, 11 + y_shift), (2, 1 + y_shift), (7, 5 + y_shift)])
        pygame.draw.polygon(s, CR, [(3, 9 + y_shift), (3, 3 + y_shift), (6, 6 + y_shift)])
        pygame.draw.polygon(s, DO, [(4, 8 + y_shift), (4, 4 + y_shift), (6, 6 + y_shift)])
        pygame.draw.polygon(s, O, [(10, 5 + y_shift), (13, 0 + y_shift), (14, 9 + y_shift)])
        pygame.draw.polygon(s, DO, [(11, 6 + y_shift), (13, 2 + y_shift), (13, 8 + y_shift)])

        # Cabeça
        pygame.draw.rect(s, O, (4, 5 + y_shift, 10, 8))
        pygame.draw.rect(s, OR, (5, 6 + y_shift, 8, 4))
        pygame.draw.rect(s, CR, (5, 10 + y_shift, 8, 2))
        pygame.draw.rect(s, CY, (6, 7 + y_shift, 2, 2))
        pygame.draw.rect(s, CY, (11, 7 + y_shift, 2, 2))
        pygame.draw.rect(s, O, (7, 9 + y_shift, 1, 2))
        pygame.draw.rect(s, O, (11, 9 + y_shift, 1, 2))
        s.set_at((5, 11 + y_shift), BL)
        s.set_at((12, 11 + y_shift), BL)

        # Tronco
        pygame.draw.rect(s, O, (4, 13 + y_shift, 9, 8))
        pygame.draw.rect(s, SH, (5, 14 + y_shift, 7, 6))
        pygame.draw.rect(s, CR, (8, 14 + y_shift, 2, 1))
        pygame.draw.rect(s, O, (2, 14 + y_shift, 3, 6))
        pygame.draw.rect(s, CR, (3, 15 + y_shift, 1, 4))

        # Pernas
        l1 = leg_offset if not jump else -2
        l2 = -leg_offset if not jump else 2
        pygame.draw.rect(s, O, (3 + l1, 20, 4, 6))
        pygame.draw.rect(s, PA, (4 + l1, 21, 2, 4))
        pygame.draw.rect(s, CR, (3 + l1, 25, 3, 2))
        pygame.draw.rect(s, O, (9 + l2, 20, 4, 6))
        pygame.draw.rect(s, PA, (10 + l2, 21, 2, 4))
        pygame.draw.rect(s, CR, (10 + l2, 25, 3, 2))

        # Braço Canhão
        if arm_mode == "up":
            pygame.draw.rect(s, O, (11, 4 + y_shift, 6, 9))
            pygame.draw.rect(s, CA, (12, 6 + y_shift, 4, 6))
            pygame.draw.rect(s, CH, (12, 6 + y_shift, 2, 4))
            pygame.draw.rect(s, O, (13, 2 + y_shift, 2, 3))
        else:
            recoil = -1 if arm_mode == "shoot" else 0
            pygame.draw.rect(s, O, (12 + recoil, 13 + y_shift, 9, 6))
            pygame.draw.rect(s, CR, (12 + recoil, 14 + y_shift, 2, 2))
            pygame.draw.rect(s, CA, (14 + recoil, 14 + y_shift, 6, 4))
            pygame.draw.rect(s, CH, (16 + recoil, 14 + y_shift, 3, 2))
            pygame.draw.rect(s, O, (20 + recoil, 15 + y_shift, 3, 2))

        return self._finalize(s, scale)

    def _build_player_sprites(self):
        anims = {
            "idle": [self._draw_pur_frame(0, "normal")],
            "run": [
                self._draw_pur_frame(-2, "normal"),
                self._draw_pur_frame(0, "normal"),
                self._draw_pur_frame(2, "normal"),
                self._draw_pur_frame(0, "normal"),
            ],
            "jump": [self._draw_pur_frame(0, "normal", jump=True)],
            "shoot": [
                self._draw_pur_frame(0, "shoot"),
                self._draw_pur_frame(0, "normal"),
            ],
            "up": [self._draw_pur_frame(0, "up")],
            "dead": [self._draw_pur_frame(0, "normal", dead=True)],
        }
        for k in list(anims.keys()):
            anims[k + "_left"] = [pygame.transform.flip(f, True, False) for f in anims[k]]
=======
        self._ensure_assets()
        self.cache = {}
        self.bg_base = self._load_image(os.path.join(ASSETS_DIR, "backgrounds", "bg_base.png"), alpha=False)
        self.ground_tile = self._load_image(os.path.join(ASSETS_DIR, "backgrounds", "ground_tile.png"), alpha=False)
        self.player_anims = self._load_player_sprites()
        self.projectiles = self._load_projectiles()
        self.ui_icons = self._load_ui_icons()

    def _ensure_assets(self):
        required_files = [
            os.path.join(ASSETS_DIR, ".assets_v2"),
            os.path.join(ASSETS_DIR, "player", "melee_0.png"),
            os.path.join(ASSETS_DIR, "player", "down_0.png"),
        ]
        if not os.path.exists(ASSETS_DIR) or any(not os.path.exists(f) for f in required_files):
            generate_all_assets(ASSETS_DIR)

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
>>>>>>> da45a41 (Novo commit fresco)
        return anims

    def get_enemy_sprites(self, enemy_type, theme):
        key = f"enemy_{enemy_type}_{theme}"
<<<<<<< HEAD
        if key in self.cache:
            return self.cache[key]

        theme_colors = {
            "tutorial": ((150, 105, 70), (210, 55, 65)),
            "noroeste": ((135, 95, 60), (245, 185, 35)),
            "nordeste": ((115, 85, 130), (255, 65, 200)),
            "sul": ((125, 110, 95), (65, 165, 240)),
            "final": ((90, 45, 55), (255, 50, 75)),
        }
        fur, accent = theme_colors.get(theme, theme_colors["tutorial"])
        O = PALETTE["outline"]
        frames = []

        for step in (0, 1):
            if enemy_type == "boxer":
                s, sc = self._px_surface(20, 24, 3)
                pygame.draw.rect(s, O, (4, 2, 12, 10))
                pygame.draw.rect(s, fur, (5, 3, 10, 8))
                pygame.draw.rect(s, accent, (5, 2, 10, 2))
                pygame.draw.rect(s, O, (6, 6, 2, 2))
                pygame.draw.rect(s, O, (4, 12, 12, 7))
                pygame.draw.rect(s, accent, (5, 13, 10, 5))
                gx = 1 if step == 0 else -2
                pygame.draw.rect(s, O, (gx, 12, 5, 5))
                pygame.draw.rect(s, PALETTE["red"], (gx + 1, 13, 3, 3))
                pygame.draw.rect(s, O, (5 + step, 19, 3, 5))
                pygame.draw.rect(s, O, (11 - step, 19, 3, 5))
                frames.append(self._finalize(s, sc))

            elif enemy_type == "agent":
                s, sc = self._px_surface(20, 26, 3)
                pygame.draw.rect(s, O, (5, 2, 10, 9))
                pygame.draw.rect(s, fur, (6, 3, 8, 7))
                pygame.draw.rect(s, O, (5, 5, 8, 2))
                pygame.draw.rect(s, O, (4, 11, 12, 9))
                pygame.draw.rect(s, (35, 38, 48), (5, 12, 10, 7))
                pygame.draw.rect(s, accent, (9, 12, 2, 6))
                pygame.draw.rect(s, O, (0, 13 + step, 6, 3))
                pygame.draw.rect(s, O, (5, 20, 3, 6))
                pygame.draw.rect(s, O, (11, 20, 3, 6))
                frames.append(self._finalize(s, sc))

            elif enemy_type == "trash":
                s, sc = self._px_surface(18, 22, 3)
                lid_y = 2 if step == 0 else 0
                pygame.draw.rect(s, O, (2, 7, 14, 15))
                pygame.draw.rect(s, (110, 120, 130), (3, 8, 12, 13))
                pygame.draw.rect(s, accent, (3, 12, 12, 2))
                pygame.draw.rect(s, O, (1, lid_y, 16, 3))
                if step == 1:
                    pygame.draw.rect(s, fur, (4, 3, 10, 4))
                    pygame.draw.rect(s, PALETTE["neon_yellow"], (6, 4, 2, 2))
                    pygame.draw.rect(s, PALETTE["neon_yellow"], (10, 4, 2, 2))
                frames.append(self._finalize(s, sc))

            elif enemy_type == "drone":
                s, sc = self._px_surface(22, 16, 3)
                prop = 1 if step == 0 else 4
                pygame.draw.rect(s, O, (4 + prop, 1, 12 - prop, 2))
                pygame.draw.rect(s, O, (4, 4, 14, 8))
                pygame.draw.rect(s, accent, (5, 5, 12, 6))
                pygame.draw.rect(s, PALETTE["white"], (6, 7, 4, 2))
                pygame.draw.rect(s, O, (8, 12, 6, 3))
                frames.append(self._finalize(s, sc))

        self.cache[key] = frames
        return frames

    def get_boss_sprites(self, boss_id):
        key = f"boss_{boss_id}"
        if key in self.cache:
            return self.cache[key]
        O = PALETTE["outline"]
        frames = []

        for step in (0, 1):
            if boss_id == "tutorial":
                s, sc = self._px_surface(34, 38, 3)
                pygame.draw.rect(s, O, (6, 3, 22, 14))
                pygame.draw.rect(s, (165, 115, 80), (7, 4, 20, 12))
                pygame.draw.rect(s, PALETTE["red"], (7, 3, 20, 3))
                pygame.draw.rect(s, O, (4, 17, 26, 14))
                pygame.draw.rect(s, (220, 220, 230), (6, 18, 22, 12))
                pygame.draw.rect(s, O, (7, 31, 7, 7 - step))
                pygame.draw.rect(s, O, (20, 31, 7, 6 + step))
                frames.append(self._finalize(s, sc))

            elif boss_id == "noroeste":
                s, sc = self._px_surface(38, 44, 3)
                pygame.draw.rect(s, O, (9, 1, 20, 6))
                pygame.draw.rect(s, (245, 195, 40), (10, 2, 18, 4))
                pygame.draw.rect(s, O, (8, 7, 22, 12))
                pygame.draw.rect(s, (155, 110, 75), (9, 8, 20, 10))
                pygame.draw.rect(s, O, (4, 19, 30, 16))
                pygame.draw.rect(s, (230, 125, 35), (5, 20, 28, 14))
                pygame.draw.rect(s, (55, 75, 115), (7, 35, 9, 9 - step))
                pygame.draw.rect(s, (55, 75, 115), (22, 35, 9, 8 + step))
                frames.append(self._finalize(s, sc))

            elif boss_id == "nordeste":
                s, sc = self._px_surface(44, 40, 3)
                pygame.draw.rect(s, O, (12, 3, 20, 15))
                pygame.draw.rect(s, (225, 232, 240), (13, 4, 18, 13))
                pygame.draw.rect(s, PALETTE["neon_cyan"], (10, 6, 4, 8))
                pygame.draw.rect(s, PALETTE["neon_cyan"], (30, 6, 4, 8))
                pygame.draw.rect(s, O, (3, 18, 38, 21))
                pygame.draw.rect(s, (45, 30, 68), (4, 19, 36, 19))
                pygame.draw.circle(s, PALETTE["neon_pink"], (22, 29), 6 + step, 2)
                frames.append(self._finalize(s, sc))

            elif boss_id == "sul":
                s, sc = self._px_surface(40, 44, 3)
                pygame.draw.rect(s, O, (3, 27, 34, 16))
                pygame.draw.rect(s, (185, 65, 75), (4, 28, 32, 5))
                pygame.draw.rect(s, (65, 125, 195), (4, 33, 32, 5))
                pygame.draw.rect(s, (85, 175, 105), (4, 38, 32, 4))
                pygame.draw.rect(s, O, (12, 4, 16, 12))
                pygame.draw.rect(s, (215, 185, 155), (13, 5, 14, 10))
                pygame.draw.rect(s, PALETTE["neon_cyan"], (14, 8, 5, 3))
                pygame.draw.rect(s, PALETTE["neon_cyan"], (21, 8, 5, 3))
                pygame.draw.rect(s, O, (10, 16, 20, 11))
                pygame.draw.rect(s, PALETTE["white"], (11, 17, 18, 9))
                frames.append(self._finalize(s, sc))

            elif boss_id == "final_mech":
                s, sc = self._px_surface(56, 56, 3)
                pygame.draw.rect(s, O, (8, 4, 40, 44))
                pygame.draw.rect(s, (75, 82, 98), (10, 6, 36, 40))
                pygame.draw.rect(s, O, (4, 6, 6, 16))
                pygame.draw.rect(s, O, (46, 6, 6, 16))
                pygame.draw.rect(s, PALETTE["red"], (16, 12, 24, 10))
                pygame.draw.rect(s, (235, 185, 175), (24, 14, 8, 7))
                pygame.draw.rect(s, O, (2, 26 + step, 10, 10))
                pygame.draw.rect(s, O, (44, 26 - step, 10, 10))
                pygame.draw.rect(s, O, (12, 48, 12, 8))
                pygame.draw.rect(s, O, (32, 48, 12, 8))
                frames.append(self._finalize(s, sc))

            elif boss_id == "final_cat":
                s, sc = self._px_surface(24, 28, 3)
                skin = (236, 184, 176)
                dark_skin = (198, 142, 136)
                pygame.draw.polygon(s, O, [(4, 9), (3, 1), (9, 6)])
                pygame.draw.polygon(s, dark_skin, [(5, 8), (4, 3), (8, 6)])
                pygame.draw.polygon(s, O, [(15, 6), (21, 1), (20, 9)])
                pygame.draw.polygon(s, dark_skin, [(16, 6), (20, 3), (19, 8)])
                pygame.draw.rect(s, O, (5, 6, 14, 10))
                pygame.draw.rect(s, skin, (6, 7, 12, 8))
                pygame.draw.rect(s, PALETTE["neon_yellow"], (8, 10, 2, 2))
                pygame.draw.rect(s, PALETTE["neon_yellow"], (14, 10, 2, 2))
                pygame.draw.rect(s, O, (7, 16, 10, 8))
                pygame.draw.rect(s, skin, (8, 17, 8, 6))
                pygame.draw.rect(s, O, (7 + step, 24, 3, 4))
                pygame.draw.rect(s, O, (14 - step, 24, 3, 4))
                frames.append(self._finalize(s, sc))

        self.cache[key] = frames
        return frames

    def _build_projectiles(self):
        s1, sc1 = self._px_surface(8, 5, 3)
        pygame.draw.rect(s1, PALETTE["outline"], (0, 0, 8, 5))
        pygame.draw.rect(s1, PALETTE["neon_cyan"], (1, 1, 6, 3))
        pygame.draw.rect(s1, PALETTE["white"], (3, 2, 3, 1))

        s2, sc2 = self._px_surface(18, 14, 3)
        pygame.draw.ellipse(s2, PALETTE["outline"], (0, 0, 18, 14))
        pygame.draw.ellipse(s2, PALETTE["neon_pink"], (1, 1, 16, 12))
        pygame.draw.ellipse(s2, PALETTE["neon_yellow"], (4, 3, 10, 8))
        pygame.draw.ellipse(s2, PALETTE["white"], (7, 5, 5, 4))

        s3, sc3 = self._px_surface(12, 7, 3)
        pygame.draw.rect(s3, PALETTE["outline"], (2, 1, 9, 5))
        pygame.draw.rect(s3, PALETTE["white"], (3, 2, 6, 3))
        pygame.draw.rect(s3, PALETTE["red"], (8, 2, 3, 3))
        pygame.draw.rect(s3, PALETTE["neon_yellow"], (0, 2, 2, 3))

        s4, sc4 = self._px_surface(7, 7, 3)
        pygame.draw.circle(s4, PALETTE["outline"], (3, 3), 3)
        pygame.draw.circle(s4, PALETTE["red"], (3, 3), 2)

        return {
            "normal": self._finalize(s1, sc1),
            "big": self._finalize(s2, sc2),
            "missile": self._finalize(s3, sc3),
            "enemy": self._finalize(s4, sc4),
        }

    def _build_ui_icons(self):
        icons = {}
        h, sc = self._px_surface(11, 10, 3)
        pts = [(1, 2), (3, 1), (5, 3), (7, 1), (9, 2), (9, 5), (5, 9), (1, 5)]
        pygame.draw.polygon(h, PALETTE["outline"], pts)
        pygame.draw.rect(h, PALETTE["red"], (2, 2, 3, 3))
        pygame.draw.rect(h, PALETTE["red"], (6, 2, 3, 3))
        pygame.draw.rect(h, PALETTE["red"], (3, 5, 5, 2))
        pygame.draw.rect(h, PALETTE["red"], (4, 7, 3, 1))
        icons["heart"] = self._finalize(h, sc)

        for up_id, col in [
            ("explosion", PALETTE["neon_yellow"]),
            ("big_shot", PALETTE["neon_pink"]),
            ("missiles", PALETTE["neon_cyan"]),
        ]:
            u, sc = self._px_surface(14, 14, 3)
            pygame.draw.rect(u, PALETTE["outline"], (0, 0, 14, 14))
            pygame.draw.rect(u, (35, 30, 50), (1, 1, 12, 12))
            if up_id == "explosion":
                pygame.draw.circle(u, col, (7, 7), 4)
                pygame.draw.circle(u, PALETTE["white"], (7, 7), 2)
            elif up_id == "big_shot":
                pygame.draw.ellipse(u, col, (2, 4, 10, 6))
            elif up_id == "missiles":
                pygame.draw.polygon(u, col, [(3, 10), (7, 3), (11, 10)])
            icons[up_id] = self._finalize(u, sc)
        return icons
=======
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
>>>>>>> da45a41 (Novo commit fresco)
