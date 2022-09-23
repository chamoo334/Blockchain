from backend.blockchain.block import Block, GENESIS_DATA

def test_genesis():
    genesis = Block.genesis()

    # assert instance of Block is returned
    assert isinstance(genesis, Block)

    # verify instantiated block data matches GENESIS_DATA
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    # insure instance of correct class
    assert isinstance(block, Block)

    # verify instantiated block data matches created
    assert block.data == data
    assert block.last_hash == last_block.hash
