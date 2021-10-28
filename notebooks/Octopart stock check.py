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

from dotenv import load_dotenv

load_dotenv()

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
    query match_mpns($queries: [PartMatchQuery!]!) {
        multi_match(queries: $queries) {
            hits
            reference
            parts {
                id
                manufacturer {
                    name
                }
                mpn
                category {
                    name
                }
                sellers {
                    company {
                      name
                    }
                    offers {
                      id
                      sku
                      moq
                      inventory_level
                      updated
                      prices {
                          price
                          currency
                          quantity
                          converted_price
                          converted_currency
                          conversion_rate
                      }
                    }
                }
            }
        }
    }
    '''

    queries = []
    for mpn in mpns:
        queries.append({
            'mpn_or_sku': part,
            'start': 0,
            'limit': 1,
            'reference': part,
            'manufacturer': manufacturer
            
        })
    resp = client.execute(dsl, {'queries': queries})
    return json.loads(resp)['data']['multi_match'][0]['parts'][0]


# %%
client = GraphQLClient('https://octopart.com/api/v4/endpoint')
client.inject_token(os.getenv('OCTOPART_TOKEN'))
part = get_part(client, part='NE555P', manufacturer='Texas Instruments')

# %%
part
