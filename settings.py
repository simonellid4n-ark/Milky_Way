SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
GRAVITY = 0.65
GROUND_Y = 450
SAVE_FILE = "milky_way_save.json"

PALETTE = {
    "black": (15, 10, 20),
    "outline": (0, 0, 0),
    "ground_dark": (23, 12, 30),
    "ground_trim": (58, 30, 74),
    "sky_light": (163, 134, 179),
    "sky_mid": (118, 86, 135),
    "building_dark": (42, 34, 51),
    "window_orange": (245, 148, 54),
    "pur_orange": (229, 131, 61),
    "pur_dark_orange": (166, 78, 46),
    "pur_cream": (252, 224, 184),
    "pur_shirt": (95, 125, 118),
    "pur_pants": (46, 62, 82),
    "pur_cannon": (38, 44, 58),
    "pur_cannon_hi": (84, 96, 122),
    "goggle_cyan": (158, 240, 255),
    "blush": (232, 138, 152),
    "neon_pink": (255, 70, 165),
    "neon_cyan": (65, 235, 255),
    "neon_yellow": (255, 215, 65),
    "neon_green": (80, 240, 130),
    "white": (248, 246, 252),
    "red": (235, 58, 72),
}

STAGE_META = {
    "tutorial": {
        "name": "Centro - Mercado do Bairro (Tutorial)",
        "theme": "tutorial",
        "boss_id": "tutorial",
        "boss_name": "Gerente Bulldog",
        "desc": "Aprenda os controles e liberte o mercado local!",
        "reward": None,
        "length": 2400,
    },
    "noroeste": {
        "name": "Noroeste - Canteiro de Obras",
        "theme": "noroeste",
        "boss_id": "noroeste",
        "boss_name": "Dogão da Obra",
        "desc": "Plataformas altas, operários e saltos sísmicos.",
        "reward": "explosion",
        "length": 3100,
    },
    "nordeste": {
        "name": "Nordeste - Balada Neon",
        "theme": "nordeste",
        "boss_id": "nordeste",
        "boss_name": "DJ Husky",
        "desc": "Drones aéreos, agentes neon e ondas sonoras.",
        "reward": "missiles",
        "length": 3100,
    },
    "sul": {
        "name": "Sul - Biblioteca Central",
        "theme": "sul",
        "boss_id": "sul",
        "boss_name": "Dra. Alice Books",
        "desc": "Emboscadas e projéteis teleguiados.",
        "reward": "big_shot",
        "length": 3100,
    },
    "final": {
        "name": "Torre da Gangue - Confronto Final",
        "theme": "final",
        "boss_id": "final_mech",
        "boss_name": "Grande Líder (Mech & Sphynx)",
        "desc": "Arena final em duas fases contra o verdadeiro vilão!",
        "reward": None,
        "length": SCREEN_WIDTH,
    },
}

UPGRADE_NAMES = {
    "explosion": "Explosão Radial (40 EN)",
    "big_shot": "Mega Tiro (35 EN)",
    "missiles": "Mísseis Teleguiados (45 EN)",
<<<<<<< HEAD
=======
}
UPGRADE_DAMAGE = {
    "explosion": 30,
    "big_shot": 20,
    "missiles": 15,
>>>>>>> da45a41 (Novo commit fresco)
}