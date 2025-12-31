# 🚀 Space Wars

**Space Wars** is a 2D arcade-style shooter game built with **Pygame**, inspired by the classic Space Invaders. Players control a spaceship, shoot down waves of alien enemies, and aim for the highest score. The game features smooth animations, pixel fonts, background stars, sound effects, and a progression system.

---

## 🕹️ Gameplay

- Move left and right with the **←** and **→** arrow keys.
- Shoot with the **Spacebar**.
- Start the game with **Enter** or by clicking the **Play** button.
- Pause/unpause with **P**.
- Mute/unmute all sounds with **M**.
- Quit the game anytime with **Q**.

---

## 📦 Project Structure

```
space_wars/
├── src/
│   ├── space_wars.py        # Main game loop and core logic
│   ├── settings.py          # Game settings and difficulty scaling
│   ├── ship.py              # Player ship logic
│   ├── bullet.py            # Bullet behavior
│   ├── alien.py             # Alien enemy logic
│   ├── stars.py             # Dynamic starfield background
│   ├── button.py            # Play/Pause/Game Over buttons
│   ├── game_stats.py        # Game state tracking and high score persistence
│   ├── scoreboard.py        # Score and level display
│
├── images/
│   ├── ship3.bmp
│   ├── alien3.bmp
│
├── sounds/
│   ├── bullet.wav
│   ├── alien_hit.wav
│   ├── ship_hit.wav
│   ├── game_over.ogg
│   ├── play.wav
│   ├── background_music.wav
│
├── fonts/
│   └── PressStart2P-Regular.ttf
│
└── high_score.txt
```

---

## 🧠 Features

- Dynamic alien fleet generation and wave progression
- High score saving between sessions
- Difficulty scaling
- Mute and pause controls with overlays
- Translucent start and game over screens
- Soundtrack and sound effects

---

## 🛠️ Requirements

- Python 3.8+
- Pygame

Install with:

```bash
pip install pygame
```

---

## 🚀 Running the Game

```bash
cd src
python space_wars.py
```

---

## 🧱 Built With

- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/)
- [Press Start 2P Font](https://fonts.google.com/specimen/Press+Start+2P)

---

## 💡 Future Ideas

- Add power-ups
- Enemy types and boss fights
- Save/load game progress
- Controller support
- Online leaderboard

---

Enjoy defending the galaxy in **Space Wars**! 🌌👾

---