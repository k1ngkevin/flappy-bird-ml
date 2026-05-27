# AI Learns Flappy Bird

A small Flappy Bird clone built with Pygame, plus a NEAT-Python trainer that evolves birds to play the game automatically. Watch as the birds get smarter each generation

## Features

- Playable Flappy Bird-style game in `game.py`
- AI training loop in `ai.py` using NEAT-Python
- Sprite-based bird, background, and pipe assets
- Live generation, score, speed, and remaining-birds display while training
- Training speed controls in the AI window

## Requirements

- Python 3
- Pygame
- NEAT-Python

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Run The AI Trainer

```bash
python ai.py
```

Controls:

- `-` button: slow down simulation speed
- `+` button: speed up simulation speed
- `Esc`: quit

The NEAT settings are stored in `config-bird.txt`.

## Run The Game

```bash
python game.py
```

Controls:

- `Space` or left mouse click: jump
- `Esc`: quit

## Hyprland / Wayland Note

If the Pygame window does not appear correctly on Hyprland, try forcing SDL to use XWayland:

in your shell config eg. `~/.bashrc`, `~/.zshrc`, etc

```bash
export SDL_VIDEODRIVER=wayland
```

## Project Structure

```text
.
├── ai.py              # NEAT training loop
├── game.py            # Game objects and playable mode
├── config-bird.txt    # NEAT configuration
├── requirements.txt   # Python dependencies
└── bird-assets/       # Sprites and background images
```
