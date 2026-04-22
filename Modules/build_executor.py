"""
Kaz Grids — Build Executor
Compile KazGrids.swf and install to game folders.
"""

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

from .build_utils import strip_marker_block, update_script_with_marker
from .grids_generator import build_grids

logger = logging.getLogger(__name__)


def compile_to_staging(grids, database, assets_path, compiler, app_version):
    """Compile KazGrids.swf to a temp staging dir.

    Returns (staging_dir, result) where result is (success_bool, message).
    Caller must clean up staging_dir.
    """
    base_swf = assets_path / "kzgrids" / "base.swf"
    stubs_path = assets_path / "kzgrids" / "stubs"

    staging_dir = Path(tempfile.mkdtemp(prefix="kzgrids_"))
    output_swf = staging_dir / "KazGrids.swf"

    result = build_grids(
        grids, database,
        str(base_swf), str(stubs_path),
        str(output_swf), str(compiler),
        app_version,
        assets_path=assets_path,
    )
    return staging_dir, result


def install_to_client(staging_swf, game_path, use_aoc):
    """Install compiled SWF + scripts to one game client.

    Returns (success, error_message).
    """
    flash_path = Path(game_path) / "Data" / "Gui" / "Default" / "Flash"
    scripts_path = Path(game_path) / "Scripts"

    try:
        flash_path.mkdir(parents=True, exist_ok=True)
        scripts_path.mkdir(parents=True, exist_ok=True)

        shutil.copy2(staging_swf, flash_path / "KazGrids.swf")

        if use_aoc:
            kazbars_dir = Path(game_path) / "Data" / "Gui" / "Aoc" / "KazGrids"
            write_xml_add_files(kazbars_dir)

        create_scripts(scripts_path, use_aoc=use_aoc)
    except OSError as e:
        return False, (
            f"Could not write files\n\n{e}\n\n"
            "Check that your disk has free space and the game folder is not read-only."
        )

    return True, ""


def uninstall_from_client(game_path):
    """Remove Kaz Grids files from one game client.

    Returns (success, message).
    """
    removed = []
    try:
        swf = Path(game_path) / "Data" / "Gui" / "Default" / "Flash" / "KazGrids.swf"
        if swf.exists():
            swf.unlink()
            removed.append("KazGrids.swf")

        aoc_dir = Path(game_path) / "Data" / "Gui" / "Aoc" / "KazGrids"
        if aoc_dir.exists():
            shutil.rmtree(aoc_dir)
            removed.append("Aoc module files")

        for script in ("reloadgrids", "unloadgrids"):
            p = Path(game_path) / "Scripts" / script
            if p.exists():
                p.unlink()
                removed.append(script)

        auto_login = Path(game_path) / "Scripts" / "auto_login"
        if auto_login.exists():
            try:
                content = auto_login.read_text(encoding='utf-8')
                new_content = strip_marker_block(content, "# KzGrids auto-load")
                if new_content != content:
                    if new_content.strip():
                        auto_login.write_text(new_content, encoding='utf-8')
                    else:
                        auto_login.unlink()
                    removed.append("auto_login entry")
            except (UnicodeDecodeError, OSError):
                pass
    except OSError as e:
        return False, f"Could not remove files:\n\n{e}"

    if not removed:
        return True, "Nothing to remove \u2014 Kaz Grids isn't installed in this client."
    return True, "Removed: " + ", ".join(removed)


def detect_aoc_any(game_paths):
    """Check all game paths for launcher bypass (aoc.exe or Aoc.log).

    Returns (aoc_installed, aoc_running).
    """
    found = False
    for path in game_paths:
        if detect_aoc_launcher(path):
            found = True
            break
    if not found:
        return False, False
    return True, is_aoc_running()


def detect_aoc_launcher(game_path):
    """Return True if this client uses launcher bypass (has aoc.exe or Aoc.log)."""
    aoc_dir = Path(game_path) / "Data" / "Gui" / "Aoc"
    return (aoc_dir / "aoc.exe").exists() or (aoc_dir / "Aoc.log").exists()


def is_aoc_running():
    """Return True if Aoc.exe process is currently running."""
    try:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq Aoc.exe', '/NH'],
            capture_output=True, text=True, timeout=5
        )
        return 'aoc.exe' in result.stdout.lower()
    except Exception:
        return False


def write_xml_add_files(kazbars_dir):
    """Write MainPrefs.xml.add and Modules.xml.add for Aoc.exe module system."""
    kazbars_dir.mkdir(parents=True, exist_ok=True)

    prefs = (
        '\t<Value name="KzGrids" value="true" />\n'
        '\t<Archive name="KzGrids settings" />\n'
    )
    modules = (
        '\t<Module\n'
        '\t\tname              = "KzGrids"\n'
        '\t\tmovie             = "KazGrids.swf"\n'
        '\t\tflags             = "GMF_CFG_STORE_USER_CONFIG"\n'
        '\t\tdepth_layer       = "Top"\n'
        '\t\tsub_depth         = "0"\n'
        '\t\tvariable          = "KzGrids"\n'
        '\t\tcriteria          = "KzGrids &amp;&amp; (guimode &amp; (GUIMODEFLAGS_INPLAY | GUIMODEFLAGS_ENABLEALLGUI))"\n'
        '\t\tconfig_name       = "KzGrids settings"\n'
        '\t/>\n'
    )

    (kazbars_dir / "MainPrefs.xml.add").write_text(prefs, encoding='utf-8')
    (kazbars_dir / "Modules.xml.add").write_text(modules, encoding='utf-8')


def create_scripts(scripts_path, use_aoc=False):
    """Write Scripts/reloadgrids, Scripts/unloadgrids and update Scripts/auto_login."""
    reload_content = "/unloadclip KazGrids.swf\n/delay 100\n/loadclip KazGrids.swf"
    unload_content = "/unloadclip KazGrids.swf"
    reload_script = scripts_path / "reloadgrids"
    unload_script = scripts_path / "unloadgrids"
    auto_login_script = scripts_path / "auto_login"

    reload_script.write_text(reload_content, encoding='utf-8')
    unload_script.write_text(unload_content, encoding='utf-8')

    if use_aoc:
        # Aoc.exe handles loading via xml.add — strip any old KzGrids marker
        if auto_login_script.exists():
            try:
                content = auto_login_script.read_text(encoding='utf-8')
            except (UnicodeDecodeError, OSError):
                logger.warning("auto_login corrupt — overwriting")
                content = ""
            content = strip_marker_block(content, "# KzGrids auto-load")
            if content.strip():
                auto_login_script.write_text(content, encoding='utf-8')
            else:
                auto_login_script.unlink(missing_ok=True)
    else:
        update_script_with_marker(auto_login_script, "# KzGrids auto-load", reload_content)
