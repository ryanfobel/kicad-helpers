# kicad-helpers

This project contains some examples and utility scripts for managing [KiCad] projects.

## Github actions

### Auto-generate manufacturing outputs

* Generate manufacturer-specific assets (configured in `.kicad_helpers_config/manufacturing`)
* Generate PCBWay assets
* Add assembly photos
* Add git commit hash to asset names
* Add position files

## Gitlab pipeline

* https://gitlab.com/pardeelab/mango-control-board.kicad/-/blob/main/.gitlab-ci.yml

## Other

## Add files to .gitignore

Ignore backup and intermediate files.

```
_autosave*
*bak
*cache.*
*.xml
*.csv
```

## [Configure git to ignore date changes in the .pro file](plotkicad)

Prevent unhelpful changes to the `*.pro` file (i.e., date the file was opened) from
being tracked by `git`.

* [ ] Add `*.pro filter=kicad_project` to the `.gitattributes` file.
* [ ] Run the following commands:

```sh
$ git config --global filter.kicad_project.clean "sed -E 's/^update=.*$/update=Date/'"
$ git config --global filter.kicad_project.smudge cat
```

## Notebooks

* sync BOM/KiCad schematic file
* update stock levels from Octopart, kitspace

[KiCad]: https://www.kicad.org/
[plotkicad]: https://jnavila.github.io/plotkicadsch/