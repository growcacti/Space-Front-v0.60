"""Headless regression checks: python test_game.py."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
from collections import defaultdict
import pygame as pg
from main import Game, Ship, Shot


class CombatTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.enemies.clear()
        self.keys = defaultdict(bool)

    def tearDown(self):
        pg.quit()

    def target(self, position=(760, 400), hp=4):
        image = pg.Surface((30, 30), pg.SRCALPHA)
        image.fill('white')
        target = Ship(image, position, hp)
        self.game.enemies.append(target)
        return target

    def test_fast_shot_crossing_target(self):
        target = self.target()
        shot = Shot((600, 400), (1, 0), 'player')
        shot.update(0.4)
        self.game.shots.append(shot)
        self.game.resolve_hits()
        self.assertEqual(target.hp, 3)
        self.assertFalse(self.game.shots)
        self.game.resolve_hits()
        self.assertEqual(target.hp, 3)

    def test_transparent_pixels_are_not_hits(self):
        image = pg.Surface((80, 80), pg.SRCALPHA)
        pg.draw.rect(image, 'white', (0, 0, 8, 8))
        target = Ship(image, (700, 400), 4)
        shot = Shot((700, 400), (1, 0), 'player')
        self.assertIsNone(shot.hit_fraction(target))

    def test_four_hits_destroy_once(self):
        target = self.target()
        for _ in range(4):
            self.game.shots.append(Shot(target.position, (1, 0), 'player'))
            self.game.resolve_hits()
        self.assertFalse(self.game.enemies)
        self.assertEqual(self.game.score, 100)
        self.assertEqual(len(self.game.explosions), 1)
        self.assertFalse(target.damage(1))
        for _ in range(45):
            self.game.update(1 / 60, self.keys, (False,) * 3)
        self.assertFalse(self.game.explosions)

    def test_photon_damage_and_enemy_damage(self):
        target = self.target()
        self.game.shots.append(Shot(target.position, (1, 0), 'player', 'photon', self.game.photon_frames))
        self.game.resolve_hits()
        self.assertEqual(target.hp, 2)
        self.game.shots.append(Shot(self.game.player.position, (1, 0), 'enemy'))
        self.game.resolve_hits()
        self.assertEqual(self.game.player.hp, 95)
        self.assertFalse(self.game.shots)

    def test_camera_does_not_change_hits(self):
        target = self.target((100760, -9600))
        self.game.camera.update(100000, -10000)
        self.game.shots.append(Shot(target.position, (1, 0), 'player'))
        self.game.resolve_hits()
        self.assertEqual(target.hp, 3)

    def test_nearest_target_takes_hit(self):
        farther = self.target((900, 400))
        nearer = self.target((750, 400))
        shot = Shot((600, 400), (1, 0), 'player')
        shot.update(0.5)
        self.game.shots.append(shot)
        self.game.resolve_hits()
        self.assertEqual(nearer.hp, 3)
        self.assertEqual(farther.hp, 4)

    def test_release_fire_pause_and_expiry(self):
        shot = Shot((0, 0), (1, 0), 'player')
        self.game.shots.append(shot)
        self.game.update(0.05, self.keys, (False,) * 3)
        self.assertGreater(shot.position.x, 0)
        position = shot.position.copy()
        self.game.paused = True
        self.game.update(0.05, self.keys, (False,) * 3)
        self.assertEqual(shot.position, position)
        self.game.paused = False
        for _ in range(65):
            self.game.update(0.05, self.keys, (False,) * 3)
        self.assertNotIn(shot, self.game.shots)

    def test_movement_is_frame_independent(self):
        self.keys[pg.K_UP] = True
        for _ in range(60):
            self.game.update(1 / 60, self.keys, (False,) * 3)
        speed = self.game.player.velocity.length()
        position = self.game.player.position.copy()
        self.game.reset()
        self.game.enemies.clear()
        for _ in range(120):
            self.game.update(1 / 120, self.keys, (False,) * 3)
        self.assertAlmostEqual(self.game.player.velocity.length(), speed, places=6)
        self.assertLess(self.game.player.position.distance_to(position), 1)

    def test_game_over_restart_and_wave(self):
        self.game.hurt_player(100)
        self.assertTrue(self.game.game_over)
        self.assertEqual(len(self.game.explosions), 1)
        self.game.reset()
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.player.hp, 100)
        self.assertEqual(len(self.game.enemies), 2)
        self.game.enemies.clear()
        for _ in range(190):
            self.game.update(1 / 60, self.keys, (False,) * 3)
        self.assertEqual(self.game.wave, 2)
        self.assertEqual(len(self.game.enemies), 3)


if __name__ == '__main__':
    unittest.main()
