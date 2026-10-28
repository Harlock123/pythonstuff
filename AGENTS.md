# AGENTS.md

Notes for anyone, human or AI agent, changing this code. The README is a single word; this file describes what is
here.

## What this is

Two small Pygame experiments: balls bouncing inside a square that rotates in the middle of an 800x600 window.
They are plain Python scripts with no package, no requirements file and no tests. They need Python 3 and Pygame,
and open a desktop window.

## Commands

```bash
python3 -m pip install pygame     # the only dependency
python3 ball.py                   # one yellow ball
python3 ball2.py                  # twelve coloured balls (the window title says eight)
```

## Layout

- `ball.py`: one ball in a 400-pixel square that turns one degree a frame.
- `ball2.py`: the same idea with a list of ball dictionaries (`pos`, `speed`, `color`) in a 450-pixel square.
  The balls bounce off the walls but pass through each other.
- Both scripts share the same helpers, copied rather than imported: `get_rotated_square_vertices`,
  `normalize_vector`, `get_closest_point_on_line` and `distance_between_points`.

## Rules that keep it working

- **Frame-based motion.** Everything moves a fixed amount per frame, and `clock.tick(60)` caps the loop at 60
  frames a second. There is no delta time, so speeds are in pixels per frame.
- **Bounce maths.** A ball bounces when it comes within `BALL_RADIUS + 1` of the nearest edge. Its velocity is
  reflected about that edge's normal, scaled back to `INITIAL_SPEED`, and the ball is pushed out of the wall. The
  push-out step keeps a ball from being caught inside the moving wall on the next frame.
- **Module-level scripts.** Each file runs its loop at import time, so importing one from the other starts a
  window. Move shared code into its own module before reusing it.

## Making a change

- Run the script you changed and watch it for a while; there is nothing automated to check it.
