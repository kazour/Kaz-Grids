Buff/debuff grid overlay editor for **Age of Conan**. Design icon grids that show your active effects on top of the game, then compile and install them in one click.

## Highlights

- **Player and Target grids** — track effects on you or your current target
- **Dynamic or Static slots** — auto-fill as buffs activate, or pin specific buffs to specific slots
- **Buff database** — map numeric spell IDs to readable names and classify them as Buff, Debuff, or Misc
- **Multi-client** — register multiple AoC installs; one build updates all of them
- **Ethram-Fal Seed Timer** — always-on-top overlay for the Viscous Seed / Lotus Fixation / Syphon cycle

## Install

1. Download `Kaz Grids.zip` below and extract it anywhere.
2. Run `Kaz Grids.exe`.
3. Click `+` next to the Clients dropdown and pick your Age of Conan folder.
4. On the Grids tab, click `+ Add Grid` — a 1×10 horizontal bar is a good starting point.
5. Click `Tracked Buffs` and pick entries from the database.
6. Click `Build & Install`. Close the game for your first build; after that, rebuild anytime and type `/reloadui` in chat to apply changes.

> **SmartScreen warning**: Windows may flag the `.exe` as unrecognized on first launch. Click **More info** → **Run anyway**. Kaz Grids is unsigned because code signing certificates aren't justified for a hobby project. If you want to verify the download, `Kaz Grids.zip.sha256` is attached alongside the zip — compare it with `Get-FileHash "Kaz Grids.zip"` in PowerShell.

## Requirements

- Windows 10 or 11
- Age of Conan installed
- No Python install needed — ships as a standalone executable
