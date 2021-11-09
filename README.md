# kicad-helpers

This project contains some examples and utility scripts for managing [KiCad] projects.

## Github actions

### Auto-generate manufacturing outputs

* Generate manufacturer-specific assets (configured in `.kicad_helpers_config/manufacturing`)

```      
.
├── manufacturing
    ├── default
    └── $MANUFACTURER_NAME
        ├── assembly_photos
        |   ├── front.png
        |   └── back.png
        ├── gerbers
        |   ├── $PROJECT_NAME.drl
        |   ├── $PROJECT_NAME.gbl
        ... ...
        |   └── $PROJECT_NAME-NPTH.drl
        ├── position
            ├── bottom_pos.pos
            └── top_pos.pos
        └── $PROJECT_NAME-BOM.csv
```

* Generate PCBWay assets
* Add assembly photos
* Add git commit hash to asset names
* Add position files
* Generate Github release on tag push

## Notebooks

* sync BOM/KiCad schematic file
* update stock levels from Octopart, kitspace

[KiCad]: https://www.kicad.org/
