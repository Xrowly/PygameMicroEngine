# Pygame Micro Engine

A **lightweight, modular micro–game engine** built on top of [Pygame], designed for quick prototypes, 2D games and demo concepts. Includes a **Scene Manager**, **Entities**, **UI Widgets**, **Lighting/FX**, **Camera** with deadzone, and a **simple ballistic physics module**.

> 🚧 **Status:** Pre-MVP / Work-in-Progress — this is an early-stage prototype, intended as a learning and experimentation project.

---

## Highlights

- 🎛️ **Scene System**: `AbstractScene` + `SceneManager` for clean scene transitions.
- 🧩 **Entities**: Sprite–based characters with helpers for movement, collisions, and clamping to viewport.
- 🖱️ **UI**: `Button` with hover/click/outline text and callbacks.
- 💡 **Lighting/FX**: `SpotLight` (elliptical beam) + `circle_light_mask` (radial gradient glow).
- 🎥 **Camera**: Horizontal camera with **deadzone** and world boundary clamping.
- 🧮 **Physics**: Simple ballistic motion (`projectile`) with gravity in **pixels** (g = 9.8 * 64).
- 📈 **Perf HUD**: `FrameRateDisplay` (FPS + avg frame time, rounded to even numbers for stability).
- 🧱 **Custom draw pipeline**: `CustomGroup` prefers `sprite.draw()` if available, otherwise blit.

---

## Project Structure

```text
PygameMicroEngine-master/
├── assets/
│   ├── ElementMakes/
│   │   └── final/
│   │       ├── BM/
│   │       ├── Shadow/
│   │       ├── Versions/
│   │       ├── background/
│   │       └── pale/
│   └── fonts/
│       └── OFL.txt
├── game.py
├── game2.py
├── physics_engine/
│   ├── __init__.py
│   └── tract.py
├── renderer/
│   ├── FrameRater.py
│   ├── Light.py
│   ├── UI/
│   │   ├── __init__.py
│   │   ├── button.py
│   │   ├── fancy_text.py
│   │   └── tamplate.py
│   ├── __init__.py
│   ├── camera.py
│   └── group_overide.py
├── scenes/
│   ├── Scene0.py
│   └── __init__.py
└── system/
    ├── GameGlobals.py
    ├── __init__.py
    ├── abstract_scene.py
    ├── entities/
    │   ├── __init__.py
    │   ├── character.py
    │   ├── mary.py
    │   └── stickfigure.py
    └── manager.py
```

---

## Quick Start

```bash
# 1) (Optional) Create virtual environment
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install pygame

# 3) Run (through scene manager)
python game2.py
# or: directly run demo loop
python game.py
```

> By default runs in **FULLSCREEN 800×600**. For windowed mode, change:
> `pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))` (remove `pygame.FULLSCREEN`).

---

## Architecture

```
[Scenes]  ─▶  SceneManager  ─▶  Game Loop  ─▶  Renderer / UI / Physics
   ▲                 │
   │                 └── enter / exit / handle_events / update / draw
   │
[Entities] ── sprite components (character, Mary, stickfigure)
```
## Demo / Playground

The included demo scripts (`game.py` / `game2.py`) show a **very experimental version** of the engine:

- The **main character can roam freely**; enemies are static and don’t do anything.  
- A **“Click Me” button** appears in a random location and barely does anything.  
- **Flashlight system** works, reacting dynamically to the mouse/player position.  
- **Projectile physics** are functional — press **Space** to see debug mode in action.  
- **Camera system is in progress** — some behaviors may not be fully implemented yet.  
- **Scenes, entities, UI, lighting, and simple physics** are demonstrated.  
- The **`assets/`** folder contains some basic images and fonts preloaded — not a polished demo, just enough to get things running.

> ⚠️ This is a playground, not a polished demo. Everything is experimental and intended for exploration — feel free to experiment, break stuff, and learn from it.
### Core Modules

- **`system/abstract_scene.py` → `AbstractScene`**
  - Contract: `enter() · exit() · handle_events(events) · update(dt) · draw(screen)`

- **`system/manager.py` → `SceneManager`**
  - `switch_to(scene)`: Exits current scene (if any) and calls `enter()` on the new one.
  - Delegates `handle_events(events)`, `update(dt)`, `draw(screen)` to current scene.

- **`system/GameGlobals.py`**
  - Global `scene_manager` (see `game2.py`) for switching scenes from anywhere.

- **`renderer/FrameRater.py` → `FrameRateDisplay`**
  - Displays FPS and **avg frame time** (ms) with smooth even rounding.

- **`renderer/Light.py`**
  - `SpotLight`: elliptical gradient beam, `create_beam()`, `draw(surface, pos, target, rotation)`
  - `circle_light_mask(radius, steps, alpha)`: radial gradient (glow/fuse effects).

- **`renderer/camera.py` → `Camera`**
  - Deadzone–based horizontal tracking, `apply(rect)` returns render offset.

- **`renderer/UI/button.py` → `Button`**
  - Hover/click states, customizable **colors** and **border**, `FancyText` outline,
    `click_callback(button)` for actions.

