import json
import os
import sys
import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GROUND_Y,
    SAVE_FILE,
    PALETTE,
    STAGE_META,
    UPGRADE_NAMES,
)
from sound import SoundManager
from sprites import SpriteBank
from entities import Player
from levels import build_stage


class MilkyWayGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Milky Way - Pur's Cyberpunk Revolution")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("consolas", 42, bold=True)
        self.font_lg = pygame.font.SysFont("consolas", 24, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_sm = pygame.font.SysFont("consolas", 14, bold=True)

        self.sound = SoundManager()
        self.sprites = SpriteBank()
        self.player = Player(100, GROUND_Y, self.sprites)

        self.completed_stages = set()
        self.unlocked_upgrades = []
        self.equipped_upgrade = None

        self.state = "MENU"
        self.current_stage_id = "tutorial"
        self.platforms = []
        self.enemies = []
        self.boss = None
        self.projectiles = []
        self.enemy_projectiles = []
        self.cam_x = 0
        self.boss_locked = False
        self.cutscene_idx = 0
        self.map_selected = "noroeste"
        self.last_reward_msg = ""

<<<<<<< HEAD
=======
        # Cache de HUD estático e superfícies pré-alocadas para manter 60 FPS estáveis
        self.hud_panel = pygame.Surface((380, 92), pygame.SRCALPHA)
        self.hud_panel.fill((18, 12, 28, 200))
        pygame.draw.rect(self.hud_panel, PALETTE["neon_cyan"], (0, 0, 380, 92), 2)

        self.empty_heart = self.sprites.ui_icons["heart"].copy()
        self.empty_heart.fill((60, 60, 60, 140), special_flags=pygame.BLEND_RGBA_MULT)

        self.txt_swap_hint = self.font_sm.render("[Q/E] Trocar  [X] Usar", True, PALETTE["white"])
        self.txt_equip_hint = self.font_sm.render("[Q/E] Equipar", True, (160, 150, 175))
        self.txt_no_upgrade = self.font_sm.render("Sem Upgrade", True, (160, 150, 175))
        self.txt_tutorial_tip = self.font_sm.render(
            "Mover: A/D | Pular: ESPACO | Mirar: W/S | Atirar/Corpo-a-Corpo: Z/J",
            True,
            PALETTE["neon_yellow"],
        )
        self.up_labels = {
            k: self.font_sm.render(v.split("(")[0].strip(), True, PALETTE["neon_yellow"])
            for k, v in UPGRADE_NAMES.items()
        }
        self.energy_labels = [
            self.font_sm.render(f"ENERGIA: {i}%", True, PALETTE["white"]) for i in range(101)
        ]
        self._cached_boss_id = None
        self._cached_boss_label = None

>>>>>>> da45a41 (Novo commit fresco)
        self.intro_slides = [
            "Era uma noite chuvosa na cidade neon... Pur só queria uma tigela de leite fresco.",
            "Ao chegar no mercado do bairro, as ruas estavam vazias e tomadas pela Gangue dos Dogs!",
            "Com seu canhão inventado na garagem, Pur decide libertar cada bairro da cidade!",
        ]
        self.final_slides = [
            "O enorme exoesqueleto desmorona! De dentro dele salta... um Gato Pelado (Sphynx)!",
            "Ele manipulava a Gangue dos Dogs para monopolizar todo o leite da cidade!",
            "Sem sua armadura, ele é derrotado rapidamente e entregue às autoridades.",
            "Pur ajuda a reconstruir a cidade e finalmente saboreia sua deliciosa tigela de leite!",
        ]

    def save_game(self):
        data = {
            "completed": list(self.completed_stages),
            "upgrades": self.unlocked_upgrades,
            "equipped": self.equipped_upgrade,
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            return False
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.completed_stages = set(data.get("completed", []))
            self.unlocked_upgrades = data.get("upgrades", [])
            self.equipped_upgrade = data.get("equipped", None)
            return True
        except Exception:
            return False

    def cycle_upgrade(self, step=1):
        if not self.unlocked_upgrades:
            return
        if self.equipped_upgrade not in self.unlocked_upgrades:
            self.equipped_upgrade = self.unlocked_upgrades[0]
        else:
            idx = (self.unlocked_upgrades.index(self.equipped_upgrade) + step) % len(self.unlocked_upgrades)
            self.equipped_upgrade = self.unlocked_upgrades[idx]

    def start_stage(self, stage_id):
        self.current_stage_id = stage_id
        completed_regions = len(self.completed_stages.intersection({"noroeste", "nordeste", "sul"}))
        self.platforms, self.enemies, self.boss = build_stage(stage_id, self.sprites, completed_regions)
        self.projectiles = []
        self.enemy_projectiles = []
        self.player.reset_for_stage(90, GROUND_Y)
        self.cam_x = 0
        self.boss_locked = (stage_id == "final")
<<<<<<< HEAD
=======
        self._cached_boss_id = None
>>>>>>> da45a41 (Novo commit fresco)
        self.state = "STAGE"
        self.sound.start_bgm()

    def handle_stage_victory(self):
        self.sound.stop_bgm()
        self.sound.play("powerup")
        self.completed_stages.add(self.current_stage_id)

        reward = STAGE_META[self.current_stage_id]["reward"]
        self.last_reward_msg = ""
        if reward and reward not in self.unlocked_upgrades:
            self.unlocked_upgrades.append(reward)
<<<<<<< HEAD
            self.equipped_upgrade = reward
=======
>>>>>>> da45a41 (Novo commit fresco)
            self.last_reward_msg = f"NOVO UPGRADE DESBLOQUEADO: {UPGRADE_NAMES[reward]}!"

        self.save_game()

        if self.current_stage_id == "final":
            self.cutscene_idx = 0
            self.state = "CUTSCENE_FINAL"
        else:
            self.state = "VICTORY_STAGE"

    def draw_hud(self):
<<<<<<< HEAD
        panel = pygame.Surface((380, 92), pygame.SRCALPHA)
        panel.fill((18, 12, 28, 200))
        pygame.draw.rect(panel, PALETTE["neon_cyan"], (0, 0, 380, 92), 2)
        self.screen.blit(panel, (12, 12))

        for i in range(self.player.max_hearts):
            hx = 24 + i * 38
            if i < self.player.hearts:
                self.screen.blit(self.sprites.ui_icons["heart"], (hx, 22))
            else:
                empty = self.sprites.ui_icons["heart"].copy()
                empty.fill((60, 60, 60, 140), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(empty, (hx, 22))

        pygame.draw.rect(self.screen, PALETTE["outline"], (24, 62, 180, 18))
        en_w = int(176 * (self.player.energy / self.player.max_energy))
        pygame.draw.rect(self.screen, PALETTE["neon_cyan"], (26, 64, en_w, 14))
        en_txt = self.font_sm.render(f"ENERGIA: {int(self.player.energy)}%", True, PALETTE["white"])
        self.screen.blit(en_txt, (32, 65))
=======
        self.screen.blit(self.hud_panel, (12, 12))

        heart_icon = self.sprites.ui_icons["heart"]
        for i in range(self.player.max_hearts):
            hx = 24 + i * 38
            self.screen.blit(heart_icon if i < self.player.hearts else self.empty_heart, (hx, 22))

        en_int = max(0, min(100, int(self.player.energy)))
        pygame.draw.rect(self.screen, PALETTE["outline"], (24, 62, 180, 18))
        en_w = int(176 * (en_int / 100.0))
        pygame.draw.rect(self.screen, PALETTE["neon_cyan"], (26, 64, en_w, 14))
        self.screen.blit(self.energy_labels[en_int], (32, 65))
>>>>>>> da45a41 (Novo commit fresco)

        slot_rect = pygame.Rect(220, 20, 48, 48)
        pygame.draw.rect(self.screen, (32, 24, 52), slot_rect)
        pygame.draw.rect(self.screen, PALETTE["neon_pink"], slot_rect, 2)
        if self.equipped_upgrade:
<<<<<<< HEAD
            icon = self.sprites.ui_icons[self.equipped_upgrade]
            self.screen.blit(icon, (slot_rect.x + 3, slot_rect.y + 3))
            up_label = self.font_sm.render(UPGRADE_NAMES[self.equipped_upgrade].split("(")[0].strip(), True, PALETTE["neon_yellow"])
            swap_label = self.font_sm.render("[Q/E] Trocar  [X] Usar", True, PALETTE["white"])
            self.screen.blit(up_label, (274, 24))
            self.screen.blit(swap_label, (274, 46))
        else:
            no_up = self.font_sm.render("Sem Upgrade", True, (160, 150, 175))
            self.screen.blit(no_up, (274, 34))
=======
            self.screen.blit(self.sprites.ui_icons[self.equipped_upgrade], (223, 23))
            self.screen.blit(self.up_labels[self.equipped_upgrade], (274, 24))
            self.screen.blit(self.txt_swap_hint, (274, 46))
        else:
            self.screen.blit(self.txt_equip_hint if self.unlocked_upgrades else self.txt_no_upgrade, (274, 34))
>>>>>>> da45a41 (Novo commit fresco)

        if self.boss_locked and self.boss and self.boss.hp > 0:
            bw = 460
            bx = (SCREEN_WIDTH - bw) // 2
            pygame.draw.rect(self.screen, (20, 12, 28), (bx - 4, SCREEN_HEIGHT - 44, bw + 8, 26))
            pygame.draw.rect(self.screen, PALETTE["red"], (bx, SCREEN_HEIGHT - 40, int(bw * (self.boss.hp / self.boss.max_hp)), 18))
            pygame.draw.rect(self.screen, PALETTE["white"], (bx - 4, SCREEN_HEIGHT - 44, bw + 8, 26), 2)
<<<<<<< HEAD
            bname = "GATO PELADO (SEM EXOESQUELETO!)" if self.boss.boss_id == "final_cat" else STAGE_META[self.current_stage_id]["boss_name"]
            bt = self.font_sm.render(bname, True, PALETTE["white"])
            self.screen.blit(bt, (bx + 10, SCREEN_HEIGHT - 38))
=======

            if self._cached_boss_id != self.boss.boss_id:
                self._cached_boss_id = self.boss.boss_id
                bname = (
                    "GATO PELADO (SEM EXOESQUELETO!)"
                    if self.boss.boss_id == "final_cat"
                    else STAGE_META[self.current_stage_id]["boss_name"]
                )
                self._cached_boss_label = self.font_sm.render(bname, True, PALETTE["white"])
            self.screen.blit(self._cached_boss_label, (bx + 10, SCREEN_HEIGHT - 38))

    def _check_boss_defeat(self):
        if self.boss and self.boss.hp <= 0:
            if self.boss.boss_id == "final_mech" and not self.boss.phase2_triggered:
                self.sound.play("explosion")
                self.boss.transform_to_naked_cat()
                return False
            else:
                self.handle_stage_victory()
                return True
        return False
>>>>>>> da45a41 (Novo commit fresco)

    def update_and_draw_stage(self):
        meta = STAGE_META[self.current_stage_id]
        level_len = meta["length"]

        if not self.boss_locked and self.player.rect.centerx >= level_len - SCREEN_WIDTH + 240:
            self.boss_locked = True
            self.cam_x = level_len - SCREEN_WIDTH

        if not self.boss_locked:
            target_cam = max(0, min(level_len - SCREEN_WIDTH, self.player.rect.centerx - SCREEN_WIDTH // 3))
<<<<<<< HEAD
            self.cam_x = max(self.cam_x, target_cam)
=======
            if target_cam > self.cam_x:
                self.cam_x = target_cam
>>>>>>> da45a41 (Novo commit fresco)

        lock_bounds = (self.cam_x, self.cam_x + SCREEN_WIDTH) if self.boss_locked else (self.cam_x, level_len)
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.platforms, level_len, lock_bounds)

<<<<<<< HEAD
=======
        if self.boss_locked and self._check_boss_defeat():
            return

>>>>>>> da45a41 (Novo commit fresco)
        for e in self.enemies:
            if e.hp > 0:
                e.update(self.player, self.platforms, self.enemy_projectiles, self.sprites)
                if e.rect.colliderect(self.player.rect):
                    self.player.take_damage(self.sound)

        if self.boss_locked and self.boss and self.boss.hp > 0:
            self.boss.update(self.player, self.cam_x, self.cam_x + SCREEN_WIDTH, self.enemy_projectiles)
            if self.boss.rect.colliderect(self.player.rect):
                self.player.take_damage(self.sound)

        for p in self.projectiles[:]:
            p.update(self.enemies, self.boss if self.boss_locked else None)
<<<<<<< HEAD
            if p.life <= 0 or p.x < self.cam_x - 60 or p.x > self.cam_x + SCREEN_WIDTH + 60 or p.y < -50:
                self.projectiles.remove(p)
                continue

            hit_done = False
            for e in self.enemies:
                if e.hp > 0 and p.rect.colliderect(e.rect):
=======

            if (
                p.rect.bottom >= GROUND_Y
                or p.life <= 0
                or p.x < self.cam_x - 60
                or p.x > self.cam_x + SCREEN_WIDTH + 60
                or p.y < -50
            ):
                self.projectiles.remove(p)
                continue

            remove_proj = False
            for e in self.enemies:
                if e.hp > 0 and p.can_hit(e) and p.rect.colliderect(e.rect):
                    p.register_hit(e)
>>>>>>> da45a41 (Novo commit fresco)
                    e.hp -= p.damage
                    e.hit_flash = 6
                    if e.hp <= 0:
                        self.player.energy = min(self.player.max_energy, self.player.energy + 12)
                        self.sound.play("explosion")
                    if p.kind != "big":
<<<<<<< HEAD
                        hit_done = True
                        break
            if hit_done and p in self.projectiles:
                self.projectiles.remove(p)
                continue

            if self.boss_locked and self.boss and self.boss.hp > 0 and p.rect.colliderect(self.boss.rect):
                self.boss.hp -= p.damage
                self.boss.hit_flash = 6
                self.player.energy = min(self.player.max_energy, self.player.energy + 4)
                if p.kind != "big" and p in self.projectiles:
                    self.projectiles.remove(p)

                if self.boss.hp <= 0:
                    if self.boss.boss_id == "final_mech" and not self.boss.phase2_triggered:
                        self.sound.play("explosion")
                        self.boss.transform_to_naked_cat()
                    else:
                        self.handle_stage_victory()
                        return

        for ep in self.enemy_projectiles[:]:
            ep.update([], None)
            if ep.life <= 0 or ep.x < self.cam_x - 50 or ep.x > self.cam_x + SCREEN_WIDTH + 50:
=======
                        remove_proj = True
                        break
                    elif len(p.distinct_hits) >= 2:
                        remove_proj = True
                        break

            if remove_proj:
                if p in self.projectiles:
                    self.projectiles.remove(p)
                continue

            if (
                self.boss_locked
                and self.boss
                and self.boss.hp > 0
                and p.can_hit(self.boss)
                and p.rect.colliderect(self.boss.rect)
            ):
                p.register_hit(self.boss)
                self.boss.hp -= p.damage
                self.boss.hit_flash = 6
                self.player.energy = min(self.player.max_energy, self.player.energy + 4)

                # Para o big_shot: desaparece apenas se já atingiu >= 2 alvos distintos;
                # caso contrário, atravessa o boss com intervalo de 0.2s entre hits.
                if p.kind != "big" or len(p.distinct_hits) >= 2:
                    if p in self.projectiles:
                        self.projectiles.remove(p)

                if self._check_boss_defeat():
                    return

        for ep in self.enemy_projectiles[:]:
            ep.update([], None)
            if (
                ep.life <= 0
                or ep.x < self.cam_x - 50
                or ep.x > self.cam_x + SCREEN_WIDTH + 50
                or ep.rect.bottom >= GROUND_Y
            ):
>>>>>>> da45a41 (Novo commit fresco)
                self.enemy_projectiles.remove(ep)
                continue
            if ep.rect.colliderect(self.player.rect):
                self.player.take_damage(self.sound)
                self.enemy_projectiles.remove(ep)

        if self.player.dead:
            self.sound.stop_bgm()
            self.state = "GAMEOVER"
            return

        bg = self.sprites.get_themed_bg(meta["theme"])
        parallax_x = int(self.cam_x * 0.35) % SCREEN_WIDTH
        self.screen.blit(bg, (-parallax_x, 0))
        self.screen.blit(bg, (SCREEN_WIDTH - parallax_x, 0))

        ground_off = int(self.cam_x) % SCREEN_WIDTH
        self.screen.blit(self.sprites.ground_tile, (-ground_off, GROUND_Y))
        self.screen.blit(self.sprites.ground_tile, (SCREEN_WIDTH - ground_off, GROUND_Y))

<<<<<<< HEAD
        for plat in self.platforms:
            plat.draw(self.screen, self.cam_x)

        for e in self.enemies:
            if e.hp > 0:
=======
        view_left = self.cam_x - 120
        view_right = self.cam_x + SCREEN_WIDTH + 120

        for plat in self.platforms:
            if plat.rect.right >= view_left and plat.rect.left <= view_right:
                plat.draw(self.screen, self.cam_x)

        for e in self.enemies:
            if e.hp > 0 and e.rect.right >= view_left and e.rect.left <= view_right:
>>>>>>> da45a41 (Novo commit fresco)
                e.draw(self.screen, self.cam_x)

        if self.boss and self.boss.hp > 0:
            self.boss.draw(self.screen, self.cam_x)

        for p in self.projectiles:
            p.draw(self.screen, self.cam_x)
        for ep in self.enemy_projectiles:
            ep.draw(self.screen, self.cam_x)

        self.player.draw(self.screen, self.cam_x)
        self.draw_hud()

        if self.current_stage_id == "tutorial" and self.cam_x < 450:
<<<<<<< HEAD
            tip = self.font_sm.render("Mover: A/D ou Setas | Pular: ESPACO | Mirar Cima: W/Cima | Atirar: Z/J", True, PALETTE["neon_yellow"])
            self.screen.blit(tip, (24, 114))
=======
            self.screen.blit(self.txt_tutorial_tip, (24, 114))
>>>>>>> da45a41 (Novo commit fresco)

    def draw_menu(self):
        self.screen.blit(self.sprites.bg_base, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 10, 25, 165))
        self.screen.blit(overlay, (0, 0))

        pygame.draw.rect(self.screen, PALETTE["neon_pink"], (SCREEN_WIDTH // 2 - 220, 75, 440, 95), border_radius=18)
        pygame.draw.rect(self.screen, (25, 16, 40), (SCREEN_WIDTH // 2 - 214, 81, 428, 83), border_radius=14)
        title = self.font_title.render("MILKY WAY", True, PALETTE["neon_cyan"])
        sub = self.font_md.render("A Revolução Felina de Pur", True, PALETTE["pur_cream"])
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 95))
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 140))

        pur_big = pygame.transform.scale(self.sprites.player_anims["idle"][0], (120, 140))
        self.screen.blit(pur_big, (SCREEN_WIDTH // 2 - 60, 200))

        btn1 = self.font_lg.render("[ENTER] Novo Jogo (Iniciar no Tutorial)", True, PALETTE["neon_yellow"])
        self.screen.blit(btn1, (SCREEN_WIDTH // 2 - btn1.get_width() // 2, 380))

        if os.path.exists(SAVE_FILE):
            btn2 = self.font_md.render("[C] Continuar Jogo Salvo", True, PALETTE["neon_green"])
            self.screen.blit(btn2, (SCREEN_WIDTH // 2 - btn2.get_width() // 2, 425))

<<<<<<< HEAD
        cred = self.font_sm.render("Grupo Solos | Danilo Simonelli Bastos & Miranda Soares", True, (200, 190, 215))
        self.screen.blit(cred, (SCREEN_WIDTH // 2 - cred.get_width() // 2, 495))

    def draw_cutscene(self, slides):
        self.screen.fill((18, 12, 28))
        pygame.draw.rect(self.screen, PALETTE["neon_pink"], (60, 60, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120), 3)
        pur_img = pygame.transform.scale(self.sprites.player_anims["idle"][0], (108, 126))
        self.screen.blit(pur_img, (SCREEN_WIDTH // 2 - 54, 110))

        text = slides[self.cutscene_idx]
        rendered = self.font_md.render(text, True, PALETTE["white"])
        self.screen.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, 290))

        hint = self.font_sm.render("Pressione [ENTER] para continuar...", True, PALETTE["neon_cyan"])
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 420))
=======
        cred = self.font_sm.render("Grupo Solos | Danilo Simonelli Bastos & João Pedro Ferreira Monteiro", True, (200, 190, 215))
        self.screen.blit(cred, (SCREEN_WIDTH // 2 - cred.get_width() // 2, 495))

    def _draw_wrapped_text(self, text, font, color, center_x, start_y, max_width, line_spacing=8):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        y = start_y
        for line in lines:
            rendered = font.render(line, True, color)
            self.screen.blit(rendered, (center_x - rendered.get_width() // 2, y))
            y += font.get_height() + line_spacing

    def draw_cutscene(self, slides):
        self.screen.fill((18, 12, 28))
        box_margin = 60
        box_rect = pygame.Rect(box_margin, box_margin, SCREEN_WIDTH - box_margin * 2, SCREEN_HEIGHT - box_margin * 2)
        pygame.draw.rect(self.screen, PALETTE["neon_pink"], box_rect, 3)

        pur_img = pygame.transform.scale(self.sprites.player_anims["idle"][0], (108, 126))
        self.screen.blit(pur_img, (SCREEN_WIDTH // 2 - 54, 105))

        text = slides[self.cutscene_idx]
        max_text_width = box_rect.width - 64
        self._draw_wrapped_text(text, self.font_md, PALETTE["white"], SCREEN_WIDTH // 2, 275, max_text_width)

        hint = self.font_sm.render("Pressione [ENTER] para continuar...", True, PALETTE["neon_cyan"])
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 425))
>>>>>>> da45a41 (Novo commit fresco)

    def draw_map_hub(self):
        self.screen.fill((18, 14, 28))
        header = self.font_lg.render("MAPA DA CIDADE - ESCOLHA A PRÓXIMA REGIÃO", True, PALETTE["neon_cyan"])
        self.screen.blit(header, (SCREEN_WIDTH // 2 - header.get_width() // 2, 22))

        cx, cy = 320, 285
        pygame.draw.circle(self.screen, (36, 26, 54), (cx, cy), 195)
        pygame.draw.circle(self.screen, PALETTE["white"], (cx, cy), 195, 3)

        pygame.draw.line(self.screen, PALETTE["white"], (cx, cy - 195), (cx, cy - 45), 2)
        pygame.draw.line(self.screen, PALETTE["white"], (cx - 45, cy + 35), (cx - 165, cy + 105), 2)
        pygame.draw.line(self.screen, PALETTE["white"], (cx + 45, cy + 35), (cx + 165, cy + 105), 2)
        pygame.draw.rect(self.screen, (52, 40, 75), (cx - 52, cy - 42, 104, 78))
        pygame.draw.rect(self.screen, PALETTE["neon_green"], (cx - 52, cy - 42, 104, 78), 2)

        t_lbl = self.font_sm.render("CENTRO (OK)", True, PALETTE["neon_green"])
        self.screen.blit(t_lbl, (cx - t_lbl.get_width() // 2, cy - 8))

        nodes = {
            "noroeste": (cx - 105, cy - 55, "1. NOROESTE", "Construção"),
            "nordeste": (cx + 105, cy - 55, "2. NORDESTE", "Balada Neon"),
            "sul": (cx, cy + 125, "3. SUL", "Biblioteca"),
        }

        for key, (nx, ny, title_txt, sub_txt) in nodes.items():
            done = key in self.completed_stages
            selected = (self.map_selected == key)
            col = PALETTE["neon_green"] if done else (PALETTE["neon_yellow"] if selected else PALETTE["neon_pink"])
            pygame.draw.circle(self.screen, col, (nx, ny), 16 if selected else 11)
            t1 = self.font_sm.render(title_txt + (" [LIBERTADO]" if done else ""), True, col)
            t2 = self.font_sm.render(sub_txt, True, PALETTE["white"])
            self.screen.blit(t1, (nx - t1.get_width() // 2, ny + 18))
            self.screen.blit(t2, (nx - t2.get_width() // 2, ny + 34))

        panel = pygame.Rect(560, 85, 365, 395)
        pygame.draw.rect(self.screen, (28, 20, 44), panel)
        pygame.draw.rect(self.screen, PALETTE["neon_pink"], panel, 2)

        sel_meta = STAGE_META[self.map_selected]
        self.screen.blit(self.font_md.render(sel_meta["name"], True, PALETTE["neon_yellow"]), (575, 102))
        self.screen.blit(self.font_sm.render(f"Chefe: {sel_meta['boss_name']}", True, PALETTE["neon_cyan"]), (575, 134))
        self.screen.blit(self.font_sm.render(sel_meta["desc"], True, PALETTE["white"]), (575, 160))

        rew = sel_meta["reward"]
        rew_txt = UPGRADE_NAMES[rew] if rew else "Nenhum"
        self.screen.blit(self.font_sm.render(f"Recompensa: {rew_txt}", True, PALETTE["neon_green"]), (575, 186))

        pygame.draw.line(self.screen, PALETTE["neon_cyan"], (575, 225), (905, 225), 2)
        self.screen.blit(self.font_md.render("INVENTÁRIO DE GADGETS", True, PALETTE["neon_cyan"]), (575, 238))
        if not self.unlocked_upgrades:
            self.screen.blit(self.font_sm.render("Derrote chefes para obter upgrades!", True, (180, 170, 195)), (575, 270))
        else:
            for idx, up in enumerate(self.unlocked_upgrades):
                eq = (up == self.equipped_upgrade)
                c = PALETTE["neon_yellow"] if eq else PALETTE["white"]
                prefix = "[EQUIPADO] " if eq else "           "
                self.screen.blit(self.font_sm.render(prefix + UPGRADE_NAMES[up], True, c), (575, 270 + idx * 28))

        controls = [
            "[1 / 2 / 3 ou Setas] Selecionar Bairro",
            "[Q / E] Trocar Upgrade Equipado",
            "[ENTER] Entrar na Fase Selecionada",
        ]
        for i, line in enumerate(controls):
            self.screen.blit(self.font_sm.render(line, True, PALETTE["pur_cream"]), (575, 385 + i * 24))

    def draw_overlay_screen(self, title_txt, title_col, sub_txt, options_txt):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((12, 8, 22, 215))
        self.screen.blit(overlay, (0, 0))

        t1 = self.font_title.render(title_txt, True, title_col)
        t2 = self.font_md.render(sub_txt, True, PALETTE["white"])
        t3 = self.font_lg.render(options_txt, True, PALETTE["neon_yellow"])
        self.screen.blit(t1, (SCREEN_WIDTH // 2 - t1.get_width() // 2, 150))
        self.screen.blit(t2, (SCREEN_WIDTH // 2 - t2.get_width() // 2, 230))
        self.screen.blit(t3, (SCREEN_WIDTH // 2 - t3.get_width() // 2, 320))

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if self.state == "MENU":
                        if event.key == pygame.K_RETURN:
                            self.completed_stages.clear()
                            self.unlocked_upgrades.clear()
                            self.equipped_upgrade = None
                            self.cutscene_idx = 0
                            self.state = "CUTSCENE_INTRO"
                        elif event.key == pygame.K_c and self.load_game():
                            if "tutorial" not in self.completed_stages:
                                self.start_stage("tutorial")
                            elif {"noroeste", "nordeste", "sul"}.issubset(self.completed_stages) and "final" not in self.completed_stages:
                                self.start_stage("final")
                            else:
                                self.state = "MAP"

                    elif self.state == "CUTSCENE_INTRO":
                        if event.key == pygame.K_RETURN:
                            self.cutscene_idx += 1
                            if self.cutscene_idx >= len(self.intro_slides):
                                self.start_stage("tutorial")

                    elif self.state == "CUTSCENE_FINAL":
                        if event.key == pygame.K_RETURN:
                            self.cutscene_idx += 1
                            if self.cutscene_idx >= len(self.final_slides):
                                self.state = "MENU"

                    elif self.state == "STAGE":
                        if event.key == pygame.K_SPACE:
                            self.player.jump(self.sound)
                        elif event.key in (pygame.K_z, pygame.K_j):
<<<<<<< HEAD
                            self.player.shoot_normal(self.projectiles, self.sound)
=======
                            self.player.attack_or_shoot(
                                self.projectiles,
                                self.enemies,
                                self.boss if self.boss_locked else None,
                                self.sound,
                            )
>>>>>>> da45a41 (Novo commit fresco)
                        elif event.key in (pygame.K_x, pygame.K_k):
                            self.player.use_upgrade(
                                self.equipped_upgrade,
                                self.projectiles,
                                self.enemies,
                                self.boss if self.boss_locked else None,
                                self.sound,
                            )
                        elif event.key in (pygame.K_q, pygame.K_TAB):
                            self.cycle_upgrade(-1)
                        elif event.key == pygame.K_e:
                            self.cycle_upgrade(1)

                    elif self.state == "MAP":
                        if event.key == pygame.K_1 or event.key == pygame.K_LEFT:
                            self.map_selected = "noroeste"
                        elif event.key == pygame.K_2 or event.key == pygame.K_RIGHT:
                            self.map_selected = "nordeste"
                        elif event.key == pygame.K_3 or event.key == pygame.K_DOWN:
                            self.map_selected = "sul"
                        elif event.key in (pygame.K_q, pygame.K_TAB):
                            self.cycle_upgrade(-1)
                        elif event.key == pygame.K_e:
                            self.cycle_upgrade(1)
                        elif event.key == pygame.K_RETURN:
                            self.start_stage(self.map_selected)

                    elif self.state == "VICTORY_STAGE":
                        if event.key == pygame.K_RETURN:
                            if {"noroeste", "nordeste", "sul"}.issubset(self.completed_stages) and "final" not in self.completed_stages:
                                self.start_stage("final")
                            else:
                                self.state = "MAP"

                    elif self.state == "GAMEOVER":
                        if event.key == pygame.K_r:
                            self.start_stage(self.current_stage_id)
                        elif event.key == pygame.K_m and "tutorial" in self.completed_stages:
                            self.state = "MAP"

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "CUTSCENE_INTRO":
                self.draw_cutscene(self.intro_slides)
            elif self.state == "CUTSCENE_FINAL":
                self.draw_cutscene(self.final_slides)
            elif self.state == "STAGE":
                self.update_and_draw_stage()
            elif self.state == "MAP":
                self.draw_map_hub()
            elif self.state == "VICTORY_STAGE":
                all_three = {"noroeste", "nordeste", "sul"}.issubset(self.completed_stages)
                next_msg = "[ENTER] Enfrentar o GRANDE LÍDER (Fase Final!)" if all_three else "[ENTER] Ir para o Mapa da Cidade"
                sub = self.last_reward_msg if self.last_reward_msg else f"Região '{STAGE_META[self.current_stage_id]['name']}' libertada!"
                self.draw_overlay_screen("REGIÃO LIBERTADA!", PALETTE["neon_green"], sub, next_msg)
            elif self.state == "GAMEOVER":
                opts = "[R] Reiniciar Fase" + ("   |   [M] Voltar ao Mapa" if "tutorial" in self.completed_stages else "")
                self.draw_overlay_screen("PUR FOI DERROTADA!", PALETTE["red"], "A Gangue dos Dogs ainda domina esta área...", opts)

            pygame.display.flip()

        pygame.quit()
        sys.exit()