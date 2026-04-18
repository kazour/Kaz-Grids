# Kaz Grids — Standalone Grid Editor

Python 3 / tkinter / ttkbootstrap app — buff-tracking grid editor for Age of Conan.

## Quick Reference

- **Entry point:** `kzgrids.py`
- **Build:** `python build.py` (PyInstaller → `dist/Kaz Grids/` → `Kaz Grids.zip`)
- **Run:** `python kzgrids.py`
- **No automated tests** — verify manually by running the app

## Code Quality Rules

- No AI slop — every line earns its place. No verbose wrappers, no unnecessary abstractions.
- No wrapper classes for single-use — inline if used once, extract only with genuine reuse.
- Don't add docstrings, comments, or type annotations to code you didn't change.
- Keep proven patterns: dataclass + to_dict/from_dict, SettingsManager, window lifecycle.

## Architecture

- **No notebook tabs** — top nav switches between Grids and Database views
- **SettingsManager:** JSON load → in-memory dict → atomic save (temp + rename)
- **Window lifecycle:** withdraw() → build widgets → restore_window_position() → deiconify()
- **Build pipeline:** Grid config → AS2 code gen (grids_generator.py) → MTASC compile → deploy to game folder
- **Live Tracker:** Independent Toplevel window, launched from Build menu

## Style

- 4-space indentation
- Constants: UPPER_SNAKE_CASE, Classes: PascalCase, Functions: snake_case, Private: _leading_underscore
- Section separators: `# ===... # SECTION NAME # ===...`
- Logging: `logger = logging.getLogger(__name__)` per module
- Design tokens in `Modules/ui_helpers.py` (THEME_COLORS, FONT_*, PAD_*, BTN_*)

## Key Files

- `Modules/ui_helpers.py` — design system (fonts, colors, layout tokens, shared widgets)
- `Modules/grids_panel.py` — grid editor UI, dialogs, grid management (largest module)
- `Modules/database_editor.py` — buff database CRUD, search, filtering
- `Modules/grids_generator.py` — AS2 code generation from grid configs
- `assets/kzgrids/Database.json` — buff database
- `settings/kzgrids_settings.json` — app settings (window pos, game clients)
