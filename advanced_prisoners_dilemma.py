import pygame
import sys
import random
import math
import os
from sound import ProceduralMusicSystem, AdvancedSoundManager
from ai import PowerfulAdaptiveAI, StrategicOpponentAI


# Set environment variables for centered display BEFORE pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = 'SDL_WINDOWPOS_CENTERED,SDL_WINDOWPOS_CENTERED'

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()


INTRO = 0
MENU = 1
BATTLE = 2
RESULTS = 3
OUTRO = 4

# Screen setup - Fullscreen with fallback
FULLSCREEN = True
# Get screen dimensions after pygame.init()
screen_info = pygame.display.Info()
if FULLSCREEN:
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h
else:
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

FPS = 60

# Colors - Enhanced Palette
BACKGROUND = (8, 10, 25)
PLAYER1_COLOR = (64, 224, 255)   # Neon Cyan
PLAYER2_COLOR = (255, 64, 129)   # Neon Pink
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 217, 61)
BUTTON_HOVER = (255, 230, 128)
COOP_COLOR = (100, 255, 150)
DEFECT_COLOR = (255, 80, 80)
GLOW_COLOR = (255, 255, 200)
NEON_BLUE = (64, 224, 255)
NEON_PINK = (255, 64, 129)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (180, 70, 255)
NEON_ORANGE = (255, 165, 0)
NEON_YELLOW = (255, 255, 0)


# Character emotions
EMOTION_HAPPY = "happy"
EMOTION_SAD = "sad"
EMOTION_THINKING = "thinking"
EMOTION_DETERMINED = "determined"
EMOTION_SURPRISED = "surprised"
EMOTION_ANGRY = "angry"
EMOTION_NEUTRAL = "neutral"



class CinematicEffect:
    """Cinematic camera effects"""
    def __init__(self):
        self.shake_intensity = 0
        self.shake_duration = 0
        self.zoom_level = 1.0
        self.target_zoom = 1.0
        self.flash_alpha = 0
        self.vignette_alpha = 0
        
    def add_shake(self, intensity=10, duration=20):
        """Add screen shake"""
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def add_flash(self, alpha=200):
        """Add screen flash"""
        self.flash_alpha = alpha
    
    def set_zoom(self, zoom):
        """Set camera zoom"""
        self.target_zoom = zoom
    
    def update(self):
        """Update cinematic effects"""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            if self.shake_duration == 0:
                self.shake_intensity = 0
        
        # Smooth zoom
        self.zoom_level += (self.target_zoom - self.zoom_level) * 0.1
        
        # Fade flash
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - 10)
    
    def get_offset(self):
        """Get screen shake offset"""
        if self.shake_duration > 0:
            return (
                random.randint(-self.shake_intensity, self.shake_intensity),
                random.randint(-self.shake_intensity, self.shake_intensity)
            )
        return (0, 0)
    
    def apply_effects(self, screen):
        """Apply cinematic effects to screen"""
        # Flash effect
        if self.flash_alpha > 0:
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surf.fill((255, 255, 255))
            flash_surf.set_alpha(self.flash_alpha)
            screen.blit(flash_surf, (0, 0))
        
        # Vignette effect
        if self.vignette_alpha > 0:
            vignette_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for i in range(100):
                alpha = int(self.vignette_alpha * (i / 100))
                size = int((100 - i) / 100 * min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2)
                pygame.draw.rect(vignette_surf, (0, 0, 0, alpha),
                               (size, size, SCREEN_WIDTH - size * 2, SCREEN_HEIGHT - size * 2))
            screen.blit(vignette_surf, (0, 0))

