import time
from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.util.hex_to_binary import hex_to_binary

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}

class Block:
    """
    Block: a unit of storage for transactions in the blockchain
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def add_block(self, data):
        self.chain.append(Block(data))

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the provided last block and data.
        Blocks are mined until proof of work requirements are met.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)
        
        # while hash[0:difficulty] != '0' * difficulty:
        #     nonce += 1
        #     timestamp = time.time_ns()
        #     difficulty = Block.adjust_difficulty(last_block, timestamp)
        #     hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes
        """
        return self.__dict__
    
    @staticmethod
    def genesis():
        """
        Generate the genesis (initial) block.
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculates difficulty according to MINE_RATE.
        Adjusts MINE_RATE as needed.
        """

        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate block using commented rules
        """

        # the block must have the proper last_hash reference
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')

        # the block must meet the proof of work requirement
        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof of work requirement was not met')

        # the difficulty must only adjust by 1
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must only adjust by 1')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )

        # the block hash must be a valid combination of the block fields
        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')

    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block's json representation back into a block instance.
        """
        return Block(**block_json)


def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'foo')
    bad_block.last_hash = 'evil_data'

    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')

if __name__ == '__main__':
    main()