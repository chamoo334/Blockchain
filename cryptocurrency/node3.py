# flask run -h localhost -p 6003
import datetime, json, hashlib, requests
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import sys


class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.generate_block(proof=1, prev_hash='0')
        self.nodes = set()

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def generate_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': prev_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while not check_proof:
            #TODO: modify proof
            hash_op = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_op[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):

            if chain[block_index]['previous_hash'] != self.hash(previous_block):
                return False

            hash_op = hashlib.sha256(str(chain[block_index]['proof']**2 - previous_block['proof']**2).encode()).hexdigest()
            if hash_op[:4] == 0000:
                return False
            
            previous_block = chain[block_index]
            block_index += 1

        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
 
        return self.get_prev_block()['index'] + 1

    def update_chain(self):
        print(self.nodes, file=sys.stdout)
        # network = self.nodes
        # longest_chain = None
        # max_length = len(self.chain)

        # for node in network:
        #     response = requests.get(f'http://{node}/get_chain')
        #     if response.status_code == 200:
        #         length = response.json()['length']
        #         chain = response.json()['chain']
        #         if length > max_length and self.is_chain_valid(chain):
        #             max_length = length
        #             longest_chain = chain

        # if longest_chain:
        #     self.chain = longest_chain
        #     return True
        return False


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    prev_hash = blockchain.hash(prev_block)
    blockchain.add_transaction(node_address, 'Node1', 1)
    proof = blockchain.proof_of_work(prev_proof)
    new_block = blockchain.generate_block(proof, prev_hash)
    response = {'message': 'Congrats - block mined & added to blockchain!',
                'index': new_block['index'],
                'timestamp': new_block['timestamp'],
                'proof': new_block['proof'],
                'previous_hash': new_block['previous_hash'],
                'transactions': new_block['transactions']}
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


@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Missing transaction information', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'Transaction added to Block[{index}]'}
    return jsonify(response), 200


# Decentralizing blockchain
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
        print(blockchain.nodes, file=sys.stdout)

        
    
    response = {'message': 'Node connected!',
                'total_nodes': len(list(blockchain.nodes)),
                'all_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


@app.route('/update_chain', methods = ['GET'])
def update_chain():
    print(blockchain.nodes, file=sys.stdout)
    is_chain_replaced = blockchain.update_chain()
    if is_chain_replaced:
        response = {'message': 'Blockchain has been updated.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'Blockchain is up to date.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200


@app.route('/get_nodes', methods = ['GET'])
def get_nodes():
    nodes = list(blockchain.nodes)
    return jsonify(nodes), 200