# Welcome to kicad-helpers
> Scripts, templates, and examples for managing KiCad projects


[![Build, Test, Package](https://github.com/ryanfobel/kicad-helpers/actions/workflows/python-package.yml/badge.svg)](https://github.com/ryanfobel/kicad-helpers/actions/workflows/python-package.yml)
[![PyPI version shields.io](https://img.shields.io/pypi/v/kicad-helpers.svg)](https://pypi.python.org/pypi/kicad-helpers/)

## Project goals

* provide a sensible default structure and scripts for managing KiCad projects
* automate everything that can be automated with continuous integrations scripts (e.g., [update BOMs][update BOMs], produce manufacturing files, [run tests][run tests], generate documentation, etc.)
* configure git and KiCad to play nicely together
* support customization via command line arguments, environment variables, etc.
* make everything easy to install/setup/use
* make [awesome documentation](https://ryanfobel.github.io/kicad-helpers/)

[update BOMs]: https://ryanfobel.github.io/kicad-helpers/#Export-a-BOM-from-the-KiCad-schematic
[run tests]: https://ryanfobel.github.io/kicad-helpers/#Run-all-tests-in-the-tests-directory

## Install

```sh
> pip install kicad_helpers
```

## Setup a new project

Open a command line shell and navigate to the directory containing your KiCad project. Then run `kh_update` to apply various project templates to the project directory:

```sh
> cd kicad/project/path
> kh_update
```

By default, this will install the following templates:
* [.github/workflows/build.yml](https://github.com/ryanfobel/kicad-helpers/blob/main/kicad_helpers/templates/.github/workflows/build.yml): a github workflow for updating the BOM, producing manufacturing files, running tests, generating documentation, etc.
* [kitspace.yaml](https://github.com/ryanfobel/kicad-helpers/blob/main/kicad_helpers/templates/kitspace.yaml): metadata file for the [kitspace](https://kitspace.org/) service
* [.kicad_helpers_config/config.kibot.yaml](https://github.com/ryanfobel/kicad-helpers/blob/main/kicad_helpers/templates/.kicad_helpers_config/config.kibot.yaml): configuration file for [KiBot](https://github.com/INTI-CMNB/KiBot) which allow automation of various KiCad actions
* [.kicad_helpers_config/manufacturers/PCBWay.kibot.yaml](https://github.com/ryanfobel/kicad-helpers/blob/main/kicad_helpers/templates/.kicad_helpers_config/manufacturers/PCBWay.kibot.yaml): [KiBot](https://github.com/INTI-CMNB/KiBot) configuration to generate manufacturing files for [PCBWay](https://www.pcbway.com/)


To overwrite existing templates, run `kh_update` with the `--overwrite` flag:

```sh
> kh_update --v --overwrite
```

    Render kitspace.yaml template.
    Render settings.ini template.
    Render .github/workflows/build.yml template.
    Render .kicad_helpers_config/drc.yaml template.
    Render .kicad_helpers_config/erc.yaml template.
    Render .kicad_helpers_config/pcb_pdf.yaml template.
    Render .kicad_helpers_config/pcb_svg.yaml template.
    Render .kicad_helpers_config/sch_pdf.yaml template.
    Render .kicad_helpers_config/sch_svg.yaml template.
    Render .kicad_helpers_config/manufacturers/default.yaml template.
    Render .kicad_helpers_config/manufacturers/PCBWay.yaml template.
    Render tests/Tests.ipynb template.
    "*.pro filter=kicad_project" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitattributes
    "*.sch filter=kicad_sch" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitattributes
    Add filters to git config.
    "_autosave*" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitignore
    "*bak" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitignore
    "*.xml" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitignore
    ".ipynb_checkpoints" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitignore
    "*-erc.txt" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitignore
    "*-drc.txt" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitignore
    "kibot_errors.filter" already exists in /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/.gitignore
    


To see the options that are available, run the command:

```sh
> kh_update --help
```

    usage: kh_update [-h] [--v] [--overwrite] [--root ROOT]
    
    Setup a new project (or update an existing project) with templates from the `kicad_helpers/templates` directory. Also
    installs git filters to prevent insignificant changes to the kicad `*.pro` and `*.sch` files from being tracked by git
    (see https://jnavila.github.io/plotkicadsch/ for more details).
    
    optional arguments:
      -h, --help   show this help message and exit
      --v          verbose (default: False)
      --overwrite  overwrite existing templates (default: False)
      --root ROOT  project root directory (default: .)
    


## Export a BOM from the KiCad schematic

```sh
> kh_sch_to_bom --v
```

    /home/ryan/miniconda3/envs/kh/bin/python3.9 -m kifield --nobackup --overwrite --group -aq -x /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/40-channel-hv-switching-board.sch -i /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/manufacturing/default/40-channel-hv-switching-board-BOM.csv
    
    


## Import data from the BOM into the KiCad schematic

```sh
> kh_sch_to_bom --v
```

    /home/ryan/miniconda3/envs/kh/bin/python3.9 -m kifield --nobackup --overwrite --fields ~quantity -x /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/manufacturing/default/40-channel-hv-switching-board-BOM.csv -i /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/40-channel-hv-switching-board.sch
    
    


## Run all tests in the `tests` directory

```sh
> kh_test
```

    testing /mnt/c/Users/ryan/OneDrive/dev/python/kicad-helpers/_temp/tests/Tests.ipynb
    All tests are passing!
    


## Contributors

* Ryan Fobel ([@ryanfobel](https://github.com/ryanfobel))
