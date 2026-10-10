"""Star Fronteerer: repaired, frame-independent Pygame game loop."""
from pathlib import Path
import argparse
import math
import random
import sys

import pygame as pg

ROOT = Path(__file__).resolve().parent
SIZE = (1300, 800)


def load_image(name):
    """Assets are relative to this file, never the terminal working directory."""
    return pg.image.load(str(ROOT / name)).convert_alpha()


class Ship:
    def __init__(self, image, position, hp=100):
        self.original = image
        self.position = pg.Vector2(position)
        self.velocity = pg.Vector2()
        self.angle = 0.0
        self.hp = hp
        self.max_hp = hp
        self.flash = 0.0
        self.contact_cooldown = 0.0
        self.fire_cooldown = 0.0
        self.sync()

    @property
    def direction(self):
        return pg.Vector2(1, 0).rotate(-self.angle)

    def sync(self):
        self.image = pg.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pg.mask.from_surface(self.image)

    def timers(self, dt):
        self.flash = max(0.0, self.flash - dt)
        self.contact_cooldown = max(0.0, self.contact_cooldown - dt)
        self.fire_cooldown = max(0.0, self.fire_cooldown - dt)

    def damage(self, amount):
        if self.hp <= 0:
            return False
        self.hp = max(0, self.hp - amount)
        self.flash = 0.12
        return self.hp == 0

    def draw(self, surface, camera, debug=False):
        rect = self.rect.move(-round(camera.x), -round(camera.y))
        surface.blit(self.image, rect)
        if self.flash:
            glow = self.mask.to_surface(setcolor=(255, 210, 120, 100),
                                        unsetcolor=(0, 0, 0, 0))
            surface.blit(glow, rect)
        if debug:
            pg.draw.rect(surface, (50, 230, 160), rect, 1)


class Shot:
    def __init__(self, position, direction, owner, kind='bullet', frames=None,
                 inherited_velocity=(0, 0)):
        self.position = pg.Vector2(position)
        self.previous = self.position.copy()
        direction = pg.Vector2(direction)
        self.direction = direction.normalize() if direction.length_squared() else pg.Vector2(1, 0)
        self.owner = owner
        self.kind = kind
        self.damage = 2 if kind == 'photon' else 1
        self.age = 0.0
        self.lifetime = 3.0
        self.frames = frames
        speed = {'bullet': 760, 'projectile': 600, 'photon': 470}[kind]
        self.velocity = self.direction * speed + pg.Vector2(inherited_velocity)
        if frames:
            # Keep the original photon animation, at a practical collision size.
            self.frames = frames
            self.image = self.frames[0]
        else:
            self.image = pg.Surface((13, 9), pg.SRCALPHA)
            color = (255, 95, 85) if owner == 'enemy' else (255, 210, 80)
            if kind == 'projectile':
                color = (80, 230, 255) if owner == 'player' else color
            pg.draw.ellipse(self.image, color, (0, 1, 13, 7))
            pg.draw.ellipse(self.image, (255, 255, 240), (4, 2, 7, 5))
        self.sync()

    def sync(self):
        image = self.frames[int(self.age * 20) % len(self.frames)] if self.frames else self.image
        if self.frames:
            self.image = pg.transform.rotate(image, -self.direction.as_polar()[1])
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pg.mask.from_surface(self.image)

    def update(self, dt):
        self.previous = self.position.copy()
        self.position += self.velocity * dt
        self.age += dt
        self.sync()

    def hit_fraction(self, ship):
        """Sweep the image mask along the travelled segment to prevent tunnelling."""
        old_rect = self.image.get_rect(center=self.previous)
        if not old_rect.union(self.rect).colliderect(ship.rect):
            return None
        distance = self.previous.distance_to(self.position)
        steps = max(1, math.ceil(distance))
        for step in range(steps + 1):
            fraction = step / steps
            rect = self.image.get_rect(center=self.previous.lerp(self.position, fraction))
            if rect.colliderect(ship.rect) and ship.mask.overlap(
                    self.mask, (rect.x - ship.rect.x, rect.y - ship.rect.y)) is not None:
                return fraction
        return None


class Explosion:
    def __init__(self, position, size=1.0):
        self.position = pg.Vector2(position)
        self.age = 0.0
        self.duration = 0.65
        self.size = size
        self.particles = [(pg.Vector2(1, 0).rotate(random.randrange(360))
                           * random.uniform(40, 170) * size,
                           random.uniform(2, 5) * size) for _ in range(24)]

    def draw(self, surface, camera):
        center = self.position - camera
        remaining = max(0, 1 - self.age / self.duration)
        pg.draw.circle(surface, (255, int(160 * remaining), 35), center,
                       max(1, int((8 + self.age * 65) * self.size)), 2)
        for velocity, radius in self.particles:
            pos = center + velocity * self.age
            pg.draw.circle(surface, (255, int(220 * remaining), 70), pos,
                           max(1, int(radius * remaining)))


