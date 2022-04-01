from flask import Flask, jsonify, request
from app.cit_block import CITcoin
from errors.error_handler import errors




# Create a CIT coin
cit_coin = CITcoin()

# Create a web app
app = Flask(__name__)
app.register_blueprint(errors)

# Register a node
@app.route('/register_node', methods=['POST'])
def register_node():
    values = request.get_json()
    print(values)

    nodes = values.get('nodes')
    if nodes is None:
        return { 'message ': 'Please supply a valid list of nodes'}, 400

    for node in nodes:
        cit_coin.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(cit_coin.nodes)
    }

    return jsonify(response), 201

# Get the full chain
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': cit_coin.chain,
        'length': len(cit_coin.chain)
    }
    return jsonify(response), 200

# Mine a new block
@app.route('/mine', methods=['GET'])
def mine():
    last_block = cit_coin.last_block
    last_proof = last_block['proof']
    proof = cit_coin.proof_of_work(last_proof)
    node_identifier = request.remote_addr

    cit_coin.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    previous_hash = cit_coin.hash(last_block)
    block = cit_coin.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

# Add a new transaction to the list of transactions
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new transaction
    index = cit_coin.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# resolve nodes (consensus)
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = cit_coin.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': cit_coin.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': cit_coin.chain
        }

    return jsonify(response), 200


# Run the app
if __name__ == '__main__':
    app.run()
    
