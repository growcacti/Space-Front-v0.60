# Star Fronteerer — repaired edition

A repaired version of John's original space game, using the original ship,
base, photon, thruster and probe artwork. Run **main.py** in the top-level
folder. The original Python files are preserved in `legacy/` for reference;
they are not used by the repaired game.

## Install and start

Extract the entire archive first. Keep `gx/`, `pht/`, and `thr/` next to main.py.
You can open main.py in IDLE and press F5 after installing pygame-ce in the
same Python interpreter that IDLE uses.

### Linux / MX Linux

Open a terminal in the extracted game folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

If Python reports that venv or Tkinter is missing, install the corresponding
packages for your Python installation. A separately installed Python may use
different packages from the distribution's Python.

### Windows

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

After setup, `start_game.sh` or `start_game.bat` uses the local `.venv` when
present. The Linux script can also be run with `bash start_game.sh`.
Both launchers work from other directories.

pygame-ce is a Pygame-compatible package imported as `pygame`. This edition
was tested with Python 3.12.14 and pygame-ce 2.5.8. Other Python versions have
not been tested here. Avoid installing both pygame and pygame-ce in the same
virtual environment.

## Controls

| Action | Control |
| --- | --- |
| Thrust | Up arrow or left mouse, outside the top control panel |
| Reverse thrust | Down arrow or middle mouse |
| Turn | Left/right arrows or mouse wheel |
| Brake | H |
| Photon: two damage per hit | Space |
| Projectile: one damage per hit | F |
| Bullet: one damage per hit | Right mouse |
| Select warp 0–3 | Keys 1–4 or click a Warp button |
| Launch probe | P |
| Pause / resume | Tab |
| Restart | R |
| Show / hide help | F1 |
| Show / hide collision rectangles | F2 |
| Exit | Escape or close window |

A ship keeps drifting after thrust is released. Turning changes its heading;
new thrust changes its movement direction. Use H to slow down.

## Combat

Enemies start nearby, pursue you, and retreat if they get too close. Red bars
show their remaining health. Each enemy has four health points: four ordinary
hits or two photon hits destroy it. Destroyed enemies disappear, produce an
animated particle explosion, and award 100 points. A new wave arrives three
seconds after the last enemy is destroyed. Later waves have more enemies, up
to eight.

Enemy shots remove five shield points; a ship collision removes ten, with a
one-second contact cooldown. At zero shields your ship explodes and you can
restart with R. Projectiles continue moving after the fire button is released.
They expire after three seconds, even off screen.

Probes drift for 30 seconds, with at most 20 deployed at once. Resource
collection is not implemented. The base is decorative. There are no sounds,
planet orbit scenes, save games, or fuel pickups in this edition.

## Repairs and improvements

- Every ship, projectile and probe uses world coordinates. Camera subtraction
  happens only when drawing. This fixes the original collision mismatch.
- Rotated ship images have matching rectangles and pixel masks. Transparent
  parts of an image do not register a hit.
- Projectile collision sweeps the distance travelled each frame. A fast shot
  can hit a target between its old and new positions.
- Each projectile damages only the first target it reaches and is then removed.
- Enemy health, hit flashes, destruction, explosions, score, player shields,
  game over, restart, and waves are implemented.
- Time comes from a capped 60 FPS clock. The player updates once per frame;
  movement, firing and animation use elapsed seconds.
- Firing from enemies and the player is kept separate. Each enemy aims toward
  the player rather than adding unrelated direction vectors.
- Input no longer refers to an old or undefined event outside the event loop.
  Unreachable duplicate event branches have been removed from the active loop.
- Warp selection persists and responds to clicks rather than mouse hovering.
- Probe launching no longer calls missing velocity attributes.
- Assets are resolved relative to main.py, allowing launch from IDLE or another
  directory. Display initialization occurs during game startup, not import.
- The expensive experimental background setup is replaced with cached,
  repeating star layers. The unused 85 MB original background image is omitted from this smaller download.
- Resizing scales a fixed logical canvas; game coordinates stay consistent.
- Clearer HUD, help, health bars, distant-enemy arrows, pause, and debug outlines.

The original experimental modules have not been modernized individually.
Use the repaired main.py; running an old file from legacy may still produce
its original errors. The specific warnings from your own machine were not
provided, so any remaining warning should be copied with its complete text.

## Verification

```bash
python test_game.py
```

Nine headless regression tests cover fast projectiles, transparent pixels,
nearest-target selection, repeated damage, enemy destruction and explosion
expiry, photon/enemy damage, camera independence, movement after releasing
fire, pause, projectile expiry, frame-independent movement, restart and waves.

For a short startup test:

```bash
python main.py --frames 120 --screenshot preview.png
```

The repaired entry point also completed this test with warnings treated as
errors. Testing used a headless display; interactive play on your own Linux
or Windows system remains to be checked.
