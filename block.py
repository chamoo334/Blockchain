from flask import Flask, jsonify
import datetime, json, hashlib


class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.genesis(proof=1, prev_hash='0')

    def generate_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': prev_hash,
                 'data': None}
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
            if hash_op[:4] == '0000':
                return False
            
            previous_block = chain[block_index]
            block_index += 1

        return True