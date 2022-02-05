"""
load transactions periodically, store to file, update with new ones
"""
from solana.rpc.api import Client, MemcmpOpt
from collections import defaultdict

# config
mint_address = "cqNTpypmbwghrf1G9VGvSENcw7M7wGSQ7JS8UTQWXwb"
top_N = 300
output_fpath = f'./top_holders.csv'

# constants
token_program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"

# setup
client = Client("https://api.mainnet-beta.solana.com/")

# get all token accounts for mint
memcmp_opts = [MemcmpOpt(offset=0, bytes=mint_address)]
result = client.get_program_accounts(pubkey=token_program_id,
                                     encoding="jsonParsed",
                                     data_size=165,
                                     memcmp_opts=memcmp_opts)

# extract owner to quantity dict
holders = defaultdict(lambda: 0)
for d in result['result']:
    owner = d['account']['data']['parsed']['info']['owner']
    amount = d['account']['data']['parsed']['info']['tokenAmount']['uiAmount']
    holders[owner] += amount

# sort
items = list(holders.items())
items.sort(key=lambda x: x[1], reverse=True)

# write file
with open(output_fpath, 'w') as f:
    for address, amount in items[:top_N]:
        f.write(f"{address}, {amount}\n")


