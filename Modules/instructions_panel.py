import tkinter as tk
from tkinter import ttk

from Modules.ui_helpers import (
    THEME_COLORS,
    FONT_BODY, FONT_SECTION,
    PAD_TAB, PAD_SMALL, PAD_XS, PAD_ROW, PAD_INNER,
    CollapsibleSection, create_scrollable_frame,
)


class InstructionsPanel(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self._wrap_labels = []  # (label, margin) pairs for dynamic wraplength
        self._create_widgets()

    def _create_widgets(self):
        outer, inner, canvas = create_scrollable_frame(self)
        outer.pack(fill='both', expand=True)
        self._canvas = canvas

        intro = ttk.Label(
            inner,
            text="Kaz Grids shows your active buffs and debuffs as icon grids "
            "on your Age of Conan game screen.",
            font=FONT_BODY, foreground=THEME_COLORS['body'],
            wraplength=700, justify='left',
        )
        intro.pack(fill='x', padx=PAD_TAB, pady=(PAD_TAB, PAD_SMALL))
        self._wrap_labels.append((intro, PAD_TAB * 2))

        # --- Quick Start ---

        qs = self._add_section(inner, "Quick Start", [
            "Follow these steps to get your first grid running:",
        ], initially_open=True)
        self._add_subsection(qs.content, "1. Add a game client", [
            "Click the + button next to the Clients dropdown at the bottom "
            "and select your Age of Conan install folder. You can add "
            "multiple clients \u2014 builds install to all of them.",
        ])
        self._add_subsection(qs.content, "2. Create a grid", [
            "Click + Add Grid in the Grids tab. The 1\u00d710 horizontal bar "
            "is a good starting point for tracking player buffs.",
        ])
        self._add_subsection(qs.content, "3. Choose which buffs to track", [
            "Use the Tracked Buffs button to pick buffs from the database. "
            "Only buffs you've selected will appear in the grid.",
        ])
        self._add_subsection(qs.content, "4. Build and install", [
            "Click Build & Install at the bottom. This installs to all your "
            "game clients at once. Close the game before your first build. "
            "After that, you can rebuild while the game is open and type "
            "/reloadui in chat to see changes instantly.",
        ])

        # --- Creating Grids ---

        creating = self._add_section(inner, "Creating Grids", [
            "Click + Add Grid, pick a shape preset (or set custom rows and columns). "
            "You can have up to 64 total slots spread across all your grids.",
        ], initially_open=True)
        self._add_paragraph(creating.content,
            "The 64-slot cap comes from an ActionScript limit on how many icon "
            "objects the overlay can manage reliably. If you hit it, reduce "
            "grid size or remove a grid rather than disabling \u2014 disabled grids "
            "still count toward the cap."
        )

        # --- Player vs Target ---

        grid_types = self._add_section(inner, "Player vs Target Grids", [
            "Each grid is tied to one source \u2014 chosen when you create the grid.",
        ])
        self._add_subsection(grid_types.content, "Player grid", [
            "Tracks buffs and debuffs on your own character.",
        ])
        self._add_subsection(grid_types.content, "Target grid", [
            "Tracks buffs and debuffs on whoever you're targeting \u2014 "
            "a mob, a friendly player, or an enemy player.",
        ])

        # --- Grid Modes ---

        modes = self._add_section(inner, "Dynamic vs Static Mode", [
            "Each grid runs in one of two modes:",
        ])
        self._add_subsection(modes.content, "Dynamic", [
            "Slots fill automatically as buffs activate, and empty when they expire. "
            "You control the fill direction, sort order, and grouping.",
        ])
        self._add_subsection(modes.content, "Dynamic options", [
            "Fill direction \u2014 left-to-right, right-to-left, top-to-bottom, "
            "bottom-to-top, or diagonal.",
            "Sort order \u2014 longest timer first, shortest timer first, or "
            "the order buffs were applied.",
            "Grouping \u2014 Buff First and Debuff First put misc effects first, then the chosen order. Mixed sorts all buffs together by time.",
        ])
        self._add_subsection(modes.content, "Static", [
            "Each slot is pinned to one or more specific buffs. The slot shows "
            "the buff when active and stays empty when it's not.",
            "If multiple buffs are assigned to the same slot, the most recently "
            "applied one is shown.",
        ])

        # --- Whitelist & Slot Assignments ---

        wl_section = self._add_section(inner, "Tracked Buffs and Slot Assignments", [
            "These are the two ways to tell a grid which buffs to track.",
        ])
        self._add_subsection(wl_section.content, "Tracked Buffs (Dynamic mode)", [
            "A list of buff names the grid watches for. Only buffs on this list "
            "appear in the grid. If no buffs are tracked, nothing is shown.",
        ])
        self._add_subsection(wl_section.content, "Slot Assignments (Static mode)", [
            "Assign one or more buffs to each slot by position. "
            "Unassigned slots stay empty.",
            "If multiple buffs share a slot, the most recently applied one is shown.",
        ])

        # --- Buffs, Debuffs, and Misc ---

        types_section = self._add_section(inner, "Buffs, Debuffs, and Misc", [
            "Age of Conan doesn\u2019t label effects as buffs or debuffs \u2014 "
            "the game just has effects. For your own character, the default UI "
            "splits them into two bars: removable effects (usually positive) and "
            "non-removable effects (usually negative), but there are exceptions "
            "in both directions. For a target, everything is shown in one place "
            "with no separation at all.",
            "The database is where you create that distinction yourself. When you "
            "add a buff ID, you assign it a type \u2014 Buff, Debuff, or Misc. "
            "The grid uses that type for icon border color and for grouping.",
        ])
        self._add_subsection(types_section.content, "Buff", [
            "Effects you\u2019ve decided are positive \u2014 typically what appears "
            "in the removable bar on your own character. Grey icon border.",
        ])
        self._add_subsection(types_section.content, "Debuff", [
            "Effects you\u2019ve decided are negative \u2014 typically what appears "
            "in the non-removable bar, or effects you track on a target. "
            "Red icon border.",
        ])
        self._add_subsection(types_section.content, "Misc", [
            "A free category for anything you want to separate out. "
            "Golden icon border.",
            "In the included database, Misc covers CC durations and heals over "
            "time \u2014 effects worth watching but distinct from standard buffs "
            "and debuffs. You can reclassify any entry however you like.",
            "In Buff First and Debuff First grouping modes, misc effects always "
            "appear before buffs and debuffs.",
        ])
        self._add_paragraph(types_section.content,
            "Tip: Avoid tracking Non-Unique debuffs on a Target grid. When "
            "multiple players apply the same debuff, separate instances are "
            "created \u2014 the grid always shows the most recent one, making "
            "the timer unreliable.",
            foreground=THEME_COLORS['warning'])

        # --- Buff Database ---

        db_section = self._add_section(inner, "The Buff Database", [
            "Every effect in Age of Conan has one or more numeric buff IDs. "
            "The Database tab is where you map those IDs to human-readable names "
            "and decide how each one is classified \u2014 so you can pick effects "
            "by name when setting up grids and have them grouped and colored correctly.",
            "Use the search bar and category/type filters to find what you need.",
        ])
        self._add_subsection(db_section.content, "Adding or editing an entry", [
            "Name \u2014 a unique label for this effect (e.g. \"Cunning Deflection\").",
            "ID(s) \u2014 the numeric buff ID(s). Enter one per line or "
            "comma-separated.",
            "Category \u2014 groups related entries together for easier browsing.",
            "Type \u2014 your classification of this effect. Sets the icon border "
            "color and controls grouping: Buff (grey), Debuff (red), Misc (golden).",
        ])

        # --- Stacking ---

        stacking = self._add_section(inner, "Stacking", [
            "Some buffs have multiple stack levels, each with its own buff ID. "
            "The stacking options in the database editor control how multiple IDs "
            "are interpreted.",
        ])
        self._add_subsection(stacking.content, "Stacking disabled (default)", [
            "Multiple IDs are treated as different ranks of the same buff. "
            "Only one rank can be active at a time \u2014 a higher rank replaces "
            "a lower one.",
        ])
        self._add_subsection(stacking.content, "Stacking enabled", [
            "IDs represent increasing stack levels. Enter them in order: "
            "stack 1 first, stack 2 second, and so on. The current stack "
            "number is displayed over the icon.",
        ])
        self._add_subsection(stacking.content, "Partial list (stacking only)", [
            "Turn this on when you only have IDs for part of the stack range. "
            "For example, if you have the last 5 IDs of a \u00d715 buff, enter "
            "those 5 IDs and set 'Start at' to 11.",
        ])
        self._add_subsection(stacking.content, "Stack range (stacking only, partial list off)", [
            "When you have the full ID list but only want the icon to appear "
            "within a certain range. 'Start at' is when the icon becomes visible, "
            "'End at' is the last stack shown (0 means show all).",
        ])

        # --- Grid display options ---

        self._add_section(inner, "Grid Display Options", [
            "Timers \u2014 show the remaining duration below each buff icon.",
            "Flash \u2014 icons pulse when a buff is about to expire. Set the "
            "threshold in seconds.",
            "Grid positions, icon size, and gaps are configured in-game via "
            "preview mode (Shift+Ctrl+Alt), or set manually in the app.",
        ])

        # --- Building & Installing ---

        build_section = self._add_section(inner, "Building and Installing", [
            "Build & Install compiles your grid layout into a game overlay file "
            "and installs it to all your game clients at once. The compiler is "
            "bundled \u2014 no extra setup needed.",
        ])
        self._add_subsection(build_section.content, "Managing game clients", [
            "Use the Clients dropdown at the bottom to manage your Age of Conan "
            "installations. Click + to add a new client.",
            "When you build, every client in the list gets updated automatically. "
            "The build summary shows the result for each client.",
        ])
        self._add_subsection(build_section.content, "With Aoc.exe (launcher bypass)", [
            "If Aoc.exe is found in any of your game clients, all clients are "
            "treated as launcher-bypass installs. Do your first build with the "
            "game closed. After that, rebuild anytime and type /reloadui in chat "
            "to apply changes instantly.",
        ])
        self._add_subsection(build_section.content, "Without Aoc.exe (standard launcher)", [
            "Grid positions aren't saved between sessions. To set them: enter "
            "preview mode in-game (Shift+Ctrl+Alt), note each grid's X/Y "
            "coordinates, enter them in the app, and rebuild.",
            "To apply changes in-game, type /reloadui then /reloadgrids in chat.",
        ])

        self._add_section(inner, "Removing Kaz Grids from a game client", [
            "Use File \u2192 Uninstall from game client\u2026 to remove KazGrids.swf "
            "and related files from the selected client. The client stays in your "
            "Clients list afterwards; remove it separately if you also want to stop "
            "managing it from the app.",
        ])

        # Bottom spacer
        ttk.Frame(inner).pack(pady=PAD_TAB)

        # Dynamic wraplength on resize (debounced)
        self._last_canvas_w = 0
        self._resize_after_id = None
        canvas.bind('<Configure>', self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        w = event.width
        if w <= 1 or w == self._last_canvas_w:
            return
        self._last_canvas_w = w
        if self._resize_after_id:
            self.after_cancel(self._resize_after_id)
        self._resize_after_id = self.after(50, self._apply_wraplengths, w)

    def _apply_wraplengths(self, w):
        self._resize_after_id = None
        for lbl, margin in self._wrap_labels:
            lbl.configure(wraplength=max(200, w - margin))

    # Section/subsection margins relative to canvas edge:
    #   section content:    PAD_TAB + collapse_indent + scrollbar ≈ 80
    #   subsection content: PAD_TAB + collapse_indent + PAD_INNER + scrollbar ≈ 100
    _SECTION_MARGIN = 80
    _SUBSECTION_MARGIN = 100

    def _add_section(self, parent, title, paragraphs, initially_open=False):
        section = CollapsibleSection(parent, title=title, initially_open=initially_open)
        section.pack(fill='x', padx=PAD_TAB, pady=(PAD_ROW, 0))
        for text in paragraphs:
            lbl = ttk.Label(section.content, text=text, font=FONT_BODY,
                            foreground=THEME_COLORS['body'], wraplength=650,
                            justify='left')
            lbl.pack(fill='x', pady=(0, PAD_XS))
            self._wrap_labels.append((lbl, self._SECTION_MARGIN))
        return section

    def _add_subsection(self, parent, title, paragraphs):
        frame = ttk.Frame(parent)
        frame.pack(fill='x', padx=(PAD_INNER, 0), pady=(PAD_XS, 0))
        ttk.Label(frame, text=title, font=FONT_SECTION,
                  foreground=THEME_COLORS['heading']).pack(fill='x', pady=(0, PAD_XS))
        for text in paragraphs:
            lbl = ttk.Label(frame, text=text, font=FONT_BODY,
                            foreground=THEME_COLORS['body'], wraplength=620,
                            justify='left')
            lbl.pack(fill='x', pady=(0, PAD_XS))
            self._wrap_labels.append((lbl, self._SUBSECTION_MARGIN))

    def _add_paragraph(self, parent, text, foreground=None):
        lbl = ttk.Label(parent, text=text, font=FONT_BODY,
                        foreground=foreground or THEME_COLORS['body'],
                        wraplength=650, justify='left')
        lbl.pack(fill='x', padx=(PAD_INNER, 0), pady=(PAD_XS, PAD_XS))
        self._wrap_labels.append((lbl, self._SUBSECTION_MARGIN))
