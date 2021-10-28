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
from six.moves import urllib
import json
import os

import pandas as pd
import datetime as dt


# # copy pasted from: https://github.com/prisma-labs/python-graphql-client/blob/master/graphqlclient/client.py
class GraphQLClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.token = None
        self.headername = None

    def execute(self, query, variables=None):
        return self._send(query, variables)

    def inject_token(self, token, headername='token'):
        self.token = token
        self.headername = headername

    def _send(self, query, variables):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers[self.headername] = '{}'.format(self.token)

        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read()))
            print('')
            raise e

def get_part(client, part, manufacturer):
    dsl = '''
    query ($info: MpnInput!) {
      part(mpn: $info) {
        mpn {
          manufacturer
          part
        }
        type
        datasheet
        description
        image {
          url
          credit_string
          credit_url
        }
        specs {
          key
          name
          value
        }
        offers {
          sku {
            vendor
            part
          }
          description
          moq
          in_stock_quantity
          stock_location
          image {
            url
            credit_string
            credit_url
          }
          specs {
            key
            name
            value
          }
          prices {
            GBP
            EUR
            USD
          }
        }
      }
    }
    '''
    resp = client.execute(dsl, {'info': {'part': part, 'manufacturer': manufacturer}})
    return json.loads(resp)['data']['part']

def get_manufacturers(client, mpn):
    dsl = '''
    query SomeParts($q: String!) {
      search(term: $q) {
            mpn {
          manufacturer
          part
        }

      }
    }
    '''
    resp = client.execute(dsl, {'q': mpn})
    return [row['mpn'] for row in json.loads(resp)['data']['search'] if row['mpn']['part'] == mpn]


# %%
# Call the kitspace partinfo API

client = GraphQLClient('https://dev-partinfo.kitspace.org/graphql')
part = get_part(client, part='NE555P', manufacturer='Texas Instruments')
part


# %%
# Convert stock levels to a dataframe

def part_stock_df(part):
    stock = {
        "Manufacturer": part["mpn"]["manufacturer"],
        "MPN": part["mpn"]["part"]
    }
    stock.update({f"{offer['sku']['vendor']}": offer['in_stock_quantity'] for offer in part['offers']})
    return pd.DataFrame(stock, index=[dt.datetime.utcnow()])

df = part_stock_df(part)
df

# %%
# Load BOM file

df = pd.read_csv("../manufacturing/40-channel-hv-switching-board_BOM.csv")
df

# %%
# Lookup manufacturers on Octopart (based on MPN) and save to BOM

if 'Manufacturer' not in df.columns:
    manufacturers = [""] * len(df)
    for i, part in df.iterrows():
        if type(part["MPN"]) == str:
            name = get_manufacturers(client, part["MPN"])[0]['manufacturer']
            print(name)
            manufacturers[i] = name
    df["Manufacturer"] = manufacturers
    df.to_csv("../40-channel-hv-switching-board_BOM.csv", index=False)

# %%
df_stock = pd.DataFrame()

# Iterate over all parts that have a MPN
for i, part in df.iloc[df["Mfg_Part_No"].dropna().index].iterrows():
    df_stock = df_stock.append(part_stock_df(get_part(client, part=part['Mfg_Part_No'], manufacturer=part['Manufacturer'])))
    
df_stock

# %%
# Get unique Manufacturer/MPN pairs

import numpy as np

for manufacturer, mpn in df_stock.groupby(['Manufacturer', 'MPN']).count().index.values:
    df_stock[np.logical_and(df_stock['Manufacturer'] == manufacturer , df_stock['MPN'] == mpn)]

# %%
df_stock[np.logical_and(df_stock['Manufacturer'] == manufacturer , df_stock['MPN'] == mpn)]

# %%
