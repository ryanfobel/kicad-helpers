# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/01_test.ipynb (unless otherwise specified).

__all__ = ['test_erc', 'test_drc', 'validate_bom', 'test_notebooks']

# Cell
import os
import subprocess

from fastcore.script import *
from nbdev.test import *
from nbdev.test import nbglob, num_cpus, parallel, _test_one, Path
import pandas as pd
import pandera as pa
from kicad_helpers import *
from .utilities import _set_root, _print_cmd_output

# Cell
def test_erc(root="."):
    returncode = 0
    config = f".kicad_helpers_config/erc.yaml"
    try:
        output = run_kibot_docker(config=config, root=root)
    except subprocess.CalledProcessError as e:
        returncode = e.returncode
        print(e.output.decode("utf-8"))
        print(f"returncode = { returncode }")
    erc_path = os.path.join(root, get_project_name(root) + ".erc")
    if os.path.exists(erc_path):
        os.remove(erc_path)
    assert returncode == 0

# Cell
def test_drc(root="."):
    returncode = 0
    config = f".kicad_helpers_config/drc.yaml"
    try:
        output = run_kibot_docker(config=config, root=root)
    except subprocess.CalledProcessError as e:
        returncode = e.returncode
        print(e.output.decode("utf-8"))
        print(f"returncode = { returncode }")
    drc_path = os.path.join(root, "drc_result.rpt")
    if os.path.exists(drc_path):
        os.remove(drc_path)
    assert returncode == 0

# Cell
def validate_bom(root="."):
    df = pd.read_csv(get_bom_path(root))
    schema = pa.DataFrameSchema({
        "Refs": pa.Column(str),
        "Quantity": pa.Column(int),
        "MPN": pa.Column(str),
        "Manufacturer": pa.Column(str),
        "datasheet": pa.Column(str, nullable=True, coerce=True),
        "footprint": pa.Column(str),
        "value": pa.Column(str),
    })

    return schema.validate(df)

# Cell
@call_parse
def test_notebooks(fname:Param("A notebook name or glob to convert", str)=None,
                   flags:Param("Space separated list of flags", str)=None,
                   n_workers:Param("Number of workers to use", int)=None,
                   verbose:Param("Print errors along the way", bool_arg)=True,
                   timing:Param("Timing each notebook to see the ones are slow", bool)=False,
                   pause:Param("Pause time (in secs) between notebooks to avoid race conditions", float)=0.5,
                   root:Param("project root directory", str)="."):
    """Test all notebooks matching `fname` in parallel, passing along `flags`"""
    root = _set_root(root)
    if flags is not None: flags = flags.split(' ')
    if fname is None:
        fname = os.path.join(root, "tests", "*.ipynb")
    files = nbglob(fname, recursive=False)
    files = [Path(f).absolute() for f in sorted(files)]
    assert len(files) > 0, "No files to test found."
    if n_workers is None: n_workers = 0 if len(files)==1 else min(num_cpus(), 8)
    # make sure we are inside the tests folder
    os.chdir(os.path.join(root, "tests"))
    results = parallel(_test_one, files, flags=flags, verbose=verbose, n_workers=n_workers, pause=pause)
    passed,times = [r[0] for r in results],[r[1] for r in results]
    if all(passed): print("All tests are passing!")
    else:
        msg = "The following notebooks failed:\n"
        raise Exception(msg + '\n'.join([f.name for p,f in zip(passed,files) if not p]))
    if timing:
        for i,t in sorted(enumerate(times), key=lambda o:o[1], reverse=True):
            print(f"Notebook {files[i].name} took {int(t)} seconds")