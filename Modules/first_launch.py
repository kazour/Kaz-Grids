"""
Kaz Grids — First Launch Dialog
Modal setup dialog shown when no game folders are configured.
"""

import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

from .ui_helpers import (
    FONT_BODY_LG, FONT_BODY, FONT_SMALL, FONT_SECTION,
    THEME_COLORS, TK_COLORS, MODULE_COLORS,
    PAD_TAB, PAD_SMALL, PAD_TINY, PAD_XS, PAD_LF,
    BTN_SMALL,
    create_dialog_header,
    restore_window_position,
    bind_label_press_effect,
)


def show_first_launch_dialog(parent, app_name, on_game_added, on_load_default,
                             on_resolution_set=None, default_profile_exists=True,
                             on_dialog_closed=None):
    """Modal first-launch setup. Returns when dialog closes."""
    dialog = tk.Toplevel(parent)
    dialog.title(f"Welcome to {app_name}")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    restore_window_position(dialog, 'first_launch', 520, 440, parent, resizable=False)

    # Header
    create_dialog_header(dialog, f"Welcome to {app_name}",
                         MODULE_COLORS['grids'], width=520)

    content = ttk.Frame(dialog)
    content.pack(fill='both', expand=True, padx=PAD_TAB * 2, pady=(PAD_TAB, PAD_LF))

    # --- Section 1: Game path ---
    ttk.Label(content, text="Game Client",
              font=FONT_SECTION, foreground=THEME_COLORS['heading']
              ).pack(anchor='w', pady=(PAD_SMALL, PAD_XS))

    ttk.Label(content, text="Where is Age of Conan installed?",
              font=FONT_SMALL, foreground=THEME_COLORS['muted']
              ).pack(anchor='w', pady=(0, PAD_XS))

    path_frame = ttk.Frame(content)
    path_frame.pack(fill='x', pady=(0, PAD_TINY))

    path_var = tk.StringVar()
    path_entry = ttk.Entry(path_frame, textvariable=path_var, font=FONT_BODY)
    path_entry.pack(side='left', fill='x', expand=True, padx=(0, PAD_SMALL))

    def browse():
        p = filedialog.askdirectory(title="Select Age of Conan Folder",
                                     parent=dialog)
        if p:
            path_var.set(p)
            if not (Path(p) / "Data" / "Gui" / "Default").exists():
                warn_label.configure(
                    text="This doesn't look like an AoC install \u2014 missing Data/Gui/Default/",
                    foreground=THEME_COLORS['warning']
                )
            else:
                warn_label.configure(text="", foreground=THEME_COLORS['muted'])

    ttk.Button(path_frame, text="Browse", width=BTN_SMALL,
               command=browse).pack(side='right')

    warn_label = ttk.Label(content, text="", font=FONT_SMALL,
                           foreground=THEME_COLORS['warning'])
    warn_label.pack(anchor='w')

    # Common locations (only show paths that exist)
    common_paths = [
        r"C:\Funcom\Age of Conan",
        r"D:\Games\Age of Conan",
        r"C:\Program Files (x86)\Funcom\Age of Conan",
    ]
    existing_paths = [cp for cp in common_paths if Path(cp).exists()]
    if existing_paths:
        ttk.Label(content, text="Found on this PC:", font=FONT_SMALL,
                  foreground=THEME_COLORS['muted']).pack(anchor='w', pady=(PAD_XS, PAD_TINY))
        for cp in existing_paths:
            lbl = ttk.Label(content, text=f"  {cp}", font=FONT_SMALL,
                            foreground=THEME_COLORS['body'], cursor='hand2',
                            takefocus=True)
            lbl.pack(anchor='w')
            lbl.bind('<Button-1>', lambda e, p=cp: path_var.set(p))
            lbl.bind('<Return>', lambda e, p=cp: path_var.set(p))
            lbl.bind('<space>', lambda e, p=cp: path_var.set(p))
            lbl.bind('<FocusIn>', lambda e, l=lbl: l.config(
                foreground=THEME_COLORS['accent']))
            lbl.bind('<FocusOut>', lambda e, l=lbl: l.config(
                foreground=THEME_COLORS['body']))
            bind_label_press_effect(lbl)

    # Separator
    ttk.Separator(content, orient='horizontal').pack(fill='x', pady=(PAD_TAB, PAD_SMALL))

    # --- Section 2: How to start ---
    ttk.Label(content, text="How do you want to start?",
              font=FONT_SECTION, foreground=THEME_COLORS['heading']
              ).pack(anchor='w', pady=(0, PAD_XS))

    # Resolution detection
    screen_w = parent.winfo_screenwidth()
    screen_h = parent.winfo_screenheight()
    detected = f"{screen_w}x{screen_h}"

    common_resolutions = ["1920x1080", "2560x1440", "3840x2160"]
    if detected not in common_resolutions:
        common_resolutions.insert(0, detected)

    res_var = tk.StringVar(value=detected)

    # --- Shared actions ---
    def _add_game_if_set():
        p = path_var.get().strip()
        if p:
            resolved = Path(p).resolve()
            parts = resolved.parts
            if len(parts) <= 3:
                name = str(resolved)
            else:
                name = f"{parts[0]}\\...\\{parts[-1]}"
            on_game_added(name, str(resolved))
        if on_resolution_set:
            on_resolution_set(res_var.get())

    def _close():
        dialog.destroy()
        if on_dialog_closed:
            on_dialog_closed()

    def load_default():
        _add_game_if_set()
        on_load_default(res_var.get())
        _close()

    def start_empty():
        _add_game_if_set()
        _close()

    def skip():
        _close()

    # --- Two equal-weight option cards ---
    _card_bg = TK_COLORS['status_bg']
    _border = TK_COLORS['border']

    cards_frame = ttk.Frame(content)
    cards_frame.pack(fill='x', pady=(0, PAD_SMALL))
    cards_frame.columnconfigure(0, weight=1, uniform='card')
    cards_frame.columnconfigure(1, weight=1, uniform='card')

    # --- Card A: Load Defaults ---
    if default_profile_exists:
        card_a = tk.Frame(cards_frame, bg=_card_bg,
                          highlightthickness=1,
                          highlightbackground=_border,
                          highlightcolor=_border)
        card_a.grid(row=0, column=0, sticky='nsew', padx=(0, PAD_XS))

        inner_a = tk.Frame(card_a, bg=_card_bg)
        inner_a.pack(fill='both', expand=True, padx=PAD_LF, pady=PAD_LF)

        ttk.Label(inner_a, text="Use Defaults",
                  font=FONT_SECTION, foreground=THEME_COLORS['heading']
                  ).pack(anchor='w')
        ttk.Label(inner_a, text="Pre-configured grids for\ncommon raid buffs and debuffs.",
                  font=FONT_SMALL, foreground=THEME_COLORS['muted']
                  ).pack(anchor='w', pady=(PAD_TINY, PAD_SMALL))

        # Resolution picker
        ttk.Label(inner_a, text="Game resolution:", font=FONT_SMALL,
                  foreground=THEME_COLORS['muted']
                  ).pack(anchor='w', pady=(0, PAD_TINY))
        res_combo = ttk.Combobox(inner_a, textvariable=res_var,
                                  values=common_resolutions, width=12, font=FONT_SMALL)
        res_combo.pack(anchor='w', pady=(0, PAD_SMALL))

        btn_defaults = ttk.Button(inner_a, text="Load Defaults",
                                   bootstyle="success", command=load_default,
                                   state='disabled')
        btn_defaults.pack(anchor='w')
    else:
        btn_defaults = None

    # --- Card B: Start Empty ---
    card_b = tk.Frame(cards_frame, bg=_card_bg,
                      highlightthickness=1,
                      highlightbackground=_border,
                      highlightcolor=_border)
    col = 1 if default_profile_exists else 0
    card_b.grid(row=0, column=col, sticky='nsew', padx=(PAD_XS, 0))

    inner_b = tk.Frame(card_b, bg=_card_bg)
    inner_b.pack(fill='both', expand=True, padx=PAD_LF, pady=PAD_LF)

    ttk.Label(inner_b, text="Start Empty",
              font=FONT_SECTION, foreground=THEME_COLORS['heading']
              ).pack(anchor='w')
    ttk.Label(inner_b, text="Build your own grids\nfrom scratch.",
              font=FONT_SMALL, foreground=THEME_COLORS['muted']
              ).pack(anchor='w', pady=(PAD_TINY, PAD_SMALL))

    # Spacer to push button to same vertical position as Load Defaults
    if default_profile_exists:
        ttk.Frame(inner_b).pack(expand=True)

    btn_empty = ttk.Button(inner_b, text="Start Empty",
                           bootstyle="info-outline", command=start_empty,
                           state='disabled')
    btn_empty.pack(anchor='w')

    # Enable/disable action buttons based on game path
    def _on_path_changed(*_):
        has_path = bool(path_var.get().strip())
        state = 'normal' if has_path else 'disabled'
        if btn_defaults:
            btn_defaults.configure(state=state)
        btn_empty.configure(state=state)

    path_var.trace_add('write', _on_path_changed)

    # Skip at the bottom
    ttk.Separator(content, orient='horizontal').pack(fill='x', side='bottom')
    skip_frame = ttk.Frame(content)
    skip_frame.pack(fill='x', side='bottom', pady=(PAD_SMALL, 0))
    skip_lbl = ttk.Label(skip_frame, text="Set up later",
                         font=FONT_SMALL, foreground=THEME_COLORS['muted'],
                         cursor='hand2', takefocus=True)
    skip_lbl.pack(side='right')
    skip_lbl.bind('<Button-1>', lambda e: skip())
    skip_lbl.bind('<Return>', lambda e: skip())
    skip_lbl.bind('<space>', lambda e: skip())
    skip_lbl.bind('<Enter>', lambda e: skip_lbl.config(
        foreground=THEME_COLORS['heading']))
    skip_lbl.bind('<Leave>', lambda e: skip_lbl.config(
        foreground=THEME_COLORS['muted']))
    bind_label_press_effect(skip_lbl)

    dialog.protocol("WM_DELETE_WINDOW", skip)