- **`renderer/UI/fancy_text.py` → `FancyText`**
  - `render(text, text_color, outline_color, outline_thickness)` with custom TTF font (e.g., *Creepster*).

- **`renderer/group_overide.py` → `CustomGroup`**
  - `draw(surface)`: calls `sprite.draw(surface)` if available — enables custom pipelines.

- **`physics_engine/tract.py`**
  - `projectile(coords, speed, angle, t)`: **ballistics** with `g = 9.8*64` (pixels/s²).
    - `traj()`, `update(dt)`, `position_at(t)`

- **`system/entities/*.py`**
  - `Character`: image loading, movement, demo **fuse glow** with `circle_light_mask`.
  - `Mary`/`stickfigure`: basic sprites with `move(dx,dy)` and `update()` that clamps to screen.

---

## Example: Minimal Scene

```python
import pygame
from system.abstract_scene import AbstractScene

class MyScene(AbstractScene):
    def enter(self):
        self.color = (30, 30, 50)
    def exit(self):
        pass
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                raise SystemExit
    def update(self, dt):
        pass
    def draw(self, screen):
        screen.fill(self.color)
```

```python
import pygame, sys
from system.GameGlobals import scene_manager
from renderer.FrameRater import FrameRateDisplay
from my_scene import MyScene

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
fr = FrameRateDisplay()

scene_manager.switch_to(MyScene())

while True:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()
    scene_manager.handle_events(events)
    scene_manager.update(dt)
    screen.fill((0,0,0))
    scene_manager.draw(screen)
    fr.draw(screen, clock)
    pygame.display.flip()
```

---

## Example: UI Button with outlined text

```python
from renderer.UI.button import Button
from renderer.UI.fancy_text import FancyText

fancy = FancyText(font_size=24, font_path="assets/fonts/Creepster_Regular.ttf")
button = Button(
    color=(200,200,200,250), width=150, height=50, pos=(250,250),
    text="Play", font_size=24,
    text_color=(255,255,255,255),
    hover_color=(0,0,0,220), click_color=(0,0,0,250),
    hover_text_color=(255,255,100,255), click_text_color=(255,100,100,255),
    border_color=(255,0,0,255), hover_border_color=(255,255,0,80),
    click_border_color=(255,100,100,255), border_width=4,
    fancy_text=fancy,
    click_callback=lambda b: print(f"{b.text} clicked")
)
# in game loop:
#   button.update(events); button.draw(screen)
```

---


## Example: Flashlight (SpotLight) + Radial Glow

```python
import pygame
from renderer.Light import SpotLight, circle_light_mask

SCREEN = (800, 600)
spot = SpotLight(display_surface=SCREEN)
beam = spot.create_beam()

overlay = pygame.Surface(SCREEN, pygame.SRCALPHA)
overlay.fill((20,30,50,120))

rot_img, rot_rect = spot.draw(beam, pygame.Vector2(pygame.mouse.get_pos()), pygame.Vector2((400,300)))
overlay.blit(rot_img, rot_rect, special_flags=pygame.BLEND_RGBA_SUB)

glow = circle_light_mask(32, 100, 90)
overlay.blit(glow, (420, 290), special_flags=pygame.BLEND_RGBA_SUB)

# afterwards: screen.blit(overlay, (0,0))
```

---

## Compatibility & Requirements

- **Python**: 3.9+ (3.10+ recommended)
- **Pygame**: 2.x
- **OS**: Windows / macOS / Linux

> ⚠️ **Case-sensitivity**: On Linux/macOS paths are case–sensitive. The project references `assets/scream.png`, while the file in *assets* appears as `Scream.png`. Rename or adjust paths to avoid load errors.

---

## Quality & Performance Notes

- HUD (`FrameRateDisplay`) computes avg frame time and rounds to **even numbers** to avoid flickering.
- `CustomGroup.draw()` enables custom per–sprite rendering for future batching/post-processing.
- Gravity constant defined in *pixels* (`g = 9.8 * 64`), suitable for arcade-like physics.

---

## Roadmap / Future Ideas

- 🎯 Camera: vertical axis, zoom, parallax layers.
- 🧮 Physics: collisions, swept AABB, integrator choices, particle system.
- 🧰 ECS: stricter separation between data (components) and logic (systems).
- 🧪 Tests: unit tests for UI / math helpers.
- ⚙️ Tooling: `requirements.txt`, `Makefile`, pre-commit (black/isort).
- 📦 Packaging: pip-installable module, semantic versioning.
- 📝 Docs: docstrings + mkdocs site with demos/GIFs.

---

## License / Credits

- **Font**: *Creepster* — see `assets/fonts/OFL.txt` (SIL Open Font License).
- **Code**: This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Screenshots

> Add/update images in the repo to show here (example):
>
> `![screenshot](assets/ElementMakes/final/Versions/V3.1.3_High_res.png)`

---

## Contributing

PRs/Issues welcome. For major changes, open an issue first to discuss scope.

---

## TL;DR

- Run `python game2.py`
- Scene-based architecture, ready-to-use UI/Light/Camera helpers
- Great for quick 2D prototypes in Pygame

[Pygame]: https://www.pygame.org/
