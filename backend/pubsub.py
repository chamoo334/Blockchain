import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNReconnectionPolicy
from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-d0056269-1a46-4950-9d0d-5299478ca97a'
pnconfig.publish_key = 'pub-c-85a3cdef-b543-4c06-a1a5-323c650dd401'
pnconfig.user_id = 'UUID'
# pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR
pnconfig.reconnect_policy = PNReconnectionPolicy.EXPONENTIAL



CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}


class Listener(SubscribeCallback):
    """
    Listener
    """
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message):
        # announce message and add block to blockchain
        print(f'\n-- Channel: {message.channel} | Message: {message.message}')

        if message.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')

class PubSub():
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        # self.pubnub.add_listener(Listener())
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes in Block channel.
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

def main():
    """Test method"""
    test_chain = Blockchain()
    pubsub = PubSub(test_chain)
    time.sleep(1) # for network connections
    pubsub.publish(CHANNELS['TEST'], { 'foo': 'bar' })


if __name__ == '__main__':
    main()
