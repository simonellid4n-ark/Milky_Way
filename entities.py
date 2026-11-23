import math
import random
import pygame
<<<<<<< HEAD
from settings import GRAVITY, GROUND_Y, PALETTE


class Projectile:
    def __init__(self, x, y, vx, vy, damage, owner="player", kind="normal", sprite=None, target=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.damage = damage
        self.owner = owner
        self.kind = kind
        self.sprite = sprite
        self.target = target
        self.life = 180
        w = sprite.get_width() if sprite else 18
        h = sprite.get_height() if sprite else 12
        self.rect = pygame.Rect(int(x - w // 2), int(y - h // 2), w, h)

    def update(self, enemies, boss):
        self.life -= 1
        if self.kind == "missile":
            candidates = [e for e in enemies if e.hp > 0]
            if boss and boss.hp > 0:
                candidates.append(boss)
            if candidates:
                self.target = min(
                    candidates,
                    key=lambda c: math.hypot(c.rect.centerx - self.x, c.rect.centery - self.y),
                )
            if self.target and self.target.hp > 0:
                dx = self.target.rect.centerx - self.x
                dy = self.target.rect.centery - self.y
                ang = math.atan2(dy, dx)
                speed = 9.0
                self.vx = self.vx * 0.85 + math.cos(ang) * speed * 0.15
                self.vy = self.vy * 0.85 + math.sin(ang) * speed * 0.15
=======
from settings import GRAVITY, GROUND_Y, PALETTE, FPS


class Projectile:
    BIG_HIT_INTERVAL_FRAMES = max(1, int(0.2 * FPS))  # 0.2 segundos (12 frames a 60 FPS)

    def __init__(self, x, y, vx, vy, damage, owner="player", kind="normal", sprite=None, target=None):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.damage = damage
        self.owner = owner
        self.kind = kind
        self.target = target
        self.life = 180

        # Controle leve de dano por intervalo (0.2s) e contagem de alvos atingidos
        self.hit_timers = {}      # {id(alvo): frames_restantes_para_proximo_hit}
        self.distinct_hits = set()  # IDs dos alvos distintos já atingidos

        # Pré-rotaciona/espelha o sprite UMA ÚNICA VEZ na criação (evita transform a cada frame)
        self.sprite = self._prepare_sprite(sprite)
        w = self.sprite.get_width() if self.sprite else 18
        h = self.sprite.get_height() if self.sprite else 12
        self.rect = pygame.Rect(int(self.x - w // 2), int(self.y - h // 2), w, h)

    def _prepare_sprite(self, sprite):
        if not sprite:
            return None
        if self.vx < 0 and self.kind in ("normal", "big"):
            return pygame.transform.flip(sprite, True, False)
        if self.vy < -2 and abs(self.vx) < 1:
            return pygame.transform.rotate(sprite, 90)
        if self.vy > 2 and abs(self.vx) < 1:
            return pygame.transform.rotate(sprite, -90)
        return sprite

    def can_hit(self, target_obj):
        tid = id(target_obj)
        return self.hit_timers.get(tid, 0) <= 0

    def register_hit(self, target_obj):
        tid = id(target_obj)
        self.distinct_hits.add(tid)
        self.hit_timers[tid] = self.BIG_HIT_INTERVAL_FRAMES

    def update(self, enemies, boss):
        self.life -= 1

        # Decrementa timers de cooldown de hit de forma enxuta
        if self.hit_timers:
            expired = []
            for tid, t in self.hit_timers.items():
                if t <= 1:
                    expired.append(tid)
                else:
                    self.hit_timers[tid] = t - 1
            for tid in expired:
                del self.hit_timers[tid]

        if self.kind == "missile":
            best_target = None
            best_dist = float("inf")
            for e in enemies:
                if e.hp > 0:
                    d = (e.rect.centerx - self.x) ** 2 + (e.rect.centery - self.y) ** 2
                    if d < best_dist:
                        best_dist = d
                        best_target = e
            if boss and boss.hp > 0:
                d = (boss.rect.centerx - self.x) ** 2 + (boss.rect.centery - self.y) ** 2
                if d < best_dist:
                    best_target = boss

            if best_target is not None:
                dx = best_target.rect.centerx - self.x
                dy = best_target.rect.centery - self.y
                ang = math.atan2(dy, dx)
                self.vx = self.vx * 0.85 + math.cos(ang) * 1.35
                self.vy = self.vy * 0.85 + math.sin(ang) * 1.35
>>>>>>> da45a41 (Novo commit fresco)

        self.x += self.vx
        self.y += self.vy
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surf, cam_x):
        if self.sprite:
<<<<<<< HEAD
            img = self.sprite
            if self.vx < 0 and self.kind in ("normal", "big"):
                img = pygame.transform.flip(img, True, False)
            elif self.vy < -2 and abs(self.vx) < 1:
                img = pygame.transform.rotate(img, 90)
            surf.blit(img, (self.rect.x - cam_x, self.rect.y))
=======
            surf.blit(self.sprite, (self.rect.x - cam_x, self.rect.y))
>>>>>>> da45a41 (Novo commit fresco)


class Platform:
    def __init__(self, x, y, w, h=18):
        self.rect = pygame.Rect(x, y, w, h)
<<<<<<< HEAD

    def draw(self, surf, cam_x):
        r = pygame.Rect(self.rect.x - cam_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(surf, PALETTE["ground_dark"], r)
        pygame.draw.rect(surf, PALETTE["neon_cyan"], (r.x, r.y, r.width, 4))
        pygame.draw.rect(surf, PALETTE["outline"], r, 2)
=======
        # Pré-renderiza a plataforma em uma Surface única para evitar 3 draw.rect por plataforma/frame
        self.surface = pygame.Surface((w, h))
        self.surface.fill(PALETTE["ground_dark"])
        pygame.draw.rect(self.surface, PALETTE["neon_cyan"], (0, 0, w, 4))
        pygame.draw.rect(self.surface, PALETTE["outline"], (0, 0, w, h), 2)

    def draw(self, surf, cam_x):
        surf.blit(self.surface, (self.rect.x - cam_x, self.rect.y))
>>>>>>> da45a41 (Novo commit fresco)


class Enemy:
    def __init__(self, x, y, enemy_type, theme, sprites, diff_mult=1.0):
        self.enemy_type = enemy_type
<<<<<<< HEAD
        self.sprites = sprites
=======
        self.sprites_left = sprites
        self.sprites_right = [pygame.transform.flip(s, True, False) for s in sprites]
>>>>>>> da45a41 (Novo commit fresco)
        self.anim_idx = 0
        self.anim_timer = 0
        self.facing_right = False
        self.start_x = x
        self.start_y = y
<<<<<<< HEAD
=======
        self.wave_phase = random.uniform(0, math.tau)
>>>>>>> da45a41 (Novo commit fresco)
        self.shoot_cd = random.randint(50, 120)

        w, h = sprites[0].get_width(), sprites[0].get_height()
        self.rect = pygame.Rect(x, y - h, w, h)
<<<<<<< HEAD
        self.vy = 0
=======
        self.vy = 0.0
>>>>>>> da45a41 (Novo commit fresco)

        if enemy_type == "boxer":
            self.max_hp = int(30 * diff_mult)
            self.speed = 2.1 * diff_mult
        elif enemy_type == "agent":
            self.max_hp = int(25 * diff_mult)
            self.speed = 0.8
        elif enemy_type == "trash":
            self.max_hp = int(35 * diff_mult)
            self.speed = 0.0
        elif enemy_type == "drone":
            self.max_hp = int(22 * diff_mult)
            self.speed = 2.4 * diff_mult
            self.rect.y = y - 140

        self.hp = self.max_hp
        self.hit_flash = 0

    def update(self, player, platforms, enemy_projectiles, sprite_bank):
        if self.hit_flash > 0:
            self.hit_flash -= 1

        dist = player.rect.centerx - self.rect.centerx
<<<<<<< HEAD
        if abs(dist) > 780:
=======
        if dist > 780 or dist < -780:
>>>>>>> da45a41 (Novo commit fresco)
            return

        self.facing_right = dist > 0
        self.anim_timer += 1
        if self.anim_timer >= 14:
            self.anim_timer = 0
<<<<<<< HEAD
            self.anim_idx = (self.anim_idx + 1) % len(self.sprites)

        if self.enemy_type == "boxer":
            self.rect.x += self.speed if self.facing_right else -self.speed
=======
            self.anim_idx = 1 - self.anim_idx

        if self.enemy_type == "boxer":
            self.rect.x += int(self.speed if self.facing_right else -self.speed)
>>>>>>> da45a41 (Novo commit fresco)
            self.vy += GRAVITY
            self.rect.y += int(self.vy)
            if self.rect.bottom >= GROUND_Y:
                self.rect.bottom = GROUND_Y
<<<<<<< HEAD
                self.vy = 0
            for p in platforms:
                if self.vy >= 0 and self.rect.colliderect(p.rect) and self.rect.bottom - self.vy <= p.rect.top + 8:
                    self.rect.bottom = p.rect.top
                    self.vy = 0

        elif self.enemy_type == "agent":
            self.shoot_cd -= 1
            if self.shoot_cd <= 0 and abs(dist) < 580:
=======
                self.vy = 0.0
            for p in platforms:
                if self.vy >= 0 and self.rect.colliderect(p.rect) and self.rect.bottom - self.vy <= p.rect.top + 8:
                    self.rect.bottom = p.rect.top
                    self.vy = 0.0

        elif self.enemy_type == "agent":
            self.shoot_cd -= 1
            if self.shoot_cd <= 0 and -580 < dist < 580:
>>>>>>> da45a41 (Novo commit fresco)
                self.shoot_cd = 115
                vx = 5.5 if self.facing_right else -5.5
                enemy_projectiles.append(
                    Projectile(self.rect.centerx, self.rect.centery - 4, vx, 0, 1, "enemy", "enemy", sprite_bank.projectiles["enemy"])
                )

        elif self.enemy_type == "trash":
<<<<<<< HEAD
            if abs(dist) < 280:
=======
            if -280 < dist < 280:
>>>>>>> da45a41 (Novo commit fresco)
                self.anim_idx = 1
                self.shoot_cd -= 1
                if self.shoot_cd <= 0:
                    self.shoot_cd = 95
                    vx = 4.5 if self.facing_right else -4.5
                    enemy_projectiles.append(
                        Projectile(self.rect.centerx, self.rect.top + 8, vx, -2.5, 1, "enemy", "enemy", sprite_bank.projectiles["enemy"])
                    )
            else:
                self.anim_idx = 0

        elif self.enemy_type == "drone":
<<<<<<< HEAD
            self.rect.x += self.speed if self.facing_right else -self.speed
            self.rect.y = (self.start_y - 140) + int(math.sin(pygame.time.get_ticks() * 0.005 + self.start_x) * 28)
            self.shoot_cd -= 1
            if self.shoot_cd <= 0 and abs(dist) < 420:
=======
            self.rect.x += int(self.speed if self.facing_right else -self.speed)
            self.wave_phase += 0.08
            self.rect.y = (self.start_y - 140) + int(math.sin(self.wave_phase) * 28)
            self.shoot_cd -= 1
            if self.shoot_cd <= 0 and -420 < dist < 420:
>>>>>>> da45a41 (Novo commit fresco)
                self.shoot_cd = 130
                enemy_projectiles.append(
                    Projectile(self.rect.centerx, self.rect.bottom, 0, 5.0, 1, "enemy", "enemy", sprite_bank.projectiles["enemy"])
                )

    def draw(self, surf, cam_x):
<<<<<<< HEAD
        img = self.sprites[self.anim_idx]
        if self.facing_right:
            img = pygame.transform.flip(img, True, False)
        surf.blit(img, (self.rect.x - cam_x, self.rect.y))
        if self.hit_flash > 0:
            flash = img.copy()
            flash.fill((255, 255, 255, 140), special_flags=pygame.BLEND_RGBA_ADD)
            surf.blit(flash, (self.rect.x - cam_x, self.rect.y))
=======
        # Pisca alternando visibilidade nos frames pares em vez de copiar Surface (zero alocação!)
        if self.hit_flash > 0 and (self.hit_flash & 1):
            return
        img = self.sprites_right[self.anim_idx] if self.facing_right else self.sprites_left[self.anim_idx]
        surf.blit(img, (self.rect.x - cam_x, self.rect.y))
>>>>>>> da45a41 (Novo commit fresco)


class Boss:
    def __init__(self, x, boss_id, sprite_bank, diff_mult=1.0):
        self.boss_id = boss_id
        self.sprite_bank = sprite_bank
        self.diff_mult = diff_mult
<<<<<<< HEAD
        self.sprites = sprite_bank.get_boss_sprites(boss_id)
=======
        raw_sprites = sprite_bank.get_boss_sprites(boss_id)
        self.sprites_left = raw_sprites
        self.sprites_right = [pygame.transform.flip(s, True, False) for s in raw_sprites]
>>>>>>> da45a41 (Novo commit fresco)
        self.anim_idx = 0
        self.anim_timer = 0
        self.facing_right = False

<<<<<<< HEAD
        w, h = self.sprites[0].get_width(), self.sprites[0].get_height()
        self.rect = pygame.Rect(x, GROUND_Y - h, w, h)
        self.vy = 0
        self.vx = -2.2
=======
        w, h = raw_sprites[0].get_width(), raw_sprites[0].get_height()
        self.rect = pygame.Rect(x, GROUND_Y - h, w, h)
        self.vy = 0.0
        self.vx = -2.2
        self.wave_phase = 0.0
>>>>>>> da45a41 (Novo commit fresco)
        self.action_timer = 90
        self.hit_flash = 0
        self.phase2_triggered = False

        hp_table = {
            "tutorial": 160,
            "noroeste": int(260 * diff_mult),
            "nordeste": int(250 * diff_mult),
            "sul": int(240 * diff_mult),
            "final_mech": 340,
        }
        self.max_hp = hp_table.get(boss_id, 220)
        self.hp = self.max_hp

    def transform_to_naked_cat(self):
        self.boss_id = "final_cat"
        self.phase2_triggered = True
<<<<<<< HEAD
        self.sprites = self.sprite_bank.get_boss_sprites("final_cat")
        w, h = self.sprites[0].get_width(), self.sprites[0].get_height()
=======
        raw_sprites = self.sprite_bank.get_boss_sprites("final_cat")
        self.sprites_left = raw_sprites
        self.sprites_right = [pygame.transform.flip(s, True, False) for s in raw_sprites]
        w, h = raw_sprites[0].get_width(), raw_sprites[0].get_height()
>>>>>>> da45a41 (Novo commit fresco)
        cx, bottom = self.rect.centerx, self.rect.bottom
        self.rect = pygame.Rect(cx - w // 2, bottom - h, w, h)
        self.max_hp = 90
        self.hp = self.max_hp
        self.vx = -5.5

    def update(self, player, arena_left, arena_right, enemy_projectiles):
        if self.hit_flash > 0:
            self.hit_flash -= 1

        self.anim_timer += 1
        if self.anim_timer >= 12:
            self.anim_timer = 0
<<<<<<< HEAD
            self.anim_idx = (self.anim_idx + 1) % len(self.sprites)
=======
            self.anim_idx = 1 - self.anim_idx
>>>>>>> da45a41 (Novo commit fresco)

        self.facing_right = player.rect.centerx > self.rect.centerx
        self.action_timer -= 1

        if self.boss_id == "tutorial":
            self.rect.x += int(self.vx)
            if self.rect.left <= arena_left + 40 or self.rect.right >= arena_right - 30:
                self.vx *= -1
            if self.action_timer <= 0:
                self.action_timer = 85
                dir_x = 1 if self.facing_right else -1
                enemy_projectiles.append(
                    Projectile(self.rect.centerx, self.rect.centery, 6.0 * dir_x, 0, 1, "enemy", "enemy", self.sprite_bank.projectiles["enemy"])
                )

        elif self.boss_id == "noroeste":
            self.rect.x += int(self.vx * 1.3)
            if self.rect.left <= arena_left + 30 or self.rect.right >= arena_right - 30:
                self.vx *= -1
            self.vy += GRAVITY
            self.rect.y += int(self.vy)
            if self.rect.bottom >= GROUND_Y:
                self.rect.bottom = GROUND_Y
<<<<<<< HEAD
                self.vy = 0
=======
                self.vy = 0.0
>>>>>>> da45a41 (Novo commit fresco)
            if self.action_timer <= 0:
                self.action_timer = 95
                self.vy = -13.5
                for sx in (-5.5, 5.5):
                    enemy_projectiles.append(
                        Projectile(self.rect.centerx, GROUND_Y - 14, sx, 0, 1, "enemy", "enemy", self.sprite_bank.projectiles["enemy"])
                    )

        elif self.boss_id == "nordeste":
<<<<<<< HEAD
            self.rect.x += int(math.sin(pygame.time.get_ticks() * 0.003) * 3)
            self.rect.clamp_ip(pygame.Rect(arena_left + 30, 0, arena_right - arena_left - 60, GROUND_Y))
=======
            self.wave_phase += 0.05
            self.rect.x += int(math.sin(self.wave_phase) * 3)
            if self.rect.left < arena_left + 30:
                self.rect.left = arena_left + 30
            elif self.rect.right > arena_right - 30:
                self.rect.right = arena_right - 30
>>>>>>> da45a41 (Novo commit fresco)
            if self.action_timer <= 0:
                self.action_timer = 75
                dir_x = 1 if self.facing_right else -1
                for vy in (-2.5, 0, 2.5):
                    enemy_projectiles.append(
                        Projectile(self.rect.centerx, self.rect.centery - 10, 6.2 * dir_x, vy, 1, "enemy", "enemy", self.sprite_bank.projectiles["enemy"])
                    )

        elif self.boss_id == "sul":
            self.rect.x += int(self.vx * 0.9)
            if self.rect.left <= arena_left + 40 or self.rect.right >= arena_right - 40:
                self.vx *= -1
            if self.action_timer <= 0:
                self.action_timer = 70
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                ang = math.atan2(dy, dx)
                enemy_projectiles.append(
                    Projectile(self.rect.centerx, self.rect.top + 25, math.cos(ang) * 6.5, math.sin(ang) * 6.5, 1, "enemy", "enemy", self.sprite_bank.projectiles["enemy"])
                )

        elif self.boss_id == "final_mech":
            self.rect.x += int(self.vx)
            if self.rect.left <= arena_left + 20 or self.rect.right >= arena_right - 20:
                self.vx *= -1
            if self.action_timer <= 0:
                self.action_timer = 65
                dir_x = 1 if self.facing_right else -1
                for dy in (-25, 15):
                    enemy_projectiles.append(
                        Projectile(self.rect.centerx, self.rect.centery + dy, 7.0 * dir_x, 0, 1, "enemy", "enemy", self.sprite_bank.projectiles["enemy"])
                    )

        elif self.boss_id == "final_cat":
            self.rect.x += int(self.vx)
            if self.rect.left <= arena_left + 20 or self.rect.right >= arena_right - 20:
                self.vx *= -1
            self.vy += GRAVITY
            self.rect.y += int(self.vy)
            if self.rect.bottom >= GROUND_Y:
                self.rect.bottom = GROUND_Y
                self.vy = -11.5

    def draw(self, surf, cam_x):
<<<<<<< HEAD
        img = self.sprites[self.anim_idx]
        if self.facing_right:
            img = pygame.transform.flip(img, True, False)
        surf.blit(img, (self.rect.x - cam_x, self.rect.y))
        if self.hit_flash > 0:
            flash = img.copy()
            flash.fill((255, 255, 255, 140), special_flags=pygame.BLEND_RGBA_ADD)
            surf.blit(flash, (self.rect.x - cam_x, self.rect.y))


class Player:
=======
        if self.hit_flash > 0 and (self.hit_flash & 1):
            return
        img = self.sprites_right[self.anim_idx] if self.facing_right else self.sprites_left[self.anim_idx]
        surf.blit(img, (self.rect.x - cam_x, self.rect.y))


class Player:
    MELEE_RANGE = 50
    MELEE_DAMAGE = 26

>>>>>>> da45a41 (Novo commit fresco)
    def __init__(self, x, y, sprite_bank):
        self.sprite_bank = sprite_bank
        self.anims = sprite_bank.player_anims
        w = self.anims["idle"][0].get_width()
        h = self.anims["idle"][0].get_height()
        self.rect = pygame.Rect(x, y - h, w - 12, h)
        self.pos_y = float(self.rect.y)
        self.vx = 0
        self.vy = 0.0
        self.on_ground = False
        self.facing_right = True
        self.looking_up = False
<<<<<<< HEAD
        self.shoot_anim_timer = 0
=======
        self.looking_down = False
        self.shoot_anim_timer = 0
        self.melee_anim_timer = 0
>>>>>>> da45a41 (Novo commit fresco)
        self.anim_idx = 0
        self.anim_timer = 0

        self.max_hearts = 3
        self.hearts = 3
        self.max_energy = 100.0
        self.energy = 100.0
        self.invuln_timer = 0
        self.shoot_cd = 0
        self.dead = False
        self.explosion_fx_timer = 0
        self.explosion_radius = 150

    def reset_for_stage(self, x=100, y=GROUND_Y):
        self.rect.x = x
        self.rect.bottom = y
        self.pos_y = float(self.rect.y)
        self.vx = 0
        self.vy = 0.0
        self.hearts = self.max_hearts
        self.energy = self.max_energy
        self.invuln_timer = 0
        self.dead = False
        self.explosion_fx_timer = 0
<<<<<<< HEAD
=======
        self.melee_anim_timer = 0
        self.shoot_anim_timer = 0
>>>>>>> da45a41 (Novo commit fresco)

    def take_damage(self, sound):
        if self.invuln_timer > 0 or self.dead:
            return
        self.hearts -= 1
        self.invuln_timer = 75
        sound.play("hit")
        if self.hearts <= 0:
            self.hearts = 0
            self.dead = True

    def update(self, keys, platforms, level_width, camera_lock_bounds=None):
        if self.dead:
            return

        self.energy = min(self.max_energy, self.energy + 0.14)

        if self.invuln_timer > 0:
            self.invuln_timer -= 1
        if self.shoot_cd > 0:
            self.shoot_cd -= 1
        if self.shoot_anim_timer > 0:
            self.shoot_anim_timer -= 1
<<<<<<< HEAD
=======
        if self.melee_anim_timer > 0:
            self.melee_anim_timer -= 1
>>>>>>> da45a41 (Novo commit fresco)
        if self.explosion_fx_timer > 0:
            self.explosion_fx_timer -= 1

        move_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= 1
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += 1
            self.facing_right = True

        self.looking_up = bool(keys[pygame.K_UP] or keys[pygame.K_w])
<<<<<<< HEAD
=======
        self.looking_down = bool(keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.looking_up
>>>>>>> da45a41 (Novo commit fresco)

        self.vx = move_x * 4.8
        self.rect.x += int(self.vx)

        min_x = camera_lock_bounds[0] if camera_lock_bounds else 0
        max_x = camera_lock_bounds[1] if camera_lock_bounds else level_width
        if self.rect.left < min_x:
            self.rect.left = min_x
        if self.rect.right > max_x:
            self.rect.right = max_x

<<<<<<< HEAD
        # Física vertical com precisão sub-pixel e sensor estável de apoio
=======
>>>>>>> da45a41 (Novo commit fresco)
        prev_bottom = self.rect.bottom
        self.vy += GRAVITY
        self.pos_y += self.vy
        self.rect.y = int(round(self.pos_y))
        self.on_ground = False

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.pos_y = float(self.rect.y)
            self.vy = 0.0
            self.on_ground = True

        if not self.on_ground and self.vy >= 0:
<<<<<<< HEAD
            # Estende 1px abaixo dos pés para detectar apoio contínuo sem trepidação
=======
>>>>>>> da45a41 (Novo commit fresco)
            feet_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height + 1)
            for p in platforms:
                if feet_rect.colliderect(p.rect) and prev_bottom <= p.rect.top + 8:
                    self.rect.bottom = p.rect.top
                    self.pos_y = float(self.rect.y)
                    self.vy = 0.0
                    self.on_ground = True
                    break

        self.anim_timer += 1
        if self.anim_timer >= 8:
            self.anim_timer = 0
            self.anim_idx += 1

    def jump(self, sound):
        if self.on_ground and not self.dead:
            self.vy = -13.2
            self.on_ground = False
            sound.play("jump")

<<<<<<< HEAD
    def shoot_normal(self, projectiles, sound):
        if self.shoot_cd > 0 or self.dead:
            return
=======
    def _can_melee_hit(self, target_rect):
        if self.rect.bottom <= target_rect.top or target_rect.bottom <= self.rect.top:
            return False
        dx = max(self.rect.left - target_rect.right, target_rect.left - self.rect.right, 0)
        dy = max(self.rect.top - target_rect.bottom, target_rect.top - self.rect.bottom, 0)
        return math.hypot(dx, dy) <= self.MELEE_RANGE

    def attack_or_shoot(self, projectiles, enemies, boss, sound):
        if self.shoot_cd > 0 or self.dead:
            return

        targets_in_range = [
            e for e in enemies
            if e.hp > 0 and self._can_melee_hit(e.rect)
        ]
        boss_in_range = (
            boss is not None
            and boss.hp > 0
            and self._can_melee_hit(boss.rect)
        )

        if targets_in_range or boss_in_range:
            self.shoot_cd = 16
            self.melee_anim_timer = 12
            sound.play("melee")

            for e in targets_in_range:
                self.facing_right = e.rect.centerx >= self.rect.centerx
                e.hp -= self.MELEE_DAMAGE
                e.hit_flash = 8
                if e.hp <= 0:
                    self.energy = min(self.max_energy, self.energy + 12)
                    sound.play("explosion")

            if boss_in_range:
                self.facing_right = boss.rect.centerx >= self.rect.centerx
                boss.hp -= self.MELEE_DAMAGE
                boss.hit_flash = 8
                self.energy = min(self.max_energy, self.energy + 4)
            return

>>>>>>> da45a41 (Novo commit fresco)
        self.shoot_cd = 14
        self.shoot_anim_timer = 10
        sound.play("shoot")

        if self.looking_up:
            px, py = self.rect.centerx, self.rect.top - 4
            vx, vy = 0, -11.5
<<<<<<< HEAD
=======
        elif self.looking_down:
            px, py = self.rect.centerx, self.rect.bottom + 4
            vx, vy = 0, 11.5
>>>>>>> da45a41 (Novo commit fresco)
        else:
            dir_x = 1 if self.facing_right else -1
            px = self.rect.right + 6 if self.facing_right else self.rect.left - 6
            py = self.rect.centery - 2
            vx, vy = 11.5 * dir_x, 0

        projectiles.append(
            Projectile(px, py, vx, vy, 12, "player", "normal", self.sprite_bank.projectiles["normal"])
        )

    def use_upgrade(self, equipped_upgrade, projectiles, enemies, boss, sound):
        if not equipped_upgrade or self.dead:
            return False

        costs = {"explosion": 40, "big_shot": 35, "missiles": 45}
        cost = costs.get(equipped_upgrade, 35)
        if self.energy < cost:
            return False

        self.energy -= cost
        self.shoot_anim_timer = 14

        if equipped_upgrade == "explosion":
            self.explosion_fx_timer = 18
            sound.play("explosion")
            cx, cy = self.rect.center
            for e in enemies:
                if e.hp > 0 and math.hypot(e.rect.centerx - cx, e.rect.centery - cy) <= self.explosion_radius:
                    e.hp -= 55
                    e.hit_flash = 8
            if boss and boss.hp > 0 and math.hypot(boss.rect.centerx - cx, boss.rect.centery - cy) <= self.explosion_radius + 40:
                boss.hp -= 55
                boss.hit_flash = 8

        elif equipped_upgrade == "big_shot":
            sound.play("big_shot")
            if self.looking_up:
                px, py = self.rect.centerx, self.rect.top - 10
                vx, vy = 0, -9.5
<<<<<<< HEAD
=======
            elif self.looking_down:
                px, py = self.rect.centerx, self.rect.bottom + 10
                vx, vy = 0, 9.5
>>>>>>> da45a41 (Novo commit fresco)
            else:
                dir_x = 1 if self.facing_right else -1
                px = self.rect.right + 14 if self.facing_right else self.rect.left - 14
                py = self.rect.centery - 2
                vx, vy = 9.5 * dir_x, 0
            projectiles.append(
                Projectile(px, py, vx, vy, 45, "player", "big", self.sprite_bank.projectiles["big"])
            )

        elif equipped_upgrade == "missiles":
            sound.play("shoot")
            dir_x = 1 if self.facing_right else -1
            for vy_init in (-4.5, 0.0, 4.5):
                projectiles.append(
                    Projectile(
                        self.rect.centerx,
                        self.rect.centery - 6,
                        5.5 * dir_x,
                        vy_init,
                        22,
                        "player",
                        "missile",
                        self.sprite_bank.projectiles["missile"],
                    )
                )
        return True

    def draw(self, surf, cam_x):
        if self.invuln_timer > 0 and (self.invuln_timer // 4) % 2 == 0 and not self.dead:
            return

        if self.dead:
            state = "dead"
<<<<<<< HEAD
        elif not self.on_ground:
            state = "jump"
        elif self.looking_up:
            state = "up"
=======
        elif self.melee_anim_timer > 0:
            state = "melee"
        elif self.looking_up:
            state = "up"
        elif self.looking_down:
            state = "down"
        elif not self.on_ground:
            state = "jump"
>>>>>>> da45a41 (Novo commit fresco)
        elif self.shoot_anim_timer > 0:
            state = "shoot"
        elif abs(self.vx) > 0.1:
            state = "run"
        else:
            state = "idle"

        if not self.facing_right:
            state += "_left"

<<<<<<< HEAD
        frames = self.anims[state]
        img = frames[self.anim_idx % len(frames)]
        surf.blit(img, (self.rect.x - cam_x - 6, self.rect.y))

        if self.explosion_fx_timer > 0:
            prog = 1.0 - (self.explosion_fx_timer / 18.0)
            rad = int(25 + prog * self.explosion_radius)
            cx = self.rect.centerx - cam_x
            cy = self.rect.centery
=======
        frames = self.anims.get(state, self.anims["idle" if self.facing_right else "idle_left"])
        img = frames[self.anim_idx % len(frames)]
        surf.blit(img, (self.rect.x - cam_x - 6, self.rect.y))

        if self.melee_anim_timer > 0:
            cx = int(self.rect.centerx - cam_x)
            cy = int(self.rect.centery)
            arc_rect = pygame.Rect(cx - self.MELEE_RANGE, cy - self.MELEE_RANGE, self.MELEE_RANGE * 2, self.MELEE_RANGE * 2)
            start_ang = -0.8 if self.facing_right else math.pi - 0.8
            end_ang = 0.8 if self.facing_right else math.pi + 0.8
            pygame.draw.arc(surf, PALETTE["neon_yellow"], arc_rect, start_ang, end_ang, 4)

        if self.explosion_fx_timer > 0:
            prog = 1.0 - (self.explosion_fx_timer / 18.0)
            rad = int(25 + prog * self.explosion_radius)
            cx = int(self.rect.centerx - cam_x)
            cy = int(self.rect.centery)
>>>>>>> da45a41 (Novo commit fresco)
            pygame.draw.circle(surf, PALETTE["neon_yellow"], (cx, cy), rad, 5)
            pygame.draw.circle(surf, PALETTE["neon_cyan"], (cx, cy), max(5, rad - 14), 3)