# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_core.ipynb (unless otherwise specified).

__all__ = ['get_project_root', 'PROJECT_ROOT', 'get_project_name', 'get_project_metadata', 'get_gitignore_list',
           'in_gitignore', 'say_hello']

# Cell
import glob
import os
import subprocess

import git

# Cell
def get_project_root():
    # Find the current projects' root directory
    git_repo = git.Repo(".", search_parent_directories=True)
    return git_repo.git.rev_parse("--show-toplevel")

# Cell
# Set the PROJECT ROOT environment variable
PROJECT_ROOT = get_project_root()
os.environ["KH_PROJECT_ROOT"] = PROJECT_ROOT
assert(os.getenv("KH_PROJECT_ROOT") == PROJECT_ROOT)

# Cell
def get_project_name():
    # This is based on the name of the KiCad `*.pro` file.
    root = get_project_root()
    return os.path.splitext(os.path.split(glob.glob(os.path.join(root, "*.pro"))[0])[1])[0]

def get_project_metadata():
    PROJECT_ROOT = get_project_root()

    # Default metadata if there's no existing `kicad.yaml` file.
    metadata = {"summary": "A description for your project",
                "site": "https://example.com # A site you would like to link to (include http:// or https://)",
                "color": "black # for example"
    }

    # If there's an existing `kicad.yaml` file, those settings override the defaults.
    try:
        with open(os.path.join(PROJECT_ROOT, "kitspace.yaml")) as f:
            metadata.update({k: v for k, v in load(f, Loader=Loader).items() if k in ["summary", "site", "color"]})
    except:
        pass

    # Add the project name
    metadata["project_name"]=get_project_name()
    return metadata

# Cell
def get_gitignore_list():
    PROJECT_ROOT = get_project_root()
    with open(f"{PROJECT_ROOT}/.gitignore") as f:
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
def say_hello(to):
    "Say hello to somebody"
    return f'Hello {to}!'