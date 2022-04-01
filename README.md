# CIT Block Chain
CITCoin for CIT Block chain


### Usage
```bash
# install dependencies
pip install -r requirements.txt

# run app
python app.py
```

### Endpoints
| Endpoint | Description | Status | Response | Error |
| --- | --- | --- | --- | --- |
|/register_node | Register a new node | 201 | { 'message': 'New nodes have been added', 'total_nodes': <number>} | 400 Please supply a valid list of nodes
|/mine | Mine CIT Coin | 200 | { 'message': '...', 'index': ...'block_hash': <hash>...} | None
|/transactions/new | Create a new transaction | 201 | { 'message': 'New transaction will be added to the next block' } | 400 Missing values
|/chain | Get the full block chain | 200 | { 'chain': <list> } | None
|/nodes/resolve | Consensus | 200 | { 'message': 'Our chain was replaced', 'new_chain': <list> } | None


### Contributing
To contribute to this project, please fork the repository and make a pull request.

### License
[MIT](/LICENSE)




