# Changelog

All notable changes to this project will be documented in this file.

---

## [0.5.1-alpha] — 2026-01-16

### ✨ Added
- Fully interactive **web-based terminal interface** with ANSI color rendering.
- Backend-driven command execution with frontend-only rendering logic.
- JSON-based **command registry (`TERMINAL_COMMANDS`)** with alias support.
- Support for common shell-like commands:
  - `help`, `clear`, `cls`
  - `uname`, `uname -a`
  - `sudo`
  - exit-like commands (`exit`, `quit`, `shutdown`, `bye`, etc.)
- **Session-based system temperature** to track user behavior.
- **Non-linear escalation model** for repeated troll commands.
- **Cooldown logic** for normal commands to reduce system temperature.
- Temporary **input lock mechanism** when terminal overheats.
- Debug-only `angerlevel / getangerlevel` command.
- Personality-driven, humorous system responses with controlled escalation.

---

### 🧠 Behavior & UX
- Terminal now adapts behavior based on user interaction patterns.
- Differentiates between curiosity and intent using repetition tracking.
- Overheat state is temporary and self-recovering.
- Backend remains authoritative; frontend enforces UI state changes.
- ANSI output renders correctly with preserved newlines and formatting.
- Terminal responses feel system-aware without being disruptive.

---

### 🛠 Fixed
- Fixed permanent overheat issue caused by session and local state desynchronization.
- Fixed improper usage of `current_app` outside Flask application context.
- Fixed command resolution failures due to missing registry entries.
- Ensured cooldown logic executes reliably after overheat.
- Prevented hard-lock scenarios by enforcing reversible penalties.

---

### 🧱 Architecture
- Clear separation of concerns:
  - **Backend**: command logic, behavior state, escalation
  - **Frontend**: rendering, ANSI parsing, UI enforcement
- Removed hardcoded command logic in favor of data-driven design.
- Centralized system identity (kernel name, version, debug mode) in app config.
- Blueprint-safe usage of `current_app` and Flask session handling.

---

### 🎭 Personality
- Introduced a stateful terminal personality.
- Responses escalate gradually based on system temperature.
- Debug introspection is gated and not exposed in production mode.

---

### ✅ Status
- Core terminal behavior is stable.
- No known blocking issues.
- Foundation ready for future features:
  - themes
  - filesystem simulation
  - streaming output
  - personality modes

---
