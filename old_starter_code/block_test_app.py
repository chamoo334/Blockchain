from flask import Flask, jsonify
from blockchain import *


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    prev_hash = blockchain.hash(prev_block)
    proof = blockchain.proof_of_work(prev_proof)
    new_block = blockchain.generate_block(proof, prev_hash)
    response = {'message': 'Congrats - block mined & added to blockchain!',
                'index': new_block['index'],
                'timestamp': new_block['timestamp'],
                'proof': new_block['proof'],
                'previous_hash': new_block['previous_hash']}
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'length': len(blockchain.chain),
                'chain': blockchain.chain}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain_valid = blockchain.is_chain_valid(blockchain.chain)

    if chain_valid:
        response = {'message': 'Blockchain is valid!'}
    else:
        response = {'message': 'Uh oh, blockchain is not valid!'}

    return jsonify(response), 200



# app.run(host='0.0.0.0', port=5000)
