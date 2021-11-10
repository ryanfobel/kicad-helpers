# kicad-helpers
> Scripts, templates, and examples for managing KiCad projects.


[![Build, Test, Package](https://github.com/ryanfobel/kicad-helpers/actions/workflows/python-package.yml/badge.svg)](https://github.com/ryanfobel/kicad-helpers/actions/workflows/python-package.yml)
[![PyPI version shields.io](https://img.shields.io/pypi/v/kicad-helpers.svg)](https://pypi.python.org/pypi/kicad-helpers/)

## Project goals:

* provide a sensible default project structure/actions for KiCad projects managed with git
* automate anything that can be automated (update BOMs, produce manufacturing files, run tests, generate documentation, etc.)
* configure git and KiCad to play nicely together
* support customization via command line arguments, environment variables, etc.
* make everything easy to install/setup/use
* make [awesome documentation](https://ryanfobel.github.io/kicad-helpers/)

## Install

`pip install kicad_helpers`

## How to use

Navigate to the directory containing your KiCad project.

```sh
cd KICAD/PROJECT/PATH
```

    usage: kh_update [-h] [--v] [--overwrite] [--root ROOT]
    
    Update project templates from the `kicad_helpers/templates` directory (ignoring anything in the project's `.gitignore`
    list).
    
    optional arguments:
      -h, --help   show this help message and exit
      --v          verbose (default: False)
      --overwrite  overwrite existing templates (default: False)
      --root ROOT  project root directory (default: .)

