# Asciifrog Project Guidelines 🐸⚡

## Engineering Standards
- **Language:** Python 3.13
- **Terminal UI:** Raw ANSI Escape Codes (Zero dependencies!).
- **Code Style:** Follow PEP 8.
- **Error Handling:** Use try-except blocks where appropriate.
- **State Management:** Keep the application state in an `App` class.

## Architecture
- App Module: Core logic and state.
- UI Module: Low-level ANSI rendering logic.
- Frog Module: Frog movement and ASCII representation.
- Cloud Module: Cloud movement and ASCII representation.

## Conventions
- Use constants for ANSI escape sequences (e.g., `CLEAR`, `MOVE_CURSOR`).
- Minimize screen redraws to prevent flickering.
