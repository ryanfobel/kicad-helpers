# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/03_bom.ipynb (unless otherwise specified).

__all__ = ['sch_to_bom', 'bom_to_sch']

# Cell
import tempfile
import subprocess
import sys
import os

from fastcore.script import *
import pandas as pd
from kicad_helpers import get_git_root, setup_test_repo, get_project_name, get_schematic_path, get_bom_path
from .core import _set_root

# Cell
@call_parse
def sch_to_bom(root:Param("project root directory", str)=".",
               v:Param("verbose", bool)=False,
               overwrite:Param("update existing schematic", bool)=False):
    """
    Update/create BOM from KiCad schematic.
    """
    root = _set_root(root)
    subprocess.check_output(f"{ sys.executable } -m kifield --nobackup --overwrite --group -aq -x { get_schematic_path(root) } -i { get_bom_path(root) }", shell=True)

@call_parse
def bom_to_sch(root:Param("project root directory", str)=".",
               v:Param("verbose", bool)=False,
               overwrite:Param("update existing schematic", bool)=False):
    """
    Update KiCad schematic from BOM file.
    """
    root = _set_root(root)
    subprocess.check_output(f"{ sys.executable } -m kifield --nobackup --overwrite --fields ~quantity -x { get_bom_path(root) } -i { get_schematic_path(root) }", shell=True)