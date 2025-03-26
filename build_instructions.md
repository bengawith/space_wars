---

### 🏗️ `build_instructions.md`

```markdown
# 🏗️ Building the Space Wars Executable with PyInstaller

This guide walks you through converting the Space Wars Pygame project into a standalone Windows executable using **PyInstaller**.

---

## ⚙️ Requirements

- Python 3.8 or newer (already installed)
- Pygame
- PyInstaller

### 🔹 Install Pygame and PyInstaller

```bash
pip install pygame pyinstaller
```

---

## 📁 Recommended Folder Structure

Your project should be organized as follows:

```
space_wars/
├── src/
│   ├── space_wars.py
│   ├── ...
├── images/
│   ├── ship3.bmp
│   ├── alien3.bmp
├── sounds/
│   ├── *.wav, *.ogg
├── fonts/
│   └── PressStart2P-Regular.ttf
├── high_score.txt
```

---

## 🔨 Building the Executable

From the **root** of your `space_wars` project, run:

```bash
pyinstaller --noconfirm --onefile --windowed ^
--add-data "images;images" ^
--add-data "sounds;sounds" ^
--add-data "fonts;fonts" ^
--add-data "high_score.txt;." ^
src/space_wars.py
```

> ✅ **Windows Note**: Use `;` to separate paths in `--add-data`. On macOS/Linux, use `:` instead.

### 💡 What the Flags Do:
- `--noconfirm`: Overwrites previous builds without prompting.
- `--onefile`: Packages everything into a single executable.
- `--windowed`: Hides the terminal/console window.
- `--add-data`: Ensures non-Python assets are included.

---

## 📦 Output Location

The compiled executable will be in:

```
dist/space_wars.exe
```

---

## 📁 Distributing the Game

To distribute the game, include the following in your `.zip` or release folder:

```
dist/
├── space_wars.exe
├── images/
├── sounds/
├── fonts/
└── high_score.txt
```

Place all assets next to the `.exe` to ensure compatibility with relative paths used in the code.

---

## ✅ Tips

- Test the `.exe` on a clean Windows machine or VM if possible.
- To reduce startup time, you can avoid `--onefile` and package with `--onedir`.

---

## 🎉 Enjoy Your Game!