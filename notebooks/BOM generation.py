# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# Note that getting a quantity column (using the -aq switch) requires a patched version of kifield
# https://github.com/devbisme/KiField/issues/59#issuecomment-952298997

# !pip install git+https://github.com/ryanfobel/kifield.git@add-quantity

# %%
# Extract info from kicad schematic to create or update BOM

import pandas as pd

# !cd .. && python -m kifield --group -aq -x "40-channel-hv-switching-board.sch" -i "manufacturing/40-channel-hv-switching-board_BOM.csv"
df = pd.read_csv("../manufacturing/40-channel-hv-switching-board_BOM.csv")
df

# %%
# Extract info from BOM and insert into kicad schematic (ignore "quantity" field)

# !cd .. && python -m kifield --fields ~quantity -x "manufacturing/40-channel-hv-switching-board_BOM.csv" -i "40-channel-hv-switching-board.sch"

# %%