class Probe:
    def __init__(self, image, position, direction):
        self.image = image
        self.position = pg.Vector2(position)
        self.velocity = pg.Vector2(direction) * 95
        self.age = 0.0


class Starfield:
    def __init__(self):
        rng = random.Random(60)
        self.layers = []
        for count, parallax in [(180, 0.15), (120, 0.4), (80, 0.8)]:
            tile = pg.Surface(SIZE)
            tile.set_colorkey((0, 0, 0))
            for _ in range(count):
                color = rng.choice([(90, 115, 150), (180, 190, 210), (140, 210, 230)])
                pg.draw.circle(tile, color, (rng.randrange(SIZE[0]), rng.randrange(SIZE[1])), 1)
            self.layers.append((tile, parallax))

    def draw(self, surface, camera):
        surface.fill((5, 8, 19))
        for tile, factor in self.layers:
            x, y = (-camera.x * factor) % SIZE[0], (-camera.y * factor) % SIZE[1]
            for dx in (x - SIZE[0], x):
                for dy in (y - SIZE[1], y):
                    surface.blit(tile, (dx, dy))


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE, pg.RESIZABLE)
        pg.display.set_caption('Star Fronteerer — repaired edition')
        self.canvas = pg.Surface(SIZE)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 24)
        self.title_font = pg.font.Font(None, 48)
        self.ship_image = load_image('gx/ships/51.png')
        self.enemy_images = [load_image('gx/ships/ship91.png'), load_image('gx/ships/nmefleet.png')]
        self.base_image = load_image('gx/ships/base3.png')
        self.probe_image = load_image('gx/ships/probe.png')
        self.photon_frames = [pg.transform.smoothscale(load_image(f'pht/pht{i}.png'), (36, 20))
                              for i in range(1, 12)]
        self.thrust_frames = [load_image(f'thr/thr{i:02}.png') for i in range(1, 6)]
        self.stars = Starfield()
        self.running = True
        self.debug = False
        self.help = True
        self.warp_buttons = [pg.Rect(20 + i * 94, 64, 86, 30) for i in range(4)]
        self.reset()

    def reset(self):
        self.player = Ship(self.ship_image, (650, 400))
        self.camera = pg.Vector2()
        self.shots = []
        self.enemies = []
        self.explosions = []
        self.probes = []
        self.score = 0
        self.wave = 1
        self.wave_timer = 0.0
        self.fuel = 900000.0
        self.warp = 0
        self.paused = False
        self.game_over = False
        self.thrusting = False
        self.elapsed = 0.0
        self.spawn_wave()

    def spawn_wave(self):
        # Enemies start within reach so collision fixes can be tried immediately.
        for i in range(min(2 + self.wave - 1, 8)):
            offset = pg.Vector2(480 + i * 60, 0).rotate(i * 145)
            enemy = Ship(self.enemy_images[i % 2], self.player.position + offset, hp=4)
            enemy.fire_cooldown = 1.5 + i * 0.4
            self.enemies.append(enemy)

    def fire(self, ship, owner, kind):
        start = ship.position + ship.direction * (max(ship.image.get_size()) / 2 + 12)
        self.shots.append(Shot(start, ship.direction, owner, kind,
                               self.photon_frames if kind == 'photon' else None,
                               ship.velocity))

    def destroy_enemy(self, enemy):
        self.explosions.append(Explosion(enemy.position))
        self.enemies.remove(enemy)
        self.score += 100

    def hurt_player(self, amount):
        if self.player.damage(amount):
            self.explosions.append(Explosion(self.player.position, 1.6))
            self.game_over = True

    def resolve_hits(self):
        for shot in self.shots[:]:
            targets = self.enemies if shot.owner == 'player' else ([self.player] if self.player.hp else [])
            hits = []
            for target in targets:
                fraction = shot.hit_fraction(target)
                if fraction is not None:
                    hits.append((fraction, target))
            if hits:
                _, target = min(hits, key=lambda item: item[0])
                self.shots.remove(shot)
                if shot.owner == 'player':
                    if target.damage(shot.damage):
                        self.destroy_enemy(target)
                else:
                    self.hurt_player(shot.damage * 5)
            elif shot.age >= shot.lifetime:
                self.shots.remove(shot)
        if not self.game_over and not self.player.contact_cooldown:
            for enemy in self.enemies[:]:
                if self.player.rect.colliderect(enemy.rect) and self.player.mask.overlap(
                        enemy.mask, (enemy.rect.x - self.player.rect.x,
                                     enemy.rect.y - self.player.rect.y)) is not None:
                    self.hurt_player(10)
                    if enemy.damage(1):
                        self.destroy_enemy(enemy)
                    self.player.contact_cooldown = 1.0
                    break

    def update(self, dt, keys=None, mouse=None):
        if self.paused:
            return
        self.elapsed += dt
        self.player.timers(dt)
        if not self.game_over:
            keys = pg.key.get_pressed() if keys is None else keys
            if mouse is None:
                mouse = list(pg.mouse.get_pressed())
                if self.screen_point(pg.mouse.get_pos()).y < 110:
                    mouse[0] = False
            turn = int(bool(keys[pg.K_LEFT])) - int(bool(keys[pg.K_RIGHT]))
            self.player.angle = (self.player.angle + turn * 160 * dt) % 360
            self.thrusting = bool((keys[pg.K_UP] or mouse[0]) and self.fuel > 0)
            thrust = int(self.thrusting) - int(bool(keys[pg.K_DOWN] or mouse[1]))
            if self.fuel > 0:
                self.player.velocity += self.player.direction * thrust * 220 * dt
                self.fuel = max(0, self.fuel - abs(thrust) * (1 + self.warp * 4) * 25 * dt)
            if keys[pg.K_h]:
                self.player.velocity *= math.exp(-5 * dt)
            speed_limit = [280, 520, 850, 1300][self.warp]
            if self.player.velocity.length() > speed_limit:
                self.player.velocity.scale_to_length(speed_limit)
            self.player.position += self.player.velocity * dt
            self.player.sync()
            if self.player.fire_cooldown <= 0:
                kind = 'photon' if keys[pg.K_SPACE] else ('projectile' if keys[pg.K_f] else ('bullet' if mouse[2] else None))
                if kind:
                    self.fire(self.player, 'player', kind)
                    self.player.fire_cooldown = 0.35 if kind == 'photon' else 0.14
        for enemy in self.enemies:
            enemy.timers(dt)
            delta = self.player.position - enemy.position
            distance = delta.length()
            if distance:
                direction = delta / distance
                enemy.angle = -direction.as_polar()[1]
                enemy.velocity = direction * (95 if distance > 240 else (-55 if distance < 170 else 0))
            else:
                enemy.velocity.update(0, 0)
            if not self.game_over:
                enemy.position += enemy.velocity * dt
            enemy.sync()
            if not self.game_over and distance < 1000 and enemy.fire_cooldown <= 0:
                self.fire(enemy, 'enemy', 'projectile')
                enemy.fire_cooldown = 1.4
        for shot in self.shots:
            shot.update(dt)
        self.resolve_hits()
        for effect in self.explosions:
            effect.age += dt
        self.explosions = [effect for effect in self.explosions if effect.age < effect.duration]
        for probe in self.probes:
            probe.position += probe.velocity * dt
            probe.age += dt
        self.probes = [probe for probe in self.probes if probe.age < 30]
        if not self.enemies and not self.game_over:
            self.wave_timer += dt
            if self.wave_timer >= 3:
                self.wave += 1
                self.wave_timer = 0
                self.spawn_wave()
        self.camera = self.player.position - pg.Vector2(SIZE) / 2

    def screen_point(self, position):
        width, height = self.screen.get_size()
        return pg.Vector2(position[0] * SIZE[0] / width, position[1] * SIZE[1] / height)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_r:
                    self.reset()
                elif event.key == pg.K_TAB and not self.game_over:
                    self.paused = not self.paused
                elif event.key == pg.K_F1:
                    self.help = not self.help
                elif event.key == pg.K_F2:
                    self.debug = not self.debug
                elif pg.K_1 <= event.key <= pg.K_4:
                    self.warp = event.key - pg.K_1
                elif event.key == pg.K_p and not self.paused and not self.game_over and len(self.probes) < 20:
                    self.probes.append(Probe(self.probe_image, self.player.position, self.player.direction))
            elif event.type == pg.MOUSEWHEEL and not self.paused and not self.game_over:
                self.player.angle = (self.player.angle + event.y * 12) % 360
                self.player.sync()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = self.screen_point(event.pos)
                for i, rect in enumerate(self.warp_buttons):
                    if rect.collidepoint(pos):
                        self.warp = i

    def text(self, value, position, color=(210, 225, 242), font=None):
        self.canvas.blit((font or self.font).render(value, True, color), position)

    def draw(self):
        self.stars.draw(self.canvas, self.camera)
        base_rect = self.base_image.get_rect(center=pg.Vector2(300, 300) - self.camera)
        self.canvas.blit(self.base_image, base_rect)
        for probe in self.probes:
            self.canvas.blit(probe.image, probe.image.get_rect(center=probe.position - self.camera))
        for enemy in self.enemies:
            enemy.draw(self.canvas, self.camera, self.debug)
            rect = enemy.rect.move(-round(self.camera.x), -round(self.camera.y))
            pg.draw.rect(self.canvas, (60, 30, 35), (rect.x, rect.y - 9, rect.w, 4))
            pg.draw.rect(self.canvas, (255, 110, 90), (rect.x, rect.y - 9, int(rect.w * enemy.hp / enemy.max_hp), 4))
        for shot in self.shots:
            rect = shot.image.get_rect(center=shot.position - self.camera)
            self.canvas.blit(shot.image, rect)
            if self.debug:
                pg.draw.rect(self.canvas, (255, 220, 90), rect, 1)
        if not self.game_over:
            if self.thrusting:
                image = pg.transform.rotate(self.thrust_frames[int(self.elapsed * 20) % 5], self.player.angle)
                pos = self.player.position - self.player.direction * 32 - self.camera
                self.canvas.blit(image, image.get_rect(center=pos))
            self.player.draw(self.canvas, self.camera, self.debug)
        for effect in self.explosions:
            effect.draw(self.canvas, self.camera)
        panel = pg.Surface((SIZE[0], 110), pg.SRCALPHA)
        panel.fill((10, 18, 34, 230))
        self.canvas.blit(panel, (0, 0))
        self.text('STAR FRONTEERER', (20, 17), (95, 220, 245))
        self.text(f'Shields {self.player.hp:3d}   Fuel {self.fuel:,.0f}   Speed {self.player.velocity.length():.0f} px/s', (285, 17))
        self.text(f'Score {self.score}   Wave {self.wave}   Enemies {len(self.enemies)}', (890, 17))
        for i, rect in enumerate(self.warp_buttons):
            pg.draw.rect(self.canvas, (35, 115, 155) if i == self.warp else (27, 42, 61), rect, border_radius=5)
            self.text(f'Warp {i}', (rect.x + 10, rect.y + 6))
        self.text('F1 Help  |  F2 Hitboxes  |  Tab Pause  |  R Restart', (460, 72))
        # Direction arrows keep distant enemies findable during exploration.
        view = self.canvas.get_rect().inflate(-80, -140)
        for enemy in self.enemies:
            point = enemy.position - self.camera
            if not view.collidepoint(point):
                delta = point - pg.Vector2(SIZE) / 2
                factor = min(570 / max(abs(delta.x), 1), 270 / max(abs(delta.y), 1))
                tip = pg.Vector2(SIZE) / 2 + delta * factor
                direction = delta.normalize()
                pg.draw.polygon(self.canvas, (255, 115, 95), [tip + direction * 10,
                    tip - direction * 7 + direction.rotate(90) * 6,
                    tip - direction * 7 - direction.rotate(90) * 6])
        if self.help:
            self.text('Arrows: thrust/reverse/turn   H: brake   Wheel: turn   1–4: warp   P: probe', (20, 735))
            self.text('Space: photon (2 damage)   F: projectile   Right mouse: bullets   Left mouse: thrust', (20, 765))
        if self.paused or self.game_over:
            overlay = pg.Surface(SIZE, pg.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            self.canvas.blit(overlay, (0, 0))
            self.text('SHIP DESTROYED' if self.game_over else 'PAUSED', (490, 340), font=self.title_font)
            self.text('Press R to restart' if self.game_over else 'Press Tab to resume', (535, 400))
        pg.transform.scale(self.canvas, self.screen.get_size(), self.screen)
        pg.display.flip()

    def run(self, frames=None, screenshot=None):
        count = 0
        while self.running and (frames is None or count < frames):
            dt = min(self.clock.tick(60) / 1000.0, 0.05)
            self.events()
            self.update(dt)
            self.draw()
            count += 1
        if screenshot:
            pg.image.save(self.canvas, screenshot)
        pg.quit()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frames', type=int, help='Run a limited number of frames for a smoke test')
    parser.add_argument('--screenshot', help='Save the last game frame as PNG')
    args = parser.parse_args()
    try:
        Game().run(args.frames, args.screenshot)
    except (FileNotFoundError, pg.error) as error:
        pg.quit()
        print(f'Unable to start Star Fronteerer: {error}\nExtract the whole archive, including gx, pht and thr.', file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
