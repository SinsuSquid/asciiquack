# Asciiquack Project Guidelines 🦆✨

## Engineering Standards
- **Language:** Python 3.13
- **Terminal UI:** `rich` for layout and styling.
- **Code Style:** Follow PEP 8. Use `black` for formatting and `ruff` for linting.
- **Error Handling:** Use try-except blocks where appropriate. Avoid bare exceptions.
- **State Management:** Keep the application state in an `App` class.

## Architecture
- **App Module:** Core logic and state.
- **UI Module:** Rendering logic using `rich.layout` and `rich.live`.
- **Duck Module:** Duck movement and ASCII representation.

## Conventions
- Use type hints for better clarity.
- Ensure the duck's movement logic is decoupled from the rendering logic.
