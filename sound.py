import pygame
import numpy as np
import math
import random


class ProceduralMusicSystem:
    """Advanced procedural music system"""
    def __init__(self):
        self.current_track = None
        self.music_volume = 0.3
        self.tracks = {}
        self.fade_duration = 2000
        self.generate_all_tracks()
        
    def generate_all_tracks(self):
        """Generate all music tracks"""
        try:
            # Intro/Menu music - Epic and mysterious
            self.tracks["intro"] = self.generate_track("intro", tempo=120, duration=4.0)
            
            # Battle music - Intense and energetic
            self.tracks["battle"] = self.generate_track("battle", tempo=140, duration=5.0)
            
            # Victory music - Triumphant
            self.tracks["victory"] = self.generate_track("victory", tempo=130, duration=3.0)
            
            # Defeat music - Somber
            self.tracks["defeat"] = self.generate_track("defeat", tempo=90, duration=3.0)
            
            # Suspense music - Tense
            self.tracks["suspense"] = self.generate_track("suspense", tempo=100, duration=4.0)
            
        except Exception as e:
            print(f"Music generation failed: {e}")
            
    def generate_track(self, track_type, tempo=120, duration=4.0):
        """Generate a procedural music track"""
        sample_rate = 22050  # Lower sample rate for faster generation
        n_samples = int(duration * sample_rate)
        
        # Musical scales
        scales = {
            "intro": [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88],  # C major
            "battle": [293.66, 329.63, 369.99, 415.30, 466.16, 523.25],  # D minor pentatonic
            "victory": [261.63, 329.63, 392.00, 523.25, 659.25],  # C major pentatonic
            "defeat": [220.00, 246.94, 261.63, 293.66, 329.63],  # A minor
            "suspense": [277.18, 311.13, 369.99, 415.30, 466.16]  # C# minor
        }
        
        scale = scales.get(track_type, scales["intro"])
        
        # Create stereo buffer
        buffer = np.zeros((n_samples, 2), dtype=np.float32)
        
        # Beat duration
        beat_duration = 60.0 / tempo
        samples_per_beat = int(beat_duration * sample_rate)
        
        # Generate melodic pattern
        num_notes = int(duration / beat_duration)
        
        for note_idx in range(num_notes):
            start_sample = note_idx * samples_per_beat
            note_duration = samples_per_beat
            
            if track_type == "battle":
                # Fast, aggressive notes
                freq = random.choice(scale)
                self.add_note(buffer, start_sample, note_duration // 2, freq, sample_rate, 0.15)
                
            elif track_type == "intro":
                # Mysterious, spacey
                freq = scale[note_idx % len(scale)]
                self.add_note(buffer, start_sample, note_duration, freq, sample_rate, 0.12, wave="sine")
                # Add harmony
                if note_idx % 2 == 0:
                    self.add_note(buffer, start_sample, note_duration, freq * 1.5, sample_rate, 0.08, wave="sine")
                    
            elif track_type == "victory":
                # Bright, ascending
                freq = scale[note_idx % len(scale)]
                self.add_note(buffer, start_sample, note_duration, freq, sample_rate, 0.18, wave="square")
                
            elif track_type == "defeat":
                # Slow, descending
                freq = scale[-(note_idx % len(scale)) - 1]
                self.add_note(buffer, start_sample, note_duration, freq, sample_rate, 0.12, wave="sine")
                
            elif track_type == "suspense":
                # Tense, dissonant
                freq = random.choice(scale)
                self.add_note(buffer, start_sample, note_duration // 3, freq, sample_rate, 0.1, wave="triangle")
        
        # Add bass line
        if track_type in ["battle", "intro"]:
            bass_freq = scale[0] / 2
            for beat in range(num_notes // 2):
                start_sample = beat * samples_per_beat * 2
                self.add_note(buffer, start_sample, samples_per_beat * 2, bass_freq, sample_rate, 0.15, wave="sine")
        
        # Normalize and convert to int16
        max_val = np.abs(buffer).max()
        if max_val > 0:
            buffer = buffer / max_val * 0.7
        
        buffer_int = (buffer * 32767).astype(np.int16)
        
        return pygame.sndarray.make_sound(buffer_int)
    
    def add_note(self, buffer, start_sample, duration, frequency, sample_rate, amplitude=0.1, wave="sine"):
        """Add a musical note to the buffer"""
        end_sample = min(start_sample + duration, len(buffer))
        
        for i in range(start_sample, end_sample):
            if i >= len(buffer):
                break
                
            t = (i - start_sample) / sample_rate
            note_progress = (i - start_sample) / duration
            
            # Envelope (ADSR)
            if note_progress < 0.1:  # Attack
                envelope = note_progress / 0.1
            elif note_progress > 0.8:  # Release
                envelope = (1.0 - note_progress) / 0.2
            else:  # Sustain
                envelope = 1.0
            
            # Generate wave
            if wave == "sine":
                sample = math.sin(2 * math.pi * frequency * t)
            elif wave == "square":
                sample = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            elif wave == "triangle":
                sample = 2.0 * abs(2.0 * ((frequency * t) % 1.0) - 1.0) - 1.0
            else:
                sample = math.sin(2 * math.pi * frequency * t)
            
            sample *= amplitude * envelope
            
            # Add to both channels with slight stereo width
            buffer[i][0] += sample * 0.9
            buffer[i][1] += sample * 1.1
    
    def play_track(self, track_name, loops=-1):
        """Play a music track"""
        if track_name in self.tracks and self.tracks[track_name]:
            try:
                self.current_track = track_name
                channel = pygame.mixer.find_channel()
                if channel:
                    channel.play(self.tracks[track_name], loops=loops)
                    channel.set_volume(self.music_volume)
            except:
                pass
    
    def stop(self):
        """Stop all music"""
        pygame.mixer.stop()

class AdvancedSoundManager:
    """Advanced sound effects manager"""
    def __init__(self):
        self.sounds = {}
        self.sound_volume = 0.5
        
    def load_sounds(self):
        """Create all sound effects"""
        try:
            # Character emotions
            self.sounds["laugh"] = self.generate_laugh()
            self.sounds["gasp"] = self.generate_gasp()
            self.sounds["think"] = self.generate_think()
            
            # Game sounds
            self.sounds["cooperate"] = self.generate_tone(523.25, 0.2, "sine")
            self.sounds["defect"] = self.generate_tone(220.00, 0.3, "square")
            self.sounds["win"] = self.generate_arpeggio([523, 659, 784, 1047], 0.6)
            self.sounds["lose"] = self.generate_arpeggio([392, 330, 294, 220], 0.6)
            self.sounds["click"] = self.generate_click()
            self.sounds["strategy_change"] = self.generate_sweep(400, 800, 0.3)
            self.sounds["thinking"] = self.generate_tone(659.25, 0.15, "sine")
            self.sounds["whoosh"] = self.generate_whoosh()
            self.sounds["impact"] = self.generate_impact()
            self.sounds["power_up"] = self.generate_power_up()
            self.sounds["explosion"] = self.generate_explosion()
            
        except Exception as e:
            print(f"Sound generation failed: {e}")
    
    def generate_laugh(self):
        """Generate laugh sound effect"""
        sample_rate = 22050
        duration = 0.4
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            t = i / sample_rate
            # Create bouncy laugh pattern
            freq = 400 + 200 * math.sin(20 * math.pi * t)
            envelope = math.exp(-t * 5) * (1 + 0.3 * math.sin(30 * math.pi * t))
            sample = max_sample * 0.2 * envelope * math.sin(2 * math.pi * freq * t)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_gasp(self):
        """Generate gasp/surprise sound"""
        sample_rate = 22050
        duration = 0.3
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            t = i / sample_rate
            freq = 800 - 400 * t
            envelope = math.exp(-t * 8)
            noise = random.uniform(-0.3, 0.3)
            sample = max_sample * 0.25 * envelope * (math.sin(2 * math.pi * freq * t) + noise)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_think(self):
        """Generate thinking sound"""
        sample_rate = 22050
        duration = 0.2
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            t = i / sample_rate
            freq = 300 + 100 * math.sin(15 * math.pi * t)
            envelope = 1 - t / duration
            sample = max_sample * 0.15 * envelope * math.sin(2 * math.pi * freq * t)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_tone(self, frequency, duration, wave_type="sine"):
        """Generate a musical tone"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            t = i / sample_rate
            envelope = min(1.0, (1 - t/duration) * 2)
            
            if wave_type == "sine":
                wave = math.sin(2 * math.pi * frequency * t)
            elif wave_type == "square":
                wave = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            else:
                wave = math.sin(2 * math.pi * frequency * t)
            
            sample = max_sample * 0.3 * envelope * wave
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_arpeggio(self, frequencies, duration):
        """Generate an arpeggio"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        segment = n_samples / len(frequencies)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            segment_idx = min(int(i / segment), len(frequencies) - 1)
            frequency = frequencies[segment_idx]
            
            t = i / sample_rate
            envelope = 1 - (i % segment) / segment
            sample = max_sample * 0.3 * envelope * math.sin(2 * math.pi * frequency * t)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_sweep(self, start_freq, end_freq, duration):
        """Generate a frequency sweep"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            t = i / sample_rate
            progress = t / duration
            freq = start_freq + (end_freq - start_freq) * progress
            envelope = 1 - progress
            sample = max_sample * 0.25 * envelope * math.sin(2 * math.pi * freq * t)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_click(self):
        """Generate click sound"""
        sample_rate = 22050
        n_samples = 1000
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            envelope = math.exp(-i / 100)
            sample = max_sample * 0.3 * envelope * random.uniform(-1, 1)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_whoosh(self):
        """Generate whoosh sound"""
        sample_rate = 22050
        duration = 0.4
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            t = i / sample_rate
            freq = 200 - 150 * (t / duration)
            noise = random.uniform(-1, 1)
            envelope = math.sin(math.pi * t / duration)
            sample = max_sample * 0.2 * envelope * noise
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_impact(self):
        """Generate impact sound"""
        sample_rate = 22050
        duration = 0.2
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            envelope = math.exp(-i / (sample_rate * 0.05))
            noise = random.uniform(-1, 1)
            bass = math.sin(2 * math.pi * 60 * i / sample_rate)
            sample = max_sample * 0.4 * envelope * (noise * 0.7 + bass * 0.3)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_power_up(self):
        """Generate power up sound"""
        sample_rate = 22050
        duration = 0.5
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            t = i / sample_rate
            freq = 200 + 600 * (t / duration)
            envelope = 1 - t / duration
            sample = max_sample * 0.25 * envelope * math.sin(2 * math.pi * freq * t)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def generate_explosion(self):
        """Generate explosion sound"""
        sample_rate = 22050
        duration = 0.6
        n_samples = int(duration * sample_rate)
        
        buffer = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2**(15) - 1
        
        for i in range(n_samples):
            t = i / sample_rate
            envelope = math.exp(-t * 4)
            noise = random.uniform(-1, 1)
            bass = math.sin(2 * math.pi * 40 * t) * 0.5
            sample = max_sample * 0.35 * envelope * (noise * 0.7 + bass * 0.3)
            buffer[i] = [sample, sample]
        
        return pygame.sndarray.make_sound(buffer)
    
    def play_sound(self, name):
        """Play a sound effect"""
        if name in self.sounds:
            try:
                channel = pygame.mixer.find_channel()
                if channel:
                    channel.play(self.sounds[name])
                    channel.set_volume(self.sound_volume)
            except:
                pass

