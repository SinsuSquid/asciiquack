# asciiquack / asciifrog 🦆🐸🌊✨

A lightweight, zero-dependency terminal rubber-animal for debugging, drifting, and dreaming.

```
      \ | /
    .-'---'-.
 --(   O u O   )--      .--.
    '-.---.-'        .-(    ).
      / | \         (         )
                     `-------'

      __             (o)(o)
    <(o )___        (  u   )    ~  ≈  ∽  ~  ≈
     (     /       (        )   ≈  ∽  ~  ≈  ∽
      `---'         `------'    ∽  ~  ≈  ∽  ~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Talk to Frog/Duck (ESC: Quit | TAB: Color | H: Hat | F: Feed | A: Animal): _
```

Inspired by the classic `asciiaquarium`, this app brings a peaceful, floating rubber companion right into your terminal. No heavy libraries, no complex setups—just pure Python and raw ANSI escape codes.

---

## ✨ Features

- **🌊 Peaceful Waves:** Watch your animal bob and drift on gentle, animated ASCII waves.
- **💬 Rubber Animal Debugging:** Talk to your companion! It listens to your debugging woes and responds with wisdom.
- **🦆🐸 Multiple Species:** Switch between a cute Duck and a round Frog at any time!
- **🐸 Froggy Mode (For JY):** A special, extra-cute chibi frog mode for when you need that extra bit of luck and cuteness.
- **☀️ Smiling Sun:** A happy, winking sun that watches over the pond.
- **☁️ Flowing Clouds:** Cartoon-style clouds that drift gently across the sky.
- **📺 Fullscreen Stability:** Uses the Alternate Screen Buffer to ensure a flicker-free, stable experience.
- **🎨 Customization:** Change colors or give your friend some style with different hats!
- **🥨 Feeding Time:** Press a key to drop some breadcrumbs and watch your friend munch away.
- **⚡ Zero Dependencies:** Built entirely with the Python standard library.

---

## 🚀 Quick Start

Since there are no dependencies, you can run it directly with Python 3:

```bash
git clone git@github.com:SinsuSquid/asciiquack.git
cd asciiquack
python3 main.py
```

---

## 🛠️ Building

If you want to package the app into a standalone executable, you can use **PyInstaller**:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```
2. **Build the binary:**
   ```bash
   pyinstaller --onefile --name asciiquack main.py
   ```
3. **Run it:**
   Check the `dist/` directory for your shiny new `asciiquack` executable!

---

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **`Enter`** | Send a message to your friend |
| **`Tab`** | Cycle colors 🎨 |
| **`H`** | Cycle through hats (Top Hat, Cap, Flower) 🎩 |
| **`F`** | Feed breadcrumbs 🥨 |
| **`A`** | **Switch Animal (Duck ↔ Frog)** 🔄 |
| **`ESC`** | Exit the pond safely |

---

## 🛠️ Built With

- **Python 3.13+**
- **Raw ANSI Escape Codes**
- **PyInstaller** (For standalone binaries)
- **Love and Animal Magic** 💖🦆🐸

---

## 📜 License

MIT License.

---

*Made with ✨ by [SinsuSquid](https://github.com/SinsuSquid) and their loyal CLI Assistant.*