class EnhancedVFXManager:
    """Enhanced VFX system"""
    def __init__(self):
        self.particles = []
        self.glows = []
        self.trails = []
        self.text_effects = []
        self.beams = []
        self.explosions = []
        self.lightning_bolts = []
        self.strategy_indicators = []
        
    def add_particles(self, x, y, color, count=20, size_range=(4, 12), speed_range=(-5, 5), gravity=0.1):
        for _ in range(count):
            self.particles.append(EnhancedParticle(x, y, color, size_range, speed_range, gravity))
    
    def add_explosion_particles(self, x, y, color, count=50):
        """Add dramatic explosion particles"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 10)
            self.particles.append(EnhancedParticle(
                x, y, color, 
                size_range=(6, 16),
                speed_range=(math.cos(angle) * speed, math.sin(angle) * speed),
                gravity=0.2
            ))
    
    def add_strategy_indicator(self, x, y, strategy_name, color):
        """Add strategy change indicator"""
        self.strategy_indicators.append(StrategyIndicator(x, y, strategy_name, color))
    
    def add_lightning(self, x1, y1, x2, y2, color, segments=10):
        """Add lightning bolt effect"""
        self.lightning_bolts.append(LightningBolt(x1, y1, x2, y2, color, segments))
    
    def add_glow(self, x, y, color, duration=40, max_size=30):
        self.glows.append(GlowEffect(x, y, color, duration, max_size))
    
    def add_trail(self, x, y, color, size=4):
        self.trails.append(TrailPoint(x, y, color, size))
    
    def add_text_effect(self, text, x, y, color, duration=80, rise_speed=2, size=32):
        self.text_effects.append(TextEffect(text, x, y, color, duration, rise_speed, size))
    
    def add_beam(self, x1, y1, x2, y2, color, duration=40, width=5):
        self.beams.append(BeamEffect(x1, y1, x2, y2, color, duration, width))
    
    def add_explosion(self, x, y, color, size=60):
        self.explosions.append(ExplosionEffect(x, y, color, size))
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
        self.glows = [g for g in self.glows if g.update()]
        self.trails = [t for t in self.trails if t.update()]
        self.text_effects = [t for t in self.text_effects if t.update()]
        self.beams = [b for b in self.beams if b.update()]
        self.explosions = [e for e in self.explosions if e.update()]
        self.lightning_bolts = [l for l in self.lightning_bolts if l.update()]
        self.strategy_indicators = [s for s in self.strategy_indicators if s.update()]
    
    def draw(self, screen, offset=(0, 0)):
        for trail in self.trails:
            trail.draw(screen, offset)
        for beam in self.beams:
            beam.draw(screen, offset)
        for lightning in self.lightning_bolts:
            lightning.draw(screen, offset)
        for particle in self.particles:
            particle.draw(screen, offset)
        for glow in self.glows:
            glow.draw(screen, offset)
        for explosion in self.explosions:
            explosion.draw(screen, offset)
        for text_effect in self.text_effects:
            text_effect.draw(screen, offset)
        for indicator in self.strategy_indicators:
            indicator.draw(screen, offset)

class StrategyIndicator:
    """Visual indicator for strategy changes"""
    def __init__(self, x, y, strategy_name, color):
        self.x = x
        self.y = y
        self.start_y = y
        self.strategy_name = strategy_name
        self.color = color
        self.life = 1.0
        self.duration = 120
        self.size = 0
        self.max_size = 150
        
    def update(self):
        self.life -= 1 / self.duration
        self.y -= 0.5
        self.size = min(self.max_size, self.size + 3)
        return self.life > 0
    
    def draw(self, screen, offset=(0, 0)):
        alpha = int(self.life * 200)
        x, y = self.x + offset[0], self.y + offset[1]
        
        # Draw expanding ring
        pygame.draw.circle(screen, (*self.color, alpha), (int(x), int(y)), 
                         int(self.size), 3)
        
        # Draw strategy name
        font = pygame.font.Font(None, 36)
        text = font.render(self.strategy_name, True, self.color)
        text.set_alpha(alpha)
        screen.blit(text, (x - text.get_width()//2, y - 20))

class LightningBolt:
    """Lightning bolt effect"""
    def __init__(self, x1, y1, x2, y2, color, segments=10):
        self.color = color
        self.duration = 15
        self.max_duration = 15
        self.points = self.generate_lightning(x1, y1, x2, y2, segments)
        
    def generate_lightning(self, x1, y1, x2, y2, segments):
        """Generate jagged lightning path"""
        points = [(x1, y1)]
        
        for i in range(1, segments):
            progress = i / segments
            x = x1 + (x2 - x1) * progress
            y = y1 + (y2 - y1) * progress
            
            # Add randomness
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-30, 30)
            
            points.append((x + offset_x, y + offset_y))
        
        points.append((x2, y2))
        return points
    
    def update(self):
        self.duration -= 1
        # Regenerate occasionally for flickering effect
        if random.random() < 0.3 and self.duration > 5:
            x1, y1 = self.points[0]
            x2, y2 = self.points[-1]
            self.points = self.generate_lightning(x1, y1, x2, y2, len(self.points) - 1)
        return self.duration > 0
    
    def draw(self, screen, offset=(0, 0)):
        if len(self.points) < 2:
            return
        
        alpha = int((self.duration / self.max_duration) * 255)
        
        # Draw multiple lines for glow effect
        for thickness in range(3, 0, -1):
            for i in range(len(self.points) - 1):
                x1, y1 = self.points[i]
                x2, y2 = self.points[i + 1]
                
                color_with_alpha = (*self.color, alpha // thickness)
                pygame.draw.line(screen, color_with_alpha,
                               (x1 + offset[0], y1 + offset[1]),
                               (x2 + offset[0], y2 + offset[1]),
                               thickness)

class EnhancedParticle:
    """Enhanced particle system"""
    def __init__(self, x, y, color, size_range=(4, 10), speed_range=(-3, 3), gravity=0.1):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.uniform(size_range[0], size_range[1])
        
        if isinstance(speed_range[0], tuple):
            self.speed_x, self.speed_y = speed_range
        else:
            self.speed_x = random.uniform(speed_range[0], speed_range[1])
            self.speed_y = random.uniform(speed_range[0], speed_range[1])
        
        self.life = 1.0
        self.decay = random.uniform(0.01, 0.03)
        self.gravity = gravity
        self.spin = random.uniform(-0.3, 0.3)
        self.angle = random.uniform(0, 360)
        self.shape = random.choice(['circle', 'square', 'star'])
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity
        self.speed_x *= 0.98  # Air resistance
        self.life -= self.decay
        self.size = max(0, self.size - 0.1)
        self.angle += self.spin
        return self.life > 0 and self.size > 0
    
    def draw(self, screen, offset=(0, 0)):
        if self.size <= 0:
            return
        
        alpha = int(self.life * 255)
        x = int(self.x + offset[0])
        y = int(self.y + offset[1])
        size = int(self.size)
        
        surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
        
        if self.shape == 'circle':
            pygame.draw.circle(surf, (*self.color, alpha), (size * 2, size * 2), size)
        elif self.shape == 'square':
            rect = pygame.Rect(size, size, size * 2, size * 2)
            surf_rotated = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
            pygame.draw.rect(surf_rotated, (*self.color, alpha), rect)
            surf = pygame.transform.rotate(surf_rotated, self.angle)
        elif self.shape == 'star':
            points = []
            for i in range(10):
                angle = math.radians(self.angle + i * 36)
                r = size * (1.5 if i % 2 == 0 else 0.7)
                points.append((
                    size * 2 + math.cos(angle) * r,
                    size * 2 + math.sin(angle) * r
                ))
            if len(points) >= 3:
                pygame.draw.polygon(surf, (*self.color, alpha), points)
        
        screen.blit(surf, (x - size * 2, y - size * 2))

class BeamEffect:
    """Enhanced beam effect"""
    def __init__(self, x1, y1, x2, y2, color, duration, width=5):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.duration = duration
        self.max_duration = duration
        self.width = width
        
    def update(self):
        self.duration -= 1
        return self.duration > 0
    
    def draw(self, screen, offset=(0, 0)):
        alpha = int((self.duration / self.max_duration) * 255)
        
        # Draw multiple layers for glow effect
        for i in range(self.width, 0, -1):
            color_alpha = (*self.color, alpha // (self.width - i + 1))
            pygame.draw.line(screen, color_alpha,
                           (self.x1 + offset[0], self.y1 + offset[1]),
                           (self.x2 + offset[0], self.y2 + offset[1]),
                           i)

class TextEffect:
    """Enhanced text effect"""
    def __init__(self, text, x, y, color, duration=60, rise_speed=2, size=32):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.duration = duration
        self.max_duration = duration
        self.rise_speed = rise_speed
        self.size = size
        self.scale = 0.5
        
    def update(self):
        self.duration -= 1
        self.y -= self.rise_speed
        self.scale = min(1.5, self.scale + 0.05)
        return self.duration > 0
    
    def draw(self, screen, offset=(0, 0)):
        alpha = int((self.duration / self.max_duration) * 255)
        font = pygame.font.Font(None, int(self.size * self.scale))
        
        # Draw text with outline
        text_surf = font.render(self.text, True, self.color)
        outline_surf = font.render(self.text, True, (0, 0, 0))
        
        text_surf.set_alpha(alpha)
        outline_surf.set_alpha(alpha // 2)
        
        x = self.x + offset[0] - text_surf.get_width() // 2
        y = self.y + offset[1]
        
        # Draw outline
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            screen.blit(outline_surf, (x + dx, y + dy))
        
        screen.blit(text_surf, (x, y))

class ExplosionEffect:
    """Dramatic explosion effect"""
    def __init__(self, x, y, color, size=50):
        self.x = x
        self.y = y
        self.color = color
        self.size = 0
        self.max_size = size
        self.life = 1.0
        self.decay = 0.03
        self.rings = []
        
        # Create expanding rings
        for i in range(5):
            self.rings.append({
                'delay': i * 5,
                'size': 0,
                'max_size': size + i * 20,
                'life': 1.0
            })
    
    def update(self):
        self.life -= self.decay
        self.size = min(self.max_size, self.size + 3)
        
        # Update rings
        for ring in self.rings:
            if ring['delay'] > 0:
                ring['delay'] -= 1
            else:
                ring['size'] = min(ring['max_size'], ring['size'] + 4)
                ring['life'] -= 0.05
        
        return self.life > 0
    
    def draw(self, screen, offset=(0, 0)):
        x = int(self.x + offset[0])
        y = int(self.y + offset[1])
        
        # Draw rings
        for ring in self.rings:
            if ring['delay'] == 0 and ring['life'] > 0:
                alpha = int(ring['life'] * 200)
                for thickness in range(5, 0, -1):
                    color_alpha = (*self.color, alpha // thickness)
                    pygame.draw.circle(screen, color_alpha, (x, y), 
                                     int(ring['size']), thickness)
        
        # Draw center glow
        alpha = int(self.life * 255)
        for i in range(5, 0, -1):
            size = int(self.size * (i / 5))
            color_alpha = (*self.color, alpha // i)
            pygame.draw.circle(screen, color_alpha, (x, y), size)

class GlowEffect:
    """Pulsing glow effect"""
    def __init__(self, x, y, color, duration, max_size=20):
        self.x = x
        self.y = y
        self.color = color
        self.duration = duration
        self.max_duration = duration
        self.size = max_size // 3
        self.max_size = max_size
        
    def update(self):
        self.duration -= 1
        pulse = math.sin((self.max_duration - self.duration) * 0.2)
        self.size = self.max_size * (0.7 + pulse * 0.3)
        return self.duration > 0
    
    def draw(self, screen, offset=(0, 0)):
        alpha = int((self.duration / self.max_duration) * 150)
        x = int(self.x + offset[0])
        y = int(self.y + offset[1])
        
        for i in range(4):
            size = int(self.size - i * 5)
            if size > 0:
                color_alpha = (*self.color, alpha // (i + 1))
                pygame.draw.circle(screen, color_alpha, (x, y), size)

class TrailPoint:
    """Smooth trail effect"""
    def __init__(self, x, y, color, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.life = 1.0
    
    def update(self):
        self.life -= 0.05
        self.size = max(0, self.size - 0.1)
        return self.life > 0
    
    def draw(self, screen, offset=(0, 0)):
        if self.size > 0:
            alpha = int(self.life * 200)
            x = int(self.x + offset[0])
            y = int(self.y + offset[1])
            pygame.draw.circle(screen, (*self.color, alpha), (x, y), int(self.size))

class EmotionalCharacter:
    """Character with emotions and animations"""
    def __init__(self, x, y, color, ai, is_adaptive=False):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.target_x = x
        self.target_y = y
        self.color = color
        self.ai = ai
        self.name = ai.name
        self.is_adaptive = is_adaptive
        
        # Character properties
        self.size = 80
        self.score = 0
        self.last_move = None
        self.emotion = EMOTION_NEUTRAL
        self.emotion_intensity = 0
        
        # Animation states
        self.move_animation = 0
        self.thinking_time = 0
        self.celebration_animation = 0
        self.defeat_animation = 0
        self.pulse = 0
        self.bounce = 0
        self.shake_offset = (0, 0)
        
        # Visual effects
        self.strategy_display = ""
        self.strategy_display_time = 0
        self.win_streak = 0
        self.particles_enabled = True
        
    def set_emotion(self, emotion, intensity=1.0):
        """Set character emotion"""
        self.emotion = emotion
        self.emotion_intensity = intensity
        
    def move_towards(self, target_x, target_y, speed=12):
        """Smooth cinematic movement"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > speed:
            # Easing function for smooth movement
            ease_factor = min(1.0, distance / 200)
            actual_speed = speed * ease_factor
            self.x += dx / distance * actual_speed
            self.y += dy / distance * actual_speed
            return False
        else:
            self.x = target_x
            self.y = target_y
            return True
    
    def update(self, vfx_manager, sound_manager):
        """Update character state and animations"""
        # Update animations
        self.pulse = (self.pulse + 0.1) % (2 * math.pi)
        self.bounce = math.sin(self.pulse) * 5
        
        if self.move_animation > 0:
            self.move_animation -= 1
            
        if self.thinking_time > 0:
            self.thinking_time -= 1
            # Add thinking particles
            if self.thinking_time % 15 == 0:
                vfx_manager.add_particles(
                    self.x, self.y - self.size - 40,
                    NEON_BLUE, 3, (2, 4), (-2, 2), -0.05
                )
            
        if self.celebration_animation > 0:
            self.celebration_animation -= 1
            # Celebration effects
            if self.celebration_animation % 10 == 0:
                vfx_manager.add_particles(
                    self.x + random.randint(-30, 30),
                    self.y + random.randint(-30, 30),
                    self.color, 8, (4, 8), (-4, 4), 0.1
                )
            
        if self.defeat_animation > 0:
            self.defeat_animation -= 1
            # Shake effect for defeat
            self.shake_offset = (
                random.randint(-3, 3),
                random.randint(-3, 3)
            )
        else:
            self.shake_offset = (0, 0)
            
        if self.strategy_display_time > 0:
            self.strategy_display_time -= 1
            
        # Decay emotion intensity
        self.emotion_intensity = max(0, self.emotion_intensity - 0.01)
        
        # Trail effect during movement
        if abs(self.x - self.target_x) > 2 or abs(self.y - self.target_y) > 2:
            if random.random() < 0.3:
                vfx_manager.add_trail(self.x, self.y, self.color, 6)
    
    def draw(self, screen, font, small_font, offset=(0, 0)):
        """Draw character with emotions"""
        draw_x = int(self.x + self.shake_offset[0] + offset[0])
        draw_y = int(self.y + self.bounce + self.shake_offset[1] + offset[1])
        
        # Pulsing aura based on emotion
        pulse_size = self.size + math.sin(self.pulse) * 10
        if self.emotion_intensity > 0:
            aura_color = self.get_emotion_color()
            aura_alpha = int(self.emotion_intensity * 100)
            
            for i in range(3):
                aura_surf = pygame.Surface((pulse_size * 2 + 20, pulse_size * 2 + 20), pygame.SRCALPHA)
                pygame.draw.circle(aura_surf, (*aura_color, aura_alpha // (i + 1)),
                                 (pulse_size + 10, pulse_size + 10), pulse_size + i * 10)
                screen.blit(aura_surf, (draw_x - pulse_size - 10, draw_y - pulse_size - 10))
        
        # Character body with gradient
        body_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Draw layered circles for depth
        for i in range(3):
            size_offset = i * 3
            alpha = 255 - i * 40
            pygame.draw.circle(body_surf, (*self.color, alpha),
                             (self.size, self.size), self.size - size_offset)
        
        # Outline
        pygame.draw.circle(body_surf, (255, 255, 255, 200),
                         (self.size, self.size), self.size, 4)
        
        screen.blit(body_surf, (draw_x - self.size, draw_y - self.size))
        
        # Draw face based on emotion
        self.draw_face(screen, draw_x, draw_y)
        
        # Draw move indicator with dramatic effects
        if self.last_move and self.move_animation > 0:
            self.draw_move_indicator(screen, draw_x, draw_y, font)
        
        # Strategy display for adaptive AI
        if self.is_adaptive and self.strategy_display_time > 0:
            self.draw_strategy_display(screen, draw_x, draw_y, font, small_font)
        
        # Name and score with better positioning
        self.draw_info(screen, draw_x, draw_y, font)
    
    def draw_face(self, screen, x, y):
        """Draw expressive face based on emotion"""
        face_color = (255, 255, 255)
        
        # Eye positions
        left_eye_x = x - 20
        right_eye_x = x + 20
        eye_y = y - 15
        
        if self.emotion == EMOTION_HAPPY:
            # Happy eyes (curved)
            pygame.draw.arc(screen, face_color,
                          (left_eye_x - 10, eye_y - 5, 20, 15),
                          math.pi, 2 * math.pi, 4)
            pygame.draw.arc(screen, face_color,
                          (right_eye_x - 10, eye_y - 5, 20, 15),
                          math.pi, 2 * math.pi, 4)
            # Big smile
            pygame.draw.arc(screen, face_color,
                          (x - 25, y, 50, 35),
                          0, math.pi, 5)
            # Rosy cheeks
            pygame.draw.circle(screen, (255, 150, 150, 100), (x - 35, y + 5), 8)
            pygame.draw.circle(screen, (255, 150, 150, 100), (x + 35, y + 5), 8)
            
        elif self.emotion == EMOTION_SAD:
            # Sad eyes - slightly downturned
            pygame.draw.ellipse(screen, face_color, (left_eye_x - 8, eye_y - 4, 16, 10))
            pygame.draw.ellipse(screen, face_color, (right_eye_x - 8, eye_y - 4, 16, 10))

            # Downturned eyebrows
            pygame.draw.arc(screen, face_color, 
                           (left_eye_x - 12, eye_y - 15, 20, 12),
                           math.pi, 2 * math.pi, 3)
            pygame.draw.arc(screen, face_color,
                           (right_eye_x - 8, eye_y - 15, 20, 12),
                           math.pi, 2 * math.pi, 3)

            # Deep frown
            pygame.draw.arc(screen, face_color,
                           (x - 25, y + 15, 50, 30),
                           math.pi, 2 * math.pi, 4)

            # Tears flowing down
            for i in range(2):
                tear_y = eye_y + 10 + i * 8
                pygame.draw.ellipse(screen, (100, 150, 255), 
                                   (left_eye_x - 2, tear_y, 4, 8))
                pygame.draw.ellipse(screen, (100, 150, 255), 
                                   (right_eye_x - 2, tear_y, 4, 8))

            # Droopy eyelids
            pygame.draw.arc(screen, face_color,
                           (left_eye_x - 8, eye_y - 6, 16, 8),
                           0, math.pi, 2)
            pygame.draw.arc(screen, face_color,
                           (right_eye_x - 8, eye_y - 6, 16, 8),
                           0, math.pi, 2)
            
        elif self.emotion == EMOTION_THINKING:
            # Focused eyes
            pygame.draw.circle(screen, face_color, (left_eye_x, eye_y), 8)
            pygame.draw.circle(screen, face_color, (right_eye_x, eye_y), 8)
            pygame.draw.circle(screen, (50, 50, 50), (left_eye_x, eye_y), 4)
            pygame.draw.circle(screen, (50, 50, 50), (right_eye_x + 3, eye_y), 4)
            # Neutral mouth
            pygame.draw.line(screen, face_color, (x - 15, y + 20), (x + 15, y + 20), 3)
            # Thought lines
            for i in range(3):
                pygame.draw.line(screen, face_color,
                               (x + 30, y - 30 + i * 10),
                               (x + 40, y - 35 + i * 10), 2)
                
        elif self.emotion == EMOTION_DETERMINED:
            # Determined eyes
            pygame.draw.line(screen, face_color, (left_eye_x - 12, eye_y - 5),
                           (left_eye_x + 12, eye_y + 5), 5)
            pygame.draw.line(screen, face_color, (right_eye_x - 12, eye_y - 5),
                           (right_eye_x + 12, eye_y + 5), 5)
            # Determined mouth
            pygame.draw.line(screen, face_color, (x - 20, y + 20), (x + 20, y + 20), 5)
            # Eyebrows
            pygame.draw.line(screen, face_color, (left_eye_x - 15, eye_y - 15),
                           (left_eye_x + 10, eye_y - 18), 4)
            pygame.draw.line(screen, face_color, (right_eye_x - 10, eye_y - 18),
                           (right_eye_x + 15, eye_y - 15), 4)
            
        elif self.emotion == EMOTION_SURPRISED:
            # Wide eyes
            pygame.draw.circle(screen, face_color, (left_eye_x, eye_y), 12)
            pygame.draw.circle(screen, (50, 50, 50), (left_eye_x, eye_y), 8)
            pygame.draw.circle(screen, face_color, (right_eye_x, eye_y), 12)
            pygame.draw.circle(screen, (50, 50, 50), (right_eye_x, eye_y), 8)
            # Open mouth
            pygame.draw.circle(screen, face_color, (x, y + 25), 12)
            
        elif self.emotion == EMOTION_ANGRY:
            # Angry eyes
            pygame.draw.line(screen, face_color, (left_eye_x - 12, eye_y - 8),
                           (left_eye_x + 12, eye_y), 5)
            pygame.draw.line(screen, face_color, (right_eye_x - 12, eye_y),
                           (right_eye_x + 12, eye_y - 8), 5)
            # Angry mouth
            pygame.draw.arc(screen, face_color,
                          (x - 20, y + 15, 40, 20),
                          math.pi, 2 * math.pi, 4)
            # Red face tint
            red_surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(red_surf, (255, 0, 0, 50), (self.size // 2, self.size // 2), self.size // 2)
            screen.blit(red_surf, (x - self.size // 2, y - self.size // 2))
            
        else:  # EMOTION_NEUTRAL
            # Normal eyes
            pygame.draw.circle(screen, face_color, (left_eye_x, eye_y), 10)
            pygame.draw.circle(screen, (50, 50, 50), (left_eye_x, eye_y), 5)
            pygame.draw.circle(screen, face_color, (right_eye_x, eye_y), 10)
            pygame.draw.circle(screen, (50, 50, 50), (right_eye_x, eye_y), 5)
            # Neutral mouth
            pygame.draw.line(screen, face_color, (x - 15, y + 20), (x + 15, y + 20), 3)
    
    def draw_move_indicator(self, screen, x, y, font):
        """Draw animated move indicator"""
        move_color = COOP_COLOR if self.last_move == 'C' else DEFECT_COLOR
        move_text = "COOPERATE" if self.last_move == 'C' else "DEFECT"
        move_emoji = "🤝" if self.last_move == 'C' else "⚔️"
        
        # Bouncing indicator
        bounce = math.sin(self.move_animation * 0.3) * 15
        indicator_y = y - self.size - 100 - bounce
        
        # Background circle
        circle_size = 50 + (60 - self.move_animation) // 2
        pygame.draw.circle(screen, move_color, (int(x), int(indicator_y)), circle_size)
        pygame.draw.circle(screen, (255, 255, 255), (int(x), int(indicator_y)), circle_size, 4)
        
        # Emoji - try common system emoji fonts, fall back to default
        emoji_font = None
        for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
            try:
                emoji_font = pygame.font.SysFont(_name, 48)
                if emoji_font:
                    break
            except Exception:
                emoji_font = None
        if not emoji_font:
            emoji_font = pygame.font.Font(None, 48)
        emoji_surf = emoji_font.render(move_emoji, True, (255, 255, 255))
        screen.blit(emoji_surf, (x - emoji_surf.get_width() // 2, indicator_y - 20))
        
        # Text label
        label_font = pygame.font.Font(None, 24)
        label_surf = label_font.render(move_text, True, (255, 255, 255))
        label_surf.set_alpha(int((self.move_animation / 90) * 255))
        screen.blit(label_surf, (x - label_surf.get_width() // 2, indicator_y + 30))
    
    def draw_strategy_display(self, screen, x, y, font, small_font):
        """Draw strategy information"""
        strategy_y = y - self.size - 150
        
        # Strategy name with background
        strategy_text = small_font.render(self.strategy_display, True, NEON_BLUE)
        bg_rect = pygame.Rect(x - strategy_text.get_width() // 2 - 10,
                            strategy_y - 5,
                            strategy_text.get_width() + 20,
                            strategy_text.get_height() + 10)
        
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (0, 0, 0, 180), (0, 0, bg_rect.width, bg_rect.height), border_radius=10)
        pygame.draw.rect(bg_surf, (*NEON_BLUE, 200), (0, 0, bg_rect.width, bg_rect.height), 2, border_radius=10)
        
        screen.blit(bg_surf, bg_rect)
        screen.blit(strategy_text, (x - strategy_text.get_width() // 2, strategy_y))
    
    def draw_info(self, screen, x, y, font):
        """Draw name and score with better layout"""
        info_y = y + self.size + 20
        
        # Background panel
        panel_width = 250
        panel_height = 70
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (*self.color, 150),
                        (0, 0, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(panel_surf, (255, 255, 255, 200),
                        (0, 0, panel_width, panel_height), 3, border_radius=15)
        
        screen.blit(panel_surf, (x - panel_width // 2, info_y))
        
        # Name
        name_font = pygame.font.Font(None, 32)
        name_surf = name_font.render(self.name, True, (255, 255, 255))
        screen.blit(name_surf, (x - name_surf.get_width() // 2, info_y + 10))
        
        # Score with color coding
        score_color = NEON_GREEN if self.score > 0 else NEON_PINK if self.score < 0 else (255, 255, 255)
        score_font = pygame.font.Font(None, 36)
        score_surf = score_font.render(f"Score: {self.score}", True, score_color)
        screen.blit(score_surf, (x - score_surf.get_width() // 2, info_y + 35))
    
    def get_emotion_color(self):
        """Get color associated with current emotion"""
        emotion_colors = {
            EMOTION_HAPPY: (100, 255, 100),
            EMOTION_SAD: (100, 100, 255),
            EMOTION_THINKING: (255, 255, 100),
            EMOTION_DETERMINED: (255, 150, 0),
            EMOTION_SURPRISED: (255, 100, 255),
            EMOTION_ANGRY: (255, 50, 50),
            EMOTION_NEUTRAL: (200, 200, 200)
        }
        return emotion_colors.get(self.emotion, (255, 255, 255))
    
    def trigger_celebration(self, vfx_manager, sound_manager):
        """Trigger victory celebration"""
        self.celebration_animation = 120
        self.set_emotion(EMOTION_HAPPY, 1.0)
        sound_manager.play_sound("laugh")
        
        # Explosion of particles
        vfx_manager.add_explosion_particles(self.x, self.y, self.color, 60)
        vfx_manager.add_explosion(self.x, self.y, self.color, 80)
    
    def trigger_defeat(self, vfx_manager, sound_manager):
        """Trigger defeat animation"""
        self.defeat_animation = 100
        self.set_emotion(EMOTION_SAD, 1.0)
        sound_manager.play_sound("gasp")
        
        # Sad particles falling
        vfx_manager.add_particles(self.x, self.y, (100, 100, 255), 30, (4, 8), (-2, 2), 0.3)
    
    def show_strategy_change(self, strategy, vfx_manager, sound_manager):
        """Show dramatic strategy change"""
        strategy_name = strategy.replace('_', ' ').title()
        self.strategy_display = f"⚡ {strategy_name}"
        self.strategy_display_time = 180
        self.set_emotion(EMOTION_DETERMINED, 0.8)
        
        # Visual effects
        vfx_manager.add_strategy_indicator(self.x, self.y - self.size, strategy_name, NEON_BLUE)
        vfx_manager.add_explosion(self.x, self.y, NEON_BLUE, 60)
        sound_manager.play_sound("power_up")

class AnimatedBackground:
    """Cinematic animated background"""
    def __init__(self):
        self.stars = []
        self.nebula_particles = []
        self.grid_offset = 0
        self.wave_offset = 0
        
        # Create stars
        for _ in range(200):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.1, 1.5),
                'size': random.randint(1, 5),
                'brightness': random.uniform(0.3, 1.0),
                'twinkle_phase': random.uniform(0, 2 * math.pi)
            })
        
        # Create nebula effect
        for _ in range(50):
            self.nebula_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(50, 200),
                'color': random.choice([
                    (100, 50, 150), (50, 100, 200), (150, 50, 100), (50, 150, 150)
                ]),
                'alpha': random.randint(5, 20),
                'drift_speed': random.uniform(0.05, 0.2),
                'drift_angle': random.uniform(0, 2 * math.pi)
            })
    
    def update(self):
        """Update background animations"""
        self.grid_offset = (self.grid_offset + 0.5) % 50
        self.wave_offset = (self.wave_offset + 0.02) % (2 * math.pi)
        
        # Update stars
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
            star['twinkle_phase'] += 0.05
        
        # Update nebula
        for particle in self.nebula_particles:
            particle['x'] += math.cos(particle['drift_angle']) * particle['drift_speed']
            particle['y'] += math.sin(particle['drift_angle']) * particle['drift_speed']
            
            # Wrap around screen
            if particle['x'] < -particle['size']:
                particle['x'] = SCREEN_WIDTH + particle['size']
            elif particle['x'] > SCREEN_WIDTH + particle['size']:
                particle['x'] = -particle['size']
            
            if particle['y'] < -particle['size']:
                particle['y'] = SCREEN_HEIGHT + particle['size']
            elif particle['y'] > SCREEN_HEIGHT + particle['size']:
                particle['y'] = -particle['size']
    
    def draw(self, screen):
        """Draw cinematic background"""
        # Base gradient
        for y in range(0, SCREEN_HEIGHT, 4):
            progress = y / SCREEN_HEIGHT
            r = int(8 + math.sin(progress * math.pi + self.wave_offset) * 5)
            g = int(10 + math.sin(progress * math.pi + self.wave_offset + 1) * 5)
            b = int(25 + math.sin(progress * math.pi + self.wave_offset + 2) * 10)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y), 4)
        
        # Draw nebula
        for particle in self.nebula_particles:
            surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*particle['color'], particle['alpha']),
                             (particle['size'], particle['size']), particle['size'])
            
            # Apply gaussian blur effect by drawing multiple circles
            for i in range(3):
                size = particle['size'] - i * 20
                if size > 0:
                    alpha = particle['alpha'] // (i + 1)
                    pygame.draw.circle(surf, (*particle['color'], alpha),
                                     (particle['size'], particle['size']), size)
            
            screen.blit(surf, (particle['x'] - particle['size'], particle['y'] - particle['size']))
        
        # Draw animated grid
        grid_color = (40, 40, 80)
        for x in range(int(-self.grid_offset), SCREEN_WIDTH, 50):
            alpha = int(100 + math.sin(x * 0.05 + self.wave_offset) * 50)
            pygame.draw.line(screen, (*grid_color, alpha), (x, 0), (x, SCREEN_HEIGHT), 1)
        
        for y in range(int(-self.grid_offset), SCREEN_HEIGHT, 50):
            alpha = int(100 + math.sin(y * 0.05 + self.wave_offset) * 50)
            pygame.draw.line(screen, (*grid_color, alpha), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw stars with twinkling
        for star in self.stars:
            twinkle = math.sin(star['twinkle_phase']) * 0.5 + 0.5
            brightness = int(star['brightness'] * 255 * twinkle)
            color = (brightness, brightness, brightness)
            
            # Draw star with glow
            if star['size'] > 2:
                glow_size = star['size'] + 3
                for i in range(3):
                    alpha = brightness // (i + 2)
                    pygame.draw.circle(screen, (*color, alpha),
                                     (int(star['x']), int(star['y'])), glow_size - i)
            
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])


class IndustryGradeGame:
    """Industry-grade AI Strategy Battle Game"""
    def __init__(self):
        # Screen setup
        if FULLSCREEN:
            # Use (0, 0) to let SDL use native resolution, or use actual screen dimensions
            try:
                # Try with native resolution first
                self.screen = pygame.display.set_mode((0, 0), 
                                                    pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
                # Get the actual size that was set
                actual_width, actual_height = self.screen.get_size()
                # Update global constants to match actual screen size
                global SCREEN_WIDTH, SCREEN_HEIGHT, CENTER_X, CENTER_Y
                SCREEN_WIDTH = actual_width
                SCREEN_HEIGHT = actual_height
                CENTER_X = SCREEN_WIDTH // 2
                CENTER_Y = SCREEN_HEIGHT // 2
            except:
                # Fallback: use explicit dimensions
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                                                    pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        pygame.display.set_caption("AI Strategy Battle Arena - Industry Edition")
        self.clock = pygame.time.Clock()
        
        # Fonts - Scale with screen size
        font_scale = min(SCREEN_WIDTH / 1920, SCREEN_HEIGHT / 1080)
        self.title_font = pygame.font.Font(None, int(96 * font_scale))
        self.subtitle_font = pygame.font.Font(None, int(48 * font_scale))
        self.font = pygame.font.Font(None, int(42 * font_scale))
        self.small_font = pygame.font.Font(None, int(28 * font_scale))
        self.tiny_font = pygame.font.Font(None, int(20 * font_scale))
        
        # Systems
        self.vfx_manager = EnhancedVFXManager()
        self.background = AnimatedBackground()
        self.sound_manager = AdvancedSoundManager()
        self.music_system = ProceduralMusicSystem()
        self.cinematic = CinematicEffect()
        
        # Load sounds and music
        self.sound_manager.load_sounds()
        
        # Game state
        self.state = INTRO
        self.intro_timer = 0
        self.outro_timer = 0
        self.max_intro_time = 300  # 5 seconds
        self.transition_alpha = 0
        self.transition_direction = 0  # 0 = fade in, 1 = fade out
        
        # Setup game
        self.setup_game()
        
        # Start intro music
        self.music_system.play_track("intro")
    
    def setup_game(self):
        """Initialize game state"""
        self.round_number = 0
        self.max_rounds = 25
        
        # Payoff matrix
        self.payoffs = {
            ('C', 'C'): (3, 3),
            ('C', 'D'): (0, 5),
            ('D', 'C'): (5, 0),
            ('D', 'D'): (1, 1)
        }
        
        # Available opponents
        self.opponent_types = [
            "cooperative", "aggressive", "random",
            "tit_for_tat", "forgiving", "strategic",
            "unpredictable", "exploitative", "mirror"
        ]
        
        # Strategy explanations
        self.strategy_explanations = {
            "minimax": "Maximizing minimum gain",
            "fuzzy": "Fuzzy logic reasoning",
            "tit_for_tat": "Mirroring with forgiveness",
            "adaptive": "Dynamic learning",
            "pattern_matcher": "Pattern exploitation",
            "bayesian": "Probabilistic inference"
        }
        
        # Create AIs and characters
        self.adaptive_ai = PowerfulAdaptiveAI()
        self.current_opponent_type = random.choice(self.opponent_types)
        self.opponent_ai = StrategicOpponentAI(self.current_opponent_type)
        
        # Character positions
        char1_x = SCREEN_WIDTH // 4
        char2_x = SCREEN_WIDTH * 3 // 4
        char_y = SCREEN_HEIGHT // 2
        
        self.player1 = EmotionalCharacter(char1_x, char_y, PLAYER1_COLOR, self.adaptive_ai, is_adaptive=True)
        self.player2 = EmotionalCharacter(char2_x, char_y, PLAYER2_COLOR, self.opponent_ai)
        
        # Game history
        self.history = []
        
        # Statistics
        self.adaptive_wins = 0
        self.opponent_wins = 0
        self.ties = 0
        
        # Auto-play settings
        self.auto_play = False
        self.auto_play_speed = 1.0
        self.round_transition = 0
        
        # UI button positions - Scale with screen
        button_width = int(250 * (SCREEN_WIDTH / 1920)+10)
        button_height = int(70 * (SCREEN_HEIGHT / 1080))
        button_y = SCREEN_HEIGHT - 150
        
        self.buttons = {
            'start': pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, button_y, button_width, button_height),
            'next_round': pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, button_y, button_width, button_height),
            'auto_play': pygame.Rect(SCREEN_WIDTH // 2 - button_width - 20, button_y + 90, button_width, button_height - 20),
            'change_opponent': pygame.Rect(SCREEN_WIDTH // 2 + 20, button_y + 90, button_width , button_height - 20),
            'skip': pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 80, 180, 50),
            'exit': pygame.Rect(20, 20, 100, 40)
        }
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Ensure autoplay is stopped before quitting
                try:
                    self.auto_play = False
                except Exception:
                    pass
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Stop autoplay when exiting via ESC
                    try:
                        self.auto_play = False
                    except Exception:
                        pass
                    return False
                elif event.key == pygame.K_f and self.state == MENU:
                    # Toggle fullscreen
                    pygame.display.toggle_fullscreen()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.sound_manager.play_sound("click")
                
                # Exit button (available in all states) - stop autoplay first
                if self.buttons['exit'].collidepoint(mouse_pos):
                    try:
                        self.auto_play = False
                    except Exception:
                        pass
                    return False
                
                if self.state == INTRO:
                    if self.buttons['skip'].collidepoint(mouse_pos):
                        self.transition_to_state(MENU)
                
                elif self.state == MENU:
                    if self.buttons['start'].collidepoint(mouse_pos):
                        self.start_battle()
                
                elif self.state == BATTLE:
                    if self.buttons['next_round'].collidepoint(mouse_pos) and self.round_transition == 0:
                        self.play_round()
                    elif self.buttons['auto_play'].collidepoint(mouse_pos):
                        self.auto_play = not self.auto_play
                        if self.auto_play:
                            self.sound_manager.play_sound("power_up")
                    elif self.buttons['change_opponent'].collidepoint(mouse_pos):
                        self.change_opponent()
                
                elif self.state == RESULTS:
                    if self.buttons['start'].collidepoint(mouse_pos):
                        self.reset_game()
                
                elif self.state == OUTRO:
                    if self.buttons['start'].collidepoint(mouse_pos):
                        self.transition_to_state(MENU)
        
        return True
    
    def transition_to_state(self, new_state):
        """Transition to new game state with effects"""
        self.state = new_state
        self.transition_alpha = 255
        self.transition_direction = 0
        
        # Play appropriate music
        if new_state == MENU:
            self.music_system.play_track("intro")
        elif new_state == BATTLE:
            self.music_system.play_track("battle")
        elif new_state == RESULTS:
            if self.player1.score > self.player2.score:
                self.music_system.play_track("victory")
            elif self.player1.score < self.player2.score:
                self.music_system.play_track("defeat")
        elif new_state == OUTRO:
            self.music_system.play_track("intro")
    
    def start_battle(self):
        """Start battle with cinematic intro"""
        self.transition_to_state(BATTLE)
        self.round_number = 0
        self.player1.score = 0
        self.player2.score = 0
        self.history = []
        self.auto_play = False
        
        # Reset AIs
        self.adaptive_ai.reset()
        self.opponent_ai.reset()
        
        # Reset character states
        self.player1.set_emotion(EMOTION_DETERMINED, 0.8)
        self.player2.set_emotion(EMOTION_DETERMINED, 0.8)
        
        # Cinematic entrance
        self.player1.target_x = SCREEN_WIDTH // 3
        self.player2.target_x = SCREEN_WIDTH * 2 // 3
        
        # Camera shake for dramatic effect
        self.cinematic.add_shake(15, 30)
        self.sound_manager.play_sound("whoosh")
    
    def reset_game(self):
        """Reset game to menu"""
        self.transition_to_state(MENU)
        self.player1.score = 0
        self.player2.score = 0
        self.history = []
        
        # Reset positions
        self.player1.target_x = SCREEN_WIDTH // 4
        self.player2.target_x = SCREEN_WIDTH * 3 // 4
        
        self.player1.set_emotion(EMOTION_NEUTRAL, 0.5)
        self.player2.set_emotion(EMOTION_NEUTRAL, 0.5)
    
    def change_opponent(self):
        """Change opponent with effects"""
        current_index = self.opponent_types.index(self.current_opponent_type)
        next_index = (current_index + 1) % len(self.opponent_types)
        self.current_opponent_type = self.opponent_types[next_index]
        self.opponent_ai = StrategicOpponentAI(self.current_opponent_type)
        self.player2.ai = self.opponent_ai
        self.player2.name = self.opponent_ai.name
        
        # Effects
        self.vfx_manager.add_explosion(self.player2.x, self.player2.y, PLAYER2_COLOR, 70)
        self.sound_manager.play_sound("power_up")
        self.player2.set_emotion(EMOTION_DETERMINED, 1.0)
    
    def play_round(self):
        """Play a round with cinematic effects"""
        if self.round_number >= self.max_rounds:
            self.end_game()
            return
        
        # Thinking phase
        self.player1.thinking_time = 60
        self.player2.thinking_time = 60
        self.player1.set_emotion(EMOTION_THINKING, 0.7)
        self.player2.set_emotion(EMOTION_THINKING, 0.7)
        self.sound_manager.play_sound("think")
        
        # Store old strategy
        old_strategy = self.player1.ai.current_strategy if hasattr(self.player1.ai, 'current_strategy') else None
        
        # AI decisions
        move1 = self.player1.ai.decide_move(self.round_number, self.player1.score, self.player2.score)
        move2 = self.player2.ai.decide_move(self.round_number, self.player2.score, self.player1.score)
        
        # Update histories
        self.player1.ai.my_history.append(move1)
        self.player1.ai.opp_history.append(move2)
        self.player2.ai.my_history.append(move2)
        self.player2.ai.opp_history.append(move1)
        
        # Calculate scores
        p1_score, p2_score = self.payoffs[(move1, move2)]
        self.player1.score += p1_score
        self.player2.score += p2_score
        
        # Update character states
        self.player1.last_move = move1
        self.player2.last_move = move2
        self.player1.move_animation = 90
        self.player2.move_animation = 90
        
        # Emotional responses based on outcome
        # Defecting agents show angry face, cooperators show appropriate reactions
        # Player1 emotions
        if move1 == 'D' and move2 == 'C':
            # Player1 defects while player2 cooperates - player1 shows angry (defector)
            self.player1.set_emotion(EMOTION_ANGRY, 0.8)
        elif move1 == 'C' and move2 == 'D':
            # Player1 cooperates but player2 defects - player1 shows sad (victim)
            self.player1.set_emotion(EMOTION_SAD, 0.7)
        elif move1 == 'D' and move2 == 'D':
            # Both defect - both show angry
            self.player1.set_emotion(EMOTION_ANGRY, 0.8)
        elif move1 == 'C' and move2 == 'C':
            # Both cooperate - both show happy
            self.player1.set_emotion(EMOTION_HAPPY, 0.5)
        else:
            self.player1.set_emotion(EMOTION_NEUTRAL, 0.3)
        
        # Player2 emotions
        if move2 == 'D' and move1 == 'C':
            # Player2 defects while player1 cooperates - player2 shows angry (defector)
            self.player2.set_emotion(EMOTION_ANGRY, 0.8)
        elif move2 == 'C' and move1 == 'D':
            # Player2 cooperates but player1 defects - player2 shows sad (victim)
            self.player2.set_emotion(EMOTION_SAD, 0.7)
        elif move2 == 'D' and move1 == 'D':
            # Both defect - both show angry
            self.player2.set_emotion(EMOTION_ANGRY, 0.8)
        elif move2 == 'C' and move1 == 'C':
            # Both cooperate - both show happy
            self.player2.set_emotion(EMOTION_HAPPY, 0.5)
        else:
            self.player2.set_emotion(EMOTION_NEUTRAL, 0.3)
        
        # Strategy change effects
        if hasattr(self.player1.ai, 'current_strategy'):
            new_strategy = self.player1.ai.current_strategy
            if old_strategy and new_strategy != old_strategy:
                self.player1.show_strategy_change(new_strategy, self.vfx_manager, self.sound_manager)
        
        # Dramatic visual effects based on moves
        if move1 == 'C' and move2 == 'C':
            # Mutual cooperation - peaceful effects
            self.vfx_manager.add_beam(self.player1.x, self.player1.y,
                                     self.player2.x, self.player2.y,
                                     COOP_COLOR, 60, 8)
            self.vfx_manager.add_glow(self.player1.x, self.player1.y, COOP_COLOR, 50, 40)
            self.vfx_manager.add_glow(self.player2.x, self.player2.y, COOP_COLOR, 50, 40)
            self.sound_manager.play_sound("cooperate")
            
        elif move1 == 'D' and move2 == 'D':
            # Mutual defection - aggressive effects
            self.vfx_manager.add_lightning(self.player1.x, self.player1.y,
                                          self.player2.x, self.player2.y,
                                          DEFECT_COLOR, 12)
            self.vfx_manager.add_explosion_particles(
                (self.player1.x + self.player2.x) // 2,
                (self.player1.y + self.player2.y) // 2,
                DEFECT_COLOR, 40
            )
            self.sound_manager.play_sound("impact")
            self.cinematic.add_shake(8, 15)
            
        else:
            # Asymmetric - one wins, one loses
            if move1 == 'D' and move2 == 'C':
                # Player 1 exploits
                self.vfx_manager.add_lightning(self.player1.x, self.player1.y,
                                              self.player2.x, self.player2.y,
                                              PLAYER1_COLOR, 10)
                self.vfx_manager.add_explosion(self.player2.x, self.player2.y, PLAYER2_COLOR, 50)
            else:
                # Player 2 exploits
                self.vfx_manager.add_lightning(self.player2.x, self.player2.y,
                                              self.player1.x, self.player1.y,
                                              PLAYER2_COLOR, 10)
                self.vfx_manager.add_explosion(self.player1.x, self.player1.y, PLAYER1_COLOR, 50)
            
            self.sound_manager.play_sound("defect")
            self.sound_manager.play_sound("explosion")
            self.cinematic.add_shake(12, 20)
        
        # Score change text effects
        if p1_score > 0:
            self.vfx_manager.add_text_effect(
                f"+{p1_score}",
                self.player1.x, self.player1.y - 120,
                NEON_GREEN, 100, 3, 48
            )
        
        if p2_score > 0:
            self.vfx_manager.add_text_effect(
                f"+{p2_score}",
                self.player2.x, self.player2.y - 120,
                NEON_GREEN, 100, 3, 48
            )
        
        # Flash effect for dramatic moments
        if abs(p1_score - p2_score) >= 5:
            self.cinematic.add_flash(150)
        
        # Record history
        self.history.append((move1, move2, p1_score, p2_score))
        self.round_number += 1
        self.round_transition = 60
        
        # Move characters together dramatically
        center_x = SCREEN_WIDTH // 2
        offset = 200
        self.player1.target_x = center_x - offset
        self.player2.target_x = center_x + offset
    
    def end_game(self):
        """End game with dramatic conclusion"""
        self.state = RESULTS
        
        # Determine winner and trigger appropriate celebrations
        if self.player1.score > self.player2.score:
            self.adaptive_wins += 1
            self.player1.trigger_celebration(self.vfx_manager, self.sound_manager)
            self.player2.trigger_defeat(self.vfx_manager, self.sound_manager)
            self.sound_manager.play_sound("win")
            
        elif self.player2.score > self.player1.score:
            self.opponent_wins += 1
            self.player2.trigger_celebration(self.vfx_manager, self.sound_manager)
            self.player1.trigger_defeat(self.vfx_manager, self.sound_manager)
            self.sound_manager.play_sound("lose")
            
        else:
            self.ties += 1
            self.player1.set_emotion(EMOTION_NEUTRAL, 0.5)
            self.player2.set_emotion(EMOTION_NEUTRAL, 0.5)
        
        # Camera effects
        self.cinematic.add_flash(200)
        self.cinematic.add_shake(20, 40)
        
        # Move characters to result positions
        self.player1.target_x = SCREEN_WIDTH // 3
        self.player2.target_x = SCREEN_WIDTH * 2 // 3
    
    def update(self):
        """Update game state"""
        # Update all systems
        self.background.update()
        self.vfx_manager.update()
        self.cinematic.update()
        
        # Update characters
        self.player1.update(self.vfx_manager, self.sound_manager)
        self.player2.update(self.vfx_manager, self.sound_manager)
        
        # Update transitions
        if self.transition_alpha > 0:
            self.transition_alpha = max(0, self.transition_alpha - 5)
        
        # State-specific updates
        if self.state == INTRO:
            self.intro_timer += 1
            if self.intro_timer >= self.max_intro_time:
                self.transition_to_state(MENU)
        
        elif self.state == BATTLE:
            # Auto-play mode
            if self.auto_play and self.round_number < self.max_rounds:
                if (self.player1.move_animation == 0 and
                    self.player2.move_animation == 0 and
                    self.round_transition == 0):
                    self.play_round()
            
            # Character movement
            self.player1.move_towards(self.player1.target_x, self.player1.target_y)
            self.player2.move_towards(self.player2.target_x, self.player2.target_y)
            
            # Round transition
            if self.round_transition > 0:
                self.round_transition -= 1
                if self.round_transition == 0:
                    # Reset positions
                    self.player1.target_x = SCREEN_WIDTH // 3
                    self.player2.target_x = SCREEN_WIDTH * 2 // 3
        
        elif self.state == RESULTS:
            # Smooth character movement
            self.player1.move_towards(self.player1.target_x, self.player1.target_y)
            self.player2.move_towards(self.player2.target_x, self.player2.target_y)
        
        elif self.state == OUTRO:
            self.outro_timer += 1
            if self.outro_timer >= 300:
                self.transition_to_state(MENU)
    
    def draw(self):
        """Main draw function"""
        offset = self.cinematic.get_offset()
        
        self.background.draw(self.screen)
        
        if self.state == INTRO:
            self.draw_intro()
        elif self.state == MENU:
            self.draw_menu(offset)
        elif self.state == BATTLE:
            self.draw_battle(offset)
        elif self.state == RESULTS:
            self.draw_results(offset)
        elif self.state == OUTRO:
            self.draw_outro()
        
        # Apply cinematic effects
        self.cinematic.apply_effects(self.screen)
        
        # Transition fade
        if self.transition_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.transition_alpha)
            self.screen.blit(fade_surf, (0, 0))
        
        # Draw exit button
        self.draw_exit_button()
        
        pygame.display.flip()
    
    def draw_intro(self):
        """Draw animated intro sequence"""
        progress = min(1.0, self.intro_timer / self.max_intro_time)
        
        # Title with scale and fade
        if progress < 0.3:
            title_progress = progress / 0.3
            scale = 0.5 + title_progress * 0.5
            alpha = int(title_progress * 255)
            
            title = self.title_font.render("AI STRATEGY", True, NEON_BLUE)
            title.set_alpha(alpha)
            
            scaled_w = int(title.get_width() * scale)
            scaled_h = int(title.get_height() * scale)
            scaled_title = pygame.transform.scale(title, (scaled_w, scaled_h))
            
            x = SCREEN_WIDTH // 2 - scaled_w // 2
            y = SCREEN_HEIGHT // 3 - scaled_h // 2
            
            self.screen.blit(scaled_title, (x, y))
            
            # Glow effect
            for i in range(3):
                glow_surf = pygame.Surface((scaled_w + i * 20, scaled_h + i * 20), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*NEON_BLUE, 30),
                               (0, 0, scaled_w + i * 20, scaled_h + i * 20))
                self.screen.blit(glow_surf, (x - i * 10, y - i * 10))
        
        # Battle Arena text
        if progress > 0.2:
            arena_progress = min(1.0, (progress - 0.2) / 0.2)
            alpha = int(arena_progress * 255)
            
            arena = self.title_font.render("BATTLE ARENA", True, NEON_PINK)
            arena.set_alpha(alpha)
            self.screen.blit(arena, (SCREEN_WIDTH // 2 - arena.get_width() // 2,
                                    SCREEN_HEIGHT // 2))
        
        # Feature list
        if progress > 0.5:
            features = [
                "🎯 Advanced AI Algorithms",
                "🎨 Cinematic Visual Effects",
                "🎵 Dynamic Procedural Music",
                "😊 Emotional Character Reactions",
                "⚡ Real-time Strategic Analysis"
            ]
            
            for i, feature in enumerate(features):
                feature_progress = min(1.0, (progress - 0.5 - i * 0.05) / 0.1)
                if feature_progress > 0:
                    alpha = int(feature_progress * 255)
                    y = SCREEN_HEIGHT * 0.65 + i * 40
                    x = SCREEN_WIDTH // 2 + (1 - feature_progress) * 100
                    
                    text = self.small_font.render(feature, True, TEXT_COLOR)
                    text.set_alpha(alpha)
                    self.screen.blit(text, (x - text.get_width() // 2, y))
        
        # Skip button
        if progress > 0.1:
            # Draw skip button with better emoji handling
            button = self.buttons.get('skip')
            if button:
                mouse_pos = pygame.mouse.get_pos()
                is_hover = button.collidepoint(mouse_pos)
                scale = 1.05 if is_hover else 1.0
                
                scaled_width = int(button.width * scale)
                scaled_height = int(button.height * scale)
                scaled_x = button.centerx - scaled_width // 2
                scaled_y = button.centery - scaled_height // 2
                
                # Draw button background without text
                self.draw_button('skip', "", alpha=200)
                
                # Emoji font setup
                emoji_font = None
                emoji_size = max(14, int(scaled_height * 0.6))
                for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
                    try:
                        emoji_font = pygame.font.SysFont(_name, emoji_size)
                        if emoji_font:
                            break
                    except Exception:
                        emoji_font = None
                if not emoji_font:
                    emoji_font = pygame.font.Font(None, emoji_size)
                
                # Regular text font
                try:
                    text_font = pygame.font.Font(None, max(12, int(scaled_height * 0.45)))
                except Exception:
                    text_font = self.font
                
                # Render emoji and text
                try:
                    emoji_surf = emoji_font.render("⏩", True, (0, 0, 0))
                except Exception:
                    emoji_surf = text_font.render(">>", True, (0, 0, 0))
                text_surf = text_font.render("SKIP INTRO", True, (0, 0, 0))
                
                # Center the emoji+text group in button
                spacing = 8
                total_width = emoji_surf.get_width() + spacing + text_surf.get_width()
                group_x = scaled_x + (scaled_width - total_width) // 2
                emoji_x = group_x
                text_x = group_x + emoji_surf.get_width() + spacing
                
                emoji_y = scaled_y + (scaled_height - emoji_surf.get_height()) // 2
                text_y = scaled_y + (scaled_height - text_surf.get_height()) // 2
                
                self.screen.blit(emoji_surf, (emoji_x, emoji_y))
                self.screen.blit(text_surf, (text_x, text_y))
        
        # Credits
        if progress > 0.8:
            credit_alpha = int((progress - 0.8) / 0.2 * 255)
            credit = self.small_font.render("© 2024 Neural Dynamics Studio", True, (150, 150, 150))
            credit.set_alpha(credit_alpha)
            self.screen.blit(credit, (SCREEN_WIDTH - credit.get_width() - 20, SCREEN_HEIGHT - 40))
    
    def draw_menu(self, offset=(0, 0)):
        """Draw main menu"""
        # Title
        title = self.title_font.render("AI STRATEGY ARENA", True, NEON_BLUE)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        title_y = int(SCREEN_HEIGHT * 0.15)
        
        # Title glow
        for i in range(5, 0, -1):
            glow = self.title_font.render("AI STRATEGY ARENA", True, (*NEON_BLUE, 50))
            self.screen.blit(glow, (title_x + i, title_y + i))
        
        self.screen.blit(title, (title_x, title_y))
        
        # Subtitle
        subtitle = self.subtitle_font.render("Adaptive AI vs Strategic Opponents", True, TEXT_COLOR)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, title_y + 100))
        
        # Draw characters
        self.vfx_manager.draw(self.screen, offset)
        self.player1.draw(self.screen, self.font, self.small_font, offset)
        self.player2.draw(self.screen, self.font, self.small_font, offset)
        
        # VS text
        vs_y = SCREEN_HEIGHT // 2 - 50
        vs_text = self.title_font.render("VS", True, NEON_YELLOW)
        vs_x = SCREEN_WIDTH // 2 - vs_text.get_width() // 2
        
        # Rotating effect
        angle = (pygame.time.get_ticks() // 20) % 360
        vs_rotated = pygame.transform.rotate(vs_text, math.sin(angle * 0.05) * 10)
        self.screen.blit(vs_rotated, (vs_x, vs_y))
        
        # Statistics panel
        stats_y = int(SCREEN_HEIGHT * 0.7)
        self.draw_stats_panel(stats_y)
        
        # Opponent info
        opp_info_y = stats_y + 80
        opp_text = self.small_font.render(
            f"Next Opponent: {self.opponent_ai.name} (Strength: {self.opponent_ai.get_strength()*100:.0f}%)",
            True, NEON_PINK
        )
        self.screen.blit(opp_text, (SCREEN_WIDTH // 2 - opp_text.get_width() // 2, opp_info_y))
        
        # Start button
        self.draw_button('start', "🚀 START BATTLE")
        
        # Instructions
        inst_text = self.tiny_font.render("Press ESC to exit | F to toggle fullscreen", True, (150, 150, 150))
        self.screen.blit(inst_text, (SCREEN_WIDTH // 2 - inst_text.get_width() // 2, SCREEN_HEIGHT - 30))
    
    def draw_stats_panel(self, y):
        """Draw statistics panel"""
        panel_width = 800
        panel_height = 60
        panel_x = SCREEN_WIDTH // 2 - panel_width // 2
        
        # Panel background
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (0, 0, 0, 180), (0, 0, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(panel_surf, (255, 255, 255, 100), (0, 0, panel_width, panel_height), 3, border_radius=15)
        self.screen.blit(panel_surf, (panel_x, y))
        
        # Set up emoji font for trophy/win indicator
        emoji_font = None
        emoji_size = max(14, int(panel_height * 0.4))
        for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
            try:
                emoji_font = pygame.font.SysFont(_name, emoji_size)
                if emoji_font:
                    break
            except Exception:
                emoji_font = None
        if not emoji_font:
            emoji_font = self.font

        # Stats text with emoji trophy for wins
        total_games = self.adaptive_wins + self.opponent_wins + self.ties
        if total_games > 0:
            win_rate = self.adaptive_wins / total_games * 100
            
            # Render emoji with proper sizing and positioning
            emoji_y_offset = -2  # Adjust vertical position of emoji
            try:
                win_symbol = emoji_font.render("🏆", True, NEON_GREEN)
                # Scale emoji if too large
                if win_symbol.get_height() > panel_height * 0.5:
                    scale = (panel_height * 0.5) / win_symbol.get_height()
                    new_size = (int(win_symbol.get_width() * scale), int(win_symbol.get_height() * scale))
                    win_symbol = pygame.transform.smoothscale(win_symbol, new_size)
            except Exception:
                win_symbol = self.small_font.render("W", True, NEON_GREEN)

            # Render text parts with consistent spacing
            spacing = " "  # Add consistent space before/after numbers
            p1_text = self.small_font.render(f"Adaptive AI:{spacing}{self.adaptive_wins}", True, NEON_GREEN)
            p2_text = self.small_font.render(f" | Opponents:{spacing}{self.opponent_wins}", True, NEON_GREEN)
            ties_text = self.small_font.render(f" | Ties:{spacing}{self.ties}", True, NEON_GREEN)
            rate_text = self.small_font.render(f" | Win Rate:{spacing}{win_rate:.1f}%", True, NEON_GREEN)
            
            # Calculate positions for centered layout
            total_width = (p1_text.get_width() + win_symbol.get_width() + p2_text.get_width() + 
                         win_symbol.get_width() + ties_text.get_width() + rate_text.get_width())
            start_x = SCREEN_WIDTH // 2 - total_width // 2
            center_y = y + (panel_height - p1_text.get_height()) // 2
            
            # Draw text parts with trophy emojis
            current_x = start_x
            # Draw text and emojis with consistent vertical alignment
            self.screen.blit(p1_text, (current_x, center_y))
            current_x += p1_text.get_width()
            emoji_y = center_y + emoji_y_offset
            self.screen.blit(win_symbol, (current_x, emoji_y))
            current_x += win_symbol.get_width() + 4  # Add small space after emoji
            
            self.screen.blit(p2_text, (current_x, center_y))
            current_x += p2_text.get_width()
            self.screen.blit(win_symbol, (current_x, emoji_y))
            current_x += win_symbol.get_width() + 4  # Add small space after emoji
            
            self.screen.blit(ties_text, (current_x, center_y))
            current_x += ties_text.get_width()
            self.screen.blit(rate_text, (current_x, center_y))
        else:
            # Initial state with no games played - use proper emoji rendering
            try:
                win_symbol = emoji_font.render("🏆", True, NEON_GREEN)
                if win_symbol.get_height() > panel_height * 0.5:
                    scale = (panel_height * 0.5) / win_symbol.get_height()
                    new_size = (int(win_symbol.get_width() * scale), int(win_symbol.get_height() * scale))
                    win_symbol = pygame.transform.smoothscale(win_symbol, new_size)
            except Exception:
                win_symbol = self.small_font.render("W", True, NEON_GREEN)

            # Split text into parts for proper emoji placement
            p1_text = self.small_font.render("Adaptive AI: 0", True, NEON_GREEN)
            p2_text = self.small_font.render(" | Opponents: 0", True, NEON_GREEN)
            rest_text = self.small_font.render(" | Ties: 0 | Win Rate: 0%", True, NEON_GREEN)
            
            total_width = (p1_text.get_width() + win_symbol.get_width() + p2_text.get_width() + 
                        win_symbol.get_width() + rest_text.get_width() + 8)  # 8 for spacing
            start_x = SCREEN_WIDTH // 2 - total_width // 2
            center_y = y + (panel_height - p1_text.get_height()) // 2
            emoji_y = center_y - 2  # Match the offset used above
            
            current_x = start_x
            self.screen.blit(p1_text, (current_x, center_y))
            current_x += p1_text.get_width()
            self.screen.blit(win_symbol, (current_x, emoji_y))
            current_x += win_symbol.get_width() + 4
            self.screen.blit(p2_text, (current_x, center_y))
            current_x += p2_text.get_width()
            self.screen.blit(win_symbol, (current_x, emoji_y))
            current_x += win_symbol.get_width() + 4
            self.screen.blit(rest_text, (current_x, center_y))
    
    def draw_battle(self, offset=(0, 0)):
        """Draw battle scene"""
        # Draw VFX first
        self.vfx_manager.draw(self.screen, offset)
        
        # Draw characters
        self.player1.draw(self.screen, self.font, self.small_font, offset)
        self.player2.draw(self.screen, self.font, self.small_font, offset)
        
        # Header panel
        header_height = 120
        header_surf = pygame.Surface((SCREEN_WIDTH, header_height), pygame.SRCALPHA)
        pygame.draw.rect(header_surf, (0, 0, 0, 200), (0, 0, SCREEN_WIDTH, header_height))
        self.screen.blit(header_surf, (0, 0))
        
        # Round counter with animation
        round_scale = 1 + math.sin(pygame.time.get_ticks() * 0.003) * 0.1
        round_font = pygame.font.Font(None, int(56 * round_scale))
        round_text = round_font.render(f"ROUND {self.round_number}/{self.max_rounds}", True, NEON_YELLOW)
        self.screen.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, 20))
        
        # Score display
        score_y = 75
        score_text = self.font.render(f"{self.player1.score}  :  {self.player2.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, score_y))
        
        # VS indicator
        vs_x = SCREEN_WIDTH // 2
        vs_y = SCREEN_HEIGHT // 2 - 60
        vs_size = 40 + math.sin(pygame.time.get_ticks() * 0.005) * 8
        # VS emoji - prefer emoji-capable system font when available
        vs_font = None
        for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
            try:
                vs_font = pygame.font.SysFont(_name, int(vs_size))
                if vs_font:
                    break
            except Exception:
                vs_font = None
        if not vs_font:
            vs_font = pygame.font.Font(None, int(vs_size))
        vs_text = vs_font.render("⚔️", True, NEON_ORANGE)
        self.screen.blit(vs_text, (vs_x - vs_text.get_width() // 2, vs_y))
        
        # Strategy info panel (positioned to avoid characters)
        self.draw_strategy_panel()
        
        # Bottom UI
        ui_y = SCREEN_HEIGHT - 200
        
        # Buttons
        self.draw_button('next_round', "🎯 NEXT ROUND" if not self.auto_play else "⏸️ PAUSE")
        
        # Render autoplay button with consistent emoji size
        button = self.buttons.get('auto_play')
        if button:
            mouse_pos = pygame.mouse.get_pos()
            is_hover = button.collidepoint(mouse_pos)
            scale = 1.05 if is_hover else 1.0
            
            scaled_width = int(button.width * scale)
            scaled_height = int(button.height * scale)
            scaled_x = button.centerx - scaled_width // 2
            scaled_y = button.centery - scaled_height // 2
            
            # Draw button background without text
            self.draw_button('auto_play', "", alpha=255)
            
            # Emoji font setup
            emoji_font = None
            emoji_size = max(14, int(scaled_height * 0.6))
            for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
                try:
                    emoji_font = pygame.font.SysFont(_name, emoji_size)
                    if emoji_font:
                        break
                except Exception:
                    emoji_font = None
            if not emoji_font:
                emoji_font = pygame.font.Font(None, emoji_size)
            
            # Regular text font
            try:
                text_font = pygame.font.Font(None, max(12, int(scaled_height * 0.45)))
            except Exception:
                text_font = self.font
            
            # Render appropriate emoji and text based on state
            emoji = "⏸️" if self.auto_play else "▶️"
            text = "STOP AUTO" if self.auto_play else "AUTO PLAY"
            
            try:
                emoji_surf = emoji_font.render(emoji, True, (0, 0, 0))
            except Exception:
                emoji_surf = text_font.render("||" if self.auto_play else ">", True, (0, 0, 0))
            text_surf = text_font.render(text, True, (0, 0, 0))
            
            # Center the emoji+text group in button
            spacing = 8
            total_width = emoji_surf.get_width() + spacing + text_surf.get_width()
            group_x = scaled_x + (scaled_width - total_width) // 2
            emoji_x = group_x
            text_x = group_x + emoji_surf.get_width() + spacing
            
            emoji_y = scaled_y + (scaled_height - emoji_surf.get_height()) // 2
            text_y = scaled_y + (scaled_height - text_surf.get_height()) // 2
            
            self.screen.blit(emoji_surf, (emoji_x, emoji_y))
            self.screen.blit(text_surf, (text_x, text_y))
        
        # Use a repeat emoji for change opponent for clarity
        self.draw_button('change_opponent', "🔁 CHANGE OPPONENT")
        
        # Progress bar
        self.draw_progress_bar()
    
    def draw_strategy_panel(self):
        """Draw strategy information as right-hand sidebar"""
        # Sidebar dimensions - slim and tall
        panel_width = min(320, int(SCREEN_WIDTH * 0.22))  # Narrower width
        panel_height = 280  # Taller for stacked content
        panel_x = SCREEN_WIDTH - panel_width - 20  # Right align
        panel_y = 140  # Start below header
        
        # Panel background
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (0, 0, 0, 200), (0, 0, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(panel_surf, (*NEON_BLUE, 160), (0, 0, panel_width, panel_height), 2, border_radius=15)
        self.screen.blit(panel_surf, (panel_x, panel_y))
        
        # Track content position
        text_y = panel_y + 15
        inner_x = panel_x + 12
        
        # Header with proper emoji rendering
        # Set up emoji font for header
        emoji_font = None
        emoji_size = max(14, int(32 * 0.8))  # 32 is the spacing we were using before
        for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
            try:
                emoji_font = pygame.font.SysFont(_name, emoji_size)
                if emoji_font:
                    break
            except Exception:
                emoji_font = None
        if not emoji_font:
            emoji_font = self.small_font
            
        # Render emoji and text separately
        try:
            emoji_surf = emoji_font.render("🧭", True, NEON_BLUE)
            if emoji_surf.get_height() > 24:  # Scale down if too large
                scale = 24 / emoji_surf.get_height()
                new_size = (int(emoji_surf.get_width() * scale), 24)
                emoji_surf = pygame.transform.smoothscale(emoji_surf, new_size)
        except Exception:
            emoji_surf = self.small_font.render("*", True, NEON_BLUE)
            
        text_surf = self.small_font.render(" Strategy Info", True, NEON_BLUE)
        
        # Draw both surfaces
        self.screen.blit(emoji_surf, (inner_x, text_y))
        self.screen.blit(text_surf, (inner_x + emoji_surf.get_width(), text_y))
        text_y += 32
        
        # Adaptive AI strategy - more compact
        if hasattr(self.player1.ai, 'current_strategy'):
            strategy_name = self.player1.ai.current_strategy.replace('_', ' ').title()
            label = self.tiny_font.render("Current Strategy:", True, TEXT_COLOR)
            self.screen.blit(label, (inner_x, text_y))
            text_y += 18
            
            strategy_text = self.tiny_font.render(strategy_name, True, NEON_GREEN)
            self.screen.blit(strategy_text, (inner_x + 8, text_y))
            text_y += 28
            
            # Explanation - wrap long text
            explanation = self.strategy_explanations.get(self.player1.ai.current_strategy, "Learning...")
            words = explanation.split()
            line = ""
            for word in words:
                if len(line) + len(word) + 1 <= 32:  # Wrap at ~32 chars
                    line = (line + " " + word).strip()
                else:
                    expl_text = self.tiny_font.render(line, True, NEON_PINK)
                    self.screen.blit(expl_text, (inner_x + 8, text_y))
                    text_y += 20
                    line = word
            if line:
                expl_text = self.tiny_font.render(line, True, NEON_PINK)
                self.screen.blit(expl_text, (inner_x + 8, text_y))
                text_y += 28
        
        # Opponent analysis - more compact
        if self.history:
            label = self.tiny_font.render("Opponent Pattern:", True, TEXT_COLOR)
            self.screen.blit(label, (inner_x, text_y))
            text_y += 18
            
            analysis_text, analysis_emoji = self.analyze_opponent_behavior()
            
            # Set up emoji font for analysis emoji
            emoji_font = None
            emoji_size = max(14, int(20 * 0.8))  # Slightly smaller than text height
            for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
                try:
                    emoji_font = pygame.font.SysFont(_name, emoji_size)
                    if emoji_font:
                        break
                except Exception:
                    emoji_font = None
            if not emoji_font:
                emoji_font = self.tiny_font
                
            # Render analysis text and emoji separately
            text_surf = self.tiny_font.render(analysis_text, True, NEON_GREEN)
            
            try:
                emoji_surf = emoji_font.render(analysis_emoji, True, NEON_GREEN)
                if emoji_surf.get_height() > 20:  # Scale down if too large
                    scale = 20 / emoji_surf.get_height()
                    new_size = (int(emoji_surf.get_width() * scale), 20)
                    emoji_surf = pygame.transform.smoothscale(emoji_surf, new_size)
            except Exception:
                emoji_surf = self.tiny_font.render("*", True, NEON_GREEN)
            
            # Draw text and emoji with spacing
            self.screen.blit(text_surf, (inner_x + 8, text_y))
            self.screen.blit(emoji_surf, (inner_x + 8 + text_surf.get_width() + 4, text_y))
            text_y += 32
        
        # Cooperation rates - stacked vertically
        if self.history:
            label = self.tiny_font.render("Cooperation:", True, TEXT_COLOR)
            self.screen.blit(label, (inner_x, text_y))
            text_y += 18
            
            p1_coop = sum(1 for move, _, _, _ in self.history if move == 'C') / len(self.history)
            p2_coop = sum(1 for _, move, _, _ in self.history if move == 'C') / len(self.history)
            
            p1_text = self.tiny_font.render(f"Adaptive AI: {p1_coop:.0%}", True, NEON_BLUE)
            p2_text = self.tiny_font.render(f"Opponent: {p2_coop:.0%}", True, NEON_PINK)
            
            self.screen.blit(p1_text, (inner_x + 8, text_y))
            self.screen.blit(p2_text, (inner_x + 8, text_y + 18))
    
    def draw_progress_bar(self):
        """Draw round progress bar"""
        bar_width = 600
        bar_height = 20
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 150
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        
        # Progress
        progress = self.round_number / self.max_rounds
        progress_width = int(bar_width * progress)
        
        # Gradient progress bar
        for i in range(progress_width):
            color_progress = i / bar_width
            r = int(NEON_BLUE[0] + (NEON_PINK[0] - NEON_BLUE[0]) * color_progress)
            g = int(NEON_BLUE[1] + (NEON_PINK[1] - NEON_BLUE[1]) * color_progress)
            b = int(NEON_BLUE[2] + (NEON_PINK[2] - NEON_BLUE[2]) * color_progress)
            pygame.draw.line(self.screen, (r, g, b), (bar_x + i, bar_y), (bar_x + i, bar_y + bar_height), 1)
        
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)
    
    def analyze_opponent_behavior(self):
        """Analyze opponent behavior pattern"""
        if not self.history:
            return "Analyzing..."
        
        opp_moves = [move for _, move, _, _ in self.history]
        coop_rate = opp_moves.count('C') / len(opp_moves)
        
        # Return text without emoji - emoji will be rendered separately
        if coop_rate > 0.8:
            return ("Highly Cooperative", "🤝")
        elif coop_rate > 0.6:
            return ("Mostly Cooperative", "😊")
        elif coop_rate > 0.4:
            return ("Balanced Strategy", "⚖️")
        elif coop_rate > 0.2:
            return ("Mostly Aggressive", "⚔️")
        else:
            return ("Highly Aggressive", "💥")
    
    def draw_results(self, offset=(0, 0)):
        """Draw results screen with celebration"""
        # Draw VFX
        self.vfx_manager.draw(self.screen, offset)
        
        # Draw characters
        self.player1.draw(self.screen, self.font, self.small_font, offset)
        self.player2.draw(self.screen, self.font, self.small_font, offset)
        
        # Results panel
        panel_width = 900
        panel_height = 600
        panel_x = SCREEN_WIDTH // 2 - panel_width // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
        
        # Panel with glow
        for i in range(5, 0, -1):
            panel_surf = pygame.Surface((panel_width + i * 10, panel_height + i * 10), pygame.SRCALPHA)
            alpha = 30 // i
            pygame.draw.rect(panel_surf, (*NEON_BLUE, alpha),
                           (0, 0, panel_width + i * 10, panel_height + i * 10), border_radius=25)
            self.screen.blit(panel_surf, (panel_x - i * 5, panel_y - i * 5))
        
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (0, 0, 0, 220), (0, 0, panel_width, panel_height), border_radius=20)
        pygame.draw.rect(panel_surf, (255, 255, 255, 150), (0, 0, panel_width, panel_height), 4, border_radius=20)
        self.screen.blit(panel_surf, (panel_x, panel_y))
        
        # Determine winner
        text_y = panel_y + 50
        
        if self.player1.score > self.player2.score:
            winner_text = "🏆 ADAPTIVE AI WINS! 🏆"
            winner_color = PLAYER1_COLOR
            result_emoji = "🎯✨"
        elif self.player2.score > self.player1.score:
            winner_text = f"🏆 {self.player2.name.upper()} WINS! 🏆"
            winner_color = PLAYER2_COLOR
            result_emoji = "💥⚡"
        else:
            winner_text = "⚖️ IT'S A TIE! ⚖️"
            winner_color = NEON_YELLOW
            result_emoji = "🤝✨"
        
        # Winner announcement
        winner_surf = self.title_font.render(winner_text, True, winner_color)
        self.screen.blit(winner_surf, (SCREEN_WIDTH // 2 - winner_surf.get_width() // 2, text_y))
        
        # Emoji
        text_y += 100
        # Result emoji - prefer emoji-capable system font when available
        emoji_font = None
        for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
            try:
                emoji_font = pygame.font.SysFont(_name, 72)
                if emoji_font:
                    break
            except Exception:
                emoji_font = None
        if not emoji_font:
            emoji_font = pygame.font.Font(None, 72)
        emoji_surf = emoji_font.render(result_emoji, True, winner_color)
        self.screen.blit(emoji_surf, (SCREEN_WIDTH // 2 - emoji_surf.get_width() // 2, text_y))
        
        # Scores
        text_y += 100
        p1_score_text = self.font.render(f"Adaptive AI: {self.player1.score} points", True, PLAYER1_COLOR)
        p2_score_text = self.font.render(f"{self.player2.name}: {self.player2.score} points", True, PLAYER2_COLOR)
        
        self.screen.blit(p1_score_text, (SCREEN_WIDTH // 2 - p1_score_text.get_width() // 2, text_y))
        self.screen.blit(p2_score_text, (SCREEN_WIDTH // 2 - p2_score_text.get_width() // 2, text_y + 50))
        
        # Statistics
        text_y += 120
        if self.history:
            p1_coop = sum(1 for move, _, _, _ in self.history if move == 'C') / len(self.history)
            p2_coop = sum(1 for _, move, _, _ in self.history if move == 'C') / len(self.history)
            mutual_coop = sum(1 for m1, m2, _, _ in self.history if m1 == 'C' and m2 == 'C')
            
            stats = [
                f"Cooperation Rates: {p1_coop:.0%} vs {p2_coop:.0%}",
                f"Mutual Cooperation: {mutual_coop} rounds",
                f"Total Rounds: {len(self.history)}"
            ]
            
            for stat in stats:
                stat_surf = self.small_font.render(stat, True, TEXT_COLOR)
                self.screen.blit(stat_surf, (SCREEN_WIDTH // 2 - stat_surf.get_width() // 2, text_y))
                text_y += 35
        
        # Play again button
        self.draw_button('start', "🔄 PLAY AGAIN")
    
    def draw_outro(self):
        """Draw outro sequence"""
        # Simple fade out with thank you message
        alpha = min(255, self.outro_timer * 2)
        
        thank_you = self.title_font.render("THANK YOU FOR PLAYING!", True, NEON_BLUE)
        thank_you.set_alpha(alpha)
        self.screen.blit(thank_you, (SCREEN_WIDTH // 2 - thank_you.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    
    def draw_button(self, button_key, text, alpha=255):
        """Draw animated button"""
        if button_key not in self.buttons:
            return
        
        button = self.buttons[button_key]
        mouse_pos = pygame.mouse.get_pos()
        is_hover = button.collidepoint(mouse_pos)
        
        # Button animation
        if is_hover:
            scale = 1.05
            color = BUTTON_HOVER
            glow_size = 8
        else:
            scale = 1.0
            color = BUTTON_COLOR
            glow_size = 4
        
        # Calculate scaled button
        scaled_width = int(button.width * scale)
        scaled_height = int(button.height * scale)
        scaled_x = button.centerx - scaled_width // 2
        scaled_y = button.centery - scaled_height // 2
        
        # Glow effect
        if is_hover:
            for i in range(glow_size, 0, -1):
                glow_rect = pygame.Rect(
                    scaled_x - i * 3, scaled_y - i * 3,
                    scaled_width + i * 6, scaled_height + i * 6
                )
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                glow_alpha = alpha // (i + 1)
                pygame.draw.rect(glow_surf, (*color, glow_alpha),
                               (0, 0, glow_rect.width, glow_rect.height), border_radius=15)
                self.screen.blit(glow_surf, glow_rect)
        
        # Main button
        button_surf = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(button_surf, (*color, alpha),
                        (0, 0, scaled_width, scaled_height), border_radius=12)
        pygame.draw.rect(button_surf, (255, 255, 255, alpha),
                        (0, 0, scaled_width, scaled_height), 4, border_radius=12)
        self.screen.blit(button_surf, (scaled_x, scaled_y))
        
        # Button text - use emoji-capable system font when the label contains emoji
        def _contains_emoji(s):
            try:
                return any((0x1F300 <= ord(ch) <= 0x1FAFF) or (0x2600 <= ord(ch) <= 0x26FF) or (0x1F000 <= ord(ch) <= 0x1FFFF) for ch in s)
            except Exception:
                return False

        if _contains_emoji(text):
            # Try common emoji-capable system fonts
            emoji_font = None
            # allow a larger emoji size for small buttons like exit
            size_multiplier = 0.45
            if button_key == 'exit':
                size_multiplier = 0.7
            font_size = max(12, int(scaled_height * size_multiplier))
            for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
                try:
                    emoji_font = pygame.font.SysFont(_name, font_size)
                    if emoji_font:
                        break
                except Exception:
                    emoji_font = None
            if not emoji_font:
                emoji_font = pygame.font.Font(None, font_size)
            text_surf = emoji_font.render(text, True, (0, 0, 0))
        else:
            # Regular text uses the game's main font
            # derive a font size that fits the button for consistency
            try:
                base_size = int(scaled_height * 0.45)
                text_font = pygame.font.Font(None, max(12, base_size))
            except Exception:
                text_font = self.font
            text_surf = text_font.render(text, True, (0, 0, 0))

        try:
            text_surf.set_alpha(alpha)
        except Exception:
            pass

        # Center text inside scaled button
        text_x = scaled_x + (scaled_width - text_surf.get_width()) // 2
        text_y = scaled_y + (scaled_height - text_surf.get_height()) // 2
        self.screen.blit(text_surf, (text_x, text_y))
    
    def draw_exit_button(self):
        """Draw exit button"""
        # Draw the base button (background, glow). We'll render the emoji and
        # label ourselves so we can control spacing and relative sizing.
        self.draw_button('exit', "", alpha=200)

        # Render a slightly smaller emoji and place it to the left of the text
        button = self.buttons.get('exit')
        if not button:
            return

        mouse_pos = pygame.mouse.get_pos()
        is_hover = button.collidepoint(mouse_pos)
        scale = 1.05 if is_hover else 1.0

        scaled_width = int(button.width * scale)
        scaled_height = int(button.height * scale)
        scaled_x = button.centerx - scaled_width // 2
        scaled_y = button.centery - scaled_height // 2

        # Emoji font slightly smaller to avoid dominating the small exit button
        emoji_font = None
        emoji_size = max(12, int(scaled_height * 0.55))
        for _name in ("Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", "Apple Color Emoji", "EmojiOne Color"):
            try:
                emoji_font = pygame.font.SysFont(_name, emoji_size)
                if emoji_font:
                    break
            except Exception:
                emoji_font = None
        if not emoji_font:
            emoji_font = pygame.font.Font(None, emoji_size)

        try:
            emoji_surf = emoji_font.render("❌", True, (0, 0, 0))
        except Exception:
            emoji_surf = emoji_font.render("X", True, (0, 0, 0))

        # Regular text font (match draw_button's non-emoji branch)
        try:
            text_font = pygame.font.Font(None, max(12, int(scaled_height * 0.45)))
        except Exception:
            text_font = self.font
        text_surf = text_font.render("EXIT", True, (0, 0, 0))

        # Spacing between emoji and text
        spacing = 8

        # Center the emoji+text group inside the scaled button
        total_width = emoji_surf.get_width() + spacing + text_surf.get_width()
        group_x = scaled_x + (scaled_width - total_width) // 2
        emoji_x = group_x
        text_x = group_x + emoji_surf.get_width() + spacing

        emoji_y = scaled_y + (scaled_height - emoji_surf.get_height()) // 2
        text_y = scaled_y + (scaled_height - text_surf.get_height()) // 2

        self.screen.blit(emoji_surf, (emoji_x, emoji_y))
        self.screen.blit(text_surf, (text_x, text_y))
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = IndustryGradeGame()
    game.run()