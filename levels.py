from settings import SCREEN_WIDTH, GROUND_Y, STAGE_META
from entities import Platform, Enemy, Boss


def build_stage(stage_id, sprite_bank, completed_regions_count):
    meta = STAGE_META[stage_id]
    theme = meta["theme"]
    length = meta["length"]
    platforms = []
    enemies = []

    diff_mult = 1.0 + (completed_regions_count * 0.15) if stage_id in ("noroeste", "nordeste", "sul") else 1.0

    if stage_id == "tutorial":
        platforms = [
            Platform(360, 355, 150),
            Platform(640, 295, 160),
            Platform(980, 350, 170),
            Platform(1280, 280, 150),
        ]
        spawns = [
            (520, "boxer"),
            (740, "agent"),
            (1080, "trash"),
            (1340, "drone"),
            (1580, "boxer"),
            (1720, "agent"),
        ]
    elif stage_id == "noroeste":
        platforms = [
            Platform(320, 360, 140),
            Platform(540, 285, 150),
            Platform(820, 340, 160),
            Platform(1120, 260, 160),
            Platform(1420, 340, 180),
            Platform(1750, 275, 150),
            Platform(2050, 350, 160),
        ]
        spawns = [
            (460, "boxer"),
            (610, "agent"),
            (900, "boxer"),
            (1180, "drone"),
            (1320, "trash"),
            (1520, "boxer"),
            (1800, "agent"),
            (1960, "drone"),
            (2150, "boxer"),
            (2280, "agent"),
        ]
    elif stage_id == "nordeste":
        platforms = [
            Platform(340, 350, 150),
            Platform(620, 275, 160),
            Platform(940, 345, 150),
            Platform(1240, 265, 170),
            Platform(1560, 340, 160),
            Platform(1880, 270, 160),
            Platform(2160, 345, 150),
        ]
        spawns = [
            (480, "drone"),
            (680, "agent"),
            (980, "drone"),
            (1160, "boxer"),
            (1320, "agent"),
            (1620, "drone"),
            (1820, "trash"),
            (1950, "agent"),
            (2200, "drone"),
            (2320, "boxer"),
        ]
    elif stage_id == "sul":
        platforms = [
            Platform(330, 355, 160),
            Platform(610, 285, 150),
            Platform(890, 225, 140),
            Platform(1190, 340, 170),
            Platform(1500, 275, 160),
            Platform(1810, 345, 160),
            Platform(2100, 280, 160),
        ]
        spawns = [
            (470, "trash"),
            (670, "agent"),
            (940, "drone"),
            (1260, "trash"),
            (1420, "boxer"),
            (1580, "agent"),
            (1860, "trash"),
            (2040, "drone"),
            (2180, "agent"),
            (2320, "boxer"),
        ]
    else:
        platforms = [
            Platform(140, 340, 160),
            Platform(660, 340, 160),
        ]
        spawns = []

    for sx, etype in spawns:
        esprites = sprite_bank.get_enemy_sprites(etype, theme)
        enemies.append(Enemy(sx, GROUND_Y, etype, theme, esprites, diff_mult))

    boss_x = length - 210 if stage_id != "final" else SCREEN_WIDTH - 230
    boss = Boss(boss_x, meta["boss_id"], sprite_bank, diff_mult)
    return platforms, enemies, boss