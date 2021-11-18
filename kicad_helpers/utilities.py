# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/02_utilities.ipynb (unless otherwise specified).

__all__ = ['get_git_root', 'setup_test_repo', 'get_project_name', 'get_project_metadata', 'get_schematic_path',
           'get_bom_path', 'get_board_path', 'get_gitignore_list', 'in_gitignore', 'install_python_package']

# Cell
import glob
import os
import subprocess
import tempfile
from pprint import pprint

import git
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from fastcore.script import *

# Cell
def get_git_root(path="."):
    # Find the current projects' root directory
    git_repo = git.Repo(path, search_parent_directories=True)
    return git_repo.git.rev_parse("--show-toplevel")

# Cell
@call_parse
def setup_test_repo(root:Param("project root directory", str)="_temp"):
    """Setup a test KiCad repository to test against.
    """
    if not os.path.exists(root):
        subprocess.check_call(f"git clone https://github.com/sci-bots/dropbot-40-channel-HV-switching-board.kicad { root }", shell=True)

# Cell
def _set_root(root):
    """If `root` is the default value ("."), use the project's git root
    or override with the environment variable `KH_PROJECT_ROOT` if it
    exists.
    """
    if root == ".":
        # Use defaults
        root = get_git_root(".")

        # Override with environment variable if set
        root = os.getenv("KH_PROJECT_ROOT", root)
    return root

# Cell
def get_project_name(root="."):
    """Get the project name based on the name of the KiCad `*.pro` file.
    """
    root = _set_root(root)
    return os.path.splitext(os.path.split(glob.glob(os.path.join(root, "*.pro"))[0])[1])[0]

# Cell
def get_project_metadata(root="."):
    """Get the project metatdata from the `kitspace.yaml` file.
    """
    root = _set_root(root)

    # Default metadata if there's no existing `kitspace.yaml` file.
    metadata = {"summary": "A description for your project",
                "site": "https://example.com # A site you would like to link to (include http:// or https://)",
                "color": "black"
    }

    try:
        # If there's an existing `kicad.yaml` file, those settings override the defaults.
        with open(os.path.join(root, "kitspace.yaml")) as f:
            metadata.update({k: v for k, v in load(f, Loader=Loader).items() if k in ["summary", "site", "color"]})
    except FileNotFoundError:
        pass

    # Add the project name
    metadata["project_name"]=get_project_name(root)
    return metadata


# Cell
def get_schematic_path(root="."):
    """Get the path to the KiCad schematic.
    """
    root = _set_root(root)
    return os.path.join(root, get_project_name(root) + ".sch")

# Cell
def get_bom_path(root="."):
    """Get the path to the BOM.
    """
    root = _set_root(root)
    return os.path.join(root, "manufacturing", "default", get_project_name(root) + "-BOM.csv")

# Cell
def get_board_path(root="."):
    """Get the path to the KiCad board file.
    """
    root = _set_root(root)
    return os.path.join(root, get_project_name(root) + ".kicad_pcb")

# Cell
def get_gitignore_list(root="."):
    root =_set_root(root)
    with open(f"{ root }/.gitignore") as f:
        gitignore = f.readlines()
    return "|".join([line.strip() for line in gitignore])

# Cell
def in_gitignore(filename):
    try:
        if len(subprocess.check_output(f"echo '{ filename }' | git check-ignore --stdin --no-index", shell=True)):
            return True
    except subprocess.CalledProcessError:
        pass
    return False

# Cell
def install_python_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])