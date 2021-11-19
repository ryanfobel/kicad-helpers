# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_actions.ipynb (unless otherwise specified).

__all__ = ['update_templates', 'sch_to_bom', 'bom_to_sch', 'run_kibot_docker', 'export_manufacturing', 'export_sch',
           'export_pcb']

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
    Install various templates from the `kicad_helpers/templates` directory
    (ignoring anything in the project's `.gitignore` list).
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

# Cell
def run_kibot_docker(config:Param(f"kibot configuation file", str),
              root:Param("project root directory", str)=".",
              v:Param("verbose", bool)=False,
              output:Param("output path relative to ROOT")="."):
    """
    Run kibot in a local docker container.
    """
    root = _set_root(root)
    if os.path.abspath(output) == output:
        print(f"OUTPUT cannot be an absolute path; it must be relative to ROOT={ root }.")
        return 1

    UID = subprocess.check_output("id -u", shell=True).decode("utf-8").strip()
    cmd = (f"docker run --rm -v { os.path.abspath(root) }:/workdir --workdir=\"/workdir\" "
           f"setsoft/kicad_auto_test:latest "
           f"/bin/bash -c \"useradd --shell /bin/bash -u { UID } -o -c '' -m docker && "
           f"runuser docker -c 'kibot -c { config } "
           f"-e { get_schematic_path(root)[len(root) + 1:] } "
           f"-b { get_board_path(root)[len(root) + 1:] } "
           f"-d { output }'\""
    )
    if v:
        print(cmd)
    subprocess.check_output(cmd, shell=True)

# Cell
@call_parse
def export_manufacturing(root:Param("project root directory", str)=".",
                         manufacturer:Param(f"\"default\" or manufacturer name", str)="default",
                         v:Param("verbose", bool)=False,
                         output:Param("output path relative to ROOT")="."):
    """
    Export manufacturing files (gerber, drill, and position) by running kibot in a local docker container.
    """
    root = _set_root(root)
    if manufacturer not in get_manufacturers(root):
        print(f"MANUFACTURER must be one of the following: { ', '.join(get_manufacturers(root)) }.")
        return 1

    config = f".kicad_helpers_config/manufacturers/{ manufacturer }.yaml"
    run_kibot_docker(config=config, root=root, v=v, output=output)

# Cell
@call_parse
def export_sch(root:Param("project root directory", str)=".",
               ext:Param(f"svg or pdf", str)="pdf",
               v:Param("verbose", bool)=False,
               output:Param("output path relative to ROOT")="."):
    """
    Export the schematic by running kibot in a local docker container.
    """
    root = _set_root(root)
    supported_types = ["svg", "pdf"]

    if ext not in supported_types:
        print(f"EXT must be one of: { ','.join(supported_types) }.")
        return 1

    config = f".kicad_helpers_config/sch_{ ext }.yaml"
    run_kibot_docker(config=config, root=root, v=v, output=output)

# Cell
@call_parse
def export_pcb(root:Param("project root directory", str)=".",
               ext:Param(f"svg or pdf", str)="pdf",
               v:Param("verbose", bool)=False,
               output:Param("output path relative to ROOT")="."):
    """
    Export the pcb layout by running kibot in a local docker container.
    """
    root = _set_root(root)
    supported_types = ["svg", "pdf"]

    if ext not in supported_types:
        print(f"EXT must be one of: { ','.join(supported_types) }.")
        return 1

    config = f".kicad_helpers_config/pcb_{ ext }.yaml"
    run_kibot_docker(config=config, root=root, v=v, output=output)