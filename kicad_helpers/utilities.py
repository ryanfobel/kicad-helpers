# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/02_utilities.ipynb (unless otherwise specified).

__all__ = ['get_git_root', 'setup_test_repo', 'get_project_name', 'get_project_metadata', 'get_schematic_path',
           'get_bom_path', 'get_board_path', 'get_manufacturers', 'get_gitignore_list', 'in_gitignore',
           'run_docker_cmd', 'run_kibot_docker', 'get_board_metadata', 'update_board_metadata',
           'get_schematic_metadata', 'update_schematic_metadata']

# Cell
import glob
import os
import re
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
def _run_cmd(cmd):
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode("utf-8")

def _print_cmd_output(cmd):
    print(_run_cmd(cmd))

# Cell
def get_git_root(path="."):
    # Find the current projects' root directory
    git_repo = git.Repo(path, search_parent_directories=True)
    return git_repo.git.rev_parse("--show-toplevel").replace("/", os.path.sep)

# Cell
@call_parse
def setup_test_repo(root:Param("project root directory", str)="_temp"):
    """Setup a test KiCad repository to test against.
    """
    if not os.path.exists(root):
        subprocess.check_call(f"git clone --recursive https://github.com/sci-bots/dropbot-40-channel-HV-switching-board.kicad { root }", shell=True)

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
def get_manufacturers(root="."):
    """Get the supported manufacturers.
    """
    root = _set_root(root)
    return [os.path.split(f)[1][:-5] for f in glob.glob(os.path.join(root, ".kicad_helpers_config", "manufacturers", "*.yaml"))]

# Cell
def get_gitignore_list(root="."):
    root =_set_root(root)
    with open(f"{ root }/.gitignore") as f:
        gitignore = f.readlines()
    return [line.strip() for line in gitignore]

# Cell
def in_gitignore(filename, root="."):
    root = _set_root(root)
    try:
        cmd = f"cd { root } && git check-ignore --no-index { filename }"
        if len(_run_cmd(cmd)):
            return True
    except subprocess.CalledProcessError:
        pass
    return False

# Cell
def run_docker_cmd(cmd,
                   workdir,
                   container,
                   v=False):
    """
    Run a command in a docker container under a UID mapped to the current user.
    This ensures that the current user is owner of any files created in the
    workdir.
    """
    UID = subprocess.check_output("id -u", shell=True).decode("utf-8").strip()
    docker_cmd = (f"docker run --rm -v { workdir }:/workdir --workdir=\"/workdir\" "
        f"{ container } "
        f"/bin/bash -c \"useradd --shell /bin/bash -u { UID } -o -c '' -m docker && "
        f"runuser docker -c '{ cmd }'\""
    )
    if v:
        print(docker_cmd)
    return subprocess.check_output(docker_cmd, stderr=subprocess.STDOUT, shell=True)

# Cell
def run_kibot_docker(config:Param(f"KiBot configuation file", str),
                     root:Param("project root directory", str)=".",
                     v:Param("verbose", bool)=False,
                     output:Param("output path relative to ROOT")="."):
    """
    Run KiBot in a local docker container.
    """
    root = _set_root(root)
    if os.path.abspath(output) == output:
        raise RuntimeError(f"OUTPUT cannot be an absolute path; it must be relative to ROOT={ root }.")

    cmd = (f"kibot -c { config } "
       f"-e { get_schematic_path(root)[len(root) + 1:] } "
       f"-b { get_board_path(root)[len(root) + 1:] } "
       f"-d { output }"
    )
    run_docker_cmd(cmd,
                   workdir=os.path.abspath(root),
                   container="setsoft/kicad_auto_test:latest",
                   v=v
    )

# Cell
def get_board_metadata(root="."):
    """Get metadata from the `*.kicad_pcb` board file.
    """
    root = _set_root(root)
    with open(get_board_path(root), 'r') as f:
        board = f.read()
    matches = re.search("\(title_block.*title (?P<title>[^\)]*)\)"
        ".*date (?P<date>[^\)]*)\)"
        ".*rev (?P<rev>[^\)]*)\)"
        ".*company (?P<company>[^\)]*)\)",
        board, re.DOTALL
    )
    return matches.groupdict()

# Cell
def update_board_metadata(update_dict, root="."):
    """Update metadata in the `*.kicad_pcb` board file.
    """
    root = _set_root(root)
    with open(get_board_path(root), 'r') as f:
        board = f.read()

    for key, value in update_dict.items():
        if " " in value and not value.startswith('\"') and not value.endswith('\"'):
            value = '\"' + value + '\"'
        board, n = re.subn(f"(?s)(?P<pre>\(title_block.*{ key } )[^\)]*\)",
            f"\g<pre>{ value })",
            board
        )
        assert n == 1
    with open(get_board_path(root), 'w') as f:
        f.write(board)

# Cell
def get_schematic_metadata(root, filename=None):
    """Get metadata from a `*.sch` schematic file.
    """
    if filename is None:
        filename = get_schematic_path(root)
    elif os.path.abspath(filename) != filename:
        filename = os.path.join(root, filename)

    with open(filename, 'r') as f:
        schematic = f.read()

    matches = re.search("Title (?P<Title>[^\n]*)\n"
        ".*Date (?P<Date>[^\n]*)\n"
        ".*Rev (?P<Rev>[^\n]*)\n"
        ".*Comp (?P<Comp>[^\n]*)\n",
        schematic, re.DOTALL
    )

    return matches.groupdict()

# Cell
def update_schematic_metadata(update_dict:dict,      # keys/values to update
                              root:str=".",          # project root directory
                              all_sheets:bool=True): # update subsheets
    """Update metadata in a `*.sch` schematic file.
    """
    root = _set_root(root)

    if all_sheets:
        files = glob.glob(os.path.join(root, "*.sch"))
    else:
        files = [get_schematic_path(root)]

    for file in files:
        with open(file, 'r') as f:
            schematic = f.read()

        for key, value in update_dict.items():
            if not value.startswith('\"') and not value.endswith('\"'):
                value = '\"' + value + '\"'
            schematic, n = re.subn(f"(?s)(?P<pre>{ key } )([^\n]*)\n",
                f"\g<pre>{ value }\n",
                schematic
            )
            assert n == 1
        with open(file, 'w') as f:
            f.write(schematic)