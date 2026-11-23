import math
import array
import pygame


class SoundManager:
    MAX_VOLUME = 0.35   # Trava de segurança: nenhum som ultrapassa 35% do volume máximo
    BGM_VOLUME = 0.14   # Volume da música de fundo (14% - suave para não cobrir os efeitos)
    SFX_VOLUME = 0.28   # Volume dos efeitos sonoros (28%)

    def __init__(self):
        self.enabled = False
        self.sounds = {}
        self.bgm_sound = None
        self.bgm_channel = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
            self._build_sounds()
            self.apply_volume_limits()
        except Exception:
            self.enabled = False

    def _tone(self, freq, duration, volume=0.2, wave="square", slide=0.0):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = array.array("h")
        amp = int(32767 * min(volume, self.MAX_VOLUME))
        for i in range(n_samples):
            t = i / sample_rate
            f = freq + slide * t
            phase = 2.0 * math.pi * f * t
            if wave == "square":
                val = 1.0 if math.sin(phase) >= 0 else -1.0
            elif wave == "triangle":
                val = 2.0 * abs(2.0 * (f * t - math.floor(f * t + 0.5))) - 1.0
            else:
                val = math.sin(phase)
            env = max(0.0, 1.0 - (i / n_samples))
            buf.append(int(amp * val * env))
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def _build_sounds(self):
        self.sounds["shoot"] = self._tone(720, 0.08, 0.16, "square", -320)
        self.sounds["big_shot"] = self._tone(240, 0.22, 0.24, "square", -90)
        self.sounds["melee"] = self._tone(520, 0.07, 0.18, "triangle", 260)
        self.sounds["jump"] = self._tone(310, 0.12, 0.16, "triangle", 280)
        self.sounds["hit"] = self._tone(150, 0.18, 0.24, "square", -60)
        self.sounds["explosion"] = self._tone(110, 0.28, 0.26, "square", -70)
        self.sounds["powerup"] = self._tone(440, 0.25, 0.20, "triangle", 440)

        # Trilha sonora chiptune sintetizada em loop
        sample_rate = 22050
        notes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 293.66, 392.00]
        note_dur = 0.18
        buf = array.array("h")
        amp = int(32767 * self.BGM_VOLUME)
        for freq in notes:
            n_samples = int(sample_rate * note_dur)
            for i in range(n_samples):
                t = i / sample_rate
                val = 1.0 if math.sin(2.0 * math.pi * freq * t) >= 0 else -1.0
                env = 0.85 - 0.35 * (i / n_samples)
                buf.append(int(amp * val * env))
        self.bgm_sound = pygame.mixer.Sound(buffer=buf.tobytes())

    def apply_volume_limits(self):
        if not self.enabled:
            return
        safe_sfx = min(self.SFX_VOLUME, self.MAX_VOLUME)
        safe_bgm = min(self.BGM_VOLUME, self.MAX_VOLUME)

        for snd in self.sounds.values():
            snd.set_volume(safe_sfx)

        if self.bgm_sound:
            self.bgm_sound.set_volume(safe_bgm)

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(safe_bgm)

    def set_bgm_volume(self, volume):
        self.BGM_VOLUME = max(0.0, min(volume, self.MAX_VOLUME))
        self.apply_volume_limits()

    def set_sfx_volume(self, volume):
        self.SFX_VOLUME = max(0.0, min(volume, self.MAX_VOLUME))
        self.apply_volume_limits()

    def play(self, name):
        if self.enabled and name in self.sounds:
            snd = self.sounds[name]
            snd.set_volume(min(self.SFX_VOLUME, self.MAX_VOLUME))
            snd.play()

    def start_bgm(self):
        if not self.enabled:
            return
        safe_bgm = min(self.BGM_VOLUME, self.MAX_VOLUME)
        if self.bgm_sound:
            self.bgm_sound.stop()
            self.bgm_sound.set_volume(safe_bgm)
            self.bgm_channel = self.bgm_sound.play(loops=-1)
            if self.bgm_channel:
                self.bgm_channel.set_volume(safe_bgm)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(safe_bgm)

    def stop_bgm(self):
        if not self.enabled:
            return
        if self.bgm_channel:
            self.bgm_channel.stop()
        elif self.bgm_sound:
            self.bgm_sound.stop()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()