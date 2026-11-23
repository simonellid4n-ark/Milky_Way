SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60

GRAVITY = 0.65
GROUND_Y = 450

SAVE_FILE = "savegame.json"

PALETTE = {
    "outline": (18, 12, 24),
    "white": (245, 245, 250),
    "red": (235, 64, 78),
    "neon_cyan": (64, 245, 240),
    "neon_pink": (245, 68, 185),
    "neon_yellow": (250, 225, 70),
    "neon_green": (75, 235, 130),
    "sky_light": (242, 232, 248),
    "sky_mid": (205, 178, 224),
    "building_dark": (48, 24, 52),
    "window_orange": (232, 165, 82),
    "ground_dark": (46, 26, 56),
    "ground_trim": (86, 54, 102),
    "pur_orange": (232, 118, 48),
    "pur_dark_orange": (196, 86, 32),
    "pur_cream": (248, 235, 206),
    "pur_shirt": (62, 138, 128),
    "pur_pants": (68, 118, 185),
    "pur_cannon": (162, 172, 186),
    "pur_cannon_hi": (212, 220, 232),
    "goggle_cyan": (118, 235, 242),
    "blush": (242, 138, 148),
}

STAGE_META = {
    "tutorial": {
        "name": "Centro - Mercado do Bairro",
        "theme": "tutorial",
        "length": 2400,
        "boss_id": "tutorial",
        "boss_name": "Cachorro-Loko",
        "reward": None,
        "desc": "Recupere o leite e aprenda os controles básicos!",
    },
    "noroeste": {
        "name": "Região Noroeste - Canteiro de Obras",
        "theme": "noroeste",
        "length": 3400,
        "boss_id": "noroeste",
        "boss_name": "Mestre-de-Obras",
        "reward": "explosion",
        "desc": "Andaimes perigosos e cães operários.",
    },
    "nordeste": {
        "name": "Região Nordeste - Boate Cyberpunk",
        "theme": "nordeste",
        "length": 3500,
        "boss_id": "nordeste",
        "boss_name": "DJ-Dog",
        "reward": "big_shot",
        "desc": "Luzes neon, drones e ondas sonoras.",
    },
    "sul": {
        "name": "Região Sul - Biblioteca Central",
        "theme": "sul",
        "length": 3400,
        "boss_id": "sul",
        "boss_name": "Bibliote-Cão",
        "reward": "missiles",
        "desc": "Plataformas altas e ataques precisos.",
    },
    "final": {
        "name": "Covil do Grande Líder",
        "theme": "final",
        "length": 1600,
        "boss_id": "final_mech",
        "boss_name": "O GRANDE LÍDER",
        "reward": None,
        "desc": "O confronto decisivo pelo futuro do leite!",
    },
}

UPGRADE_NAMES = {
    "explosion": "Explosão Radial (40 EN)",
    "big_shot": "Mega Tiro (35 EN)",
    "missiles": "Mísseis Teleguiados (45 EN)",
}