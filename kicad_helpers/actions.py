# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_actions.ipynb (unless otherwise specified).

__all__ = ['update_templates', 'sch_to_bom', 'bom_to_sch']

# Cell
import os
import sys
import pkg_resources
import subprocess

import jinja2
from fastcore.script import *
import pandas as pd

from kicad_helpers import *
from .utilities import _set_root

# Cell
@call_parse
def update_templates(v:Param("verbose", bool),
                     overwrite:Param("overwrite existing templates", bool),
                     root:Param("project root directory", str)="."):
    """
    Install various templates from the `kicad_helpers/templates` directory (ignoring anything in the project's
    `.gitignore` list). Similar to `nbdev`: [nbdev_new](https://nbdev.fast.ai/tutorial.html#Set-up-Repo). Templates
    are stored in the [kicad_helpers/templates](https://github.com/ryanfobel/kicad-helpers/tree/main/kicad_helpers/templates)
    folder, and are included with the python package by adding the followingline to the `MANIFEST.in` file:
    ```
    graft kicad_helpers/templates
    ```
    """
    templates_path = os.path.abspath(pkg_resources.resource_filename('kicad_helpers', 'templates'))
    root = _set_root(root)
    metadata = get_project_metadata(root)
    file_list = []
    exists_flag = False
    for root_, dirs, files in os.walk(templates_path):
        if len(files):
            for file in files:
                path = os.path.join(root_[len(templates_path) + 1:], file)
                if not in_gitignore(path):
                    src_path = os.path.abspath(os.path.join(templates_path, path))
                    dst_path = os.path.abspath(os.path.join(root, path))

                    # Create the `dst_path` directory if it doesn't exist
                    os.makedirs(os.path.split(dst_path)[0], exist_ok=True)

                    if os.path.exists(dst_path):
                        if not overwrite:
                            if v:
                                print(f"{ path } already exists")
                                exists_flag = True
                            continue

                    with open(src_path) as f:
                        template = jinja2.Template(f.read())

                    with open(dst_path, "w") as f:
                        if v:
                            print(f"Rendering { path } template.")
                        f.write(template.render(**metadata))

    if not overwrite and exists_flag:
        print("To overwrite existing files, use the --overwrite flag.")

# Cell
@call_parse
def sch_to_bom(root:Param("project root directory", str)=".",
               v:Param("verbose", bool)=False,
               overwrite:Param("update existing schematic", bool)=False):
    """
    Update/create BOM from KiCad schematic.
    """
    root = _set_root(root)
    cmd = f"{ sys.executable } -m kifield --nobackup --overwrite --group -aq -x { get_schematic_path(root) } -i { get_bom_path(root) }"
    if v:
        print(cmd)
    subprocess.check_output(cmd, shell=True)

# Cell
@call_parse
def bom_to_sch(root:Param("project root directory", str)=".",
               v:Param("verbose", bool)=False,
               overwrite:Param("update existing schematic", bool)=False):
    """
    Update KiCad schematic from BOM file.
    """
    root = _set_root(root)
    cmd = f"{ sys.executable } -m kifield --nobackup --overwrite --fields ~quantity -x { get_bom_path(root) } -i { get_schematic_path(root) }"
    if v:
        print(cmd)
    subprocess.check_output(cmd, shell=True)