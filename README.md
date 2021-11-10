# kicad-helpers
> Scripts, templates, and examples for managing KiCad projects.


[![Build, Test, Package](https://github.com/ryanfobel/kicad-helpers/actions/workflows/python-package.yml/badge.svg)](https://github.com/ryanfobel/kicad-helpers/actions/workflows/python-package.yml)
[![PyPI version shields.io](https://img.shields.io/pypi/v/kicad-helpers.svg)](https://pypi.python.org/pypi/kicad-helpers/)

## Project goals:

* provide a sensible default project structure and scripts for managing KiCad projects with git
* automate anything that can be automated (update BOMs, produce manufacturing files, run tests, generate documentation, etc.)
* configure git and KiCad to play nicely together
* support customization via command line arguments, environment variables, etc.
* make everything easy to install/setup/use
* make [awesome documentation](https://ryanfobel.github.io/kicad-helpers/)

## Install

`pip install kicad_helpers`

## How to use

Navigate to the directory containing your KiCad project:

```sh
cd KICAD/PROJECT/PATH
```

Run the `kh_update` script to update all project templates:

```sh
kh_update --help
```

    usage: kh_update [-h] [--v] [--overwrite] [--root ROOT]
    
    Update project templates from the `kicad_helpers/templates` directory (ignoring anything in the project's `.gitignore`
    list).
    
    optional arguments:
      -h, --help   show this help message and exit
      --v          verbose (default: False)
      --overwrite  overwrite existing templates (default: False)
      --root ROOT  project root directory (default: .)


The following templates are installed by default:
* [.github/workflows/build.yml](https://github.com/ryanfobel/kicad-helpers/blob/main/kicad_helpers/templates/.github/workflows/build.yml): a github workflow for updating the BOM, producing manufacturing files, running tests, generating documentation, etc.
* [kitspace.yaml](https://github.com/ryanfobel/kicad-helpers/blob/main/kicad_helpers/templates/kitspace.yaml): metadata file for the [kitspace](https://kitspace.org/) service
* [.kicad_helpers_config/config.kibot.yaml](https://github.com/ryanfobel/kicad-helpers/blob/main/kicad_helpers/templates/.kicad_helpers_config/config.kibot.yaml): configuration file for [KiBot](https://github.com/INTI-CMNB/KiBot) which allow automation of various KiCad actions
* [.kicad_helpers_config/manufacturers/PCBWay.kibot.yaml](https://github.com/ryanfobel/kicad-helpers/blob/main/kicad_helpers/templates/.kicad_helpers_config/manufacturers/PCBWay.kibot.yaml): [KiBot](https://github.com/INTI-CMNB/KiBot) configuration to generate manufacturing files for [PCBWay](https://www.pcbway.com/)

To overwrite existing templates, run the command with the `--overwrite` flag, e.g.:

```sh
kh_update --v --overwrite
```

    kitspace.yaml already exists
    Rendering kitspace.yaml template.
    .github/workflows/build.yml already exists
    Rendering .github/workflows/build.yml template.
    .kicad_helpers_config/config.kibot.yaml already exists
    Rendering .kicad_helpers_config/config.kibot.yaml template.
    .kicad_helpers_config/manufacturers/PCBWay.kibot.yaml already exists
    Rendering .kicad_helpers_config/manufacturers/PCBWay.kibot.yaml template.

