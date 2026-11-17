import io
import math
import random
import struct
import wave
import pygame


class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
            self._generate_all_sfx()
        except Exception:
            self.enabled = False

    def _make_wave(self, samples, sample_rate=22050):
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            raw = b"".join(struct.pack("<h", max(-32767, min(32767, int(s)))) for s in samples)
            wf.writeframes(raw)
        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def _generate_all_sfx(self):
        sr = 22050
        # Tiro normal
        shoot = []
        for i in range(int(sr * 0.09)):
            t = i / sr
            freq = 880 - 5200 * t
            env = (1 - t / 0.09) * 8000
            val = env * (1 if math.sin(2 * math.pi * freq * t) > 0 else -1)
            shoot.append(val)
        self.sounds["shoot"] = self._make_wave(shoot, sr)

        # Mega tiro
        big = []
        for i in range(int(sr * 0.22)):
            t = i / sr
            freq = 320 - 900 * t
            env = (1 - t / 0.22) * 14000
            val = env * math.sin(2 * math.pi * max(60, freq) * t)
            big.append(val)
        self.sounds["big_shot"] = self._make_wave(big, sr)

        # Explosão
        exp = []
        for i in range(int(sr * 0.30)):
            t = i / sr
            env = (1 - t / 0.30) * 15000
            val = env * random.uniform(-1, 1) * math.sin(2 * math.pi * 80 * t)
            exp.append(val)
        self.sounds["explosion"] = self._make_wave(exp, sr)

        # Pulo
        jmp = []
        for i in range(int(sr * 0.12)):
            t = i / sr
            freq = 240 + 1800 * t
            env = (1 - t / 0.12) * 7000
            jmp.append(env * math.sin(2 * math.pi * freq * t))
        self.sounds["jump"] = self._make_wave(jmp, sr)

        # Dano
        hit = []
        for i in range(int(sr * 0.18)):
            t = i / sr
            freq = 160 - 400 * t
            env = (1 - t / 0.18) * 12000
            hit.append(env * (1 if math.sin(2 * math.pi * max(40, freq) * t) > 0 else -1))
        self.sounds["hit"] = self._make_wave(hit, sr)

        # Vitória / Powerup
        win = []
        notes = [523.25, 659.25, 783.99, 1046.50]
        for n in notes:
            for i in range(int(sr * 0.08)):
                t = i / sr
                env = (1 - t / 0.08) * 9000
                win.append(env * math.sin(2 * math.pi * n * t))
        self.sounds["powerup"] = self._make_wave(win, sr)

        # Loop Synthwave Bassline
        bass = []
        seq = [110, 110, 130.81, 146.83, 110, 110, 164.81, 146.83]
        step_len = int(sr * 0.18)
        for freq in seq:
            for i in range(step_len):
                t = i / sr
                env = math.exp(-t * 6.5) * 3200
                saw = ((t * freq) % 1.0) * 2 - 1
                bass.append(env * saw)
        self.sounds["bgm"] = self._make_wave(bass, sr)

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def start_bgm(self):
        if self.enabled and "bgm" in self.sounds:
            self.sounds["bgm"].play(loops=-1)

    def stop_bgm(self):
        if self.enabled and "bgm" in self.sounds:
            self.sounds["bgm"].stop()